from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length = 6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length = 6)

class UserUpdate(BaseModel):
    is_active: bool | None = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str