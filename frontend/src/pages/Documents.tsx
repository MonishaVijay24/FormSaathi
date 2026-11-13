import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Badge, Button, Card, Page } from "../components/ui";
import { useApplication } from "../context/ApplicationContext";
import { documentService } from "../services";
import { FileText, CheckCircle2, AlertCircle, ChevronRight, Upload } from "lucide-react";

export default function Documents() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const [busy, setBusy] = useState("");
  const [msg, setMsg] = useState("");

  const needs = state.answers.annual_income && !state.documents.find((d) => d.id === "income")?.uploaded;

  const up = async (id: string) => {
    setBusy(id);
    setMsg("Uploading document...");
    dispatch({ t: "doc", v: await documentService.upload(id) });
    setBusy("");
    setMsg("Document uploaded and verified successfully.");
  };

  return (
    <Page title="Supporting Documents" desc="Review and upload supporting documents required for your application checks.">
      <div className="space-y-8 mt-8">
        {needs && (
          <Card className="bg-saffron/10 border-saffron/30 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
                <AlertCircle className="w-6 h-6 text-saffron flex-shrink-0" />
                <div>
                    <h4 className="font-bold text-ink">Income Certificate Required</h4>
                    <p className="text-sm text-slate">Your application needs an income certificate to verify the annual income you entered.</p>
                </div>
            </div>
            <Button kind="cta" disabled={!!busy} onClick={() => up("income")}>
                Upload Income Certificate
            </Button>
          </Card>
        )}

        {msg && (
            <div role="status" className="p-4 bg-leaf/10 text-leaf rounded-xl font-medium text-center">
                {msg}
            </div>
        )}

        <div className="grid md:grid-cols-2 gap-6">
          {state.documents.map((d) => (
            <Card key={d.id} className="space-y-4 hover:border-leaf/30 transition-all">
              <div className="flex justify-between items-start">
                <div className="flex items-center gap-3">
                    <div className="p-3 bg-leaf/10 rounded-xl text-leaf">
                        <FileText className="w-6 h-6" />
                    </div>
                    <div>
                        <h3 className="font-serif font-bold text-lg">{d.title}</h3>
                        <p className="text-xs text-slate">{["identity", "income"].includes(d.id) ? "Required for verification checks." : "Optional supporting document."}</p>
                    </div>
                </div>
                <Badge t={d.uploaded ? "ok" : "info"}>
                    {d.uploaded ? <CheckCircle2 className="w-4 h-4 mr-1 inline" /> : null}
                    {d.uploaded ? "Uploaded" : "Pending"}
                </Badge>
              </div>

              {d.uploaded && (
                <div className="p-4 bg-parchment/40 rounded-xl space-y-2 text-sm">
                  <p className="font-semibold text-ink truncate">{d.filename}</p>
                  <p className="text-slate text-xs">
                    Extracted Values: {Object.entries(d.values).map(([k, v]) => `${k}: ${v}`).join(", ")}
                  </p>
                  <p className="text-xs text-leaf font-medium">Confidence: {Math.round(d.confidence * 100)}%</p>
                </div>
              )}

              {!d.uploaded && (
                <Button kind="ghost" className="w-full" disabled={!!busy} onClick={() => up(d.id)}>
                    <Upload className="w-4 h-4 mr-2" /> {busy === d.id ? "Uploading..." : "Upload Sample Document"}
                </Button>
              )}
            </Card>
          ))}
        </div>

        <div className="pt-6 flex justify-end">
          <Button kind="cta" className="px-8" onClick={() => nav("/validation")}>
            Run Validation Checks <ChevronRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </div>
    </Page>
  );
}
