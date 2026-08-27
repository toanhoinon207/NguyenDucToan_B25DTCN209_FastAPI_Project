from fastapi import APIRouter, Depends, status
from app.schemas.user import RefreshTokenRequest, TokenResponse, UserCreate, UserLogin, UserResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth_service import login_user, refresh_token_service, register_user

router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

@router.post("/register", response_model = UserResponse, status_code = status.HTTP_201_CREATED, summary = "Đăng ký tài khoản")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_data)

@router.post("/login", response_model = TokenResponse, status_code = status.HTTP_200_OK, summary = "Đăng nhập tài khoản")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_data)

@router.post("/refresh", response_model = TokenResponse, status_code = status.HTTP_200_OK, summary = "Refresh token")
def refresh(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_token_service(db, token_data.refresh_token)