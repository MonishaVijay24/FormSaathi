import i18n from "i18next";
import { initReactI18next } from "react-i18next";

export const resources = {
  en: {
    translation: {
      appName: "FormSaathi AI",
      tagline: "Your Application Companion",
      draftNotice: "SAMPLE — FICTIONAL DATA. This is a draft and has not been submitted or approved.",
      language: "Language",
    },
  },
  kn: {
    translation: {
      appName: "FormSaathi AI",
      tagline: "ನಿಮ್ಮ ಅರ್ಜಿ ಸಹಾಯಕ",
      draftNotice: "SAMPLE — ಕಾಲ್ಪನಿಕ ಮಾಹಿತಿ. ಇದು ಕರಡು ಮಾತ್ರ; ಸಲ್ಲಿಸಲಾಗಿಲ್ಲ ಅಥವಾ ಅನುಮೋದಿಸಲಾಗಿಲ್ಲ.",
      language: "ಭಾಷೆ",
    },
  },
} as const;

void i18n.use(initReactI18next).init({
  resources,
  lng: "en",
  fallbackLng: "en",
  interpolation: { escapeValue: false },
});

export default i18n;
