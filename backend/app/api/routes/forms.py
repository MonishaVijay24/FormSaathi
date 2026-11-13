from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.core.deps import require_session
from app.core.errors import AppError
from app.data.field_library import LIB
from app.schemas.models import SessionData
from app.services import ocr_service
from app.services.form_mapper import forms, map_labels, guess_form

router = APIRouter(prefix="/forms", tags=["Forms"])
_MAGIC = {b"\xff\xd8\xff": "image/jpeg", b"\x89PNG": "image/png", b"%PDF": "application/pdf"}


@router.get("", summary="List the two demo forms")
def list_forms(lang: str = "en"):
    lang = lang if lang in ("en", "kn", "hi") else "en"
    return [{"form_id": f["id"], "title": f["title"][lang], "field_count": len(f["fields"]), "evidence": f["evidence"]}
            for f in forms().values()]


@router.get("/{form_id}/fields", summary="Question list for a form (no answers)")
def form_fields(form_id: str, lang: str = "en"):
    f = forms().get(form_id)
    if not f:
        raise AppError(404, "UNKNOWN_FORM", "Unknown form.")
    lang = lang if lang in ("en", "kn", "hi") else "en"
    return [{"field_id": i, "label": LIB[i]["label"][lang], "prompt": LIB[i]["prompt"][lang], "group": LIB[i]["group"],
             "input_mode": LIB[i]["input_mode"], "required": LIB[i]["required"], "sensitive": LIB[i]["sensitive"]}
            for i in f["fields"]]


@router.post("/extract", summary="Upload a photo/PDF of the BLANK form -> detect fields -> map to questions")
def extract_form(file: UploadFile = File(...), form_id: Optional[str] = Form(None),
                 s: SessionData = Depends(require_session)):
    data = file.file.read()
    mime = next((m for sig, m in _MAGIC.items() if data.startswith(sig)), None)
    if not mime:
        raise AppError(415, "UNSUPPORTED_FILE", "Please upload a JPG, PNG or PDF file.")
    raw = ocr_service.extract_form_fields(data, mime, form_id)
    mapped = map_labels(raw["labels"])
    gid = form_id or guess_form(raw["labels"], raw["form_title"])
    return {"form_id": gid, "engine": raw["engine"], "detected_labels": raw["labels"],
            "field_ids": [m["field_id"] for m in mapped["matched"]], **mapped,
            "note": "Unmatched labels are not asked yet. Pass field_ids to POST /applications/start."}
