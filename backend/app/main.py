import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, session, profile, forms, applications, voice, export, privacy
from app.config import get_settings
from app.core.errors import AppError, app_error_handler
from app.core.session_store import get_store
from app.services import tts_service


@asynccontextmanager
async def lifespan(_):
    async def janitor():
        while True:
            await asyncio.sleep(300)
            get_store().purge_expired()
            tts_service.purge_old()
    get_store()
    task = asyncio.create_task(janitor())
    yield
    task.cancel()


DESC = """Backend for **FormSaathi AI** (demo, fictional data only).

**Try it in Swagger:** `POST /api/session` -> `POST /api/profile/demo-load` -> `POST /api/profile/confirm-all`
-> `POST /api/applications/start` -> loop `current/answer` + `current/confirm` -> `current/validate` -> `export/form.pdf`.

The session cookie is HttpOnly and set by `POST /api/session`; Swagger sends it automatically.
AI reads and explains. Rules decide. The applicant confirms. Nothing is ever submitted."""

app = FastAPI(title="FormSaathi AI API", version="0.1.0", description=DESC, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=get_settings().origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"], expose_headers=["X-Session-Expires-In", "Content-Disposition"])
app.add_exception_handler(AppError, app_error_handler)
for r in (health, session, profile, forms, applications, voice, export, privacy):
    app.include_router(r.router, prefix="/api")
