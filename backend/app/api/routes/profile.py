from typing import Annotated, Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
from app.config import get_settings
from app.core.deps import require_session
from app.core.errors import AppError
from app.core.session_store import get_store
from app.data.field_library import SENSITIVE_KEYS
from app.schemas.models import DocType, SessionData, StoredDocument
from app.services import ocr_service, profile_service as ps
import time

router = APIRouter(prefix="/profile", tags=["Profile"])
_MAGIC = {b"\xff\xd8\xff": "image/jpeg", b"\x89PNG": "image/png", b"%PDF": "application/pdf"}


def profile_out(s: SessionData) -> dict:
    fields = [{"key": p.key, "value": None if p.key in SENSITIVE_KEYS else p.value, "value_display": ps.display_value(p),
               "source_doc": p.source_doc, "confidence": p.confidence, "confirmed": p.confirmed,
               "low_confidence": p.confidence < 0.8} for p in s.profile.values()]
    name = s.profile.get("name")
    return {"display_name": name.value if name else None, "fields": fields,
            "documents": [{"doc_type": d.doc_type, "filename": d.filename, "engine": d.engine} for d in s.documents.values()]}


def _need_consent(s: SessionData):
    if not s.consent:
        raise AppError(403, "CONSENT_REQUIRED", "Please give consent to process documents first.")


@router.get("", summary="Profile built from uploaded documents (sensitive values masked)")
def get_profile(s: SessionData = Depends(require_session)):
    return profile_out(s)


@router.post("/documents", summary="Upload a document image/PDF -> OCR -> profile fields")
def upload_document(doc_type: Annotated[DocType, Form()], file: UploadFile = File(...),
                    s: SessionData = Depends(require_session)):
    _need_consent(s)
    data = file.file.read()
    if len(data) > get_settings().max_upload_mb * 1024 * 1024:
        raise AppError(413, "FILE_TOO_LARGE", f"File is larger than {get_settings().max_upload_mb} MB.")
    mime = next((m for sig, m in _MAGIC.items() if data.startswith(sig)), None)
    if not mime:
        raise AppError(415, "UNSUPPORTED_FILE", "Please upload a JPG, PNG or PDF file.")
    fields, engine = ocr_service.extract_document(doc_type, data, mime)
    s.documents[doc_type] = StoredDocument(doc_type=doc_type, filename=(file.filename or doc_type)[:80],
                                           uploaded_at=time.time(), engine=engine, fields=fields)
    ps.rebuild_profile(s)
    get_store().save(s)
    return {"doc_type": doc_type, "engine": engine,
            "extracted": [{"key": k, "value_display": ps.display_value(s.profile[k]) if k in s.profile else v.value,
                           "confidence": v.confidence, "needs_review": v.confidence < 0.8} for k, v in fields.items()],
            "consistency_issues": ps.consistency(s)}


@router.post("/demo-load", summary="Load the 4 sample documents (Aadhaar, PAN, BPL, passbook) without OCR")
def demo_load(include_income_certificate: bool = False, s: SessionData = Depends(require_session)):
    _need_consent(s)
    for d in ["aadhaar", "pan", "bpl", "passbook"] + (["income_certificate"] if include_income_certificate else []):
        fields = ocr_service._from_mock(d)
        s.documents[d] = StoredDocument(doc_type=d, filename=f"demo_{d}.jpeg", uploaded_at=time.time(),
                                        engine="demo", fields=fields)
    ps.rebuild_profile(s)
    get_store().save(s)
    return {**profile_out(s), "consistency_issues": ps.consistency(s)}


class FieldPatch(BaseModel):
    value: Optional[str] = None
    confirmed: bool = True


@router.patch("/fields/{key}", summary="Confirm or correct one extracted value")
def patch_field(key: str, body: FieldPatch, s: SessionData = Depends(require_session)):
    pf = s.profile.get(key)
    if not pf:
        raise AppError(404, "UNKNOWN_PROFILE_FIELD", f"No profile field '{key}'.")
    if body.value is not None and body.value != pf.value:
        pf.value, pf.edited, pf.confidence = body.value.strip(), True, 1.0
    pf.confirmed, pf.confirmed_at = body.confirmed, time.time()
    get_store().save(s)
    return profile_out(s)


@router.post("/confirm-all", summary="Confirm every extracted value")
def confirm_all(s: SessionData = Depends(require_session)):
    ps.confirm_all(s)
    get_store().save(s)
    return profile_out(s)


@router.get("/consistency", summary="Details that differ between your documents")
def consistency(s: SessionData = Depends(require_session)):
    return {"issues": ps.consistency(s)}


@router.delete("/documents/{doc_type}", summary="Remove one document (and its profile values)")
def delete_document(doc_type: DocType, s: SessionData = Depends(require_session)):
    s.documents.pop(doc_type, None)
    ps.rebuild_profile(s)
    get_store().save(s)
    return profile_out(s)
