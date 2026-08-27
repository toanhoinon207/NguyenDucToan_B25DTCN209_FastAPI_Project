from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class ConstructionSite(Base):
    __tablename__ = "construction_sites"
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    description = Column(Text, nullable = True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    created_at = Column(DateTime, nullable = False, default = datetime.now)
    is_deleted = Column(Boolean, default = False, nullable = False)
    owner = relationship("User", back_populates = "owned_sites")
    members = relationship("SiteMember", back_populates = "site")
    work_items = relationship("WorkItem", back_populates = "site")

class SiteMember(Base):
    __tablename__ = "site_members"
    site_id = Column(Integer, ForeignKey("construction_sites.id"), primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key = True)
    role = Column(Enum("OWNER", "MEMBER"), nullable = False, default = "MEMBER")
    joined_at = Column(DateTime, nullable = False, default = datetime.now)
    site = relationship("ConstructionSite", back_populates = "members")
    user = relationship("User", back_populates = "memberships")