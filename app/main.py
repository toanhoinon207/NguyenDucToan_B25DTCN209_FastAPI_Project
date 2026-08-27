from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from app.db.database import Base, engine
from app.models.site import ConstructionSite, SiteMember
from app.models.user import User
from app.models.work_item import WorkItem
from app.models.activity_log import ActivityLog
from app.models.comment import WorkItemComment
from app.utils.exceptions import http_exception_handler, validation_exception_handler
from app.routers.auth import router as AuthRouter
from app.routers.users import router as UsersRouter
from app.routers.site import router as SiteRouter
from app.routers.work_item import router as WorkItemRouter
from app.routers.comment import router as CommentRouter

Base.metadata.create_all(bind = engine)

app = FastAPI(title="Construction Management API")

app.include_router(AuthRouter)
app.include_router(UsersRouter)
app.include_router(SiteRouter)
app.include_router(WorkItemRouter)
app.include_router(CommentRouter)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "API đang chạy",
        "data": {
            "status": "OK"
        }
    }

@app.get("/test/400")
def test_400():
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST,
        detail = "Dữ liệu không hợp lệ"
    )

@app.get("/test/403")
def test_403():
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Bạn không có quyền truy cập"
    )

@app.get("/test/404")
def test_404():
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Không tìm thấy tài nguyên"
    )