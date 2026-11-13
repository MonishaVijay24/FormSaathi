import time
from fastapi import APIRouter, Depends, Request, Response
from app.config import get_settings
from app.core.deps import (peek_session, require_session, set_session_cookie, clear_session_cookie, _sid)
from app.core.session_store import get_store
from app.schemas.models import SessionCreate, SessionStatus, SessionData
from app.services import profile_service as ps

router = APIRouter(prefix="/session", tags=["Session"])


def _status(s: SessionData) -> SessionStatus:
    st = get_settings()
    rem = max(0, int(s.expires_at - time.time()))
    return SessionStatus(language=s.language, consent=s.consent, seconds_remaining=rem,
                         warn=rem <= st.session_warn_seconds, warn_after_seconds=st.session_warn_seconds,
                         has_application=s.application is not None)


@router.post("", response_model=SessionStatus, summary="Start a session (sets the HttpOnly cookie)")
def create_session(body: SessionCreate, request: Request, response: Response):
    try:                                   # replace any previous session for this browser
        get_store().delete(_sid(request))
    except Exception:
        pass
    s = get_store().create(body.language, body.consent)
    set_session_cookie(response, s.id)
    return _status(s)


@router.get("", response_model=SessionStatus, summary="Timer poll. Does NOT extend the session")
def session_status(s: SessionData = Depends(peek_session)):
    return _status(s)


@router.post("/extend", response_model=SessionStatus, summary="'Extend time' button. Keeps all answers")
def extend(s: SessionData = Depends(require_session)):
    return _status(s)


@router.get("/resume", summary="After a page reload: everything needed to restore the UI")
def resume(s: SessionData = Depends(require_session)):
    from app.api.routes.profile import profile_out
    from app.services import application_service as svc
    out = {"session": _status(s), "profile": profile_out(s), "application": None}
    if s.application:
        a = s.application
        out["application"] = {
            "form_id": a.form_id, "language": a.language,
            "answers": {k: {"value": v.value, "confirmed": v.confirmed, "source": v.source} for k, v in a.answers.items()},
            "question": svc.build_question(s, a.language)}
        get_store().save(s)
    return out


@router.put("/language/{lang}", response_model=SessionStatus, summary="Switch language; progress is kept")
def set_language(lang: str, s: SessionData = Depends(require_session)):
    if lang in ("en", "kn", "hi"):
        s.language = lang
        if s.application:
            s.application.language = lang
        get_store().save(s)
    return _status(s)


@router.delete("", status_code=204, summary="Delete session: removes answers, documents and profile")
def delete_session(response: Response, s: SessionData = Depends(require_session)):
    get_store().delete(s.id)
    clear_session_cookie(response)
