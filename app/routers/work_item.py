from typing import Literal
from fastapi import APIRouter, Depends, Query, UploadFile, status, File
from sqlalchemy.orm import Session
from app.schemas.work_item import WorkItemCreate, WorkItemResponse, WorkItemStatusUpdate, WorkItemUpdate
from app.db.database import get_db
from app.models.user import User
from app.dependences.auth import get_current_user
from app.services.work_item_service import create_work_item, delete_work_item, get_site_work_items, get_work_item, update_work_item_status, update_work_items
from app.services.upload_file_service import upload_file

router = APIRouter(
    prefix = "/work-items",
    tags=["Work Items"]
)

@router.post("/{site_id}/work-items", response_model = WorkItemResponse, status_code = status.HTTP_201_CREATED, summary = "Tạo hạng mục thi công")
def create_item(site_id: int, work_item_data: WorkItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_work_item(db = db, site_id = site_id, user_id = current_user.id, work_item_data = work_item_data)
 
@router.get("/{site_id}/work-items", response_model = list[WorkItemResponse], summary = "Lấy danh sách hạng mục thi công")
def get_work_items(site_id: int, search: str | None = None, status_filter: Literal["TODO", "IN_PROGRESS", "DONE"] | None = None, priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None, assignee_id: int | None = Query(default = None, gt = 0), limit: int = Query(default = 10, ge = 1, le = 100), offset: int = Query(default = 0, ge = 0), sort_by: Literal["created_at", "due_date"] = "created_at", sort_order: Literal["asc", "desc"] = "desc", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_site_work_items(db = db, site_id = site_id, user_id = current_user.id, search=search, status_filter= status_filter, priority = priority, assignee_id = assignee_id, limit = limit, offset = offset, sort_by = sort_by, sort_order = sort_order)

@router.get("/{work_item_id}", response_model = WorkItemResponse, summary = "Xem chi tiết hạng mục thi công")
def get_work_item_detail(work_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_work_item(db = db, work_item_id = work_item_id, user_id = current_user.id)

@router.patch("/{work_item_id}", response_model = WorkItemResponse, summary = "OWNER cập nhật hạng mục")
def update_work_item_api(work_item_id: int, work_item_data: WorkItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_work_items(db = db, work_item_id = work_item_id, user_id = current_user.id, work_item_data = work_item_data)

@router.patch("/{work_item_id}/status", response_model = WorkItemResponse, summary = "Cập nhật trạng thái hạng mục")
def update_status(work_item_id: int, data: WorkItemStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_work_item_status(db = db, work_item_id = work_item_id, user_id = current_user.id, status_value = data.status)

@router.delete("/{work_item_id}", summary = "Xóa hạng mục thi công")
def delete_item(work_item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_work_item(db = db, work_item_id = work_item_id, user_id = current_user.id)

@router.post("/{work_item_id}/upload", summary = "Tải file đính kèm cho hạng mục thi công")
async def upload_work_item_file(work_item_id: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await upload_file(db, work_item_id, current_user.id, file)