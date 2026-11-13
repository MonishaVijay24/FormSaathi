import { useNavigate } from "react-router-dom";
import { ArrowRight, CheckCircle, FileCheck2, Globe2, Landmark, Mic, ShieldCheck, UploadCloud, Volume2 } from "lucide-react";
import { useApplication } from "../context/ApplicationContext";
import GlareHover from "../components/react-bits/GlareHover/GlareHover";

const steps = [
  { icon: UploadCloud, title: "Upload once", desc: "Keep your documents together and let us read the form." },
  { icon: Volume2, title: "Understand clearly", desc: "Get every question explained in English or Kannada." },
  { icon: Mic, title: "Answer naturally", desc: "Speak or type at your own pace, with guidance throughout." },
  { icon: FileCheck2, title: "Check before submitting", desc: "Spot missing information before you download." },
];

export default function Landing() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const start = () => { dispatch({ t: "start" }); nav("/profile"); };

  return (
    <div className="min-h-screen bg-[#f7f3e8] text-ink">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 md:px-10">
        <div className="flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-xl bg-leaf text-xl font-bold text-white shadow-soft">FS</div>
          <div><p className="font-serif text-xl font-bold leading-none">FormSaathi <span className="text-saffron">AI</span></p><p className="mt-1 text-[10px] font-bold uppercase tracking-[.18em] text-textSecondary">Your form companion</p></div>
        </div>
        <div className="hidden items-center gap-8 text-sm font-bold text-textSecondary md:flex">
          <a className="text-leaf" href="#home">Home</a><a className="hover:text-leaf" href="#how">How it works</a><a className="hover:text-leaf" href="#trust">Trust & access</a>
        </div>
        <div className="flex items-center gap-2">
          <select value={state.language} onChange={(e) => dispatch({ t: "lang", v: e.target.value as "en" | "kn" })} aria-label="Language selector" className="hidden rounded-xl border border-[#ded7c7] bg-white px-3 py-2 text-sm font-bold sm:block">
            <option value="en">English</option><option value="kn">ಕನ್ನಡ</option>
          </select>
          <button onClick={start} className="btn-primary !px-4 !py-2.5 text-sm">Get started <ArrowRight className="h-4 w-4" /></button>
        </div>
      </nav>

      <main id="home" className="mx-auto max-w-7xl px-5 pb-20 pt-10 md:px-10 md:pt-20">
        <section className="grid items-center gap-12 lg:grid-cols-[1.05fr_.95fr]">
          <div>
            <div className="eyebrow mb-5 flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-[#d49a32]" /> A simpler way to apply</div>
            <h1 className="max-w-3xl font-serif text-5xl font-bold leading-[1.05] tracking-tight md:text-7xl">Government forms, <span className="text-leaf">made human.</span></h1>
            <p className="mt-6 max-w-xl text-lg leading-8 text-textSecondary">FormSaathi helps you complete applications with confidence — in your language, with your documents and a helpful voice guide by your side.</p>
            <div className="mt-8 flex flex-wrap items-center gap-4"><button onClick={start} className="btn-primary !px-7 !py-4 text-base">Start application <ArrowRight className="h-5 w-5" /></button><a href="#how" className="font-bold text-leaf underline decoration-leaf/30 underline-offset-8">See how it works</a></div>
            <div className="mt-8 flex flex-wrap gap-5 text-sm font-semibold text-textSecondary"><span className="flex items-center gap-2"><ShieldCheck className="h-4 w-4 text-leaf" /> Private by design</span><span className="flex items-center gap-2"><Globe2 className="h-4 w-4 text-leaf" /> English + ಕನ್ನಡ</span></div>
          </div>
          <GlareHover width="100%" height="auto" background="#ffffff" borderRadius="24px" borderColor="#e5dfd0" glareColor="#e3f1df" glareOpacity={0.28} className="w-full shadow-premium">
            <div className="soft-grid w-full rounded-[24px] p-5 md:p-8">
              <div className="flex items-center justify-between"><div className="flex items-center gap-3"><div className="grid h-12 w-12 place-items-center rounded-2xl bg-leafTint text-leaf"><Landmark /></div><div><h2 className="font-serif text-xl font-bold">Bank account opening</h2><p className="text-sm text-textSecondary">Guided application</p></div></div><span className="rounded-full bg-leafTint px-3 py-1 text-xs font-bold text-leaf">Ready</span></div>
              <div className="mt-8 rounded-2xl border border-[#e5dfd0] bg-[#fbf8ef] p-5"><p className="text-sm font-bold text-leaf">Question 3 of 8</p><p className="mt-3 font-serif text-2xl font-bold">What is your annual income?</p><p className="mt-2 text-sm text-textSecondary">ನಿಮ್ಮ ವಾರ್ಷಿಕ ಆದಾಯ ಎಷ್ಟು?</p></div>
              <div className="flex items-center justify-center py-8"><div className="relative grid h-28 w-28 place-items-center rounded-full bg-leaf text-white shadow-[0_12px_30px_rgba(31,91,46,.24)]"><span className="absolute inset-2 rounded-full border border-white/30" /><Mic className="h-10 w-10" /></div></div>
              <div className="flex items-center justify-between border-t border-[#e5dfd0] pt-4 text-xs font-semibold text-textSecondary"><span>Progress 38%</span><span className="text-leaf">Your answers stay yours</span></div>
            </div>
          </GlareHover>
        </section>

        <section id="how" className="mt-28"><div className="mb-9 max-w-xl"><p className="eyebrow">A guided journey</p><h2 className="mt-2 font-serif text-4xl font-bold">From first upload to final download.</h2></div><div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{steps.map((step, index) => <div key={step.title} className="card-base group"><div className="mb-7 flex items-center justify-between"><div className="grid h-12 w-12 place-items-center rounded-2xl bg-leafTint text-leaf"><step.icon /></div><span className="font-serif text-3xl font-bold text-[#d9e7d2]">0{index + 1}</span></div><h3 className="font-serif text-xl font-bold">{step.title}</h3><p className="mt-2 text-sm leading-6 text-textSecondary">{step.desc}</p></div>)}</div></section>
        <section id="trust" className="mt-20 grid gap-5 rounded-2xl bg-leaf p-6 text-white md:grid-cols-[1fr_auto] md:items-center md:p-10"><div><p className="eyebrow !text-[#d9e7d2]">Designed for real life</p><h2 className="mt-2 font-serif text-3xl font-bold">No jargon. No guesswork. No rushing.</h2><p className="mt-3 max-w-2xl text-sm leading-6 text-white/75">Large, readable screens, voice-first support and clear checks help you complete important applications with dignity.</p></div><CheckCircle className="hidden h-20 w-20 text-[#d49a32] md:block" /></section>
      </main>
    </div>
  );
}
