from fastapi import APIRouter
from app.core.errors import AppError
from app.security.request_validator import GenericAIRequest
from app.services.gemini_client import get_gemini

router = APIRouter(prefix="/privacy", tags=["Privacy"])


@router.post("/generic-question")
def generic_question(body: GenericAIRequest):
    """Only fixed generic field metadata can reach Gemini; extra fields are rejected."""
    client = get_gemini()
    try:
        return {"text": client.generate_generic(body), "source": "gemini" if client.ready else "local-fallback"}
    except AppError:
        raise
    except Exception as exc:
        raise AppError(502, "GENERIC_AI_UNAVAILABLE", "Generic question service is unavailable.") from exc
