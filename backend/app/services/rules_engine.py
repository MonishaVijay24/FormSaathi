import re
from datetime import date
from typing import Optional
from app.schemas.models import Issue, SessionData
from app.services.i18n import SOURCE_NAMES, t_all
from app.services.text_utils import parse_date, mask
from app.services.matcher import rules


def _issue(field: dict, code: str, msg_key: str, value: str, **kw) -> Issue:
    shown = mask(value) if field["sensitive"] else value
    return Issue(field_id=field["id"], status="fix_required", rule_code=code, severity="should_fix",
                 form_value=shown, action="fix_field",
                 message=t_all(msg_key, label=field["label"], value=shown, **kw))


def check_format(field: dict, value: str) -> Optional[Issue]:
    """Deterministic format rules. Returns an Issue or None."""
    r = field["rule"]
    if not r:
        return None
    if r == "pin" and not re.fullmatch(r"\d{6}", value):
        return _issue(field, "PIN_INVALID", "PIN_INVALID", value)
    if r == "mobile" and not re.fullmatch(r"[6-9]\d{9}", value):
        return _issue(field, "MOBILE_INVALID", "MOBILE_INVALID", value)
    if r == "aadhaar" and not re.fullmatch(r"\d{12}|DEMO\d{8}", value):      # DEMO prefix = sample cards
        return _issue(field, "AADHAAR_INVALID", "AADHAAR_INVALID", value)
    if r == "pan" and not re.fullmatch(r"[A-Z]{5}\d{4}[A-Z]|DEMO-PAN-\d{4}", value):
        return _issue(field, "PAN_INVALID", "PAN_INVALID", value)
    if r == "ifsc" and not re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", value):
        return _issue(field, "IFSC_INVALID", "IFSC_INVALID", value)
    if r == "account" and not re.fullmatch(r"\d{9,18}", value):
        return _issue(field, "ACCOUNT_LENGTH", "ACCOUNT_LENGTH", value, count=len(value))
    if r == "dob":
        d = parse_date(value)
        if not d or d > date.today() or d.year < 1900:
            return _issue(field, "DOB_INVALID", "DOB_INVALID", value)
    if r == "number" and not re.fullmatch(r"\d+", value):
        return _issue(field, "NUMBER_INVALID", "NUMBER_INVALID", value)
    return None


def evidence_issues(session: SessionData) -> list[Issue]:
    """Ask-only-if-needed: request ONLY the missing document a rule needs."""
    from app.data.field_library import LIB
    app = session.application
    out = []
    for rule in rules()["evidence"].get(app.form_id, []):
        a = app.answers.get(rule["field"])
        if a and a.confirmed and not any(d in session.documents for d in rule["any_of"]):
            f = LIB[rule["field"]]
            out.append(Issue(field_id=rule["field"], status="evidence_needed", rule_code="EVIDENCE_REQUIRED",
                             severity=rule["severity"], requested_document=rule["request"],
                             form_value=a.value, action="upload_document",
                             message=t_all("EVIDENCE", label=f["label"], doc=SOURCE_NAMES[rule["request"]])))
    return out
