from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.site import ConstructionSiteCreate, SiteMemberCreate
from app.models.site import ConstructionSite, SiteMember
from app.models.user import User
from app.services.log_service import create_activity_log

def create_construction_site(db: Session, site_data: ConstructionSiteCreate, owner_id: int):
    site = ConstructionSite(
        name = site_data.name,
        description = site_data.description,
        owner_id = owner_id
    )
    db.add(site)
    db.flush()

    member = SiteMember(
        site_id = site.id,
        user_id = site.owner_id,
        role = "OWNER"
    )
    db.add(member)

    create_activity_log(
        db = db,
        user_id = owner_id,
        action = "CREATE_SITE",
        site_id = site.id,
        description = f"Tạo công trình '{site.name}'"
    )
    db.commit()
    db.refresh(site)
    return site

def get_user_sites(db: Session, user_id: int, search: str | None = None):
    query = db.query(ConstructionSite).join(SiteMember, SiteMember.site_id == ConstructionSite.id).filter(SiteMember.user_id == user_id, ConstructionSite.is_deleted == False)
    if search:
        query = query.filter(ConstructionSite.name.ilike(f"%{search}%"))
    return query.all()

def get_site_detail(db: Session, site_id: int, user_id: int):
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
    return site

def get_site_owner(db: Session, site_id: int, user_id: int):
    site = db.query(ConstructionSite).filter(ConstructionSite.id == site_id, ConstructionSite.is_deleted == False).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    member = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == user_id, SiteMember.role == "OWNER").first()
    if member is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Bạn không phải OWNER của công trình này"
        )    
    return site

def update_construction_site(db: Session, site_id: int, user_id: int, site_data):
    site = get_site_owner(db = db, site_id = site_id, user_id = user_id)
    if site_data.name is not None:
        site.name = site_data.name
    if site_data.description is not None:
        site.description = site_data.description
    create_activity_log(
        db = db,
        user_id = user_id,
        action = "UPDATE_SITE",
        site_id = site.id,
        description = f"Cập nhật công trình '{site.name}'"
    )
    db.commit()
    db.refresh(site)
    return site

def delete_construction_site(db: Session, site_id: int, user_id: int):
    site = get_site_owner(db = db, site_id = site_id, user_id = user_id)
    site.is_deleted = True
    create_activity_log(
        db = db,
        user_id = user_id,
        action = "DELETE_SITE",
        site_id = site_id,
        description = f"Xóa công trình {site.name}"
    )
    db.commit()
    return {
        "message": "Xóa công trình thành công"
    }

def restore_construction_site(db: Session, site_id: int, user_id: int):
    site = db.query(ConstructionSite).filter(ConstructionSite.id == site_id).first()
    if site is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    owner = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == user_id, SiteMember.role == "OWNER").first()
    if owner is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Bạn không phải OWNER của công trình này"
        )

    if site.is_deleted is False:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Công trình chưa bị xóa"
        )

    site.is_deleted = False
    create_activity_log(
        db = db,
        user_id = user_id,
        action = "RESTORE_SITE",
        site_id = site.id,
        description = f"Khôi phục công trình '{site.name}'"
    )
    db.commit()
    db.refresh(site)
    return site

def add_site_member(db: Session, site_id: int, user_id: int, member_data: SiteMemberCreate):
    get_site_owner(db = db, site_id = site_id, user_id = user_id)
    user = db.query(User).filter(User.id == member_data.user_id, User.is_active == True).first()
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy người dùng"
        )

    existing_member = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == member_data.user_id).first()
    if existing_member is not None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Người dùng đã là MEMBER của công trình"
        )

    existing_membership = db.query(SiteMember).filter(SiteMember.user_id == member_data.user_id, SiteMember.role == "MEMBER").first()
    if existing_membership is not None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Người dùng đã là MEMBER của một công trình khác"
        )
    
    member = SiteMember(
        site_id = site_id,
        user_id = member_data.user_id,
        role = "MEMBER" 
    )
    db.add(member)
    create_activity_log(
        db = db,
        user_id = user_id,
        action = "ADD_MEMBER",
        site_id = site_id,
        description = f"Thêm user {member_data.user_id} vào công trình"
    )
    db.commit()
    db.refresh(member)
    return member

def delete_site_member(db: Session, site_id: int, owner_id: int, member_user_id: int):
    get_site_owner(db = db, site_id = site_id, user_id = owner_id)
    member = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == member_user_id).first()
    if member is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Người dùng không phải MEMBER của công trình"
        )
    if member.role == "OWNER":
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Không thể xóa OWNER của công trình"
        )
    db.delete(member)
    create_activity_log(
        db = db,
        user_id = owner_id,
        action = "REMOVE_MEMBER",
        site_id = site_id,
        description = f"Xóa user {member_user_id} khỏi công trình"
    )
    db.commit()
    return {
        "message": "Xóa MEMBER thành công"
    }

def get_site_members(db: Session, site_id: int, user_id: int):
    get_site_detail(db = db, site_id = site_id, user_id = user_id)
    members = db.query(SiteMember).filter(SiteMember.site_id == site_id).all()
    return members