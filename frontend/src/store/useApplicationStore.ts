import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { ApplicationState, FieldAnswer, FormField, FormType, Lang, ProfileField, SupportingDocument, ValidationIssue } from "../types";
import { MOCK_DOCS } from "../mocks/data";

export const initialState: ApplicationState = {
  sessionId: null,
  language: "en",
  selectedForm: null,
  currentStep: 0,
  profile: [],
  fields: [],
  answers: {},
  documents: structuredClone(MOCK_DOCS),
  resolved: [],
  validationIssues: [],
  readinessScore: 0,
};

export type Action =
  | { t: "lang"; v: Lang } | { t: "start" } | { t: "form"; v: FormType } | { t: "profile"; v: ProfileField[] }
  | { t: "confirmProfile"; key: string; value: string } | { t: "fields"; v: FormField[] } | { t: "field"; id: string; patch: Partial<FormField> }
  | { t: "answer"; v: FieldAnswer } | { t: "doc"; v: SupportingDocument } | { t: "resolve"; id: string }
  | { t: "validation"; issues: ValidationIssue[]; score: number } | { t: "reset" } | { t: "step"; v: number };

function reduceState(state: ApplicationState, action: Action): ApplicationState {
  switch (action.t) {
    case "lang": return { ...state, language: action.v };
    case "start": return { ...initialState, language: state.language, sessionId: `demo-${Date.now()}` };
    case "form": return { ...state, selectedForm: action.v, currentStep: 2 };
    case "profile": return { ...state, profile: action.v };
    case "confirmProfile": return { ...state, profile: state.profile.map((field) => field.key === action.key ? { ...field, value: action.value, confirmed: true, confirmedAt: new Date().toISOString() } : field) };
    case "fields": return { ...state, fields: action.v, currentStep: 3 };
    case "field": return { ...state, fields: state.fields.map((field) => field.field_id === action.id ? { ...field, ...action.patch } : field) };
    case "answer": return { ...state, answers: { ...state.answers, [action.v.field_id]: action.v } };
    case "doc": return { ...state, documents: state.documents.map((doc) => doc.id === action.v.id ? action.v : doc) };
    case "resolve": return { ...state, resolved: [...new Set([...state.resolved, action.id])] };
    case "validation": return { ...state, validationIssues: action.issues, readinessScore: action.score, currentStep: 4 };
    case "step": return { ...state, currentStep: action.v };
    case "reset": return { ...initialState, language: state.language };
  }
}

type Store = ApplicationState & { dispatch: (action: Action) => void };
export const useApplicationStore = create<Store>()(
  persist(
    (set) => ({
      ...initialState,
      dispatch: (action) => set((state) => ({ ...reduceState(state, action), dispatch: state.dispatch })),
    }),
    {
      name: "formsaathi-demo",
      storage: createJSONStorage(() => sessionStorage),
      partialize: (state) => import.meta.env.VITE_PERSIST_SESSION === "true" ? state : initialState,
    },
  ),
);
