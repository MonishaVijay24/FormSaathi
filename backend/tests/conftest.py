import os, tempfile
_tmp = tempfile.mkdtemp()
os.environ.update(MOCK_AI="true", TTS_ENABLED="false", DB_PATH=f"{_tmp}/s.db", TTS_CACHE_DIR=f"{_tmp}/tts",
                  SECRET_KEY="test", SESSION_IDLE_MINUTES="15")
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
