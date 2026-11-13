import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CheckCircle, UploadCloud, Edit3, ArrowRight, FileText, ShieldCheck, LoaderCircle } from "lucide-react";
import { useApplication } from "../context/ApplicationContext";
import { profileService } from "../services";

export default function Profile() {
  const { state, dispatch } = useApplication();
  const nav = useNavigate();
  const [editingKey, setEditingKey] = useState<string | null>(null);
  const [editValues, setEditValues] = useState<Record<string, string>>({});
  const [consent, setConsent] = useState(false);
  const [processing, setProcessing] = useState<string | null>(null);
  const [status, setStatus] = useState("");

  const docs = [
    { id: "aadhaar", name: "Aadhaar", tag: "(Required)", uploaded: true },
    { id: "marks", name: "Marks Card", tag: "(Optional)", uploaded: false },
    { id: "income", name: "Income Certificate", tag: "(Optional)", uploaded: false },
    { id: "bank", name: "Bank Passbook", tag: "(Optional)", uploaded: false },
  ];

  const useSample = async (id: string) => {
    if (!consent) {
      setStatus("Please confirm the consent checkbox before using a sample document.");
      return;
    }
    setProcessing(id);
    setStatus("Reading page 1 of 1… Identifying fields… Checking details…");
    const extracted = await profileService.extract();
    dispatch({ t: "profile", v: extracted });
    setProcessing(null);
    setStatus("Sample document processed. Please review and confirm each value.");
  };

  const profileFields = [
    { key: "name", label: "Full Name", value: "Ananya Rao", confirmed: true },
    { key: "dob", label: "Date of Birth", value: "15 Apr 2002", confirmed: true },
    { key: "address", label: "Address", value: "Bengaluru, Karnataka – 560076", confirmed: false },
  ];
  const confirmedValues = new Map(state.profile.map((field) => [field.key, field]));

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Step 1 · Your details</p>
        <h1 className="page-heading mt-2">Create your profile</h1>
        <p className="text-textSecondary mt-2">Upload your documents once. We’ll read the details and you can confirm them.</p>
      </div>

      <div className="flex items-start gap-3 rounded-2xl border border-leaf/20 bg-leafTint/50 p-4">
        <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-leaf" />
        <div className="flex-1"><h2 className="font-bold text-ink">Before you upload</h2><p className="mt-1 text-sm leading-6 text-textSecondary">We use documents only to help fill this fictional demo. Your documents stay on your device in this demo.</p><label className="mt-3 flex min-h-11 cursor-pointer items-center gap-3 text-sm font-bold text-ink"><input type="checkbox" checked={consent} onChange={(event) => setConsent(event.target.checked)} className="h-5 w-5 accent-leaf" /> I understand and consent to document processing.</label></div>
      </div>

      {/* Document Upload Cards */}
      <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
        {docs.map((d) => (
          <button key={d.id} type="button" onClick={() => void useSample(d.id)} className={`card-base relative text-left transition-all ${d.uploaded ? "border-leaf bg-leafTint/30" : "hover:-translate-y-1 hover:border-leaf"} disabled:cursor-wait disabled:opacity-70`} disabled={processing !== null}>
            {d.uploaded && (
              <div className="absolute top-3 right-3 w-6 h-6 bg-leaf text-white rounded-full flex items-center justify-center text-xs">
                ✓
              </div>
            )}
            <FileText className={`w-8 h-8 mb-3 ${d.uploaded ? "text-leaf" : "text-textSecondary"}`} />
            <h3 className="font-bold text-ink">{d.name}</h3>
            <p className="text-xs text-textSecondary mb-4">{d.tag}</p>
            <span className={`inline-flex min-h-11 items-center gap-2 text-xs font-bold px-3 py-1 rounded-xl ${d.uploaded ? "bg-leaf text-white" : "bg-cream text-textSecondary"}`}>
              {processing === d.id ? <LoaderCircle className="h-4 w-4 animate-spin" /> : null}{d.uploaded ? "Use SAMPLE document" : "Use SAMPLE document"}
            </span>
          </button>
        ))}
      </div>
      {status && <p role="status" aria-live="polite" className="rounded-xl bg-[#fbf8ef] p-3 text-sm font-semibold text-leaf">{status}</p>}

      {/* Extracted Details Card */}
      <div className="card-base space-y-6">
        <div className="flex items-center justify-between border-b border-[#EADFC4] pb-4">
          <div>
            <h2 className="font-serif text-xl font-bold text-ink">Extracted Details</h2>
            <p className="text-xs text-textSecondary mt-0.5">(Please review and confirm)</p>
          </div>
          <span className="text-xs font-bold px-3 py-1 bg-leafTint text-leaf rounded-full">AI Verified</span>
        </div>

        <div className="space-y-4">
          {profileFields.map((f) => {
            const isEditing = editingKey === f.key;
            return (
              <div key={f.key} className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-cream rounded-2xl border border-[#EADFC4]">
                <div>
                  <span className="text-xs font-bold text-textSecondary uppercase tracking-wider">{f.label}</span>
                  {isEditing ? (
                    <input
                      type="text"
                      className="mt-1 w-full bg-white border border-leaf px-3 py-1.5 rounded-xl text-sm font-semibold focus:outline-none"
                      defaultValue={editValues[f.key] ?? f.value}
                      onChange={(e) => setEditValues({ ...editValues, [f.key]: e.target.value })}
                      autoFocus
                    />
                  ) : (
                    <p className="font-bold text-ink text-base mt-0.5">{editValues[f.key] ?? confirmedValues.get(f.key)?.value ?? f.value}</p>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {confirmedValues.get(f.key)?.confirmed && !isEditing ? (
                    <span className="px-3 py-1 bg-leafTint text-leaf text-xs font-bold rounded-full flex items-center gap-1">
                      <CheckCircle className="w-3.5 h-3.5" /> Confirmed
                    </span>
                  ) : isEditing ? (
                    <button
                      onClick={() => { setEditingKey(null); }}
                      className="btn-primary !py-1.5 !px-4 !text-xs"
                    >
                      Save
                    </button>
                  ) : (
                    <div className="flex gap-2">
                    <button
                      onClick={() => dispatch({ t: "confirmProfile", key: f.key, value: editValues[f.key] ?? f.value })}
                      className="btn-primary !min-h-11 !py-1.5 !px-4 !text-xs"
                    >
                      Confirm
                    </button>
                    <button
                      onClick={() => setEditingKey(f.key)}
                      className="btn-secondary !py-1.5 !px-4 !text-xs flex items-center gap-1"
                    >
                      <Edit3 className="w-3.5 h-3.5" /> Edit
                    </button>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="flex justify-end pt-4">
        <button
          onClick={() => nav("/forms")}
          className="btn-primary"
        >
          Continue to Applications <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
