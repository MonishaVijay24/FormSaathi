import { useRef, useState } from "react";
interface Rec { lang: string; interimResults: boolean; onresult: ((e: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void) | null; onerror: (() => void) | null; onend: (() => void) | null; start(): void; stop(): void; }
type RecCtor = new () => Rec;
const w = window as unknown as { SpeechRecognition?: RecCtor; webkitSpeechRecognition?: RecCtor };
const Ctor = w.SpeechRecognition ?? w.webkitSpeechRecognition;
export function useSpeech(lang: "en" | "kn", onText: (t: string) => void) {
  const [listening, setListening] = useState(false);
  const [error, setError] = useState("");
  const ref = useRef<Rec | null>(null);
  const start = () => {
    if (!Ctor) return;
    const r = new Ctor(); r.lang = lang === "kn" ? "kn-IN" : "en-IN"; r.interimResults = false;
    r.onresult = (e) => onText(e.results[0][0].transcript);
    r.onerror = () => { setError("Speech was not recognised. Please type your answer."); setListening(false); };
    r.onend = () => setListening(false);
    ref.current = r; setError(""); setListening(true); r.start();
  };
  const speak = (text: string) => { if ("speechSynthesis" in window) { const u = new SpeechSynthesisUtterance(text); u.lang = lang === "kn" ? "kn-IN" : "en-IN"; speechSynthesis.cancel(); speechSynthesis.speak(u); } };
  return { supported: !!Ctor, listening, error, start, stop: () => ref.current?.stop(), speak };
}
