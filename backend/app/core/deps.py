import time
from fastapi import Request, Response
from itsdangerous import URLSafeSerializer, BadSignature
from app.config import get_settings
from app.core.errors import AppError
from app.core.session_store import get_store
from app.schemas.models import SessionData


def _signer() -> URLSafeSerializer:
    return URLSafeSerializer(get_settings().secret_key, salt="fs-session")


def set_session_cookie(response: Response, sid: str) -> None:
    st = get_settings()
    response.set_cookie(st.cookie_name, _signer().dumps(sid), httponly=True, secure=st.cookie_secure,
                        samesite=st.cookie_samesite, max_age=st.session_max_hours * 3600, path="/")


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(get_settings().cookie_name, path="/")


def _sid(request: Request) -> str:
    raw = request.cookies.get(get_settings().cookie_name)
    if not raw:
        raise AppError(401, "NO_SESSION", "No session. Call POST /api/session first.")
    try:
        return _signer().loads(raw)
    except BadSignature:
        raise AppError(401, "NO_SESSION", "Invalid session cookie.")


def peek_session(request: Request) -> SessionData:
    """Read the session WITHOUT extending it (used for timer polling)."""
    s = get_store().load(_sid(request), touch=False)
    if not s:
        raise AppError(401, "SESSION_EXPIRED", "Your session has expired. Please start again.")
    return s


def require_session(request: Request, response: Response) -> SessionData:
    """Read the session and slide the idle timeout (any real action counts as activity)."""
    s = get_store().load(_sid(request), touch=True)
    if not s:
        raise AppError(401, "SESSION_EXPIRED", "Your session has expired. Please start again.")
    response.headers["X-Session-Expires-In"] = str(max(0, int(s.expires_at - time.time())))
    return s
