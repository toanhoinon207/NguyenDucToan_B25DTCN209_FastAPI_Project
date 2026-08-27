from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(255), unique = True, nullable = False)
    password_hash = Column(String(255), nullable = False)
    full_name = Column(String(255), nullable = False)
    role = Column(Enum("USER", "ADMIN"), nullable = False, default = "USER")
    is_active = Column(Boolean, default = True)
    created_at = Column(DateTime, nullable = False, default = datetime.now)
    owned_sites = relationship("ConstructionSite", back_populates = "owner")
    memberships = relationship("SiteMember", back_populates = "user")
    assigned_work_items = relationship("WorkItem", back_populates = "assignee")
    work_item_comments = relationship("WorkItemComment", back_populates = "user")