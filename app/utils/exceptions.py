from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
            "data": None,
            "errors": None,
            "path": request.url.path
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {
            "success": False,
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": exc.errors()[0]["msg"],
            "data": None,
            "errors": exc.errors()[0]["msg"],
            "path": request.url.path
        }
    )