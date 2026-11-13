"""Only fixed generic prompt construction is permitted at the Gemini boundary."""
from app.security.privacy_gateway import GenericAIRequest, generic_prompt

__all__ = ["generic_prompt", "GenericAIRequest"]
