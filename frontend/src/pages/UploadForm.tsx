import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { UploadCloud, FileText, CheckCircle, AlertTriangle, ArrowRight } from "lucide-react";
import { useApplication } from "../context/ApplicationContext";
import { formService } from "../services";

const OK = ["application/pdf", "image/jpeg", "image/png"];
const MAX = 10 * 1024 * 1024;

export default function UploadForm() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const inp = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const pick = (f?: File) => {
    setErr("");
    if (!f) return;
    if (!OK.includes(f.type)) return setErr("Please upload a PDF, JPG, or PNG file.");
    if (f.size > MAX) return setErr("File is too large (max 10MB).");
    setFile(f);
  };

  const run = async (sample: boolean) => {
    setBusy(true);
    setErr("");
    try {
      const fields = await formService.analyzeForm(sample ? null : file, () => {}, state.selectedForm ?? "bank");
      dispatch({ t: "fields", v: fields });
      setBusy(false);
      nav("/extraction");
    } catch (e) {
      setErr((e as Error).message);
      setBusy(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Step 2 · Form document</p>
        <h1 className="page-heading mt-2">Upload your form</h1>
        <p className="text-textSecondary mt-2">Add a clear PDF or image. We’ll read the fields and turn them into simple questions.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-6">
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => { e.preventDefault(); pick(e.dataTransfer.files[0]); }}
            className="soft-grid border-2 border-dashed border-leaf/25 rounded-2xl p-12 text-center bg-[#fbf8ef] hover:bg-white hover:border-leaf transition-all cursor-pointer"
            onClick={() => inp.current?.click()}
          >
            <div className="mx-auto mb-4 grid h-16 w-16 place-items-center rounded-2xl bg-leafTint text-leaf"><UploadCloud className="w-8 h-8" /></div>
            <h3 className="font-serif font-bold text-xl text-ink">Drag & drop your file here</h3>
            <p className="text-textSecondary mt-2">or click to upload from your device</p>
            <input ref={inp} type="file" accept=".pdf,.jpg,.jpeg,.png" className="sr-only" onChange={(e) => pick(e.target.files?.[0])} />
          </div>

          {file && (
            <div className="flex items-center justify-between p-4 bg-white rounded-2xl border border-leaf shadow-soft">
              <div className="flex items-center gap-3">
                <FileText className="text-leaf" />
                <span className="font-bold text-ink">{file.name}</span>
                <span className="text-xs text-textSecondary">{Math.round(file.size / 1024)} KB</span>
              </div>
              <button onClick={() => setFile(null)} className="text-error font-bold text-sm">Change</button>
            </div>
          )}
        </div>

        <div className="space-y-6">
          <div className="card-base border-leaf/20 bg-leafTint/60">
            <h3 className="font-serif font-bold text-lg mb-2">Need a sample?</h3>
            <p className="text-sm text-textSecondary mb-6">Use a demo bank form to try the experience.</p>
            <button className="btn-secondary w-full" onClick={() => run(true)} disabled={busy}>
              Use Sample Form
            </button>
          </div>

          <button
            className="btn-primary w-full"
            onClick={() => run(false)}
            disabled={!file || busy}
          >
            {busy ? "Analyzing..." : "Analyze File"} <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {err && (
        <div className="p-4 bg-errorTint text-error rounded-xl flex items-center gap-2 font-bold">
          <AlertTriangle className="w-5 h-5" /> {err}
        </div>
      )}
    </div>
  );
}
