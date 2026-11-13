import { deleteSession, extractProfile, generate, parseForm, uploadEvidence, validate } from "./mockApi";
import type { FormType } from "../types";

export const STAGES = ["Uploading file…", "Reading page 1 of 1…", "Identifying fields…", "Checking details…", "Form analysis completed."];

export const profileService = {
  extract: extractProfile,
};

export const formService = {
  async analyzeForm(file: File | null, onStage: (stage: string, percent: number) => void, formType: FormType = "bank") {
    return parseForm(file, formType, onStage);
  },
};

export const documentService = {
  upload: uploadEvidence,
};

export const validationService = {
  validate,
};

export const sessionService = {
  generatePdf: generate,
  deleteSession,
};
