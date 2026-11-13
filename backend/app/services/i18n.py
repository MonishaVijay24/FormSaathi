"""All spoken / shown messages in English, Kannada, Hindi.
NOTE: Kannada & Hindi strings need review by a fluent speaker before demo."""
LANGS = ("en", "kn", "hi")

SOURCE_NAMES = {
    "aadhaar": {"en": "Aadhaar", "kn": "ಆಧಾರ್", "hi": "आधार"},
    "pan": {"en": "PAN card", "kn": "ಪ್ಯಾನ್ ಕಾರ್ಡ್", "hi": "पैन कार्ड"},
    "bpl": {"en": "BPL card", "kn": "ಬಿಪಿಎಲ್ ಕಾರ್ಡ್", "hi": "बीपीएल कार्ड"},
    "passbook": {"en": "bank passbook", "kn": "ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್", "hi": "बैंक पासबुक"},
    "income_certificate": {"en": "income certificate", "kn": "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ", "hi": "आय प्रमाण पत्र"},
    "marks_card": {"en": "marks card", "kn": "ಅಂಕಪಟ್ಟಿ", "hi": "अंक पत्र"},
}

TEXT = {
    "PREFILL": {
        "en": "From your {source}, your {label} is {value}. Is this correct? Please say yes or no.",
        "kn": "ನಿಮ್ಮ {source} ಪ್ರಕಾರ ನಿಮ್ಮ {label} {value}. ಇದು ಸರಿಯೇ? ಹೌದು ಅಥವಾ ಇಲ್ಲ ಎಂದು ಹೇಳಿ.",
        "hi": "आपके {source} के अनुसार आपका {label} {value} है। क्या यह सही है? हाँ या नहीं बोलिए।"},
    "CONFIRM": {
        "en": "You said {value}. Is this correct? Please say yes or no.",
        "kn": "ನೀವು {value} ಎಂದು ಹೇಳಿದಿರಿ. ಇದು ಸರಿಯೇ? ಹೌದು ಅಥವಾ ಇಲ್ಲ ಎಂದು ಹೇಳಿ.",
        "hi": "आपने {value} कहा। क्या यह सही है? हाँ या नहीं बोलिए।"},
    "KEEP": {
        "en": "Do you want to keep your answer? Say yes to keep it, or no to answer again.",
        "kn": "ನಿಮ್ಮ ಉತ್ತರವನ್ನೇ ಇಟ್ಟುಕೊಳ್ಳಬೇಕೇ? ಹೌದು ಎಂದರೆ ಉಳಿಸಿ, ಇಲ್ಲ ಎಂದರೆ ಮತ್ತೆ ಹೇಳಿ.",
        "hi": "क्या आप अपना उत्तर रखना चाहते हैं? रखने के लिए हाँ, फिर से बताने के लिए नहीं बोलिए।"},
    "DONE": {
        "en": "All questions are done. Please review your application.",
        "kn": "ಎಲ್ಲಾ ಪ್ರಶ್ನೆಗಳು ಮುಗಿದಿವೆ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಅರ್ಜಿಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "hi": "सभी प्रश्न पूरे हो गए। कृपया अपना आवेदन जाँचिए।"},
    "YES_NO_UNCLEAR": {
        "en": "I did not catch that. Please say yes or no.",
        "kn": "ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಹೌದು ಅಥವಾ ಇಲ್ಲ ಎಂದು ಹೇಳಿ.",
        "hi": "मुझे समझ नहीं आया। कृपया हाँ या नहीं बोलिए।"},
    "CHOICE_UNCLEAR": {
        "en": "I did not understand. Please choose one option: {options}.",
        "kn": "ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಒಂದು ಆಯ್ಕೆ ಹೇಳಿ: {options}.",
        "hi": "मुझे समझ नहीं आया। कृपया एक विकल्प चुनें: {options}।"},
    "TRANSLIT_FAIL": {
        "en": "I could not convert this to English letters. Please type it in English letters.",
        "kn": "ಇದನ್ನು ಇಂಗ್ಲಿಷ್ ಅಕ್ಷರಗಳಿಗೆ ಬದಲಿಸಲು ಆಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಇಂಗ್ಲಿಷ್ ಅಕ್ಷರಗಳಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ.",
        "hi": "इसे अंग्रेज़ी अक्षरों में बदल नहीं सका। कृपया अंग्रेज़ी अक्षरों में टाइप कीजिए।"},
    "REQUIRED": {
        "en": "Please give your {label}. This cannot be left empty.",
        "kn": "ದಯವಿಟ್ಟು ನಿಮ್ಮ {label} ಹೇಳಿ. ಇದನ್ನು ಖಾಲಿ ಬಿಡಲಾಗುವುದಿಲ್ಲ.",
        "hi": "कृपया अपना {label} बताइए। इसे खाली नहीं छोड़ सकते।"},
    "PIN_INVALID": {
        "en": "The PIN code must be exactly 6 digits. You gave {value}. Please say it again.",
        "kn": "ಪಿನ್ ಕೋಡ್ ಸರಿಯಾಗಿ 6 ಅಂಕಿಗಳಿರಬೇಕು. ನೀವು {value} ಎಂದಿರಿ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಹೇಳಿ.",
        "hi": "पिन कोड ठीक 6 अंकों का होना चाहिए। आपने {value} बताया। कृपया फिर से बताइए।"},
    "MOBILE_INVALID": {
        "en": "A mobile number must have 10 digits and start with 6, 7, 8 or 9. Please say it again.",
        "kn": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ 10 ಅಂಕಿಗಳಿರಬೇಕು ಮತ್ತು 6, 7, 8 ಅಥವಾ 9 ರಿಂದ ಆರಂಭವಾಗಬೇಕು. ದಯವಿಟ್ಟು ಮತ್ತೆ ಹೇಳಿ.",
        "hi": "मोबाइल नंबर 10 अंकों का होना चाहिए और 6, 7, 8 या 9 से शुरू होना चाहिए। कृपया फिर से बताइए।"},
    "AADHAAR_INVALID": {
        "en": "An Aadhaar number must have 12 digits. Please enter it again.",
        "kn": "ಆಧಾರ್ ಸಂಖ್ಯೆ 12 ಅಂಕಿಗಳಿರಬೇಕು. ದಯವಿಟ್ಟು ಮತ್ತೆ ನಮೂದಿಸಿ.",
        "hi": "आधार नंबर 12 अंकों का होना चाहिए। कृपया फिर से दर्ज कीजिए।"},
    "PAN_INVALID": {
        "en": "A PAN has 5 letters, 4 digits and 1 letter. Please enter it again.",
        "kn": "ಪ್ಯಾನ್ ಸಂಖ್ಯೆಯಲ್ಲಿ 5 ಅಕ್ಷರ, 4 ಅಂಕಿ ಮತ್ತು 1 ಅಕ್ಷರ ಇರಬೇಕು. ದಯವಿಟ್ಟು ಮತ್ತೆ ನಮೂದಿಸಿ.",
        "hi": "पैन में 5 अक्षर, 4 अंक और 1 अक्षर होता है। कृपया फिर से दर्ज कीजिए।"},
    "IFSC_INVALID": {
        "en": "An IFSC code has 11 characters: 4 letters, a zero, then 6 letters or digits.",
        "kn": "ಐಎಫ್‌ಎಸ್‌ಸಿ ಕೋಡ್ 11 ಅಕ್ಷರಗಳು: 4 ಅಕ್ಷರ, ಒಂದು ಸೊನ್ನೆ, ನಂತರ 6 ಅಕ್ಷರ ಅಥವಾ ಅಂಕಿ.",
        "hi": "आईएफएससी कोड 11 अक्षरों का होता है: 4 अक्षर, एक शून्य, फिर 6 अक्षर या अंक।"},
    "ACCOUNT_LENGTH": {
        "en": "An account number should have 9 to 18 digits. You gave {count}. Please enter the full number.",
        "kn": "ಖಾತೆ ಸಂಖ್ಯೆ 9 ರಿಂದ 18 ಅಂಕಿಗಳಿರಬೇಕು. ನೀವು {count} ಅಂಕಿ ಕೊಟ್ಟಿದ್ದೀರಿ. ಪೂರ್ಣ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.",
        "hi": "खाता नंबर 9 से 18 अंकों का होना चाहिए। आपने {count} अंक दिए। कृपया पूरा नंबर दर्ज कीजिए।"},
    "DOB_INVALID": {
        "en": "I could not read this date. Please say day, month and year, for example 15 June 1955.",
        "kn": "ಈ ದಿನಾಂಕ ಓದಲಾಗಲಿಲ್ಲ. ದಿನ, ತಿಂಗಳು, ವರ್ಷ ಹೇಳಿ, ಉದಾಹರಣೆಗೆ 15 ಜೂನ್ 1955.",
        "hi": "यह तारीख़ पढ़ नहीं सका। दिन, महीना और साल बताइए, जैसे 15 जून 1955।"},
    "NUMBER_INVALID": {
        "en": "Please give a number only, for example 18000.",
        "kn": "ದಯವಿಟ್ಟು ಸಂಖ್ಯೆ ಮಾತ್ರ ಹೇಳಿ, ಉದಾಹರಣೆಗೆ 18000.",
        "hi": "कृपया केवल संख्या बताइए, जैसे 18000।"},
    "MISMATCH": {
        "en": "The {label} you gave, {said}, does not match {doc} in your {source}. Please check.",
        "kn": "ನೀವು ಹೇಳಿದ {label} {said} ನಿಮ್ಮ {source} ನಲ್ಲಿರುವ {doc} ಗೆ ಹೊಂದುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರಿಶೀಲಿಸಿ.",
        "hi": "आपने जो {label} {said} बताया, वह आपके {source} में दिए {doc} से मेल नहीं खाता। कृपया जाँचिए।"},
    "VARIATION": {
        "en": "The {label} you gave, {said}, looks similar to but is not the same as {doc} in your {source}. Please check the spelling.",
        "kn": "ನೀವು ಹೇಳಿದ {label} {said}, ನಿಮ್ಮ {source} ನಲ್ಲಿರುವ {doc} ಗೆ ಹೋಲುತ್ತದೆ ಆದರೆ ಒಂದೇ ಅಲ್ಲ. ಕಾಗುಣಿತ ಪರಿಶೀಲಿಸಿ.",
        "hi": "आपने जो {label} {said} बताया, वह आपके {source} में दिए {doc} से मिलता-जुलता है पर वही नहीं है। कृपया वर्तनी जाँचिए।"},
    "CROSS_DOC": {
        "en": "{label} differs between your documents: {a} in your {s1} and {b} in your {s2}.",
        "kn": "{label} ನಿಮ್ಮ ದಾಖಲೆಗಳಲ್ಲಿ ಬೇರೆಬೇರೆ ಇದೆ: {s1} ನಲ್ಲಿ {a} ಮತ್ತು {s2} ನಲ್ಲಿ {b}.",
        "hi": "{label} आपके दस्तावेज़ों में अलग है: {s1} में {a} और {s2} में {b}।"},
    "EVIDENCE": {
        "en": "Your {label} needs a supporting document. Please upload your {doc}.",
        "kn": "ನಿಮ್ಮ {label} ಗೆ ಬೆಂಬಲ ದಾಖಲೆ ಬೇಕು. ದಯವಿಟ್ಟು ನಿಮ್ಮ {doc} ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "hi": "आपके {label} के लिए सहायक दस्तावेज़ चाहिए। कृपया अपना {doc} अपलोड कीजिए।"},
    "ELIGIBILITY": {
        "en": "Please check eligibility: this scheme asks for age 65 or above and family income below Rs 20,000. This is only a hint, not a decision.",
        "kn": "ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ: ಈ ಯೋಜನೆಗೆ 65 ವರ್ಷ ಮೇಲ್ಪಟ್ಟವರು ಮತ್ತು ಕುಟುಂಬ ಆದಾಯ 20,000 ರೂ. ಕ್ಕಿಂತ ಕಡಿಮೆ ಇರಬೇಕು. ಇದು ಸೂಚನೆ ಮಾತ್ರ, ತೀರ್ಮಾನವಲ್ಲ.",
        "hi": "पात्रता जाँचिए: इस योजना में आयु 65 वर्ष या अधिक और पारिवारिक आय 20,000 रुपये से कम होनी चाहिए। यह केवल सुझाव है, निर्णय नहीं।"},
}


def t(key: str, lang: str, **kw) -> str:
    tpl = TEXT[key].get(lang) or TEXT[key]["en"]
    return tpl.format(**kw)


def t_all(key: str, **kw) -> dict[str, str]:
    """Render a message in all languages. A kwarg value may be a {lang: text} dict."""
    out = {}
    for l in LANGS:
        args = {k: (v[l] if isinstance(v, dict) else v) for k, v in kw.items()}
        out[l] = t(key, l, **args)
    return out
