from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token, hash_password, verify_password

def register_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email đã tồn tại"
        )
    
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email = user_data.email,
        password_hash = hashed_password,
        full_name = user_data.full_name,
        role = "USER",
        is_active = True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user_data: UserLogin):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Email hoặc mật khẩu không đúng"
        )
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Email hoặc mật khẩu không đúng"
        )
    if not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Tài khoản đã ngừng hoạt động"
        )
    
    token_payload = {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    }
    access_token = create_access_token(data = token_payload)
    refresh_token = create_refresh_token(data = token_payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"  
    }

def refresh_token_service(db: Session, refresh_token: str):
    try:
        payload = decode_refresh_token(refresh_token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Token không hợp lệ"
            )
    except ValueError as exc:
        if str(exc) == "TOKEN_EXPIRED":
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Refresh token đã hết hạn"
            )
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Refresh token không hợp lệ"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Người dùng không tồn tại"
        )
    if not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Tài khoản đã ngừng hoạt động"
        )

    token_payload = {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    }
    new_access_token = create_access_token(data = token_payload)
    new_refresh_token = create_refresh_token(data = token_payload)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }