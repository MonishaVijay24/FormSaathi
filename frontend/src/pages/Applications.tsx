import { useNavigate } from "react-router-dom";
import { Landmark, GraduationCap, ArrowRight, BookOpen } from "lucide-react";
import { useApplication } from "../context/ApplicationContext";
import type { FormType } from "../types";

const apps: Array<{
  id: FormType;
  Icon: typeof Landmark;
  name: string;
  desc: string;
  req: string;
  color: "leaf" | "saffron";
}> = [
  {
    id: "bank",
    Icon: Landmark,
    name: "Bank Account Opening",
    desc: "8–12 fields for personal, address & bank details.",
    req: "Identity document, income proof.",
    color: "leaf"
  },
  {
    id: "pension",
    Icon: GraduationCap,
    name: "Sandhya Suraksha Yojane",
    desc: "Senior citizen pension application (demo).",
    req: "Aadhaar, income certificate, passbook.",
    color: "saffron"
  }
];

export default function Applications() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Start something important</p>
        <h1 className="page-heading mt-2">Choose an application</h1>
        <p className="text-textSecondary mt-2">Select a form and we’ll guide you through each step, in your language.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {apps.map((app) => (
          <div key={app.id} className="card-base flex flex-col border-2 border-transparent hover:-translate-y-1 hover:border-leaf/30 transition-all group">
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-6 ${app.color === 'leaf' ? 'bg-leafTint text-leaf' : 'bg-amberTint text-saffron'}`}>
              <app.Icon className="w-7 h-7" />
            </div>
            <div className="mb-2 flex items-start justify-between gap-3"><h2 className="font-serif text-2xl font-bold text-ink">{app.name}</h2><span className="rounded-full bg-[#f7f3e8] px-2.5 py-1 text-[10px] font-bold text-textSecondary">POPULAR</span></div>
            <p className="text-textSecondary text-sm mb-4">{app.desc}</p>

            <div className="bg-cream p-4 rounded-xl mb-6 border border-[#EADFC4]">
                <p className="text-xs font-bold text-textSecondary uppercase tracking-wider mb-2">Requirements</p>
                <p className="text-sm font-medium text-ink">{app.req}</p>
            </div>

            <button
              className={`mt-auto ${app.color === 'leaf' ? 'btn-primary' : 'btn-accent'} w-full justify-center`}
              onClick={() => { dispatch({ t: "form", v: app.id }); nav("/upload"); }}
            >
              Select This Form <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>

      <div className="card-base flex items-center justify-between mt-8">
        <div className="flex items-center gap-4">
            <div className="p-3 bg-leafTint rounded-xl text-leaf">
                <BookOpen className="w-6 h-6" />
            </div>
            <div>
                <h3 className="font-bold text-ink">Need help choosing?</h3>
                <p className="text-sm text-textSecondary">View our guide on which application fits your requirements.</p>
            </div>
        </div>
        <button className="btn-secondary">Read guide <ArrowRight className="h-4 w-4" /></button>
      </div>
    </div>
  );
}
