import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Download, Printer, Edit3, Trash2, ShieldAlert, CheckCircle2, FileText, ChevronLeft } from "lucide-react";
import { Button, Card, Page, Progress } from "../components/ui";
import { useApplication } from "../context/ApplicationContext";
import { sessionService } from "../services";

const mask = (v: string) => v.length > 4 ? "•".repeat(v.length - 4) + v.slice(-4) : v;

export default function Preview() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const [msg, setMsg] = useState("");

  const done = state.fields.filter((f) => state.answers[f.field_id]?.confirmed);
  const pct = state.fields.length ? Math.round((done.length / state.fields.length) * 100) : 0;

  const download = async () => {
    setMsg("Generating your draft PDF...");
    await sessionService.generatePdf();
    setMsg("Draft ready. Use ‘Save as PDF’ in the print window.");
    window.print();
  };

  return (
    <Page title="Final Draft & Summary" desc="Review your final application form before downloading.">
      <div className="space-y-8 mt-8">
        {/* Warning Banner */}
        <Card className="bg-saffron/10 border-saffron/30 flex items-start gap-4">
            <ShieldAlert className="w-6 h-6 text-saffron flex-shrink-0 mt-0.5" />
            <div className="space-y-1">
                <h4 className="font-bold text-ink">Important Notice</h4>
                <p className="text-sm text-slate">
                    This is a completed draft for your review. It has not been officially submitted to or approved by any bank, government office, or scholarship authority.
                </p>
            </div>
        </Card>

        {/* Main Document Preview Card */}
        <Card className="p-8 space-y-8 bg-white shadow-premium border border-ink/5">
            <div className="text-center border-b border-ink/10 pb-6 space-y-2">
                <span className="eyebrow">Official draft document</span>
                <h2 className="font-serif text-3xl font-bold text-ink">Demo Bank Account Opening Form</h2>
                <p className="text-sm text-slate">FormSaathi AI Generated Draft • {new Date().toLocaleDateString()}</p>
            </div>

            <div className="space-y-4">
                <h3 className="font-serif font-bold text-lg text-ink">Application Details</h3>
                <div className="divide-y divide-ink/5">
                    {state.fields.map((f) => {
                        const a = state.answers[f.field_id];
                        return (
                            <div key={f.field_id} className="grid sm:grid-cols-2 py-3 items-center gap-2">
                                <dt className="text-sm font-medium text-slate">{f.label_original}</dt>
                                <dd className="font-semibold text-ink">
                                    {a?.confirmed ? (f.sensitive ? mask(a.value) : a.value) : <span className="text-terracotta italic text-sm">Not answered</span>}
                                </dd>
                            </div>
                        );
                    })}
                </div>
            </div>

            <div className="pt-6 border-t border-ink/10 space-y-4">
                <div className="flex justify-between items-center">
                    <span className="font-semibold text-ink">Overall Readiness</span>
                    <span className="font-bold text-leaf">{state.readinessScore}%</span>
                </div>
                <Progress value={state.readinessScore} label="Application readiness" />
            </div>
        </Card>

        {msg && (
            <div role="status" className="p-4 bg-leaf/10 text-leaf rounded-xl text-center font-medium">
                {msg}
            </div>
        )}

        {/* Action Buttons */}
        <div className="no-print flex flex-wrap gap-4 justify-between items-center pt-4">
            <Button kind="ghost" onClick={() => nav("/assistant")}>
                <ChevronLeft className="w-4 h-4 mr-2" /> Back to Assistant
            </Button>

            <div className="flex flex-wrap gap-3">
                <Button kind="ghost" onClick={() => window.print()}>
                    <Printer className="w-4 h-4 mr-2" /> Print
                </Button>
                <Button kind="cta" className="px-6" onClick={download}>
                    <Download className="w-4 h-4 mr-2" /> Download PDF
                </Button>
                <Button kind="ghost" className="text-terracotta border-terracotta/20 hover:bg-terracotta/5" onClick={async () => {
                    if (confirm("Delete this session and all answers?")) {
                        await sessionService.deleteSession();
                        dispatch({ t: "reset" });
                        nav("/");
                    }
                }}>
                    <Trash2 className="w-4 h-4 mr-2" /> Delete Session
                </Button>
            </div>
        </div>
      </div>
    </Page>
  );
}
