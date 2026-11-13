import { BANK_FIELDS, MOCK_DOCS, MOCK_PROFILE } from "../mocks/data";
import type { ApplicationState, FieldAnswer, FormField, FormType, ProfileField, SupportingDocument, ValidationIssue } from "../types";

const wait = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));
const clone = <T>(value: T): T => structuredClone(value);

export async function uploadProfileDocument(id: string, file?: File): Promise<{ id: string; filename: string }> {
  await wait(800);
  return { id, filename: file?.name ?? `sample_${id}.pdf` };
}

export async function extractProfile(): Promise<ProfileField[]> {
  await wait(1000);
  return clone(MOCK_PROFILE);
}

export async function confirmProfileField(key: string, value: string): Promise<ProfileField> {
  await wait(350);
  const field = MOCK_PROFILE.find((item) => item.key === key);
  return { ...(field ?? MOCK_PROFILE[0]), key, value, confirmed: true, confirmedAt: new Date().toISOString() };
}

export async function parseForm(file: File | null, formType: FormType = "bank", onStage?: (label: string, percent: number) => void): Promise<FormField[]> {
  if (file?.name.toLowerCase().includes("fail")) {
    await wait(600);
    throw new Error("We could not read this file. Try a clearer PDF, JPG or PNG.");
  }
  const stages = ["Uploading file…", "Reading page 1 of 1…", "Identifying fields…", "Checking details…", "Form analysis completed."];
  for (let index = 0; index < stages.length; index += 1) {
    onStage?.(stages[index], Math.round(((index + 1) / stages.length) * 100));
    await wait(300);
  }
  if (formType === "pension") {
    return clone(BANK_FIELDS.map((field) => ({ ...field, group: field.group === "Bank Details" ? "Bank Information" : field.group })));
  }
  return clone(BANK_FIELDS);
}

export async function saveAnswer(answer: FieldAnswer): Promise<FieldAnswer> {
  await wait(300);
  return clone(answer);
}

export async function uploadEvidence(id: string): Promise<SupportingDocument> {
  await wait(800);
  const document = MOCK_DOCS.find((item) => item.id === id);
  if (!document) throw new Error("That sample document is not available.");
  return { ...clone(document), uploaded: true, filename: `sample_${id}.pdf` };
}

export async function compare(state: ApplicationState): Promise<ValidationIssue[]> {
  await wait(450);
  const name = state.answers.applicant_name?.value?.trim() ?? "";
  const identity = state.documents.find((document) => document.id === "identity");
  return [{
    field_id: "applicant_name",
    label: "Applicant name",
    severity: "should_fix",
    status: name === identity?.values.name || state.resolved.includes("applicant_name") ? "looks_consistent" : "please_verify",
    message_en: "Compare the form name with your uploaded identity document.",
    message_kn: "ಫಾರ್ಮ್ ಹೆಸರನ್ನು ಗುರುತಿನ ದಾಖಲೆಯೊಂದಿಗೆ ಹೋಲಿಸಿ.",
    action: "confirm_or_edit",
    form_value: name,
    doc_value: identity?.values.name,
    source_document: "Sample Aadhaar (SAMPLE)",
  }];
}

export async function validate(state: ApplicationState): Promise<{ issues: ValidationIssue[]; score: number }> {
  await wait(700);
  const a = (id: string) => state.answers[id]?.value?.trim() ?? "";
  const issues: ValidationIssue[] = await compare(state);
  const income = state.documents.find((document) => document.id === "income");
  issues.push({
    field_id: "annual_income",
    label: "Annual income",
    severity: "should_fix",
    status: income?.uploaded ? "looks_consistent" : "evidence_needed",
    message_en: income?.uploaded ? "Income evidence is available." : "Upload an income certificate to check this value.",
    message_kn: income?.uploaded ? "ಆದಾಯದ ದಾಖಲೆ ಲಭ್ಯವಿದೆ." : "ಈ ಮೌಲ್ಯವನ್ನು ಪರಿಶೀಲಿಸಲು ಆದಾಯ ಪ್ರಮಾಣಪತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
    action: income?.uploaded ? "confirm_or_edit" : "upload_document",
    needs_doc: "income",
    form_value: a("annual_income"),
    doc_value: income?.values.income,
  });
  issues.push({
    field_id: "account_number",
    label: "Account number",
    severity: "blocking",
    status: /^\d{9,18}$/.test(a("account_number")) ? "looks_consistent" : "possible_mismatch",
    message_en: "The account number should be 9–18 digits.",
    message_kn: "ಖಾತೆ ಸಂಖ್ಯೆ 9–18 ಅಂಕಿಗಳಾಗಿರಬೇಕು.",
    action: "manual_review",
    form_value: a("account_number"),
  });
  const total = issues.reduce((sum, item) => sum + (item.severity === "blocking" ? 5 : 3), 0);
  const passed = issues.reduce((sum, item) => sum + (item.status === "looks_consistent" ? (item.severity === "blocking" ? 5 : 3) : 0), 0);
  return { issues, score: total ? Math.round((passed / total) * 100) : 0 };
}

export async function generate(): Promise<{ ok: true }> {
  await wait(800);
  return { ok: true };
}

export async function deleteSession(): Promise<{ deleted: true }> {
  await wait(400);
  return { deleted: true };
}
