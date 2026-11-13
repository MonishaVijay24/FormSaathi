import { ArrowRight, Bell, BriefcaseBusiness, CheckCircle2, ChevronRight, Clock3, Headphones, Languages, Plus, ShieldCheck } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Card, Button } from "../components/ui";
import { useApplication } from "../context/ApplicationContext";

const recent = [
  { title: "Bank Account Opening Form", date: "Today", status: "In progress", progress: 60, tone: "bg-[#d49a32]" },
  { title: "Pension Application", date: "Yesterday", status: "Draft", progress: 30, tone: "bg-[#bd684e]" },
  { title: "Bank Account Opening", date: "12 Jun 2024", status: "Completed", progress: 100, tone: "bg-[#2e9d57]" },
];

export default function Dashboard() {
  const nav = useNavigate();
  const { dispatch } = useApplication();
  const start = () => { dispatch({ t: "start" }); nav("/profile"); };

  return (
    <div className="space-y-8">
      <header className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div><p className="eyebrow">Good morning, Ananya</p><h1 className="page-heading mt-2">Welcome to FormSaathi!</h1><p className="mt-2 max-w-2xl text-textSecondary">Fill government and banking application forms easily, with voice support in your language.</p></div>
        <button aria-label="Notifications" className="hidden h-11 w-11 place-items-center rounded-xl border border-[#e5dfd0] bg-white text-leaf md:grid"><Bell className="h-5 w-5" /><span className="absolute ml-5 mt-[-18px] h-2 w-2 rounded-full bg-[#bd684e]" /></button>
      </header>

      <section className="relative overflow-hidden rounded-2xl bg-[#d49a32] p-6 text-ink shadow-soft md:p-8">
        <div className="relative z-10 max-w-2xl"><p className="text-xs font-bold uppercase tracking-[.18em] text-ink/60">Ready when you are</p><h2 className="mt-2 font-serif text-3xl font-bold">Start a new application</h2><p className="mt-2 max-w-lg text-sm leading-6 text-ink/75">Upload a form and begin with calm, step-by-step voice guidance. This demo uses fictional data only.</p><Button onClick={start} className="mt-6 !bg-forest !text-white hover:!bg-leaf"><Plus className="h-4 w-4" /> Start application <ArrowRight className="h-4 w-4" /></Button></div>
        <div className="absolute -right-10 -top-20 h-64 w-64 rounded-full border-[34px] border-white/20" /><div className="absolute -bottom-28 right-20 h-56 w-56 rounded-full border-[22px] border-white/15" />
      </section>

      <div className="grid gap-8 xl:grid-cols-[1fr_320px]">
        <section><div className="mb-4 flex items-center justify-between"><div><p className="eyebrow">Your workspace</p><h2 className="mt-1 font-serif text-2xl font-bold">Recent applications</h2></div><button onClick={() => nav("/forms")} className="flex items-center gap-1 text-sm font-bold text-leaf">View all <ChevronRight className="h-4 w-4" /></button></div><div className="space-y-3">{recent.map((item) => <Card key={item.title + item.date} className="flex flex-col gap-4 !p-4 sm:flex-row sm:items-center"><div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-leafTint text-leaf"><BriefcaseBusiness className="h-5 w-5" /></div><div className="min-w-0 flex-1"><div className="flex flex-wrap items-center gap-2"><h3 className="font-bold">{item.title}</h3><span className={`rounded-full px-2.5 py-1 text-xs font-bold text-ink ${item.tone}/20`}>{item.status}</span></div><p className="mt-1 flex items-center gap-1 text-xs text-textSecondary"><Clock3 className="h-3 w-3" /> {item.date}</p></div><div className="w-full sm:w-36"><div className="mb-1 flex justify-between text-xs font-bold text-textSecondary"><span>Progress</span><span>{item.progress}%</span></div><div className="h-2 rounded-full bg-[#eee8d9]"><div className="h-2 rounded-full bg-leaf" style={{ width: `${item.progress}%` }} /></div></div><ChevronRight className="hidden h-5 w-5 text-textSecondary sm:block" /></Card>)}</div></section>
        <aside className="space-y-4"><Card className="bg-forest text-white"><Headphones className="h-7 w-7 text-[#d49a32]" /><h3 className="mt-5 font-serif text-xl font-bold">Need help?</h3><p className="mt-2 text-sm leading-6 text-white/70">Talk to FormSaathi AI for guidance anytime.</p><button onClick={() => nav("/answer")} className="mt-5 flex min-h-11 w-full items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-bold text-forest">Start voice help <ArrowRight className="h-4 w-4" /></button></Card><Card><div className="flex items-center gap-3"><Languages className="h-5 w-5 text-leaf" /><h3 className="font-bold">Supported languages</h3></div><div className="mt-4 space-y-3 text-sm text-textSecondary"><p>ಕನ್ನಡ <span className="float-right rounded-full bg-leafTint px-2 py-0.5 text-xs font-bold text-leaf">Available</span></p><p>English <span className="float-right rounded-full bg-leafTint px-2 py-0.5 text-xs font-bold text-leaf">Available</span></p><p>हिन्दी <span className="float-right rounded-full bg-[#f7f3e8] px-2 py-0.5 text-xs font-bold">Soon</span></p></div></Card><div className="flex gap-3 rounded-2xl border border-[#e5dfd0] bg-[#fbf8ef] p-4 text-sm text-textSecondary"><ShieldCheck className="h-5 w-5 shrink-0 text-leaf" /><span>AI reads and explains. Rules decide. You confirm.</span></div></aside>
      </div>
    </div>
  );
}
