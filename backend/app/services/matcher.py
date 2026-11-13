import json
from functools import lru_cache
from pathlib import Path
from typing import Optional
from rapidfuzz import fuzz
from app.schemas.models import Issue, ProfileField
from app.services.i18n import SOURCE_NAMES, t_all
from app.services.text_utils import normalize_value, mask

DATA = Path(__file__).resolve().parent.parent / "data"


@lru_cache
def rules() -> dict:
    return json.loads((DATA / "rules.json").read_text(encoding="utf-8"))


def compare_values(kind: str, a: str, b: str) -> Optional[tuple[str, int]]:
    """None if equal, else (status, score). Deterministic; fuzzy only to *flag* spelling variants."""
    if a == b:
        return None
    th = rules()["thresholds"]
    if kind in ("name", "text"):
        score = int(fuzz.token_sort_ratio(a, b))
        limit = th["name_verify"] if kind == "name" else th["text_verify"]
        return ("please_verify" if score >= limit else "possible_mismatch"), score
    return "possible_mismatch", 0


def compare_to_profile(field: dict, value: str, profile: dict[str, ProfileField]) -> Optional[Issue]:
    pf = profile.get(field["profile_key"]) if field["profile_key"] else None
    if not pf:
        return None
    ftype = "text" if field["type"] == "choice" else field["type"]
    doc_val = normalize_value(ftype, pf.value)
    res = compare_values(field["compare"] or "exact", value, doc_val)
    if not res:
        return None
    status, _ = res
    sens = field["sensitive"]
    said, doc = (mask(value), mask(doc_val)) if sens else (value, doc_val)
    key = "VARIATION" if status == "please_verify" else "MISMATCH"
    return Issue(
        field_id=field["id"], status=status, rule_code=f"{field['id'].upper()}_{key}",
        severity="should_fix", form_value=said, evidence_value=doc, source_doc=pf.source_doc,
        message=t_all(key, label=field["label"], said=said, doc=doc, source=SOURCE_NAMES[pf.source_doc]),
        action="confirm_or_edit")
