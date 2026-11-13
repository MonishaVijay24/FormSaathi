"""Document + form OCR. Order: mock (demo) -> Gemini Vision -> Tesseract fallback (low confidence)."""
import io, json, re
from pathlib import Path
from app.config import get_settings
from app.core.errors import AppError
from app.schemas.models import DocFieldValue
from app.services.gemini_client import get_gemini

DATA = Path(__file__).resolve().parent.parent / "data"
DOC_LABELS = {"aadhaar": "Aadhaar card", "pan": "PAN card", "bpl": "BPL ration card",
              "passbook": "bank passbook front page", "income_certificate": "income certificate",
              "marks_card": "marks card"}
DOC_KEYS = {
    "aadhaar": ["name", "father_name", "mother_name", "dob", "gender", "aadhaar_number", "mobile", "email",
                "address_line1", "village", "taluk", "district", "state", "pin_code"],
    "pan": ["pan", "name", "father_name", "dob"],
    "bpl": ["name", "father_name", "mother_name", "dob", "age", "gender", "ration_card_no", "ration_card_type",
            "address_line1", "village", "taluk", "district", "state", "pin_code"],
    "passbook": ["name", "account_holder", "father_name", "account_number", "ifsc", "bank_name", "branch",
                 "branch_code", "cif_no", "account_type", "mobile", "dob", "pan", "address_line1", "village",
                 "taluk", "district", "pin_code"],
    "income_certificate": ["name", "annual_income"],
    "marks_card": ["name"],
}


def demo_documents() -> dict:
    return json.loads((DATA / "demo_documents.json").read_text(encoding="utf-8"))


def _from_mock(doc_type: str) -> dict[str, DocFieldValue]:
    return {k: DocFieldValue(value=v, confidence=0.95) for k, v in demo_documents().get(doc_type, {}).items()}


def _clean(raw: dict, doc_type: str) -> dict[str, DocFieldValue]:
    allowed = set(DOC_KEYS[doc_type])
    out = {}
    for k, v in (raw.get("fields") or {}).items():
        if k in allowed and isinstance(v, dict) and str(v.get("value", "")).strip():
            conf = max(0.0, min(1.0, float(v.get("confidence", 0.5) or 0.5)))
            out[k] = DocFieldValue(value=str(v["value"]).strip(), confidence=conf)
    return out


def _tesseract(doc_type: str, data: bytes) -> dict[str, DocFieldValue]:
    try:
        import pytesseract
        from PIL import Image
        text = pytesseract.image_to_string(Image.open(io.BytesIO(data)))
    except Exception:
        raise AppError(502, "OCR_UNAVAILABLE", "Could not read this document. Try a clearer photo or type the details.")
    found = {}
    for key, pat in {"dob": r"\b\d{2}/\d{2}/\d{4}\b", "mobile": r"\b[6-9]\d{9}\b",
                     "ifsc": r"\b[A-Z]{4}0[A-Z0-9]{6}\b", "pin_code": r"\b\d{6}\b"}.items():
        m = re.search(pat, text)
        if m and key in DOC_KEYS[doc_type]:
            found[key] = DocFieldValue(value=m.group(0), confidence=0.5)   # always low => user must review
    return found


def extract_document(doc_type: str, data: bytes, mime: str) -> tuple[dict[str, DocFieldValue], str]:
    s = get_settings()
    if s.use_mock_ai:
        return _from_mock(doc_type), "mock"
    prompt = (
        f"You are reading a SAMPLE (fictional demo) Indian {DOC_LABELS[doc_type]}. Extract ONLY text that is "
        'visible, as JSON: {"fields": {"<key>": {"value": "<as printed>", "confidence": <0..1>}}}. '
        f"Allowed keys: {', '.join(DOC_KEYS[doc_type])}. Dates as DD/MM/YYYY. Split the address into "
        "address_line1, village, taluk, district, state, pin_code. Omit keys that are not visible. Never guess.")
    if mime == "application/pdf":
        raise AppError(503, "LOCAL_OCR_UNAVAILABLE", "Local PDF OCR is unavailable. Convert the page to an image or enter details manually.")
    return _tesseract(doc_type, data), "tesseract"


def extract_form_fields(data: bytes, mime: str, form_hint: str | None) -> dict:
    """Return the list of input labels printed on an uploaded blank form."""
    from app.services.form_mapper import template_labels
    return {"form_title": form_hint or "demo", "labels": template_labels(form_hint), "engine": "local-template"}
