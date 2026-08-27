from datetime import datetime, timedelta
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class WorkItem(Base):
    __tablename__ = "work_items"
    id = Column(Integer, primary_key = True)
    site_id = Column(Integer, ForeignKey("construction_sites.id"), nullable = False)
    title = Column(String(255), nullable = False)
    description = Column(Text, nullable = True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable = True)
    status = Column(Enum("TODO", "IN_PROGRESS", "DONE"), nullable = False, default = "TODO")
    priority = Column(Enum("LOW", "MEDIUM", "HIGH"), nullable = False, default = "MEDIUM")
    due_date = Column(DateTime, nullable = False)
    created_at = Column(DateTime, nullable = False, default = datetime.now)
    file_path = Column(String(500), nullable = True)
    site = relationship("ConstructionSite", back_populates = "work_items")
    assignee = relationship("User", back_populates = "assigned_work_items")
    comments = relationship("WorkItemComment", back_populates="work_item", cascade="all, delete-orphan")