import time
from typing import Optional
from app.data.field_library import KEY_KIND, KEY_TYPE, KEY_LABEL, SENSITIVE_KEYS
from app.schemas.models import SessionData, ProfileField, Issue
from app.services.i18n import SOURCE_NAMES, t_all
from app.services.matcher import compare_values
from app.services.text_utils import normalize_value, age_from_dob, mask

PRIORITY = ["aadhaar", "pan", "bpl", "passbook", "income_certificate", "marks_card"]


def norm_key(key: str, value: str) -> str:
    t = KEY_TYPE.get(key, "text")
    return normalize_value("text" if t == "choice" else t, value)


def rebuild_profile(s: SessionData) -> None:
    """Merge documents into one profile (priority order). Keep user confirmations/edits."""
    old, new = s.profile, {}
    for doc_type in PRIORITY:
        doc = s.documents.get(doc_type)
        if not doc:
            continue
        for key, fv in doc.fields.items():
            if key in new:
                continue
            prev = old.get(key)
            if prev and prev.edited:
                new[key] = prev
                continue
            pf = ProfileField(key=key, value=fv.value, source_doc=doc_type, confidence=fv.confidence)
            if prev and prev.confirmed and norm_key(key, prev.value) == norm_key(key, fv.value):
                pf.confirmed, pf.confirmed_at = True, prev.confirmed_at
            new[key] = pf
    s.profile = new


def confirm_all(s: SessionData) -> None:
    now = time.time()
    for pf in s.profile.values():
        pf.confirmed, pf.confirmed_at = True, now


def display_value(pf: ProfileField) -> str:
    return mask(pf.value) if pf.key in SENSITIVE_KEYS else pf.value


def consistency(s: SessionData) -> list[Issue]:
    """Compare the same detail across uploaded documents (e.g. PAN differs between PAN card and passbook)."""
    by_key: dict[str, list[tuple[str, str]]] = {}
    for doc_type in PRIORITY:
        doc = s.documents.get(doc_type)
        for k, fv in (doc.fields.items() if doc else []):
            by_key.setdefault(k, []).append((doc_type, fv.value))
    issues: list[Issue] = []
    label = lambda k: KEY_LABEL.get(k, {l: k.replace("_", " ") for l in ("en", "kn", "hi")})
    for k, vals in by_key.items():
        if len(vals) < 2 or k in ("age", "email", "account_type", "branch_code"):
            continue
        (d1, v1) = vals[0]
        for d2, v2 in vals[1:]:
            res = compare_values(KEY_KIND.get(k) or "exact", norm_key(k, v1), norm_key(k, v2))
            if res:
                sens = k in SENSITIVE_KEYS
                a, b = (mask(v1), mask(v2)) if sens else (v1, v2)
                issues.append(Issue(
                    field_id=k, status=res[0], rule_code=f"{k.upper()}_CROSS_DOC", severity="should_fix",
                    form_value=a, evidence_value=b, source_doc=f"{d1} vs {d2}", action="confirm_or_edit",
                    message=t_all("CROSS_DOC", label=label(k), a=a, b=b, s1=SOURCE_NAMES[d1], s2=SOURCE_NAMES[d2])))
    # printed age vs age computed from date of birth
    dob = by_key.get("dob", [(None, "")])[0][1]
    for d, v in by_key.get("age", []):
        calc = age_from_dob(dob) if dob else None
        if calc is not None and v.isdigit() and int(v) != calc:
            msg = {"en": f"Age on your {SOURCE_NAMES[d]['en']} is {v}, but your date of birth gives {calc}.",
                   "kn": f"ನಿಮ್ಮ {SOURCE_NAMES[d]['kn']} ನಲ್ಲಿ ವಯಸ್ಸು {v}, ಆದರೆ ಹುಟ್ಟಿದ ದಿನಾಂಕದ ಪ್ರಕಾರ {calc}.",
                   "hi": f"आपके {SOURCE_NAMES[d]['hi']} में आयु {v} है, पर जन्म तिथि के अनुसार {calc} है।"}
            issues.append(Issue(field_id="age", status="please_verify", rule_code="AGE_VS_DOB", severity="minor",
                                form_value=v, evidence_value=str(calc), source_doc=d, message=msg))
    return issues
