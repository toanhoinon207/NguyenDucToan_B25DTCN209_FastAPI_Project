from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.db.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    action = Column(String(50), nullable = False)
    site_id = Column(Integer, ForeignKey("construction_sites.id"), nullable = True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable = False, default = datetime.now)