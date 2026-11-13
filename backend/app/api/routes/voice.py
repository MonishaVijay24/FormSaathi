from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse
from app.core.deps import require_session
from app.core.errors import AppError
from app.schemas.models import SessionData, SpeakIn
from app.services import tts_service
from app.services.gemini_client import get_gemini

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/speak", summary="Text -> speech (kn/hi/en). Returns audio_url or tts_fallback=true")
def speak(body: SpeakIn, s: SessionData = Depends(require_session)):
    return tts_service.speak(body.text, body.lang)


@router.get("/audio/{audio_id}", summary="Fetch generated MP3", response_class=FileResponse)
def audio(audio_id: str, s: SessionData = Depends(require_session)):
    p = tts_service.audio_path(audio_id)
    if not p:
        raise AppError(404, "AUDIO_NOT_FOUND", "Audio expired. Ask for the question again.")
    return FileResponse(p, media_type="audio/mpeg")


@router.post("/transcribe", summary="Speech -> text with Gemini (optional; browser SpeechRecognition also works)")
def transcribe(lang: str = Form("kn"), file: UploadFile = File(...), s: SessionData = Depends(require_session)):
    raise AppError(503, "LOCAL_STT_UNAVAILABLE", "Cloud speech transcription is disabled for privacy. Use local speech recognition or type your answer.")
