from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Literal

class ConstructionSiteBase(BaseModel):
    name: str = Field(..., min_length = 1, max_length = 255)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Tên công trình không được để trống")

        return value
    
class ConstructionSiteCreate(ConstructionSiteBase):
    pass

class ConstructionSiteUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ConstructionSiteResponse(ConstructionSiteBase):
    id: int
    owner_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes = True)

class SiteMemberBase(BaseModel):
    role: Literal["OWNER", "MEMBER"] = "MEMBER"

class SiteMemberCreate(BaseModel):
    user_id: int

class SiteMemberUpdate(BaseModel):
    role: Literal["OWNER", "MEMBER"] | None = None

class SiteMemberResponse(SiteMemberBase):
    site_id: int
    user_id: int
    joined_at: datetime
    model_config = ConfigDict(from_attributes = True)