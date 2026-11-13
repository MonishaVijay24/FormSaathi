import time
from app.core.session_store import get_store

JPEG = b"\xff\xd8\xff\xe0" + b"0" * 64


def boot(c, lang="en"):
    assert c.post("/api/session", json={"language": lang, "consent": True}).status_code == 200
    assert c.post("/api/profile/demo-load").status_code == 200
    assert c.post("/api/profile/confirm-all").status_code == 200


def run_form(c, form_id, answers, lang="en"):
    q = c.post("/api/applications/start", json={"form_id": form_id, "language": lang}).json()
    guard = 0
    while not q["done"] and guard < 60:
        guard += 1
        fid = q["field_id"]
        if q["stage"] == "prefill":
            q = c.post("/api/applications/current/confirm", json={"field_id": fid, "confirmed": True, "language": lang}).json()
        else:
            r = c.post("/api/applications/current/answer",
                       json={"field_id": fid, "value": answers[fid], "input_mode": "text", "language": lang}).json()
            assert not r["retry"], r
            q = c.post("/api/applications/current/confirm", json={"field_id": fid, "transcript": "yes", "language": lang}).json()
    assert q["done"]


def test_no_session_is_401(client):
    r = client.get("/api/profile")
    assert r.status_code == 401 and r.json()["error"]["code"] == "NO_SESSION"


def test_consent_required(client):
    client.post("/api/session", json={"language": "kn", "consent": False})
    assert client.post("/api/profile/demo-load").json()["error"]["code"] == "CONSENT_REQUIRED"


def test_upload_and_consistency(client):
    client.post("/api/session", json={"language": "kn", "consent": True})
    r = client.post("/api/profile/documents", data={"doc_type": "aadhaar"}, files={"file": ("a.jpg", JPEG, "image/jpeg")})
    assert r.status_code == 200 and r.json()["engine"] == "mock"
    client.post("/api/profile/documents", data={"doc_type": "pan"}, files={"file": ("p.jpg", JPEG, "image/jpeg")})
    r = client.post("/api/profile/documents", data={"doc_type": "passbook"}, files={"file": ("b.jpg", JPEG, "image/jpeg")})
    codes = [i["rule_code"] for i in r.json()["consistency_issues"]]
    assert "PAN_CROSS_DOC" in codes                       # planted: DEMO-PAN-1234 vs DEMO-PAN-0001
    bad = client.post("/api/profile/documents", data={"doc_type": "pan"}, files={"file": ("x.txt", b"hello", "text/plain")})
    assert bad.status_code == 415


def test_bank_form_full_flow_and_pdf(client):
    boot(client)
    run_form(client, "bank_account", {"marital_status": "married", "occupation": "farmer", "annual_income": "₹18,000"})
    ev = client.get("/api/applications/current/validate").json()
    assert ev["completed"] == ev["total_fields"] and ev["readiness"] >= 90
    pdf = client.get("/api/export/form.pdf")
    assert pdf.content[:4] == b"%PDF"
    assert client.get("/api/export/report.pdf").content[:4] == b"%PDF"


def test_name_mismatch_is_explained_and_clears_after_fix(client):
    boot(client)
    q = client.post("/api/applications/start", json={"form_id": "pension", "language": "en"}).json()
    assert q["field_id"] == "aadhaar_number" and q["stage"] == "prefill"
    assert "ending" in q["prompt"]["text"]  # masked read-back
    for fid in ["aadhaar_number", "title"]:
        client.post("/api/applications/current/confirm", json={"field_id": fid, "confirmed": True})
    q = client.get("/api/applications/current/question").json()
    assert q["field_id"] == "applicant_name"
    client.post("/api/applications/current/confirm", json={"field_id": "applicant_name", "confirmed": False})
    r = client.post("/api/applications/current/answer",
                    json={"field_id": "applicant_name", "value": "Ramesh Kumar", "input_mode": "text", "language": "en"}).json()
    assert r["status"] == "possible_mismatch" and "RAMESH GOWDA" in r["issue"]["message"]["en"]
    assert "ರಮೇಶ" not in r["issue"]["message"]["en"] and r["issue"]["message"]["kn"] and r["issue"]["message"]["hi"]
    client.post("/api/applications/current/confirm", json={"field_id": "applicant_name", "confirmed": True})
    ev = client.get("/api/applications/current/validate").json()
    assert any(i["field_id"] == "applicant_name" for i in ev["issues"])
    fixed = client.patch("/api/applications/answers/applicant_name", json={"value": "Ramesh Gowda"}).json()
    assert not any(i["field_id"] == "applicant_name" for i in fixed["issues"])


def test_format_error_blocks_and_choice_unclear(client):
    boot(client)
    client.post("/api/applications/start", json={"form_id": "bank_account", "language": "en"})
    for fid in ["applicant_name", "father_name", "mother_name", "dob", "gender"]:
        client.post("/api/applications/current/confirm", json={"field_id": fid, "confirmed": True})
    r = client.post("/api/applications/current/answer", json={"field_id": "marital_status", "value": "banana"}).json()
    assert r["retry"] and r["issue"]["rule_code"] == "CHOICE_UNCLEAR"


def test_wrong_pin_and_account_rules(client):
    from app.data.field_library import LIB
    from app.services.rules_engine import check_format
    assert check_format(LIB["pin_code"], "56004").rule_code == "PIN_INVALID"
    assert check_format(LIB["account_number"], "12345678").rule_code == "ACCOUNT_LENGTH"
    assert check_format(LIB["ifsc"], "BKID0001234") is None
    assert check_format(LIB["dob"], "31/02/1990").rule_code == "DOB_INVALID"


def test_evidence_only_missing_document_requested(client):
    boot(client)
    run_form(client, "pension", {"relation_type": "s/o", "marital_status": "married", "annual_income": "18000"})
    ok = client.get("/api/applications/current/validate").json()
    assert not any(i["status"] == "evidence_needed" for i in ok["issues"])     # BPL card counts as income proof
    client.delete("/api/profile/documents/bpl")
    ev = client.get("/api/applications/current/validate").json()
    need = [i for i in ev["issues"] if i["status"] == "evidence_needed"]
    assert len(need) == 1 and need[0]["requested_document"] == "income_certificate"


def test_yes_no_in_kannada_hindi_and_unclear(client):
    from app.services.text_utils import parse_yes_no
    assert parse_yes_no("ಹೌದು") == "yes" and parse_yes_no("नहीं") == "no" and parse_yes_no("जी नहीं") == "no"
    assert parse_yes_no("hmm") == "unknown"


def test_session_timeout_resume_extend_and_expiry(client):
    boot(client)
    client.post("/api/applications/start", json={"form_id": "bank_account", "language": "kn"})
    client.post("/api/applications/current/confirm", json={"field_id": "applicant_name", "confirmed": True})
    r = client.get("/api/session/resume").json()                       # simulates page reload (cookie kept)
    assert r["application"]["answers"]["applicant_name"]["confirmed"] is True
    before = client.get("/api/session").json()["seconds_remaining"]
    assert client.post("/api/session/extend").json()["seconds_remaining"] >= before
    # force expiry
    from app.core.deps import _signer
    sid = _signer().loads(client.cookies.get("fs_session"))
    s = get_store().load(sid); s.expires_at = time.time() - 1; get_store().save(s)
    r = client.get("/api/session")
    assert r.status_code == 401 and r.json()["error"]["code"] == "SESSION_EXPIRED"


def test_delete_session(client):
    boot(client)
    assert client.delete("/api/session").status_code == 204
    assert client.get("/api/profile").status_code == 401


def test_form_extract_maps_labels(client):
    client.post("/api/session", json={"language": "en", "consent": True})
    r = client.post("/api/forms/extract", data={"form_id": "pension"}, files={"file": ("f.jpg", JPEG, "image/jpeg")}).json()
    assert "applicant_name" in r["field_ids"] and "ifsc" not in r["unmatched"]
