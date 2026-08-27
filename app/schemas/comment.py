from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    work_item_id: int
    user_id: int
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes = True)