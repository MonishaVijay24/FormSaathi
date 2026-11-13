"""Strict public request schema for the AI privacy gateway."""
from app.security.privacy_gateway import GenericAIRequest, validate_generic_request

__all__ = ["GenericAIRequest", "validate_generic_request"]
