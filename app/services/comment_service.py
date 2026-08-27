from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.comment import WorkItemComment
from app.models.site import ConstructionSite, SiteMember
from app.models.work_item import WorkItem
from app.schemas.comment import CommentCreate

def get_work_item_member(db: Session, work_item_id: int, user_id: int):
    work_item = (db.query(WorkItem).filter(WorkItem.id == work_item_id).first())
    if work_item is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy hạng mục thi công"
        )
    
    site = (db.query(ConstructionSite).filter(ConstructionSite.id == work_item.site_id, ConstructionSite.is_deleted == False).first())
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    member = (db.query(SiteMember).filter(SiteMember.site_id == work_item.site_id, SiteMember.user_id == user_id).first())
    if member is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Bạn không thuộc công trình này"
        )
    return work_item

def create_comment(db: Session, work_item_id: int, user_id: int, comment_data: CommentCreate):
    work_item = get_work_item_member(db = db, work_item_id = work_item_id, user_id = user_id)
    content = comment_data.content.strip()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Nội dung comment không được để trống"
        )

    comment = WorkItemComment( work_item_id = work_item.id, user_id = user_id, content = content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_work_item_comments(db: Session, work_item_id: int, user_id: int):
    work_item = get_work_item_member(db = db, work_item_id = work_item_id, user_id = user_id)
    return (db.query(WorkItemComment).filter(WorkItemComment.work_item_id == work_item.id).order_by(WorkItemComment.created_at.asc()).all())