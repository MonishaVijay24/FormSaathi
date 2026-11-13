"""Shared question library. Both forms pick fields from here by id (see forms.json).
Each field: trilingual label + prompt, type, input mode, rule, compare kind, profile_key.
Kannada/Hindi text needs fluent-speaker review."""
LANGS = ("en", "kn", "hi")
LIB: dict[str, dict] = {}

GROUPS = {
    "personal": {"en": "Personal Information", "kn": "ವೈಯಕ್ತಿಕ ಮಾಹಿತಿ", "hi": "व्यक्तिगत जानकारी"},
    "address": {"en": "Address Information", "kn": "ವಿಳಾಸ ಮಾಹಿತಿ", "hi": "पता जानकारी"},
    "income": {"en": "Income Details", "kn": "ಆದಾಯ ವಿವರ", "hi": "आय विवरण"},
    "bank": {"en": "Bank Information", "kn": "ಬ್ಯಾಂಕ್ ಮಾಹಿತಿ", "hi": "बैंक जानकारी"},
    "identity": {"en": "Identity & Documents", "kn": "ಗುರುತು ಮತ್ತು ದಾಖಲೆಗಳು", "hi": "पहचान और दस्तावेज़"},
}


def opt(value, kn, hi, syn=()):
    syns = {value.lower(), kn.lower(), hi.lower(), *[s.lower() for s in syn]}
    return {"value": value, "label": {"en": value, "kn": kn, "hi": hi},
            "synonyms": sorted(syns, key=len, reverse=True)}


def _f(fid, group, labels, prompts, **kw):
    LIB[fid] = {"id": fid, "group": group, "label": dict(zip(LANGS, labels)),
                "prompt": dict(zip(LANGS, prompts)), "type": "text", "input_mode": "voice",
                "rule": None, "compare": None, "profile_key": None, "sensitive": False,
                "required": True, "options": None, "aliases": [], "derived": None, **kw}


_f("applicant_name", "personal", ("name", "ಹೆಸರು", "नाम"),
   ("Please tell me your full name.", "ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ಹೇಳಿ.", "कृपया अपना पूरा नाम बताइए।"),
   type="name", compare="name", profile_key="name",
   aliases=["Name", "Applicant Name", "Applicant full name", "Full name", "Name (same as ID proof)"])
_f("father_name", "personal", ("father's name", "ತಂದೆಯ ಹೆಸರು", "पिता का नाम"),
   ("Please tell me your father's name.", "ನಿಮ್ಮ ತಂದೆಯ ಹೆಸರನ್ನು ಹೇಳಿ.", "अपने पिता का नाम बताइए।"),
   type="name", compare="name", profile_key="father_name", aliases=["Father's name", "Name of Father"])
_f("mother_name", "personal", ("mother's name", "ತಾಯಿಯ ಹೆಸರು", "माता का नाम"),
   ("Please tell me your mother's name.", "ನಿಮ್ಮ ತಾಯಿಯ ಹೆಸರನ್ನು ಹೇಳಿ.", "अपनी माता का नाम बताइए।"),
   type="name", compare="name", profile_key="mother_name", aliases=["Mother's name", "Name of Mother"])
_f("dob", "personal", ("date of birth", "ಹುಟ್ಟಿದ ದಿನಾಂಕ", "जन्म तिथि"),
   ("Please tell me your date of birth: day, month and year.",
    "ನಿಮ್ಮ ಹುಟ್ಟಿದ ದಿನಾಂಕವನ್ನು ಹೇಳಿ: ದಿನ, ತಿಂಗಳು, ವರ್ಷ.",
    "अपनी जन्म तिथि बताइए: दिन, महीना और साल।"),
   type="date", rule="dob", compare="exact", profile_key="dob", aliases=["Date of Birth", "DOB"])
_f("gender", "personal", ("gender", "ಲಿಂಗ", "लिंग"),
   ("What is your gender? Male, female or other.", "ನಿಮ್ಮ ಲಿಂಗ ಯಾವುದು? ಪುರುಷ, ಮಹಿಳೆ ಅಥವಾ ಇತರೆ.", "आपका लिंग क्या है? पुरुष, महिला या अन्य।"),
   type="choice", input_mode="choice", compare="exact", profile_key="gender", aliases=["Gender"],
   options=[opt("Male", "ಪುರುಷ", "पुरुष", ["man", "purusha"]),
            opt("Female", "ಮಹಿಳೆ", "महिला", ["woman", "stree", "स्त्री", "ಸ್ತ್ರೀ"]),
            opt("Third Gender", "ತೃತೀಯ ಲಿಂಗ", "तीसरा लिंग", ["other", "transgender", "ಇತರೆ", "अन्य"])])
_f("marital_status", "personal", ("marital status", "ವೈವಾಹಿಕ ಸ್ಥಿತಿ", "वैवाहिक स्थिति"),
   ("What is your marital status?", "ನಿಮ್ಮ ವೈವಾಹಿಕ ಸ್ಥಿತಿ ಯಾವುದು?", "आपकी वैवाहिक स्थिति क्या है?"),
   type="choice", input_mode="choice", aliases=["Marital Status"],
   options=[opt("Married", "ವಿವಾಹಿತ", "विवाहित"),
            opt("Unmarried", "ಅವಿವಾಹಿತ", "अविवाहित", ["single"]),
            opt("Widowed", "ವಿಧವೆ", "विधवा", ["widow", "widower", "ವಿಧುರ", "विधुर"]),
            opt("Divorced", "ವಿಚ್ಛೇದಿತ", "तलाकशुदा"),
            opt("Other", "ಇತರೆ", "अन्य")])
_f("occupation", "personal", ("occupation", "ವೃತ್ತಿ", "पेशा"),
   ("What is your occupation or work?", "ನಿಮ್ಮ ವೃತ್ತಿ ಅಥವಾ ಕೆಲಸ ಯಾವುದು?", "आपका पेशा या काम क्या है?"),
   aliases=["Occupation Type", "Occupation"])
_f("title", "personal", ("title", "ಶೀರ್ಷಿಕೆ", "शीर्षक"),
   ("Are you Sri or Smt?", "ನೀವು ಶ್ರೀ ಅಥವಾ ಶ್ರೀಮತಿ?", "आप श्री हैं या श्रीमती?"),
   type="choice", input_mode="choice", derived="title_from_gender", aliases=["Title"],
   options=[opt("Sri", "ಶ್ರೀ", "श्री", ["shri", "mr"]),
            opt("Smt", "ಶ್ರೀಮತಿ", "श्रीमती", ["smt.", "mrs", "shrimati"])])
_f("relation_type", "personal", ("relation type", "ಸಂಬಂಧ", "संबंध"),
   ("Are you son of, wife of, daughter of, or care of? Say S O, W O, D O or C O.",
    "ನೀವು ಯಾರ ಮಗ, ಪತ್ನಿ, ಮಗಳು ಅಥವಾ ಪಾಲನೆಯಲ್ಲಿ? ಎಸ್/ಒ, ಡಬ್ಲ್ಯೂ/ಒ, ಡಿ/ಒ ಅಥವಾ ಸಿ/ಒ ಹೇಳಿ.",
    "आप किसके पुत्र, पत्नी, पुत्री या देखरेख में हैं? S/O, W/O, D/O या C/O बोलिए।"),
   type="choice", input_mode="choice", aliases=["Relation type"],
   options=[opt("S/O", "ಎಸ್/ಒ", "एस/ओ", ["so", "s/o", "son of", "ಮಗ", "पुत्र"]),
            opt("W/O", "ಡಬ್ಲ್ಯೂ/ಒ", "डब्ल्यू/ओ", ["wo", "w/o", "wife of", "ಪತ್ನಿ", "पत्नी"]),
            opt("D/O", "ಡಿ/ಒ", "डी/ओ", ["do", "d/o", "daughter of", "ಮಗಳು", "पुत्री"]),
            opt("C/O", "ಸಿ/ಒ", "सी/ओ", ["co", "c/o", "care of"])])
_f("relation_name", "personal", ("father's or husband's name", "ತಂದೆ ಅಥವಾ ಪತಿಯ ಹೆಸರು", "पिता या पति का नाम"),
   ("Please tell me your father's or husband's name.", "ನಿಮ್ಮ ತಂದೆ ಅಥವಾ ಪತಿಯ ಹೆಸರು ಹೇಳಿ.", "अपने पिता या पति का नाम बताइए।"),
   type="name", compare="name", profile_key="father_name", aliases=["Relation's name (father / husband)"])
_f("annual_income", "income", ("annual income", "ವಾರ್ಷಿಕ ಆದಾಯ", "वार्षिक आय"),
   ("What is your family's yearly income in rupees?", "ನಿಮ್ಮ ಕುಟುಂಬದ ವಾರ್ಷಿಕ ಆದಾಯ ಎಷ್ಟು ರೂಪಾಯಿ?", "आपके परिवार की वार्षिक आय कितने रुपये है?"),
   type="number", rule="number", compare="exact", profile_key="annual_income",
   aliases=["Annual Income", "Annual family income (Rs)", "Annual Income Rs."])
_f("address_line1", "address", ("house and street address", "ಮನೆ ಮತ್ತು ರಸ್ತೆ ವಿಳಾಸ", "घर और सड़क का पता"),
   ("Please tell me your house number and street.", "ನಿಮ್ಮ ಮನೆ ಸಂಖ್ಯೆ ಮತ್ತು ರಸ್ತೆಯ ವಿಳಾಸ ಹೇಳಿ.", "अपना घर नंबर और सड़क का पता बताइए।"),
   compare="text", profile_key="address_line1", aliases=["Address line 1 (house / street)", "Address"])
_f("village", "address", ("village or town", "ಗ್ರಾಮ ಅಥವಾ ಪಟ್ಟಣ", "गाँव या शहर"),
   ("Please tell me your village or town.", "ನಿಮ್ಮ ಗ್ರಾಮ ಅಥವಾ ಪಟ್ಟಣದ ಹೆಸರು ಹೇಳಿ.", "अपने गाँव या शहर का नाम बताइए।"),
   compare="text", profile_key="village", aliases=["Village / Town"])
_f("taluk", "address", ("taluk", "ತಾಲ್ಲೂಕು", "तालुक"),
   ("Please tell me your taluk.", "ನಿಮ್ಮ ತಾಲ್ಲೂಕಿನ ಹೆಸರು ಹೇಳಿ.", "अपने तालुक का नाम बताइए।"),
   compare="text", profile_key="taluk", aliases=["Taluk"])
_f("district", "address", ("district", "ಜಿಲ್ಲೆ", "ज़िला"),
   ("Please tell me your district.", "ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ಹೆಸರು ಹೇಳಿ.", "अपने ज़िले का नाम बताइए।"),
   compare="text", profile_key="district", aliases=["District"])
_f("pin_code", "address", ("PIN code", "ಪಿನ್ ಕೋಡ್", "पिन कोड"),
   ("Please tell me your 6 digit PIN code.", "ನಿಮ್ಮ 6 ಅಂಕಿಯ ಪಿನ್ ಕೋಡ್ ಹೇಳಿ.", "अपना 6 अंकों का पिन कोड बताइए।"),
   type="digits", input_mode="keypad", rule="pin", compare="exact", profile_key="pin_code", aliases=["PIN code"])
_f("mobile", "personal", ("mobile number", "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ", "मोबाइल नंबर"),
   ("Please enter your 10 digit mobile number.", "ನಿಮ್ಮ 10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.", "अपना 10 अंकों का मोबाइल नंबर दर्ज कीजिए।"),
   type="digits", input_mode="keypad", rule="mobile", compare="exact", profile_key="mobile", sensitive=True,
   aliases=["Mobile number"])
_f("pan", "identity", ("PAN number", "ಪ್ಯಾನ್ ಸಂಖ್ಯೆ", "पैन नंबर"),
   ("Please enter your PAN number.", "ನಿಮ್ಮ ಪ್ಯಾನ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.", "अपना पैन नंबर दर्ज कीजिए।"),
   type="id", input_mode="keypad", rule="pan", compare="exact", profile_key="pan", sensitive=True,
   required=False, aliases=["PAN"])
_f("aadhaar_number", "identity", ("Aadhaar number", "ಆಧಾರ್ ಸಂಖ್ಯೆ", "आधार नंबर"),
   ("Please enter your 12 digit Aadhaar number.", "ನಿಮ್ಮ 12 ಅಂಕಿಯ ಆಧಾರ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.", "अपना 12 अंकों का आधार नंबर दर्ज कीजिए।"),
   type="digits", input_mode="keypad", rule="aadhaar", compare="exact", profile_key="aadhaar_number",
   sensitive=True, aliases=["Aadhaar number"])
_f("ration_card_no", "identity", ("ration card number", "ಪಡಿತರ ಚೀಟಿ ಸಂಖ್ಯೆ", "राशन कार्ड नंबर"),
   ("Please enter your ration card number.", "ನಿಮ್ಮ ಪಡಿತರ ಚೀಟಿ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.", "अपना राशन कार्ड नंबर दर्ज कीजिए।"),
   type="digits", input_mode="keypad", compare="exact", profile_key="ration_card_no", sensitive=True,
   aliases=["Ration card no."])
_f("ration_card_type", "identity", ("ration card type", "ಪಡಿತರ ಚೀಟಿ ವಿಧ", "राशन कार्ड प्रकार"),
   ("Which ration card do you have? BPL, Antyodaya or other.", "ನಿಮ್ಮ ಪಡಿತರ ಚೀಟಿ ಯಾವುದು? ಬಿಪಿಎಲ್, ಅಂತ್ಯೋದಯ ಅಥವಾ ಇತರೆ.", "आपका राशन कार्ड कौन सा है? बीपीएल, अंत्योदय या अन्य।"),
   type="choice", input_mode="choice", compare="exact", profile_key="ration_card_type",
   aliases=["Ration card type"],
   options=[opt("BPL", "ಬಿಪಿಎಲ್", "बीपीएल"), opt("AAY", "ಅಂತ್ಯೋದಯ", "अंत्योदय", ["antyodaya"]),
            opt("Other", "ಇತರೆ", "अन्य", ["apl"])])
_f("bank_name", "bank", ("bank name", "ಬ್ಯಾಂಕ್ ಹೆಸರು", "बैंक का नाम"),
   ("Please tell me your bank's name.", "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಹೆಸರು ಹೇಳಿ.", "अपने बैंक का नाम बताइए।"),
   compare="text", profile_key="bank_name", aliases=["Bank name"])
_f("branch", "bank", ("bank branch", "ಬ್ಯಾಂಕ್ ಶಾಖೆ", "बैंक शाखा"),
   ("Please tell me your bank branch.", "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಶಾಖೆಯ ಹೆಸರು ಹೇಳಿ.", "अपनी बैंक शाखा का नाम बताइए।"),
   compare="text", profile_key="branch", aliases=["Branch"])
_f("account_holder", "bank", ("account holder name", "ಖಾತೆದಾರರ ಹೆಸರು", "खाताधारक का नाम"),
   ("Please tell me the name of the bank account holder.", "ಬ್ಯಾಂಕ್ ಖಾತೆದಾರರ ಹೆಸರು ಹೇಳಿ.", "बैंक खाताधारक का नाम बताइए।"),
   type="name", compare="name", profile_key="account_holder", aliases=["Account holder name"])
_f("account_number", "bank", ("account number", "ಖಾತೆ ಸಂಖ್ಯೆ", "खाता नंबर"),
   ("Please enter your bank account number.", "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.", "अपना बैंक खाता नंबर दर्ज कीजिए।"),
   type="digits", input_mode="keypad", rule="account", compare="exact", profile_key="account_number",
   sensitive=True, aliases=["Account number", "Account No."])
_f("ifsc", "bank", ("IFSC code", "ಐಎಫ್‌ಎಸ್‌ಸಿ ಕೋಡ್", "आईएफएससी कोड"),
   ("Please enter your bank's IFSC code. It is printed on your passbook.", "ನಿಮ್ಮ ಬ್ಯಾಂಕ್‌ನ ಐಎಫ್‌ಎಸ್‌ಸಿ ಕೋಡ್ ನಮೂದಿಸಿ. ಇದು ಪಾಸ್‌ಬುಕ್‌ನಲ್ಲಿದೆ.", "अपने बैंक का आईएफएससी कोड दर्ज कीजिए। यह पासबुक पर छपा है।"),
   type="id", input_mode="keypad", rule="ifsc", compare="exact", profile_key="ifsc", aliases=["IFSC code"])

# profile_key -> comparison kind / value type (used by cross-document consistency)
KEY_KIND = {f["profile_key"]: f["compare"] for f in LIB.values() if f["profile_key"]}
KEY_TYPE = {f["profile_key"]: f["type"] for f in LIB.values() if f["profile_key"]}
KEY_LABEL = {f["profile_key"]: f["label"] for f in LIB.values() if f["profile_key"]}
SENSITIVE_KEYS = {f["profile_key"] for f in LIB.values() if f["profile_key"] and f["sensitive"]} | {"cif_no"}
