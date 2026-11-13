import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Keyboard, Mic, RotateCcw, Volume2, MicOff, CheckCircle2, ChevronRight, Languages } from "lucide-react";
import { Button, Card, Field, inputCls, Page, Progress } from "../components/ui";
import { useApplication } from "../context/ApplicationContext";
import { useSpeech } from "../hooks/useSpeech";
import type { FormField } from "../types";

const SAMPLE: Record<string, string> = { applicant_name: "Ananya R.", dob: "15/04/2002", mobile: "9876543210", address_permanent: "Sample address, Bengaluru", occupation: "Student", annual_income: "180000", account_number: "123456789012", ifsc: "DEMO0001234" };

export default function Assistant() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const l = state.language;
  const fields = state.fields;
  const idx = fields.findIndex((f) => !state.answers[f.field_id]?.confirmed);
  const f: FormField | undefined = fields[idx];

  const [val, setVal] = useState("");
  const [tr, setTr] = useState("");
  const [typing, setTyping] = useState(false);
  const [err, setErr] = useState("");
  const [note, setNote] = useState("");

  const sp = useSpeech(l, (t) => {
    setTr(t);
    setVal(t);
    setNote("Voice captured. Please verify your response.");
  });

  useEffect(() => {
    setVal(""); setTr(""); setTyping(false); setErr(""); setNote("");
  }, [f?.field_id]);

  if (!fields.length) return <Page title="No questions yet" desc="Upload a form first."><Button onClick={() => nav("/upload")}>Go to upload</Button></Page>;

  if (!f) return (
    <Page title="Ready to Proceed" desc="Great! You've answered all the questions.">
        <Card className="text-center py-12 space-y-6">
            <div className="w-20 h-20 bg-leaf/10 rounded-full flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-10 h-10 text-leaf" />
            </div>
            <div className="space-y-2">
                <h3 className="text-2xl font-serif font-bold">Questionnaire Complete</h3>
                <p className="text-slate">All required information has been captured successfully.</p>
            </div>
            <Button kind="cta" className="px-8" onClick={() => nav("/documents")}>
                Proceed to Documents <ChevronRight className="w-4 h-4" />
            </Button>
        </Card>
    </Page>
  );

  const confirm = () => {
    if (f.required && !val.trim()) return setErr("Please provide an answer before confirming.");
    if (f.digits && !/^\d+$/.test(val.trim())) return setErr("Please use numbers only.");
    dispatch({ t: "answer", v: { field_id: f.field_id, value: val.trim(), transcript: tr || undefined, source: tr ? "voice" : "text", confirmed: true } });
    setNote("Answer confirmed.");
  };

  const q = f.label_simple[l];

  return (
    <Page title="Your voice, your answer" desc="Answer naturally in English or Kannada. Use the microphone or type your response.">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
                <span className="text-xs font-bold text-leaf uppercase tracking-widest">Question {idx + 1} of {fields.length}</span>
                <p className="text-sm text-slate font-medium">{f.group}</p>
            </div>
            <div className="w-full md:w-48">
                <Progress value={Math.round((idx / fields.length) * 100)} label="Overall progress" />
            </div>
        </div>

        <Card className="p-8 border-leaf/20 bg-leafTint/40">
            <div className="flex justify-between items-start mb-6">
                <h2 lang={l} className="text-3xl font-serif font-bold text-ink leading-tight">{q}</h2>
                <Button kind="ghost" className="rounded-full w-12 h-12 p-0 flex-shrink-0" onClick={() => sp.speak(q)}>
                    <Volume2 className="w-5 h-5" />
                </Button>
            </div>
            <p className="text-lg text-slate italic">
                {l === "kn" ? f.label_simple.en : f.label_simple.kn}
            </p>
        </Card>

        <Card className="p-10 space-y-8 text-center bg-white shadow-premium border-2 border-leaf/10">
          {!f.digits && (
            <div className="space-y-6">
                <div className="relative inline-block">
                    {sp.listening && (
                        <div className="absolute inset-0 animate-ping rounded-full bg-leaf/20 scale-150"></div>
                    )}
                    <button
                        aria-label={sp.listening ? "Stop listening" : "Tap to speak"}
                        onClick={sp.supported ? (sp.listening ? sp.stop : sp.start) : () => setNote("Speech recognition not supported in this browser.")}
                        className={`relative z-10 w-32 h-32 rounded-full transition-all duration-300 flex items-center justify-center ${
                            sp.listening ? "bg-saffron text-ink scale-110 shadow-xl" : "bg-leaf text-white hover:bg-ink shadow-lg"
                        }`}
                    >
                        {sp.listening ? <MicOff className="w-10 h-10" /> : <Mic className="w-10 h-10" />}
                    </button>
                </div>

                <div className="space-y-2">
                    <p className={`text-xl font-bold ${sp.listening ? "text-saffron animate-pulse" : "text-ink"}`}>
                        {sp.listening ? "Listening..." : "Tap and Speak"}
                    </p>
                    <p className="text-sm text-slate">You can speak in {l === "kn" ? "Kannada" : "English"}</p>
                </div>

                <div className="flex justify-center gap-2">
                    <Button kind="ghost" className="text-xs" onClick={() => { const t = SAMPLE[f.field_id] ?? ""; setTr(t); setVal(t); setNote("Sample data added."); }}>
                        Use Sample Data (Demo)
                    </Button>
                </div>
            </div>
          )}

          {f.digits && (
            <div className="space-y-6">
                <Keypad value={val} onChange={setVal} masked={f.sensitive} />
            </div>
          )}

          {(typing || tr || f.digits) && (
            <div className="max-w-md mx-auto space-y-4 pt-4 border-t border-parchment">
                <Field id="ans" label="Your Response" hint={tr ? "Verify the transcription and edit if needed." : "Enter your answer manually."} error={err}>
                    <input
                        id="ans"
                        className={`${inputCls} text-lg text-center font-semibold bg-leaf/5 border-leaf/10`}
                        value={val}
                        onChange={(e) => setVal(e.target.value)}
                        autoFocus
                    />
                </Field>
                <div className="flex gap-3">
                    <Button className="flex-1 px-8 py-4" onClick={confirm}>Confirm Answer</Button>
                    <Button kind="ghost" className="flex-1" onClick={() => { setVal(""); setTr(""); setTyping(false); }}>
                        <RotateCcw className="w-4 h-4 mr-2" /> Clear
                    </Button>
                </div>
            </div>
          )}

          {!(typing || tr || f.digits) && (
              <Button kind="ghost" className="mx-auto" onClick={() => setTyping(true)}>
                  <Keyboard className="w-4 h-4 mr-2" /> Type Instead
              </Button>
          )}

          {(sp.error || note) && (
            <p role="status" className={`text-sm font-semibold px-4 py-2 rounded-lg inline-block ${sp.error ? "bg-terracotta/10 text-terracotta" : "bg-leaf/10 text-leaf"}`}>
                {sp.error || note}
            </p>
          )}
        </Card>
      </div>
    </Page>
  );
}

function Keypad({ value, onChange, masked }: { value: string; onChange: (v: string) => void; masked: boolean }) {
  return (
    <div className="space-y-6">
        <div className="bg-ink/5 py-4 px-6 rounded-2xl min-h-[4rem] flex items-center justify-center">
            <p aria-live="polite" className="text-3xl font-bold tracking-widest text-ink">
                {value ? (masked ? "•".repeat(Math.max(0, value.length - 4)) + value.slice(-4) : value) : <span className="text-ink/20 tracking-normal font-medium">Enter digits</span>}
            </p>
        </div>
        <div className="grid grid-cols-3 gap-3 max-w-xs mx-auto" role="group" aria-label="Numeric keypad">
            {["1","2","3","4","5","6","7","8","9","⌫","0","C"].map((k) => (
                <button
                    key={k}
                    aria-label={k === "⌫" ? "Delete last digit" : k === "C" ? "Clear all" : k}
                    className="h-16 rounded-xl bg-white border border-ink/10 shadow-sm text-xl font-bold text-ink hover:bg-leaf hover:text-white hover:border-leaf transition-all active:scale-95"
                    onClick={() => onChange(k === "⌫" ? value.slice(0, -1) : k === "C" ? "" : value + k)}
                >
                    {k}
                </button>
            ))}
        </div>
    </div>
  );
}
