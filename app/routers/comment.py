from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependences.auth import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import create_comment, get_work_item_comments

router = APIRouter(
    prefix = "/work-items",
    tags = ["Work Item Comments"]
)

@router.post("/{work_item_id}/comments", response_model = CommentResponse, status_code = status.HTTP_201_CREATED, summary = "Thêm ghi chú nhật ký thi công")
def create_work_item_comment(work_item_id: int, comment_data: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_comment( db=db, work_item_id = work_item_id, user_id = current_user.id, comment_data = comment_data)

@router.get("/{work_item_id}/comments", response_model = list[CommentResponse], summary = "Xem ghi chú nhật ký thi công")
def get_comments(work_item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_work_item_comments(db = db, work_item_id = work_item_id, user_id = current_user.id)