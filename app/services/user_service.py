from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User

def get_users(db: Session, email: str | None = None, full_name: str | None = None, is_active: bool | None = None):
    query = db.query(User)
    if full_name:
        query = query.filter((User.full_name.ilike(f"%{full_name}%")))
    if email:
        query = query.filter((User.email.ilike(f"%{email}%")))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()

def update_user_status(db: Session, user_id: int, is_active: bool):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User không tồn tại"
        )
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user
