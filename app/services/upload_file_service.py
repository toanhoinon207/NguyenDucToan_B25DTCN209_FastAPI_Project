import os
import uuid
from fastapi import HTTPException, status, UploadFile
from app.models.work_item import WorkItem
from app.models.site import ConstructionSite, SiteMember

ALLOWED_EXT = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_MIME = {"application/pdf", "image/png", "image/jpeg"}
MAX_SIZE = 50 * 1024 * 1024

async def upload_file(db, work_item_id, user_id, file: UploadFile):
    work_item = db.query(WorkItem).filter(WorkItem.id == work_item_id).first()
    if not work_item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy hạng mục"
        )

    site = db.query(ConstructionSite).filter(ConstructionSite.id == work_item.site_id, ConstructionSite.is_deleted == False).first()
    if not site:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy công trình"
        )

    member = db.query(SiteMember).filter(SiteMember.site_id == work_item.site_id, SiteMember.user_id == user_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của công trình này"
        )
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT or file.content_type not in ALLOWED_MIME:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "File không hợp lệ"
        )
    os.makedirs("uploads", exist_ok = True)
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join("uploads", filename)
    size = 0
    try:
        with open(path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_SIZE:
                    raise HTTPException(
                        status_code = status.HTTP_413_CONTENT_TOO_LARGE,
                        detail = "File vượt quá 50MB"
                    ) 
                f.write(chunk)
        work_item.file_path = path
        db.commit()
        db.refresh(work_item)
        return {
            "message": "Upload thành công",
            "file_path": path
        }
    except HTTPException:
        db.rollback()
        if os.path.exists(path):
            os.remove(path)
        raise
    finally:
        await file.close()