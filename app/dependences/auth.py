from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Token không hợp lệ"
            )
    except ValueError as exc:
        if str(exc) == "TOKEN_EXPIRED":
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Token đã hết hạn"
            )
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token không hợp lệ"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Người dùng không tồn tại"
        )
    if not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Tài khoản đã ngừng hoạt động"
        )
    return user

def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Bạn không có quyền thực hiện thao tác này"
            )
        return current_user
    return role_checker