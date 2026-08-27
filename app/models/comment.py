from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class WorkItemComment(Base):
    __tablename__ = "work_item_comments"
    id = Column(Integer, primary_key = True)
    work_item_id = Column(Integer, ForeignKey("work_items.id"), nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime, nullable = False, default = datetime.now)
    work_item = relationship("WorkItem", back_populates = "comments")
    user = relationship("User",back_populates = "work_item_comments")