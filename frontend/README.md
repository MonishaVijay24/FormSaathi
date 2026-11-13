# FormSaathi AI – Frontend (mock-only)
React + TypeScript + Vite + Tailwind + Zustand + react-i18next. Run: `npm install && npm run dev`. Build: `npm run build && npm run preview`.
There is no backend or network API in this project. All delayed fictional data is in `src/services/mockApi.ts`; the page-facing exports are in `src/services/index.ts`.
The app never submits or claims approval. Outputs are marked as fictional drafts. Set `VITE_PERSIST_SESSION=true` only when sessionStorage persistence is useful for local testing.
State: `src/context/ApplicationContext.tsx` (useReducer) persists fictional demo state to localStorage key `formsaathi-demo`. Files are never stored.
Demo path: Start → confirm profile → Demo Bank form → sample form → review → assistant ("Use sample transcript" per question) → documents → check (name mismatch "Ananya Rao" vs "Ananya R.", income evidence needed) → fix → preview → print/delete.
Not included in this build: react-i18next (UI strings are inline English; question text is bilingual), scholarship form schema, ESLint/Prettier, session timer.
