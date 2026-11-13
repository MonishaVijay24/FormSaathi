"""Map labels printed on an uploaded blank form to our question library (so we can ask them as questions)."""
import json
from pathlib import Path
from rapidfuzz import process, fuzz
from app.data.field_library import LIB

DATA = Path(__file__).resolve().parent.parent / "data"


def forms() -> dict:
    return json.loads((DATA / "forms.json").read_text(encoding="utf-8"))


def template_labels(form_id: str | None) -> list[str]:
    f = forms().get(form_id or "bank_account") or forms()["bank_account"]
    return [LIB[i]["aliases"][0] if LIB[i]["aliases"] else LIB[i]["label"]["en"] for i in f["fields"]]


def map_labels(labels: list[str]) -> dict:
    choices = {}
    for fid, f in LIB.items():
        for a in f["aliases"] + [f["label"]["en"]]:
            choices[a] = fid
    matched, unmatched, seen = [], [], set()
    for lab in labels:
        hit = process.extractOne(lab, list(choices.keys()), scorer=fuzz.WRatio, score_cutoff=72)
        if hit and choices[hit[0]] not in seen:
            seen.add(choices[hit[0]])
            matched.append({"label": lab, "field_id": choices[hit[0]], "score": int(hit[1])})
        else:
            unmatched.append(lab)
    return {"matched": matched, "unmatched": unmatched}


def guess_form(labels: list[str], title: str = "") -> str:
    blob = (title + " " + " ".join(labels)).lower()
    if any(w in blob for w in ("pension", "sandhya", "ration", "taluk", "aadhaar number")):
        return "pension"
    return "bank_account"
