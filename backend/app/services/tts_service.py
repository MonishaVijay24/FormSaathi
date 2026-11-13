"""Privacy-safe speech response. Cloud speech synthesis is intentionally disabled."""
def speak(text: str, lang: str) -> dict:
    """-> {"text": ..., "audio_url": str|None, "tts_fallback": bool}"""
    return {"text": text, "audio_url": None, "tts_fallback": True, "lang": lang}


def audio_path(audio_id: str):
    return None


def purge_old() -> int:
    return 0
