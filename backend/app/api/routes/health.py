from fastapi import APIRouter
from app.config import get_settings
from app.core.errors import AppError
from app.services.gemini_client import get_gemini

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Liveness + configuration summary")
def health():
    s = get_settings()
    return {"status": "ok", "env": s.app_env, "mock_ai": s.use_mock_ai,
            "gemini_key_present": bool(s.gemini_api_key), "tts_enabled": s.tts_enabled,
            "idle_timeout_minutes": s.session_idle_minutes}


@router.get("/gemini", summary="Live Gemini key test (dev only)")
def gemini_check():
    if get_settings().app_env != "dev":
        raise AppError(404, "NOT_FOUND", "Not available.")
    return get_gemini().ping()
