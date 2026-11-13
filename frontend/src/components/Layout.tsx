import React from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { LayoutDashboard, UserCircle, Briefcase, HelpCircle, Languages, LogOut, FileStack } from "lucide-react";
import { useApplication } from "../context/ApplicationContext";
import { sessionService } from "../services";

const SIDEBAR_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/forms", label: "New Application", icon: Briefcase },
  { to: "/profile", label: "My Profile", icon: UserCircle },
  { to: "/documents", label: "Documents", icon: FileStack },
  { to: "/support", label: "Help & Support", icon: HelpCircle },
];

const STEPS = [
  { path: "/profile", label: "Profile", num: 1 },
  { path: "/forms", label: "Form", num: 2 },
  { path: "/answer", label: "Answer", num: 3 },
  { path: "/validation", label: "Verify", num: 4 },
  { path: "/preview", label: "Download", num: 5 },
];

export function Stepper() {
  const location = useLocation();
  const currentPath = location.pathname;

  const getStepStatus = (path: string, num: number) => {
    // Determine active or completed based on path matching
    const order = ["/profile", "/forms", "/upload", "/extraction", "/answer", "/documents", "/validation", "/verify", "/preview"];
    const currentIndex = order.findIndex(p => currentPath.includes(p) || currentPath === p);
    const stepIndex = order.findIndex(p => p === path || (num === 2 && (path === "/forms" && (currentPath.includes("upload") || currentPath.includes("review")))));

    if (currentIndex > stepIndex) return "completed";
    if (currentIndex === stepIndex || (num === 2 && currentPath.includes("upload"))) return "current";
    return "upcoming";
  };

  return (
    <div className="bg-white rounded-2xl border border-[#e5dfd0] shadow-soft p-3 md:p-4 mb-6 flex items-center justify-between overflow-x-auto">
      {STEPS.map((s, idx) => {
        const status = getStepStatus(s.path, s.num);
        return (
          <div key={s.path} className="flex items-center gap-3">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
              status === "completed" ? "bg-leaf text-white" :
              status === "current" ? "bg-leaf text-white ring-4 ring-leafTint" :
              "bg-[#f3eddd] text-textSecondary"
            }`}>
              {status === "completed" ? "✓" : s.num}
            </div>
            <span className={`text-sm font-semibold whitespace-nowrap ${status === "current" ? "text-leaf font-bold" : "text-textSecondary"}`}>
              {s.label}
            </span>
            {idx < STEPS.length - 1 && <div className="hidden sm:block w-8 md:w-16 h-px bg-[#e5dfd0]" />}
          </div>
        );
      })}
    </div>
  );
}

export function Layout({ children }: { children: React.ReactNode }) {
  const { state, dispatch } = useApplication();
  const [resetModal, setResetModal] = React.useState(false);
  const nav = useNavigate();

  return (
    <div className="min-h-screen flex bg-transparent">
      {/* Sidebar */}
      <aside className="no-print w-56 bg-leaf text-white flex flex-col fixed inset-y-0 left-0 z-50 max-md:w-[72px]">
        <div className="p-5 flex items-center gap-3 max-md:justify-center">
          <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center text-leaf font-serif font-bold text-xl shadow-soft">
            FS
          </div>
          <span className="font-serif text-xl font-bold text-white max-md:hidden">FormSaathi <span className="text-amber">AI</span></span>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          <div className="text-xs font-bold text-white/60 uppercase tracking-wider px-3 mb-2 max-md:hidden">Navigation</div>
          {SIDEBAR_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${
                isActive ? "bg-leafTint text-leaf font-bold" : "text-white/80 hover:bg-white/10"
                }`
              }
            >
              <item.icon className="w-5 h-5" />
              <span className="max-md:hidden">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="p-3 m-3 bg-white/10 rounded-2xl border border-white/20 space-y-3 max-md:hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white/70">LANGUAGE</span>
            <Languages className="w-4 h-4 text-amber" />
          </div>
          <div className="flex gap-2">
            {(["en", "kn"] as const).map((l) => (
              <button
                key={l}
                onClick={() => dispatch({ t: "lang", v: l })}
                className={`flex-1 py-1.5 text-xs rounded-lg font-bold transition-all ${
                  state.language === l ? "bg-white text-leaf" : "bg-transparent border border-white/30 text-white"
                }`}
              >
                {l === "kn" ? "ಕನ್ನಡ" : "English"}
              </button>
            ))}
          </div>
          <button
            onClick={() => setResetModal(true)}
            className="w-full text-xs text-red-200 font-semibold py-2 rounded-lg hover:bg-white/10 transition-all flex items-center justify-center gap-1"
          >
            <LogOut className="w-3.5 h-3.5" /> Reset Session
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-56 max-md:ml-[72px] p-5 md:p-8 lg:p-12 max-w-[1500px] min-w-0">
        <Stepper />
        <div className="bg-white/80 rounded-2xl border border-[#e5dfd0] shadow-soft p-5 md:p-8 lg:p-10">
          {children}
          <div className="mt-10 border-t border-[#e5dfd0] pt-4 text-center text-xs text-textSecondary">
            AI reads and explains. Rules decide. You confirm. <span className="font-bold text-terracotta">SAMPLE — FICTIONAL DATA. Draft only; not submitted or approved.</span>
          </div>
        </div>
      </main>
      <nav className="no-print fixed inset-x-0 bottom-0 z-40 hidden justify-around border-t border-[#e5dfd0] bg-white/95 p-2 backdrop-blur max-md:flex">
        {SIDEBAR_ITEMS.slice(0, 4).map((item) => <NavLink key={item.to} to={item.to} aria-label={item.label} className={({ isActive }) => `grid min-h-11 min-w-14 place-items-center rounded-xl text-[10px] ${isActive ? "bg-leafTint text-leaf" : "text-textSecondary"}`}><item.icon className="h-5 w-5" /></NavLink>)}
      </nav>

      {resetModal && (
        <div className="fixed inset-0 bg-ink/40 backdrop-blur-sm grid place-items-center p-4 z-50">
          <div className="bg-white rounded-[16px] p-6 max-w-sm w-full space-y-4 shadow-soft border border-[#EADFC4]">
            <h3 className="text-xl font-bold font-serif text-ink">Reset Session?</h3>
            <p className="text-textSecondary text-sm">This will clear all your progress and demo answers.</p>
            <div className="flex gap-3">
              <button
                className="flex-1 bg-error text-white font-bold py-2 rounded-xl"
                onClick={async () => {
                  await sessionService.deleteSession();
                  dispatch({ t: "reset" });
                  setResetModal(false);
                  nav("/");
                }}
              >
                Reset
              </button>
              <button className="flex-1 bg-cream text-ink font-bold py-2 rounded-xl" onClick={() => setResetModal(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
