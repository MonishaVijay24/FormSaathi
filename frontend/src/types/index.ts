export type Lang = "en" | "kn";
export type FormType = "bank" | "pension" | "scholarship";
export interface FormField { field_id: string; label_original: string; label_simple: Record<Lang, string>; data_type: "text"|"number"|"date"|"select"|"address"; group: string; required: boolean; sensitive: boolean; digits?: boolean; confidence: number; }
export interface FieldAnswer { field_id: string; value: string; transcript?: string; source: "voice"|"text"|"profile"; confirmed: boolean; }
export interface ProfileField { key: string; label: string; value: string; masked: boolean; source: string; confidence: number; confirmed: boolean; confirmedAt?: string; }
export interface SupportingDocument { id: string; title: string; filename?: string; uploaded: boolean; values: Record<string,string>; confidence: number; }
export type ValidationStatus = "looks_consistent"|"please_verify"|"possible_mismatch"|"evidence_needed"|"low_confidence";
export interface ValidationIssue { field_id: string; label: string; status: ValidationStatus; severity: "blocking"|"should_fix"|"minor"; message_en: string; message_kn: string; form_value?: string; doc_value?: string; source_document?: string; action: "confirm_or_edit"|"upload_document"|"manual_review"; needs_doc?: string; }
export interface ApplicationState { sessionId: string|null; language: Lang; selectedForm: FormType|null; currentStep: number; profile: ProfileField[]; fields: FormField[]; answers: Record<string,FieldAnswer>; documents: SupportingDocument[]; resolved: string[]; validationIssues: ValidationIssue[]; readinessScore: number; }
