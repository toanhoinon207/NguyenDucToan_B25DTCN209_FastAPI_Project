from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.site import ConstructionSiteCreate, ConstructionSiteResponse, ConstructionSiteUpdate, SiteMemberCreate, SiteMemberResponse
from app.dependences.auth import get_current_user, require_role
from app.models.user import User
from app.services.site_services import add_site_member, create_construction_site, delete_construction_site, delete_site_member, get_site_detail, get_site_members, get_user_sites, restore_construction_site, update_construction_site
from app.db.database import get_db

router = APIRouter(
    prefix = "/construction-sites",
    tags = ["Construction Sites"]
)

@router.post("", response_model = ConstructionSiteResponse, status_code = status.HTTP_201_CREATED, summary = "Tạo công trình")
def create_site(site_data: ConstructionSiteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_construction_site(db = db, site_data = site_data, owner_id = current_user.id)

@router.get("", response_model = list[ConstructionSiteResponse], summary = "Lấy danh sách công trình")
def get_construction_sites(search: str | None = Query(default = None, description = "Tìm theo tên công trình"), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_sites(db = db, user_id = current_user.id, search = search)

@router.get("/{site_id}", response_model = ConstructionSiteResponse, summary = "Xem chi tiết công trình")
def get_construction_site(site_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_site_detail(db = db, site_id = site_id, user_id = current_user.id)

@router.put("/{site_id}", response_model = ConstructionSiteResponse, summary = "Cập nhật công trình")
def update_site(site_id: int, site_data: ConstructionSiteUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_construction_site(db = db, site_id = site_id, user_id = current_user.id, site_data = site_data)

@router.patch("/{site_id}", response_model = ConstructionSiteResponse, summary = "Cập nhật công trình")
def patch_site(site_id: int, site_data: ConstructionSiteUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_construction_site(db = db, site_id = site_id, user_id = current_user.id, site_data = site_data)

@router.delete("/{site_id}", summary = "Xóa công trình")
def delete_site(site_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_construction_site(db = db, site_id = site_id, user_id = current_user.id)

@router.put( "/{site_id}/restore", response_model = ConstructionSiteResponse, summary = "Khôi phục công trình")
def restore_site(site_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return restore_construction_site(db = db, site_id = site_id, user_id = current_user.id)

@router.post("/{site_id}/members", response_model = SiteMemberResponse, status_code = status.HTTP_201_CREATED, summary = "Thêm thành viên công trình")
def add_member(site_id: int, member_data: SiteMemberCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_site_member(db = db, site_id = site_id, user_id = current_user.id, member_data = member_data)

@router.delete("/{site_id}/members/{user_id}", summary = "Xóa thành viên công trình")
def delete_member(site_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_site_member(db = db, site_id = site_id, owner_id = current_user.id, member_user_id = user_id)

@router.get("/{site_id}/members", response_model = list[SiteMemberResponse], summary = "Lấy danh sách thành viên công trình")
def get_members(site_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_site_members(db = db, site_id = site_id, user_id = current_user.id)