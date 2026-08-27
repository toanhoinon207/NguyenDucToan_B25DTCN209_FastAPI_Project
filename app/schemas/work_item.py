from datetime import datetime, timedelta
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class WorkItemBase(BaseModel):
    title: str
    description: str | None = None
    status: Literal["TODO", "IN_PROGRESS", "DONE"] = "TODO"
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    due_date: datetime | None = Field( default = None, json_schema_extra = {"example": datetime.now() + timedelta(days = 5)})

class WorkItemCreate(WorkItemBase):
    assignee_id: int | None = None

class WorkItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None

class WorkItemStatusUpdate(BaseModel):
    status: Literal["TODO", "IN_PROGRESS", "DONE"]

class WorkItemResponse(WorkItemBase):
    id: int
    site_id: int
    assignee_id: int | None
    created_at: datetime
    file_path: str | None = None 
    model_config = ConfigDict(from_attributes = True)