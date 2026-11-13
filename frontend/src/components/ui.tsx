import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Link, type LinkProps } from "react-router-dom";
const base = "inline-flex items-center justify-center gap-2 rounded-xl px-6 py-2.5 font-semibold transition active:scale-[0.98] disabled:opacity-50 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-leaf/20";
const kinds = { primary: "bg-leaf text-white hover:bg-leafHover shadow-sm", cta: "bg-[#d49a32] text-ink hover:bg-[#bd8424] shadow-sm", ghost: "border border-leaf/25 text-leaf bg-white hover:bg-leafTint" };
type K = keyof typeof kinds;
export const Button = ({ kind = "primary", className = "", ...p }: ButtonHTMLAttributes<HTMLButtonElement> & { kind?: K }) => <button className={`${base} ${kinds[kind]} ${className}`} {...p} />;
export const LinkButton = ({ kind = "primary", className = "", ...p }: LinkProps & { kind?: K }) => <Link className={`${base} ${kinds[kind]} ${className}`} {...p} />;
export const Card = ({ children, className = "" }: { children: ReactNode; className?: string }) => <section className={`rounded-2xl bg-white p-6 shadow-premium border border-[#e5dfd0] ${className}`}>{children}</section>;
const tone = { ok: "bg-green-100 text-green-900", warn: "bg-amber-100 text-amber-900", bad: "bg-red-100 text-red-900", info: "bg-slate/10 text-slate" };
export const Badge = ({ t = "info", children }: { t?: keyof typeof tone; children: ReactNode }) => <span className={`rounded-full px-3 py-1 text-sm font-semibold ${tone[t]}`}>{children}</span>;
export const Progress = ({ value, label }: { value: number; label: string }) => <div role="progressbar" aria-label={label} aria-valuenow={value} aria-valuemin={0} aria-valuemax={100} className="h-3 w-full rounded-full bg-ink/10"><div className="h-3 rounded-full bg-saffron transition-all" style={{ width: `${value}%` }} /></div>;
export const Page = ({ title, desc, children, loading, error, onRetry }: { title: string; desc: string; children?: ReactNode; loading?: string; error?: string; onRetry?: () => void }) => (
  <div className="space-y-6"><header><p className="eyebrow mb-2">FormSaathi workspace</p><h1 className="page-heading">{title}</h1><p className="text-slate mt-2 max-w-2xl">{desc}</p></header>
    <div aria-live="polite">{loading && <p className="font-semibold text-leaf">{loading}</p>}</div>
    {error && <div role="alert" className="rounded-xl bg-red-50 border border-terracotta p-4 text-red-900">{error} {onRetry && <Button kind="ghost" onClick={onRetry}>Retry</Button>}</div>}
    {children}</div>);
export const Field = ({ id, label, hint, required = true, error, children }: { id: string; label: string; hint: string; required?: boolean; error?: string; children: ReactNode }) => (
  <div className="space-y-1"><label htmlFor={id} className="font-semibold block">{label} <span className="text-sm text-slate">({required ? "required" : "optional"})</span></label>
    <p id={id + "-h"} className="text-sm text-slate">{hint}</p>{children}{error && <p id={id + "-e"} role="alert" className="text-sm text-terracotta font-semibold">{error}</p>}</div>);
export const inputCls = "w-full rounded-xl border border-ink/20 bg-white px-4 py-3 focus:ring-2 focus:ring-leaf/20 focus:border-leaf transition";
