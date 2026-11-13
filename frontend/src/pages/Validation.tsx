import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AlertTriangle, CheckCircle2, FileQuestion, XCircle, RefreshCw, ChevronRight, Info } from "lucide-react";
import { Badge, Button, Card, Field, Page, Progress, inputCls } from "../components/ui";
import { useApplication } from "../context/ApplicationContext";
import { documentService, validationService } from "../services";
import type { ValidationStatus } from "../types";

const LBL: Record<ValidationStatus, [string, "ok" | "warn" | "bad" | "info"]> = {
  looks_consistent: ["Looks consistent", "ok"],
  please_verify: ["Please verify", "warn"],
  possible_mismatch: ["Possible mismatch", "bad"],
  evidence_needed: ["Evidence needed", "info"],
  low_confidence: ["Low confidence", "warn"]
};

export default function Validation() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const l = state.language;
  const [busy, setBusy] = useState(false);
  const [edit, setEdit] = useState<string | null>(null);
  const [val, setVal] = useState("");

  const run = useCallback(async (s = state) => {
    setBusy(true);
    const r = await validationService.validate(s);
    dispatch({ t: "validation", issues: r.issues, score: r.score });
    setBusy(false);
  }, [state, dispatch]);

  useEffect(() => {
    void run();
  }, [state.answers, state.documents, state.resolved]); // eslint-disable-line

  const open = state.validationIssues.filter((i) => i.status !== "looks_consistent");
  const blocking = open.filter((i) => i.severity === "blocking");

  return (
    <Page title="Application Validation" desc="We're checking your form answers against your uploaded documents for consistency.">
      <div className="space-y-8 mt-8">
        <Card className="bg-leaf text-white p-8 relative overflow-hidden border-0">
            <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div className="space-y-4 flex-1">
                    <h2 className="font-serif text-3xl font-bold">Readiness Score: {state.readinessScore}%</h2>
                    <div className="w-full max-w-md">
                        <Progress value={state.readinessScore} label="Application readiness" />
                    </div>
                    <p className="text-white/70 text-sm max-w-lg">
                        This score reflects the completeness and internal consistency of your application.
                        {blocking.length > 0 ? ` There are ${blocking.length} blocking issues to resolve.` : " Your application looks mostly ready!"}
                    </p>
                </div>
                <div className="flex-shrink-0">
                    <Button kind="cta" className="px-8 shadow-xl" onClick={() => nav("/preview")}>
                        Preview Final Draft <ChevronRight className="w-4 h-4 ml-2" />
                    </Button>
                </div>
            </div>
            {/* Background design element */}
            <div className="absolute -right-12 -bottom-12 w-48 h-48 bg-leaf/20 rounded-full blur-3xl"></div>
        </Card>

        <div className="grid gap-6">
            <div className="flex items-center justify-between">
                <h3 className="text-xl font-serif font-bold text-ink">Validation Results</h3>
                <Button kind="ghost" className="text-xs gap-2" onClick={() => run()}>
                    <RefreshCw className={`w-3 h-3 ${busy ? "animate-spin" : ""}`} /> Re-run Checks
                </Button>
            </div>

            {state.validationIssues.map((i) => {
                const [t, tone] = LBL[i.status];
                const Icon = i.status === "looks_consistent" ? CheckCircle2 : i.status === "possible_mismatch" ? XCircle : i.status === "evidence_needed" ? FileQuestion : AlertTriangle;
                const isMismatch = i.status === "possible_mismatch";
                const isResolved = i.status === "looks_consistent";

                return (
                    <Card key={i.field_id} className={`transition-all duration-300 ${isResolved ? "opacity-70 grayscale-[0.5] hover:grayscale-0 hover:opacity-100" : "border-l-4 border-l-saffron shadow-md"}`}>
                        <div className="flex flex-col md:flex-row md:items-start gap-6">
                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${
                                isResolved ? "bg-leaf/10 text-leaf" : isMismatch ? "bg-terracotta/10 text-terracotta" : "bg-saffron/10 text-saffron"
                            }`}>
                                <Icon className="w-6 h-6" />
                            </div>

                            <div className="flex-1 space-y-4">
                                <div className="flex flex-wrap items-center gap-3">
                                    <h4 className="font-bold text-ink text-lg">{i.label}</h4>
                                    <Badge t={tone}>{t}</Badge>
                                </div>

                                <p className="text-slate leading-relaxed">{l === "kn" ? i.message_kn : i.message_en}</p>

                                {(i.form_value || i.doc_value) && (
                                    <div className="grid sm:grid-cols-2 gap-4 p-4 bg-parchment/30 rounded-2xl border border-ink/5">
                                        <div>
                                            <p className="text-[10px] font-bold text-slate uppercase tracking-wider mb-1">Form Entry</p>
                                            <p className="font-semibold text-ink">{i.form_value || "—"}</p>
                                        </div>
                                        <div>
                                            <p className="text-[10px] font-bold text-slate uppercase tracking-wider mb-1">Found in Documents</p>
                                            <p className="font-semibold text-ink">{i.doc_value || "—"}</p>
                                        </div>
                                        {i.source_document && (
                                            <div className="sm:col-span-2 pt-2 border-t border-ink/5 flex items-center gap-2">
                                                <Info className="w-3 h-3 text-slate" />
                                                <span className="text-xs text-slate">Verified via {i.source_document}</span>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {!isResolved && (
                                    <div className="flex flex-wrap gap-3 pt-2">
                                        {i.action === "upload_document" && (
                                            <Button kind="cta" onClick={async () => dispatch({ t: "doc", v: await documentService.upload(i.needs_doc!) })}>
                                                Upload {i.needs_doc?.split("_").join(" ")}
                                            </Button>
                                        )}
                                        {i.action === "confirm_or_edit" && (
                                            <Button className="px-6" onClick={() => dispatch({ t: "resolve", id: i.field_id })}>
                                                Confirm Value
                                            </Button>
                                        )}
                                        <Button kind="ghost" className="px-6" onClick={() => { setEdit(i.field_id); setVal(i.form_value ?? ""); }}>
                                            Edit Answer
                                        </Button>
                                    </div>
                                )}

                                {edit === i.field_id && (
                                    <div className="mt-4 p-6 bg-white border border-leaf/20 rounded-2xl shadow-inner space-y-4 animate-in fade-in slide-in-from-top-2">
                                        <Field id="fix" label={`Correct ${i.label}`} hint="Enter the accurate value as per your documents.">
                                            <input id="fix" className={inputCls} value={val} onChange={(e) => setVal(e.target.value)} autoFocus />
                                        </Field>
                                        <div className="flex gap-2 justify-end">
                                            <Button kind="ghost" onClick={() => setEdit(null)}>Cancel</Button>
                                            <Button onClick={() => { dispatch({ t: "answer", v: { field_id: i.field_id, value: val.trim(), source: "text", confirmed: true } }); setEdit(null); }}>
                                                Save and Re-check
                                            </Button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </Card>
                );
            })}
        </div>
      </div>
    </Page>
  );
}
