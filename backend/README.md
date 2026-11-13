# FormSaathi AI: Backend (FastAPI)

Demo backend for the FormSaathi frontend. **Fictional data only.** Nothing is ever submitted to a bank or government office.
Principle: *AI reads and explains, rules decide, the applicant confirms.*

## 1. Run it
```bash
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                   # Windows: copy .env.example .env
# Set ENCRYPTION_KEY in .env to the output of: python -c "import base64,secrets; print(base64.b64encode(secrets.token_bytes(32)).decode())"
uvicorn app.main:app --reload --port 8000
```
Swagger: http://localhost:8000/docs  |  ReDoc: /redoc  |  OpenAPI JSON: /openapi.json
Tests: `pytest -q` (12 tests, run in mock mode, no internet needed)

Optional for real OCR fallback: install Tesseract (`sudo apt install tesseract-ocr` / Windows installer).

## 2. Gemini privacy boundary
```bash
# Configure GEMINI_API_KEY in .env only if using generic question generation.
# POST /api/privacy/generic-question accepts fixed generic field labels only.
```
Document OCR, uploaded documents, applicant speech, answers and personal text are blocked from Gemini. Cloud TTS is disabled; use browser speech synthesis or typing. Local OCR requires Tesseract; PDF OCR currently falls back to manual entry/template fields.

Applicant session rows are AES-256-GCM encrypted at rest. `ENCRYPTION_KEY` must decode from base64 to exactly 32 random bytes; losing it makes existing session rows unreadable. Keep it server-side and out of source control. This prototype does not provide production user authentication or a durable applicant profile database.

## 3. Swagger walkthrough (5 minutes)
1. `POST /api/session` body `{"language":"kn","consent":true}` -> cookie is set (Swagger keeps it).
2. `POST /api/profile/demo-load` -> loads Ramesh's 4 sample documents. (Or `POST /api/profile/documents` with `doc_type=aadhaar` + your JPEG. In mock mode it returns the seeded values; with Gemini on it truly OCRs the image.)
3. `GET /api/profile/consistency` -> planted problems: **PAN differs** (`DEMO-PAN-1234` vs `DEMO-PAN-0001`) and **BPL age 70 vs DOB-computed 71**.
4. `POST /api/profile/confirm-all` (or `PATCH /api/profile/fields/{key}` per value).
5. `POST /api/applications/start` `{"form_id":"pension","language":"kn"}` -> first question, with `prompt.audio_url`.
6. Loop: if `stage=="prefill"`, call `current/confirm`; if `stage=="answer"`, call `current/answer`, then `current/confirm` (`confirmed:true` or `transcript:"ಹೌದು"`).
7. Try a mismatch: answer the name as `Ramesh Kumar` -> `possible_mismatch` with a message in en/kn/hi naming both values and the source document.
8. `GET /api/applications/current/validate` -> readiness %, issues, `evidence_needed` (e.g. only the income certificate).
9. `GET /api/export/form.pdf` and `/api/export/report.pdf`.
10. `GET /api/session` (timer poll, does not extend), `POST /api/session/extend`, `GET /api/session/resume` (after reload).

## 4. Directory structure
```
backend/
├── app/
│   ├── main.py                      # FastAPI app, CORS, routers, janitor task
│   ├── config.py                    # settings from .env
│   ├── core/
│   │   ├── errors.py                # uniform {"error":{code,message,details}}
│   │   ├── session_store.py         # SQLite sessions, idle + absolute timeout
│   │   └── deps.py                  # signed HttpOnly cookie, peek vs touch
│   ├── schemas/models.py            # Pydantic models (Swagger examples)
│   ├── api/routes/
│   │   ├── health.py                # /health, /health/gemini
│   │   ├── session.py               # create, poll, extend, resume, language, delete
│   │   ├── profile.py               # upload doc (OCR), demo-load, confirm/edit, consistency
│   │   ├── forms.py                 # list forms, question list, extract fields from a blank-form photo
│   │   ├── applications.py          # question loop: start, question, answer, confirm, edit, validate
│   │   ├── voice.py                 # TTS (kn/hi/en), audio fetch, Gemini speech-to-text
│   │   └── export.py                # form PDF, report PDF, report JSON
│   ├── services/
│   │   ├── gemini_client.py         # vision JSON, transliteration, transcription, ping
│   │   ├── ocr_service.py           # mock -> Gemini -> Tesseract fallback
│   │   ├── form_mapper.py           # printed labels -> question library
│   │   ├── application_service.py   # prefill, read-back, confirm, readiness
│   │   ├── matcher.py               # name/text/exact comparison (RapidFuzz)
│   │   ├── rules_engine.py          # format rules, ask-only-if-needed evidence rules
│   │   ├── profile_service.py       # merge docs, cross-document consistency
│   │   ├── tts_service.py           # gTTS adapter + cache (swap for Bhashini)
│   │   ├── pdf_service.py           # ReportLab draft + report
│   │   ├── text_utils.py            # normalisation, dates, yes/no, choices
│   │   └── i18n.py                  # all spoken messages in en/kn/hi
│   └── data/
│       ├── field_library.py         # 27 questions: labels, prompts (en/kn/hi), rules
│       ├── forms.json               # bank_account (15 q) and pension (23 q)
│       ├── rules.json               # weights, thresholds, evidence + eligibility rules
│       └── demo_documents.json      # values read from your 4 sample images
├── scripts/check_gemini.py
├── tests/                           # pytest
├── storage/                         # sqlite + tts cache (git-ignored)
├── .env.example  requirements.txt  Dockerfile  pytest.ini
```
Put it next to your frontend: `project-root/{frontend, backend}`.

## 5. Handwritten-note requirements, where they live
| Requirement | Where |
|---|---|
| Instruction/hint per input | `field_library.py` prompts + `/forms/{id}/fields` |
| Errors in text **and** voice | every `Issue.message` is en/kn/hi; responses carry `prompt` (audio or `tts_fallback`) |
| No context change on focus | frontend rule; backend only changes state on explicit POST/PATCH |
| Auto-determined info | profile prefill + `title` derived from gender (confirm still required) |
| Time limit warning + extension | `GET /session` (`warn`, `seconds_remaining`), `POST /session/extend`, header `X-Session-Expires-In` |
| Grouped fields | `group` on every question, `progress.groups` |
| Simple language | short prompts in 3 languages |
| Feedback after action / processing status | every action returns the new state; frontend shows progress during OCR |
| Alignment | frontend |

## 6. Frontend integration (React)
```ts
// api.ts: cookies must be sent
const api = (path: string, init: RequestInit = {}) =>
  fetch(`http://localhost:8000/api${path}`, { credentials: "include",
    headers: init.body instanceof FormData ? {} : { "Content-Type": "application/json" }, ...init })
  .then(async r => { if (!r.ok) throw (await r.json()).error; return r.json(); });

// on app load (reload support)
try { const st = await api("/session/resume"); /* restore profile, answers, st.application.question */ }
catch (e: any) { if (e.code === "NO_SESSION" || e.code === "SESSION_EXPIRED") /* show start screen */ }

// timer: poll every 20s (does not extend); when warn === true show "Extend time"
const t = await api("/session"); if (t.warn) showExtendBanner(t.seconds_remaining);

// play question audio (or fall back to the browser voice)
q.prompt.audio_url ? new Audio("http://localhost:8000" + q.prompt.audio_url).play()
                   : speechSynthesis.speak(Object.assign(new SpeechSynthesisUtterance(q.prompt.text), { lang: "kn-IN" }));
```
* Vite dev: either set `CORS_ORIGINS` to your port, or proxy `/api` -> `http://localhost:8000` in `vite.config.ts` (then use relative URLs).
* Also keep a **localStorage snapshot** of the last question/answers as a UI cache. The server session is the source of truth. If `/session/resume` returns 401 the snapshot must be discarded.
* Browser speech-to-text (`webkitSpeechRecognition`, `kn-IN`/`hi-IN`) works without the server. Send its transcript to `/current/answer`. `/voice/transcribe` is the Gemini alternative.
* Keypad fields (`input_mode: "keypad"`) should send digits via `input_mode:"keypad"`. Sensitive fields come back masked.

## 7. Privacy and security notes
* Demo uses fictional documents only. Sample Aadhaar/PAN use a `DEMO` prefix, and the Aadhaar/PAN format rules accept it.
* Explicit consent flag is required before any upload (`403 CONSENT_REQUIRED`). Show purpose text in the UI.
* Uploads: magic-byte type check (JPG/PNG/PDF), size cap, never stored on disk. Only extracted fields live in the session.
* Sessions: signed HttpOnly cookie, idle timeout (default 15 min, sliding), absolute cap (4 h), purge job, `DELETE /session` wipes everything. An expired session is deleted, not restorable.
* Sensitive values (Aadhaar, PAN, mobile, account, ration card) are masked in API output and PDFs by default, and read back masked unless `reveal=true`.
* Session database rows are AES-256-GCM encrypted. Uploads are processed in memory and not retained. Cloud Gemini OCR, cloud STT, cloud TTS and personal-data transliteration are blocked.
* A text match is **not** identity verification or document authenticity. Readiness is a checklist score, not approval odds. Eligibility is only a hint.
* Before real data: legal review (DPDP Act), HTTPS (`COOKIE_SECURE=true`), real authentication/authorization, key management/rotation and threat-model review.

## 8. Deployment notes
* Docker: `docker build -t formsaathi-api . && docker run -p 8000:8000 --env-file .env -v $PWD/storage:/srv/storage formsaathi-api`.
* Production: `COOKIE_SECURE=true`, strong `SECRET_KEY`, `APP_ENV=prod` (disables `/health/gemini`), exact `CORS_ORIGINS`; if frontend and API are on different sites use `COOKIE_SAMESITE=none`.
* One worker per SQLite file is fine for a demo. Use Redis/Postgres for several workers.

## 9. Known limits / honest caveats
* Kannada and Hindi strings are my translations and need a fluent-speaker review.
* Voice responses use browser speech synthesis; applicant audio is not sent to the backend for transcription. A tested local STT/TTS engine remains future work.
* Printed PDFs use Helvetica, so only Latin text prints. Values are transliterated to English letters by design. Add a Noto Kannada font in `pdf_service.py` if you need Kannada on paper.
* `forms/extract` maps detected labels to the 27 known questions. Unknown labels are listed as `unmatched` (not asked yet).
* Mock mode returns seeded data for any image. Real OCR accuracy has to be tested with your key on your 4 images.

## 10. Phased plan
**MVP (done in this skeleton):** session+cookie, profile from 4 docs, consistency checks, two forms, voice prompts kn/hi/en, read-back confirm loop, mismatch messages, ask-only-if-needed, readiness, PDFs, tests.
**Phase 2:** add a tested local OCR pipeline for PDFs and tune confidence; wire frontend; browser STT + keypad; Kannada/Hindi copy review; low-confidence review UI.
**Phase 3:** blank-form photo -> custom questions for unmatched labels (Gemini explains + translates); Kannada PDF font; Redis sessions; accuracy metrics on clean/messy/new-layout test sets; accessibility test pass.
