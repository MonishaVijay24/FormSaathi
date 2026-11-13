"""Run:  python scripts/check_gemini.py [path/to/demo_adhaar_card.jpeg]
Checks: (1) key present, (2) text call works, (3) optional vision OCR call on a sample image."""
import sys, json, mimetypes
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import get_settings
from app.services.gemini_client import get_gemini

s = get_settings()
print(f"model={s.gemini_model}  key_present={bool(s.gemini_api_key)}  mock_ai={s.mock_ai}")
g = get_gemini()
print("TEXT :", g.ping())
if len(sys.argv) > 1:
    p = Path(sys.argv[1])
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    s.mock_ai = False
    from app.services import ocr_service
    fields, engine = ocr_service.extract_document("aadhaar", p.read_bytes(), mime)
    print("VISION:", engine)
    print(json.dumps({k: v.model_dump() for k, v in fields.items()}, indent=2, ensure_ascii=False))
