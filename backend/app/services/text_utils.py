import re
from datetime import date, datetime
from typing import Optional

_DIG = {ord(c): str(i) for i, c in enumerate("೦೧೨೩೪೫೬೭೮೯")}
_DIG.update({ord(c): str(i) for i, c in enumerate("०१२३४५६७८९")})


def ascii_digits(s: str) -> str:
    return s.translate(_DIG)


def has_indic(s: str) -> bool:
    return any(0x0900 <= ord(c) <= 0x0DFF for c in s)


_DATE_FORMATS = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d %m %Y", "%d %B %Y", "%d %b %Y", "%Y-%m-%d"]
_MONTHS_KN_HI = {  # spoken month names -> English (extend as needed)
    "ಜನವರಿ": "January", "ಫೆಬ್ರವರಿ": "February", "ಮಾರ್ಚ್": "March", "ಏಪ್ರಿಲ್": "April", "ಮೇ": "May",
    "ಜೂನ್": "June", "ಜುಲೈ": "July", "ಆಗಸ್ಟ್": "August", "ಸೆಪ್ಟೆಂಬರ್": "September",
    "ಅಕ್ಟೋಬರ್": "October", "ನವೆಂಬರ್": "November", "ಡಿಸೆಂಬರ್": "December",
    "जनवरी": "January", "फरवरी": "February", "मार्च": "March", "अप्रैल": "April", "मई": "May",
    "जून": "June", "जुलाई": "July", "अगस्त": "August", "सितंबर": "September",
    "अक्टूबर": "October", "नवंबर": "November", "दिसंबर": "December",
}


def parse_date(s: str) -> Optional[date]:
    s = ascii_digits(s).strip().replace(",", " ")
    for k, v in _MONTHS_KN_HI.items():
        s = s.replace(k, v)
    s = re.sub(r"\s+", " ", s)
    for f in _DATE_FORMATS:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    return None


def normalize_value(ftype: str, raw: str) -> str:
    s = ascii_digits((raw or "").strip())
    if ftype == "name":
        s = re.sub(r"[^A-Za-z .'-]", "", s)
        return re.sub(r"\s+", " ", s).strip().upper()
    if ftype == "date":
        d = parse_date(s)
        return d.strftime("%d/%m/%Y") if d else s
    if ftype == "number":
        return re.sub(r"[^\d.]", "", s).split(".")[0]
    if ftype == "digits":
        return re.sub(r"[\s\-]", "", s).upper()
    if ftype == "id":
        return re.sub(r"\s", "", s).upper()
    return re.sub(r"\s+", " ", s).strip().upper()   # text / choice-as-text


def age_from_dob(dob: str, today: Optional[date] = None) -> Optional[int]:
    d = parse_date(dob)
    if not d:
        return None
    today = today or date.today()
    return today.year - d.year - ((today.month, today.day) < (d.month, d.day))


def mask(v: str, keep: int = 4) -> str:
    v = v or ""
    return v if len(v) <= keep else "X" * (len(v) - keep) + v[-keep:]


def speak_value(value: str, sensitive: bool, reveal: bool, digitish: bool) -> str:
    if sensitive and not reveal:
        return "ending " + " ".join(value[-4:])
    if digitish or sensitive:
        return " ".join(value.replace("/", " / "))
    return value


_YES = {"yes", "y", "yeah", "yep", "correct", "right", "ok", "okay", "sure",
        "ಹೌದು", "ಸರಿ", "ಹೂಂ", "हाँ", "हां", "जी", "सही", "ठीक"}
_NO = {"no", "nope", "wrong", "incorrect", "not", "don't", "ಇಲ್ಲ", "ಅಲ್ಲ", "ತಪ್ಪು", "नहीं", "नही", "ना", "गलत"}


def parse_yes_no(text: str) -> str:
    toks = [t.strip(".,;:!?।'\"").lower() for t in (text or "").split()]
    if any(t in _NO for t in toks):
        return "no"
    if any(t in _YES for t in toks):
        return "yes"
    return "unknown"


def match_choice(options: list[dict], text: str) -> Optional[str]:
    low = (text or "").lower().strip()
    toks = [t.strip(".,;:!?।'\"") for t in low.split()]
    for o in options:                      # exact token (or whole text) match first
        for syn in o["synonyms"]:
            if " " not in syn and (syn in toks or syn == low):
                return o["value"]
    for o in options:                      # multi-word synonyms
        for syn in o["synonyms"]:
            if " " in syn and syn in low:
                return o["value"]
    return None
