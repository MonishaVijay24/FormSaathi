from typing import Literal, Optional
from pydantic import BaseModel, Field

Lang = Literal["en", "kn", "hi"]
Status = Literal["looks_consistent", "please_verify", "possible_mismatch",
                 "evidence_needed", "low_confidence", "fix_required"]
Severity = Literal["blocking", "should_fix", "minor"]
DocType = Literal["aadhaar", "pan", "bpl", "passbook", "income_certificate", "marks_card"]
FormId = Literal["bank_account", "pension"]


class Issue(BaseModel):
    field_id: str
    status: Status
    rule_code: str
    severity: Severity = "should_fix"
    message: dict[str, str]                 # {"en","kn","hi"}
    form_value: Optional[str] = None        # masked if sensitive
    evidence_value: Optional[str] = None    # masked if sensitive
    source_doc: Optional[str] = None
    requested_document: Optional[str] = None
    action: str = "confirm_or_edit"


# ---------- stored session state ----------
class DocFieldValue(BaseModel):
    value: str
    confidence: float = 1.0


class StoredDocument(BaseModel):
    doc_type: str
    filename: str
    uploaded_at: float
    engine: str = "mock"
    fields: dict[str, DocFieldValue] = {}


class ProfileField(BaseModel):
    key: str
    value: str
    source_doc: str
    confidence: float = 1.0
    confirmed: bool = False
    edited: bool = False
    confirmed_at: Optional[float] = None


class Answer(BaseModel):
    field_id: str
    value: str
    source: str = "text"          # profile | computed | voice | text | edit
    transcript: Optional[str] = None
    confirmed: bool = False
    confirmed_at: Optional[float] = None
    issue: Optional[Issue] = None


class Pending(BaseModel):
    field_id: str
    value: str
    source: str
    source_doc: Optional[str] = None
    transcript: Optional[str] = None
    issue: Optional[Issue] = None
    stage: Literal["prefill", "answer"] = "answer"


class ApplicationState(BaseModel):
    form_id: str
    language: str = "kn"
    field_ids: list[str]
    answers: dict[str, Answer] = {}
    pending: Optional[Pending] = None
    skipped_prefill: list[str] = []
    created_at: float = 0


class SessionData(BaseModel):
    id: str
    created_at: float
    last_active: float
    expires_at: float
    language: str = "kn"
    consent: bool = False
    documents: dict[str, StoredDocument] = {}
    profile: dict[str, ProfileField] = {}
    application: Optional[ApplicationState] = None


# ---------- API request / response ----------
class SessionCreate(BaseModel):
    language: Lang = "kn"
    consent: bool = Field(..., description="User consent to document processing (required)")
    model_config = {"json_schema_extra": {"example": {"language": "kn", "consent": True}}}


class SessionStatus(BaseModel):
    active: bool = True
    language: str
    consent: bool
    seconds_remaining: int
    warn: bool
    warn_after_seconds: int
    has_application: bool = False


class StartIn(BaseModel):
    form_id: FormId
    language: Lang = "kn"
    field_ids: Optional[list[str]] = Field(None, description="Optional subset/order from /forms/extract")
    model_config = {"json_schema_extra": {"example": {"form_id": "bank_account", "language": "kn"}}}


class AnswerIn(BaseModel):
    field_id: str
    value: str = Field(..., description="Transcript or typed text")
    input_mode: Literal["voice", "text", "keypad", "choice"] = "voice"
    language: Lang = "kn"
    reveal: bool = Field(False, description="Read sensitive values back in full instead of masked")
    model_config = {"json_schema_extra": {"example": {
        "field_id": "applicant_name", "value": "Ramesh Kumar", "input_mode": "text", "language": "en"}}}


class ConfirmIn(BaseModel):
    field_id: str
    confirmed: Optional[bool] = Field(None, description="Explicit yes/no (button)")
    transcript: Optional[str] = Field(None, description="Spoken yes/no, parsed in en/kn/hi")
    language: Lang = "kn"
    model_config = {"json_schema_extra": {"example": {"field_id": "applicant_name", "confirmed": True, "language": "kn"}}}


class EditIn(BaseModel):
    value: str
    language: Lang = "kn"


class SpeakIn(BaseModel):
    text: str = Field(..., max_length=500)
    lang: Lang = "kn"
