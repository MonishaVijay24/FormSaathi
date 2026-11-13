import { useNavigate } from "react-router-dom";
import { Badge, Button, Card, Page, inputCls } from "../components/ui";
import { useApplication } from "../context/ApplicationContext";
import { CheckCircle2, AlertTriangle, Settings2, ArrowRight } from "lucide-react";

export default function Extraction() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const l = state.language;

  if (!state.fields.length) return <Page title="No fields detected" desc="Please upload a form document first."><Button onClick={() => nav("/upload")}>Go to upload</Button></Page>;

  return (
    <Page title="Review Extracted Fields" desc="Verify the information we've identified from your document. Correct any details if needed.">
      <div className="grid lg:grid-cols-[350px,1fr] gap-8 mt-8">
        <div className="space-y-6">
            <Card className="sticky top-24 border-leaf/20">
                <h3 className="font-serif font-bold text-lg mb-4">Summary</h3>
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <span className="text-slate text-sm">Total Fields</span>
                        <span className="font-bold">{state.fields.length}</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-slate text-sm">High Confidence</span>
                        <Badge t="ok">{state.fields.filter(f => f.confidence > 0.9).length}</Badge>
                    </div>
                </div>
            </Card>
        </div>

        <div className="space-y-6">
          {state.fields.map((f) => (
            <Card key={f.field_id} className="border-leaf/10 hover:border-leaf/30 transition-colors">
              <div className="flex justify-between items-start mb-4">
                <div>
                    <h4 className="font-semibold text-ink">{f.label_original}</h4>
                    <p className="text-sm text-leaf font-medium mt-1">{f.label_simple[l]}</p>
                </div>
                <Badge t={f.confidence > 0.9 ? "ok" : "warn"}>
                    {f.confidence > 0.9 ? <CheckCircle2 className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
                </Badge>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-1">
                    <label className="text-xs font-semibold text-slate uppercase">Type</label>
                    <select
                        className={inputCls}
                        value={f.data_type}
                        onChange={(e) => dispatch({ t: "field", id: f.field_id, patch: { data_type: e.target.value as typeof f.data_type } })}
                    >
                        {["text", "number", "date", "select", "address"].map((t) => <option key={t} value={t}>{t}</option>)}
                    </select>
                </div>
                <div className="flex items-end pb-2">
                    <label className="flex items-center gap-2 cursor-pointer font-medium">
                        <input
                            type="checkbox"
                            className="w-4 h-4 accent-leaf"
                            checked={f.required}
                            onChange={(e) => dispatch({ t: "field", id: f.field_id, patch: { required: e.target.checked } })}
                        />
                        Required Field
                    </label>
                </div>
              </div>
            </Card>
          ))}

          <div className="pt-6 flex justify-end">
            <Button kind="cta" className="px-8" onClick={() => nav("/assistant")}>
                Looks Correct, Start Filling <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </Page>
  );
}
