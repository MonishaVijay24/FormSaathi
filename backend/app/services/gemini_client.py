"""Thin wrapper over google-genai. Gemini is an *interpreter* (OCR, transliteration, STT);
rules decide, the applicant confirms. Backend-only: the key never reaches the browser."""
import json, re, time
from typing import Optional
from app.config import get_settings
from app.core.errors import AppError


def _parse_json(text: str) -> dict:
    text = re.sub(r"^```(?:json)?|```$", "", (text or "").strip(), flags=re.M).strip()
    return json.loads(text)


class GeminiClient:
    def __init__(self):
        self.s = get_settings()
        self._c = None

    @property
    def ready(self) -> bool:
        return not self.s.use_mock_ai

    def _client(self):
        if self._c is None:
            from google import genai
            self._c = genai.Client(api_key=self.s.gemini_api_key)
        return self._c

    def _call(self, contents, json_mode: bool):
        from google.genai import types
        cfg = types.GenerateContentConfig(temperature=0,
                                          response_mime_type="application/json" if json_mode else None)
        try:
            return self._client().models.generate_content(model=self.s.gemini_model, contents=contents, config=cfg)
        except Exception as e:  # network, quota, bad key ...
            raise AppError(502, "GEMINI_ERROR", f"Gemini request failed: {type(e).__name__}")

    def generate_json(self, prompt: str, data: Optional[bytes] = None, mime: Optional[str] = None) -> dict:
        raise AppError(403, "PRIVACY_BLOCKED", "Gemini document processing is disabled by the privacy firewall.")
        from google.genai import types
        contents = [prompt] if data is None else [types.Part.from_bytes(data=data, mime_type=mime), prompt]
        resp = self._call(contents, json_mode=True)
        try:
            return _parse_json(resp.text)
        except Exception:
            raise AppError(502, "GEMINI_BAD_JSON", "Gemini returned unreadable output. Please retry.")

    def generate_text(self, prompt: str) -> str:
        raise AppError(403, "PRIVACY_BLOCKED", "Use the Privacy Gateway with an allowlisted generic request.")

    def generate_generic(self, request) -> str:
        from app.security.privacy_gateway import validate_generic_request, generic_prompt
        safe = validate_generic_request(request)
        if not self.ready:
            return generic_prompt(safe)
        return (self._call([generic_prompt(safe)], json_mode=False).text or "").strip()
        return (self._call([prompt], json_mode=False).text or "").strip()

    def transliterate_to_latin(self, text: str) -> str:
        raise AppError(403, "PRIVACY_BLOCKED", "Applicant-specific text cannot be sent to Gemini.")
        out = self.generate_text(
            "Transliterate this personal name or address into English (Latin) letters, phonetically. "
            f"Do NOT translate its meaning. Reply with the result only.\n{text}")
        return out.strip().strip('"')

    def transcribe(self, audio: bytes, mime: str, lang: str) -> str:
        raise AppError(403, "PRIVACY_BLOCKED", "Applicant speech cannot be sent to Gemini.")
        from google.genai import types
        name = {"kn": "Kannada", "hi": "Hindi", "en": "English"}[lang]
        resp = self._call([types.Part.from_bytes(data=audio, mime_type=mime),
                           f"Transcribe this {name} speech exactly. Reply with the transcript only."], json_mode=False)
        return (resp.text or "").strip()

    def ping(self) -> dict:
        t0 = time.time()
        if not self.s.gemini_api_key:
            return {"ok": False, "detail": "GEMINI_API_KEY is empty"}
        try:
            reply = self.generate_text("Reply with the single word OK.")
            return {"ok": True, "model": self.s.gemini_model, "reply": reply[:20],
                    "latency_ms": int((time.time() - t0) * 1000)}
        except AppError as e:
            return {"ok": False, "model": self.s.gemini_model, "detail": e.message}


_client = GeminiClient()


def get_gemini() -> GeminiClient:
    return _client
