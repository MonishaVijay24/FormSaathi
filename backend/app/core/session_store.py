import sqlite3, time, uuid, os
from functools import lru_cache
from typing import Optional
from app.config import get_settings
from app.schemas.models import SessionData
from app.security.encryption import encrypt_value, decrypt_value


class SessionStore:
    """SQLite-backed sessions. Survives page reloads and server restarts.
    Swap for Redis in production by keeping this same interface."""

    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.path = path
        with self._conn() as c:
            c.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, data TEXT NOT NULL, expires_at REAL NOT NULL)")

    def _conn(self):
        return sqlite3.connect(self.path, timeout=10)

    def _deadline(self, s: SessionData, now: float) -> float:
        st = get_settings()
        return min(now + st.session_idle_minutes * 60, s.created_at + st.session_max_hours * 3600)

    def create(self, language: str, consent: bool) -> SessionData:
        now = time.time()
        s = SessionData(id=uuid.uuid4().hex, created_at=now, last_active=now, expires_at=0,
                        language=language, consent=consent)
        s.expires_at = self._deadline(s, now)
        self.save(s)
        return s

    def load(self, sid: str, touch: bool = False) -> Optional[SessionData]:
        with self._conn() as c:
            row = c.execute("SELECT data FROM sessions WHERE id=?", (sid,)).fetchone()
        if not row:
            return None
        s = SessionData.model_validate_json(decrypt_value(row[0], context=f"session:{sid}"))
        now = time.time()
        if now > s.expires_at:
            self.delete(sid)
            return None
        if touch:
            s.last_active = now
            s.expires_at = self._deadline(s, now)
            self.save(s)
        return s

    def save(self, s: SessionData) -> None:
        with self._conn() as c:
            encrypted = encrypt_value(s.model_dump_json(), context=f"session:{s.id}")
            c.execute("INSERT OR REPLACE INTO sessions (id, data, expires_at) VALUES (?,?,?)",
                      (s.id, encrypted, s.expires_at))

    def delete(self, sid: str) -> None:
        with self._conn() as c:
            c.execute("DELETE FROM sessions WHERE id=?", (sid,))

    def purge_expired(self) -> int:
        with self._conn() as c:
            return c.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),)).rowcount


@lru_cache
def get_store() -> SessionStore:
    return SessionStore(get_settings().db_path)
