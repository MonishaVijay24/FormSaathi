from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    secret_key: str = "change-me"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    cookie_name: str = "fs_session"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    session_idle_minutes: int = 15
    session_warn_seconds: int = 120
    session_max_hours: int = 4

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    mock_ai: bool = True

    tts_enabled: bool = False
    audio_ttl_minutes: int = 60

    db_path: str = "./storage/sessions.db"
    tts_cache_dir: str = "./storage/tts"
    max_upload_mb: int = 8
    encryption_key: str = ""

    @property
    def use_mock_ai(self) -> bool:
        return self.mock_ai or not self.gemini_api_key

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
