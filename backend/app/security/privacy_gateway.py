"""Allowlist boundary for generic Gemini requests. Applicant content has no schema path here."""
from pydantic import BaseModel, ConfigDict, Field
from app.core.errors import AppError

ALLOWED_TASKS = {"generate_generic_question", "explain_generic_field"}
ALLOWED_LANGUAGES = {"en", "kn", "hi"}
ALLOWED_LABELS = {
    "Annual family income", "Marital status", "Relationship type",
    "Ration card type", "Whether receiving another pension", "Declaration confirmation",
}
BLOCKED = "Privacy protection activated. Personal information cannot be shared with the AI service."


class GenericAIRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    task: str
    field_label: str = Field(min_length=1, max_length=80)
    language: str


def validate_generic_request(payload: GenericAIRequest) -> GenericAIRequest:
    if payload.task not in ALLOWED_TASKS or payload.language not in ALLOWED_LANGUAGES or payload.field_label not in ALLOWED_LABELS:
        raise AppError(422, "PRIVACY_BLOCKED", BLOCKED)
    return payload


def generic_prompt(payload: GenericAIRequest) -> str:
    validate_generic_request(payload)
    return (f"Provide a short, generic {payload.task.replace('_', ' ')} for the form field "
            f"'{payload.field_label}' in language code {payload.language}. Do not ask for or infer an individual's answer.")
