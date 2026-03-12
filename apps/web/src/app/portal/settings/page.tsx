"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1";

interface DealerSettings {
  id: string;
  name: string;
  contact_email: string;
  crm_email: string | null;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  makes: string[];
  subscription_tier: string;
  max_leads_per_day: number;
  min_lead_score: number;
  radius_miles: number;
  exclusive_leads: boolean;
}

function InfoTip({ text }: { text: string }) {
  const [open, setOpen] = useState(false);
  return (
    <span className="relative ml-1.5 inline-block">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
        className="inline-flex h-4 w-4 items-center justify-center rounded-full bg-gray-200 text-[10px] font-bold leading-none text-gray-500 hover:bg-blue-100 hover:text-blue-600 focus:outline-none"
        aria-label="More info"
      >
        i
      </button>
      {open && (
        <span className="absolute bottom-full left-1/2 z-10 mb-2 w-56 -translate-x-1/2 rounded-lg bg-gray-900 px-3 py-2 text-xs leading-relaxed text-white shadow-lg">
          {text}
          <span className="absolute left-1/2 top-full -translate-x-1/2 border-4 border-transparent border-t-gray-900" />
        </span>
      )}
    </span>
  );
}

export default function PortalSettingsPage() {
  const router = useRouter();
  const [settings, setSettings] = useState<DealerSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Editable fields
  const [crmEmail, setCrmEmail] = useState("");
  const [radiusMiles, setRadiusMiles] = useState(500);    // default: unlimited
  const [maxLeadsPerDay, setMaxLeadsPerDay] = useState(999); // default: unlimited
  const [minLeadScore, setMinLeadScore] = useState(0);      // default: lowest

  useEffect(() => {
    const dealerId = sessionStorage.getItem("portal_dealer_id");
    if (!dealerId) {
      router.replace("/portal");
      return;
    }

    fetch(`${API_BASE}/portal/settings/${dealerId}`, {
      headers: { "Content-Type": "application/json" },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return res.json();
      })
      .then((d: DealerSettings) => {
        setSettings(d);
        setCrmEmail(d.crm_email || "");
        setRadiusMiles(d.radius_miles);
        setMaxLeadsPerDay(d.max_leads_per_day);
        setMinLeadScore(d.min_lead_score);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [router]);

  async function handleSave() {
    const dealerId = sessionStorage.getItem("portal_dealer_id");
    if (!dealerId) return;

    setSaving(true);
    setError("");
    setSuccess("");

    try {
      const res = await fetch(`${API_BASE}/portal/settings/${dealerId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          crm_email: crmEmail || null,
          radius_miles: radiusMiles,
          max_leads_per_day: maxLeadsPerDay,
          min_lead_score: minLeadScore,
        }),
      });
      if (!res.ok) throw new Error(`Error ${res.status}`);
      setSuccess("Settings saved successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
      </div>
    );
  }

  if (!settings) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-10">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
          <p className="text-sm font-medium text-red-700">Failed to load settings</p>
          <p className="mt-1 text-xs text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
      <p className="mt-1 text-sm text-gray-500">Manage your dealership preferences and lead delivery settings.</p>

      {/* Read-only dealer info */}
      <div className="mt-8 rounded-xl border border-gray-200 bg-white p-6">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">Dealership Info</h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <p className="text-xs text-gray-500">Name</p>
            <p className="text-sm font-medium text-gray-900">{settings.name}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Subscription</p>
            <p className="text-sm font-medium capitalize text-gray-900">{settings.subscription_tier}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Contact Email</p>
            <p className="text-sm font-medium text-gray-900">{settings.contact_email}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Phone</p>
            <p className="text-sm font-medium text-gray-900">{settings.phone}</p>
          </div>
          <div className="sm:col-span-2">
            <p className="text-xs text-gray-500">Address</p>
            <p className="text-sm font-medium text-gray-900">
              {settings.address}, {settings.city}, {settings.state} {settings.zip_code}
            </p>
          </div>
          <div className="sm:col-span-2">
            <p className="text-xs text-gray-500">Makes</p>
            <div className="mt-1 flex flex-wrap gap-1.5">
              {settings.makes.map((make) => (
                <span key={make} className="rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                  {make}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Editable settings */}
      <div className="mt-6 rounded-xl border border-gray-200 bg-white p-6">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">Lead Delivery Settings</h2>
        <div className="mt-4 space-y-5">
          <div>
            <label htmlFor="crm-email" className="block text-sm font-medium text-gray-700">
              CRM Email
              <InfoTip text="Leads are delivered to this email address. Use your CRM inbox (e.g., DealerSocket, VinSolutions) so leads flow directly into your sales workflow." />
            </label>
            <input
              id="crm-email"
              type="email"
              value={crmEmail}
              onChange={(e) => setCrmEmail(e.target.value)}
              placeholder="crm@yourdealership.com"
              className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <div>
            <label htmlFor="radius" className="block text-sm font-medium text-gray-700">
              Lead Radius: {radiusMiles >= 500 ? "Unlimited" : `${radiusMiles} miles`}
              <InfoTip text="Only receive leads from consumers within this distance of your dealership. Smaller radius = more local, higher-intent buyers. Set to Unlimited to receive leads from anywhere." />
            </label>
            <input
              id="radius"
              type="range"
              min={10}
              max={500}
              step={5}
              value={radiusMiles}
              onChange={(e) => setRadiusMiles(Number(e.target.value))}
              className="mt-2 w-full accent-blue-600"
            />
            <div className="mt-1 flex justify-between text-xs text-gray-400">
              <span>10 mi</span>
              <span>Unlimited</span>
            </div>
          </div>

          <div>
            <label htmlFor="max-leads" className="block text-sm font-medium text-gray-700">
              Max Leads / Day: {maxLeadsPerDay >= 999 ? "Unlimited" : maxLeadsPerDay}
              <InfoTip text="Caps how many leads you receive daily. Set this to match your team's capacity — unanswered leads lose value quickly. The best response time is under 5 minutes. Set to Unlimited to receive all available leads." />
            </label>
            <input
              id="max-leads"
              type="range"
              min={1}
              max={999}
              step={1}
              value={maxLeadsPerDay}
              onChange={(e) => setMaxLeadsPerDay(Number(e.target.value))}
              className="mt-2 w-full accent-blue-600"
            />
            <div className="mt-1 flex justify-between text-xs text-gray-400">
              <span>1</span>
              <span>Unlimited</span>
            </div>
          </div>

          <div>
            <label htmlFor="min-score" className="block text-sm font-medium text-gray-700">
              Min Lead Score: {minLeadScore === 0 ? "Any" : minLeadScore}
              <InfoTip text="Only receive leads scored at or above this threshold (0-100). Higher scores indicate stronger purchase intent based on income match, timeline, and incentive value. Set to 0 to receive all leads." />
            </label>
            <input
              id="min-score"
              type="range"
              min={0}
              max={100}
              step={5}
              value={minLeadScore}
              onChange={(e) => setMinLeadScore(Number(e.target.value))}
              className="mt-2 w-full accent-blue-600"
            />
            <div className="mt-1 flex justify-between text-xs text-gray-400">
              <span>Any</span>
              <span>100</span>
            </div>
          </div>
        </div>

        {error && (
          <div className="mt-4 rounded-lg bg-red-50 px-4 py-2.5 text-sm text-red-700">{error}</div>
        )}
        {success && (
          <div className="mt-4 rounded-lg bg-green-50 px-4 py-2.5 text-sm text-green-700">{success}</div>
        )}

        <div className="mt-6">
          <button
            onClick={handleSave}
            disabled={saving}
            className="rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </div>
    </div>
  );
}
