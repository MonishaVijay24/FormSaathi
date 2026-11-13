"""Question loop: prefill from profile -> ask -> read back -> confirm -> next. Rules decide, user confirms."""
import time
from typing import Optional
from app.core.errors import AppError
from app.data.field_library import LIB, GROUPS
from app.schemas.models import ApplicationState, Answer, Pending, Issue, SessionData
from app.services import tts_service
from app.services.form_mapper import forms
from app.services.gemini_client import get_gemini
from app.services.i18n import SOURCE_NAMES, t, t_all
from app.services.matcher import compare_to_profile, rules
from app.services.rules_engine import check_format, evidence_issues
from app.services.text_utils import (normalize_value, has_indic, match_choice, mask, speak_value,
                                     parse_yes_no, age_from_dob)

MOCK_TRANSLIT = {"ರಮೇಶ್ ಗೌಡ": "RAMESH GOWDA", "ರಮೇಶ್ ಕುಮಾರ್": "RAMESH KUMAR",
                 "रमेश गौड़ा": "RAMESH GOWDA", "रमेश कुमार": "RAMESH KUMAR"}


def get_field(fid: str) -> dict:
    if fid not in LIB:
        raise AppError(404, "UNKNOWN_FIELD", f"Unknown field '{fid}'.")
    return LIB[fid]


def start_application(s: SessionData, form_id: str, language: str, field_ids: Optional[list[str]]) -> None:
    form = forms()[form_id]
    ids = [i for i in (field_ids or form["fields"]) if i in LIB]
    if not ids:
        raise AppError(422, "NO_FIELDS", "No supported fields to ask.")
    s.language = language
    s.application = ApplicationState(form_id=form_id, language=language, field_ids=ids, created_at=time.time())


def app_of(s: SessionData) -> ApplicationState:
    if not s.application:
        raise AppError(409, "NO_APPLICATION", "Start an application first (POST /api/applications/start).")
    return s.application


def current_field_id(a: ApplicationState) -> Optional[str]:
    for fid in a.field_ids:
        ans = a.answers.get(fid)
        if not ans or not ans.confirmed:
            return fid
    return None


def progress(a: ApplicationState, lang: str) -> dict:
    done = sum(1 for f in a.field_ids if a.answers.get(f) and a.answers[f].confirmed)
    groups: dict[str, list[int]] = {}
    for f in a.field_ids:
        g = groups.setdefault(LIB[f]["group"], [0, 0])
        g[1] += 1
        g[0] += 1 if a.answers.get(f) and a.answers[f].confirmed else 0
    return {"answered": done, "total": len(a.field_ids), "percent": round(100 * done / len(a.field_ids)),
            "groups": [{"group": g, "label": GROUPS[g][lang], "done": v[0], "total": v[1]} for g, v in groups.items()]}


def _derive(field: dict, s: SessionData) -> Optional[tuple[str, str]]:
    if field["derived"] == "title_from_gender":
        g = s.profile.get("gender")
        if g and g.confirmed:
            return ("Sri" if g.value.lower().startswith("m") else "Smt"), g.source_doc
    return None


def profile_proposal(s: SessionData, field: dict) -> Optional[tuple[str, str, str]]:
    """(value, source_kind, source_doc) from CONFIRMED profile values only."""
    d = _derive(field, s)
    if d:
        return d[0], "computed", d[1]
    pf = s.profile.get(field["profile_key"]) if field["profile_key"] else None
    if pf and pf.confirmed:
        ft = "text" if field["type"] == "choice" else field["type"]
        v = pf.value if field["type"] == "choice" else normalize_value(ft, pf.value)
        return v, "profile", pf.source_doc
    return None


def _spoken(field: dict, value: str, reveal: bool) -> str:
    return speak_value(value, field["sensitive"], reveal, field["type"] in ("digits", "date", "number"))


def _display(field: dict, value: str) -> str:
    return mask(value) if field["sensitive"] else value


def _question_dict(s: SessionData, field: Optional[dict], stage: str, text: str, lang: str,
                   value: Optional[str] = None, source_doc: Optional[str] = None) -> dict:
    a = s.application
    base = {"stage": stage, "done": field is None, "progress": progress(a, lang),
            "prompt": tts_service.speak(text, lang)}
    if field is None:
        return {**base, "field_id": None}
    return {**base, "field_id": field["id"], "label": field["label"][lang], "group": field["group"],
            "input_mode": field["input_mode"], "sensitive": field["sensitive"], "required": field["required"],
            "options": [{"value": o["value"], "label": o["label"][lang]} for o in (field["options"] or [])] or None,
            "proposed_value": _display(field, value) if value else None,
            "proposed_source": SOURCE_NAMES[source_doc][lang] if source_doc else None}


def build_question(s: SessionData, lang: str, reveal: bool = False) -> dict:
    a = app_of(s)
    fid = current_field_id(a)
    if fid is None:
        a.pending = None
        return _question_dict(s, None, "done", t("DONE", lang), lang)
    f = LIB[fid]
    if a.pending and a.pending.field_id != fid:
        a.pending = None
    if not a.pending and fid not in a.skipped_prefill:
        p = profile_proposal(s, f)
        if p:
            a.pending = Pending(field_id=fid, value=p[0], source=p[1], source_doc=p[2], stage="prefill")
    p = a.pending
    if p and p.stage == "prefill":
        text = t("PREFILL", lang, source=SOURCE_NAMES[p.source_doc][lang], label=f["label"][lang],
                 value=_spoken(f, p.value, reveal))
        return _question_dict(s, f, "prefill", text, lang, p.value, p.source_doc)
    if p:
        return _question_dict(s, f, "confirm", _confirm_text(f, p, lang, reveal), lang, p.value)
    return _question_dict(s, f, "answer", f["prompt"][lang], lang)


def _confirm_text(f: dict, p: Pending, lang: str, reveal: bool) -> str:
    if p.issue:
        return p.issue.message[lang] + " " + t("KEEP", lang)
    return t("CONFIRM", lang, value=_spoken(f, p.value, reveal))


def to_latin(text: str, lang: str) -> str:
    g = get_gemini()
    if g.ready:
        out = g.transliterate_to_latin(text)
        if out:
            return out
    elif text.strip() in MOCK_TRANSLIT:
        return MOCK_TRANSLIT[text.strip()]
    raise AppError(422, "TRANSLITERATION_FAILED", t("TRANSLIT_FAIL", lang), {"messages": t_all("TRANSLIT_FAIL")})


def process_raw(s: SessionData, f: dict, raw: str, lang: str) -> tuple[Optional[str], Optional[Issue], bool]:
    """-> (normalized_value, issue, retry). retry=True means the answer cannot be accepted yet."""
    raw = (raw or "").strip()
    if not raw:
        return None, Issue(field_id=f["id"], status="fix_required", rule_code="REQUIRED", severity="blocking",
                           message=t_all("REQUIRED", label=f["label"])), True
    if f["type"] == "choice":
        v = match_choice(f["options"], raw)
        if v is None:
            opts = {l: ", ".join(o["label"][l] for o in f["options"]) for l in ("en", "kn", "hi")}
            return None, Issue(field_id=f["id"], status="low_confidence", rule_code="CHOICE_UNCLEAR",
                               message=t_all("CHOICE_UNCLEAR", options=opts)), True
        value = v
    else:
        if f["type"] in ("name", "text") and has_indic(raw):
            raw = to_latin(raw, lang)
        value = normalize_value(f["type"], raw)
    fmt = check_format(f, value)
    if fmt:
        return value, fmt, True
    return value, compare_to_profile(f, value, s.profile), False


def submit_answer(s: SessionData, fid: str, raw: str, mode: str, lang: str, reveal: bool = False) -> dict:
    a = app_of(s)
    if fid != current_field_id(a):
        raise AppError(409, "NOT_CURRENT_FIELD", "Answer the current question first, or use PATCH to edit an earlier answer.")
    f = get_field(fid)
    value, issue, retry = process_raw(s, f, raw, lang)
    if retry:
        a.pending = None
        return {"field_id": fid, "retry": True, "normalized_value": value, "status": issue.status, "issue": issue,
                "needs_attention": True, "prompt": tts_service.speak(issue.message[lang], lang)}
    a.pending = Pending(field_id=fid, value=value, source=mode, transcript=raw, issue=issue, stage="answer")
    text = _confirm_text(f, a.pending, lang, reveal)
    return {"field_id": fid, "retry": False, "normalized_value": _display(f, value),
            "status": issue.status if issue else "looks_consistent", "issue": issue,
            "needs_attention": issue is not None, "prompt": tts_service.speak(text, lang)}


def confirm(s: SessionData, fid: str, confirmed: Optional[bool], transcript: Optional[str], lang: str) -> dict:
    a = app_of(s)
    p = a.pending
    if not p or p.field_id != fid:
        raise AppError(409, "NOTHING_TO_CONFIRM", "There is no pending answer for this field.")
    if confirmed is None:
        yn = parse_yes_no(transcript or "")
        if yn == "unknown":
            raise AppError(422, "YES_NO_UNCLEAR", t("YES_NO_UNCLEAR", lang), {"messages": t_all("YES_NO_UNCLEAR")})
        confirmed = yn == "yes"
    if confirmed:
        a.answers[fid] = Answer(field_id=fid, value=p.value, source=p.source, transcript=p.transcript,
                                confirmed=True, confirmed_at=time.time(), issue=p.issue)
    elif p.stage == "prefill":
        a.skipped_prefill.append(fid)
    a.pending = None
    return build_question(s, lang)


def edit_answer(s: SessionData, fid: str, raw: str, lang: str) -> dict:
    """Change an earlier answer (also used to simulate 'someone edits a value' before re-check)."""
    a = app_of(s)
    if fid not in a.field_ids:
        raise AppError(404, "UNKNOWN_FIELD", "This field is not in the current application.")
    f = get_field(fid)
    value, issue, retry = process_raw(s, f, raw, lang)
    if retry:
        raise AppError(422, issue.rule_code, issue.message[lang], {"issue": issue.model_dump()})
    a.answers[fid] = Answer(field_id=fid, value=value, source="edit", transcript=raw, confirmed=True,
                            confirmed_at=time.time(), issue=issue)
    return evaluate(s)


def evaluate(s: SessionData) -> dict:
    """Re-run every check from current values (so fixed problems clear and new ones appear)."""
    a = app_of(s)
    w = rules()["weights"]
    total = passed = 0
    issues: list[Issue] = []
    completed = 0
    for fid in a.field_ids:
        f, ans = LIB[fid], a.answers.get(fid)
        ok = bool(ans and ans.confirmed and ans.value)
        total += w["blocking"] if f["required"] else w["minor"]
        if ok:
            completed += 1
            passed += w["blocking"] if f["required"] else w["minor"]
        elif f["required"]:
            issues.append(Issue(field_id=fid, status="fix_required", rule_code="REQUIRED", severity="blocking",
                                message=t_all("REQUIRED", label=f["label"]), action="answer_question"))
            continue
        else:
            continue
        if f["rule"]:
            total += w["should_fix"]
            bad = check_format(f, ans.value)
            if bad:
                issues.append(bad)
            else:
                passed += w["should_fix"]
        if f["profile_key"] and f["profile_key"] in s.profile:
            total += w["should_fix"]
            cmp_ = compare_to_profile(f, ans.value, s.profile)
            if cmp_: issues.append(cmp_)
            else: passed += w["should_fix"]
    for ev in evidence_issues(s):
        total += w[ev.severity]
        issues.append(ev)
    # evidence rules that are satisfied still count as passed checks
    from app.services.matcher import rules as _r
    for rule in _r()["evidence"].get(a.form_id, []):
        if a.answers.get(rule["field"]) and not any(i.rule_code == "EVIDENCE_REQUIRED" for i in issues):
            total += w[rule["severity"]]; passed += w[rule["severity"]]
    notes = _eligibility_notes(s)
    review = sum(1 for i in issues if i.status in ("please_verify", "low_confidence", "possible_mismatch"))
    return {"readiness": round(100 * passed / total) if total else 0, "total_fields": len(a.field_ids),
            "completed": completed, "needs_review": review,
            "issues_count": sum(1 for i in issues if i.status in ("fix_required", "evidence_needed")),
            "issues": issues, "open_blocking": [i for i in issues if i.severity == "blocking"],
            "notes": notes, "note": "Readiness is a checklist score, not the chance of approval. Draft only; nothing is submitted."}


def _eligibility_notes(s: SessionData) -> list[dict]:
    a = s.application
    cfg = rules()["eligibility"].get(a.form_id)
    if not cfg:
        return []
    dob = a.answers.get("dob")
    inc = a.answers.get("annual_income")
    age = age_from_dob(dob.value) if dob else None
    income = int(inc.value) if inc and inc.value.isdigit() else None
    if (age is not None and age < cfg["min_age"]) or (income is not None and income >= cfg["max_income"]):
        return [t_all("ELIGIBILITY")]
    return []
