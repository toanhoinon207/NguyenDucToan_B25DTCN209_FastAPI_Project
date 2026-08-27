from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog

def create_activity_log(db: Session, user_id: int, action: str, site_id: int | None = None, description: str | None = None):
    log = ActivityLog(
        user_id = user_id,
        action = action,
        site_id = site_id,
        description = description
    )
    db.add(log)
    return log