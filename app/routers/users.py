from fastapi import APIRouter, Depends, Query
from app.dependences.auth import get_current_user, require_role
from app.models.user import User
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.user_service import get_users, update_user_status

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.get("/me", response_model = UserResponse, summary = "Lấy thông tin tài khoản")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("", response_model = list[UserResponse], summary = "Lấy danh sách người dùng")
def get_list_user(email: str | None = Query(default = None), full_name: str | None = Query(default = None), is_active: bool | None = Query(default = None), current_user: User = Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    return get_users(db = db, email= email, full_name = full_name, is_active = is_active)

@router.put("/{user_id}",  response_model = UserResponse, summary = "Cập nhật trạng thái người dùng")
def update_user(user_id: int, is_active: bool, current_user: User = Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    return update_user_status(db = db, user_id = user_id, is_active = is_active)