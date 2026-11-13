from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Uniform error: {"error": {"code": "...", "message": "...", "details": {...}}}"""

    def __init__(self, status: int, code: str, message: str, details: dict | None = None):
        self.status, self.code, self.message, self.details = status, code, message, details or {}


async def app_error_handler(_: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message, "details": exc.details}},
    )
