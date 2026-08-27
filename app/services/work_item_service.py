from datetime import datetime, timedelta
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.schemas.work_item import WorkItemCreate, WorkItemUpdate
from app.models.work_item import WorkItem
from app.models.site import ConstructionSite, SiteMember

def create_work_item(db: Session, site_id: int, user_id: int, work_item_data: WorkItemCreate):
    site = db.query(ConstructionSite).filter(ConstructionSite.id == site_id, ConstructionSite.is_deleted == False).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    member = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == user_id).first()
    if member is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Bạn không phải MEMBER của công trình này"
        )

    if work_item_data.assignee_id is not None:
        assignee = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == work_item_data.assignee_id).first()
        if assignee is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Người được phân công không thuộc công trình"
            )
        
    created_at = datetime.now()
    if work_item_data.due_date is not None:
        due_date = work_item_data.due_date
    else:
        due_date = created_at + timedelta(days = 5)
    
    work_item = WorkItem(
        site_id = site_id,
        title = work_item_data.title,
        description = work_item_data.description,
        status = work_item_data.status,
        priority = work_item_data.priority,
        due_date = due_date,
        created_at = created_at,
        assignee_id = work_item_data.assignee_id
    )
    db.add(work_item)
    db.commit()
    db.refresh(work_item)
    return work_item

def get_site_work_items(db: Session, site_id: int, user_id: int, search: str | None = None, status_filter: str | None = None, priority: str | None = None, assignee_id: int | None = None, limit: int = 10, offset: int = 0, sort_by: str = "created_at", sort_order: str = "desc"):
    site = db.query(ConstructionSite).filter(ConstructionSite.id == site_id, ConstructionSite.is_deleted == False).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )
    
    member = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == user_id).first()
    if member is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Bạn không phải MEMBER của công trình này"
        )

    query = db.query(WorkItem).filter(WorkItem.site_id == site_id)
    if search:
        query = query.filter(WorkItem.title.ilike(f"%{search}%"))
    if status_filter:
        query = query.filter(WorkItem.status == status_filter)
    if priority:
        query = query.filter(WorkItem.priority == priority)
    if assignee_id is not None:
        query = query.filter(WorkItem.assignee_id == assignee_id)
    column = getattr(WorkItem, sort_by)
    if sort_order == "asc":
        query = query.order_by(column.asc())
    else:
        query = query.order_by(column.desc())
    return query.offset(offset).limit(limit).all()

def get_work_item(db: Session, work_item_id: int, user_id: int):
    work_item = db.query(WorkItem).filter(WorkItem.id == work_item_id).first()
    if work_item is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy hạng mục thi công"
        )
    
    site = db.query(ConstructionSite).filter(ConstructionSite.id == work_item.site_id, ConstructionSite.is_deleted == False).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    member = db.query(SiteMember).filter(SiteMember.site_id == work_item.site_id, SiteMember.user_id == user_id).first()
    if member is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Bạn không thuộc công trình này"
        )
    return work_item

def update_work_items( db: Session, work_item_id: int, user_id: int, work_item_data: WorkItemUpdate):
    work_item = db.query(WorkItem).filter(WorkItem.id == work_item_id).first()
    if work_item is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy hạng mục thi công"
        )

    site = db.query(ConstructionSite).filter(ConstructionSite.id == work_item.site_id, ConstructionSite.is_deleted == False).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    owner = db.query(SiteMember).filter(SiteMember.site_id == work_item.site_id, SiteMember.user_id == user_id, SiteMember.role == "OWNER").first()
    if owner is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Chỉ OWNER mới có quyền cập nhật hạng mục"
        )

    update_data = work_item_data.model_dump(exclude_unset = True)

    if "assignee_id" in update_data:
        assignee_id = update_data["assignee_id"]
        if assignee_id is not None:
            assignee = db.query(SiteMember).filter(SiteMember.site_id == work_item.site_id, SiteMember.user_id == assignee_id).first()
            if assignee is None:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Người được phân công không thuộc công trình"
                )

    for field, value in update_data.items():
        setattr(work_item, field, value)
    db.commit()
    db.refresh(work_item)
    return work_item

def update_work_item_status(db: Session, work_item_id: int, user_id: int, status_value: str):
    work_item = db.query(WorkItem).filter(WorkItem.id == work_item_id).first()
    if work_item is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy hạng mục thi công"
        )

    site = db.query(ConstructionSite).filter(ConstructionSite.id == work_item.site_id, ConstructionSite.is_deleted == False).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    member = db.query(SiteMember).filter(SiteMember.site_id == work_item.site_id, SiteMember.user_id == user_id).first()
    if member is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Bạn không thuộc công trình này"
        )

    work_item.status = status_value
    db.commit()
    db.refresh(work_item)
    return work_item

def delete_work_item(db: Session, work_item_id: int, user_id: int):
    work_item = db.query(WorkItem).filter(WorkItem.id == work_item_id).first()
    if work_item is None:
        raise HTTPException(
            status_code=  status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hạng mục thi công"
        )

    site = db.query(ConstructionSite).filter(ConstructionSite.id == work_item.site_id, ConstructionSite.is_deleted == False).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    member = db.query(SiteMember).filter(SiteMember.site_id == work_item.site_id, SiteMember.user_id == user_id, SiteMember.role == "OWNER").first()
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa hạng mục thi công"
        )

    db.delete(work_item)
    db.commit()
    return {
        "message": "Xóa hạng mục thi công thành công"
    }

