from fastapi import APIRouter, Depends
from app.core.deps import require_session
from app.core.session_store import get_store
from app.schemas.models import AnswerIn, ConfirmIn, EditIn, SessionData, StartIn
from app.services import application_service as svc

router = APIRouter(prefix="/applications", tags=["Application (question loop)"])


@router.post("/start", summary="Start a form. Returns the first question (with audio)")
def start(body: StartIn, s: SessionData = Depends(require_session)):
    svc.start_application(s, body.form_id, body.language, body.field_ids)
    q = svc.build_question(s, body.language)
    get_store().save(s)
    return q


@router.get("/current/question", summary="Current question: prefill proposal, confirm prompt or plain question")
def question(lang: str = "kn", reveal: bool = False, s: SessionData = Depends(require_session)):
    q = svc.build_question(s, lang if lang in ("en", "kn", "hi") else "kn", reveal)
    get_store().save(s)
    return q


@router.post("/current/answer", summary="Submit a spoken/typed answer. Returns read-back prompt + any mismatch")
def answer(body: AnswerIn, s: SessionData = Depends(require_session)):
    out = svc.submit_answer(s, body.field_id, body.value, body.input_mode, body.language, body.reveal)
    get_store().save(s)
    return out


@router.post("/current/confirm", summary="Yes/No to the read-back. Yes saves and moves on")
def confirm(body: ConfirmIn, s: SessionData = Depends(require_session)):
    q = svc.confirm(s, body.field_id, body.confirmed, body.transcript, body.language)
    get_store().save(s)
    return q


@router.patch("/answers/{field_id}", summary="Edit an earlier answer; re-checks and returns readiness")
def edit(field_id: str, body: EditIn, s: SessionData = Depends(require_session)):
    out = svc.edit_answer(s, field_id, body.value, body.language)
    get_store().save(s)
    return out


@router.get("/current/validate", summary="Re-run all checks: readiness %, issues, evidence requests")
def validate(s: SessionData = Depends(require_session)):
    return svc.evaluate(s)


@router.get("/current/summary", summary="All answers so far (sensitive values masked)")
def summary(s: SessionData = Depends(require_session)):
    from app.data.field_library import LIB
    from app.services.text_utils import mask
    a = svc.app_of(s)
    return {"form_id": a.form_id, "answers": [
        {"field_id": f, "label": LIB[f]["label"]["en"], "group": LIB[f]["group"],
         "value": (mask(a.answers[f].value) if LIB[f]["sensitive"] else a.answers[f].value) if f in a.answers else None,
         "confirmed": bool(f in a.answers and a.answers[f].confirmed)} for f in a.field_ids]}
