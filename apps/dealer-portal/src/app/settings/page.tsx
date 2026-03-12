"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEALER_ID = "demo";

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

export default function SettingsPage() {
  const [settings, setSettings] = useState<DealerSettings | null>(null);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  // Editable fields
  const [crmEmail, setCrmEmail] = useState("");
  const [radiusMiles, setRadiusMiles] = useState(25);
  const [maxLeadsPerDay, setMaxLeadsPerDay] = useState(50);
  const [minLeadScore, setMinLeadScore] = useState(20);
  const [makes, setMakes] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/portal/settings/${DEALER_ID}`)
      .then((r) => {
        if (!r.ok) throw new Error("Failed");
        return r.json();
      })
      .then((data: DealerSettings) => {
        setSettings(data);
        setCrmEmail(data.crm_email || "");
        setRadiusMiles(data.radius_miles);
        setMaxLeadsPerDay(data.max_leads_per_day);
        setMinLeadScore(data.min_lead_score);
        setMakes(data.makes.join(", "));
      })
      .catch(() => {});
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    try {
      const body: Record<string, unknown> = {
        radius_miles: radiusMiles,
        max_leads_per_day: maxLeadsPerDay,
        min_lead_score: minLeadScore,
      };
      if (crmEmail) body.crm_email = crmEmail;
      if (makes.trim()) {
        body.makes = makes
          .split(",")
          .map((m) => m.trim())
          .filter(Boolean);
      }

      const resp = await fetch(
        `${API_BASE}/api/v1/portal/settings/${DEALER_ID}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      );
      if (resp.ok) setSaved(true);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h2 className="text-2xl font-bold text-gray-900">Settings</h2>
      <p className="mt-1 text-gray-600">
        Manage your dealer profile and lead preferences.
      </p>

      {/* Dealer Profile (read-only) */}
      {settings && (
        <div className="mt-6 rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Dealer Profile
          </h3>
          <dl className="mt-4 grid grid-cols-2 gap-4 text-sm">
            <div>
              <dt className="text-gray-500">Name</dt>
              <dd className="font-medium">{settings.name}</dd>
            </div>
            <div>
              <dt className="text-gray-500">Contact Email</dt>
              <dd className="font-medium">{settings.contact_email}</dd>
            </div>
            <div>
              <dt className="text-gray-500">Phone</dt>
              <dd className="font-medium">{settings.phone}</dd>
            </div>
            <div>
              <dt className="text-gray-500">Location</dt>
              <dd className="font-medium">
                {settings.city}, {settings.state} {settings.zip_code}
              </dd>
            </div>
            <div>
              <dt className="text-gray-500">Subscription</dt>
              <dd className="font-medium capitalize">
                {settings.subscription_tier}
              </dd>
            </div>
            <div>
              <dt className="text-gray-500">Exclusive Leads</dt>
              <dd className="font-medium">
                {settings.exclusive_leads ? "Yes" : "No"}
              </dd>
            </div>
          </dl>
        </div>
      )}

      {/* Editable Settings */}
      <div className="mt-6 rounded-lg border border-gray-200 bg-white p-6">
        <h3 className="text-lg font-semibold text-gray-900">
          Lead Preferences
        </h3>

        <div className="mt-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              CRM Email Address (for ADF lead delivery)
            </label>
            <input
              type="email"
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
              value={crmEmail}
              onChange={(e) => setCrmEmail(e.target.value)}
              placeholder="crm-intake@yourdealership.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Make/Model Preferences (comma-separated)
            </label>
            <input
              type="text"
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
              value={makes}
              onChange={(e) => setMakes(e.target.value)}
              placeholder="Honda, Toyota, Hyundai"
            />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                ZIP Radius (miles)
              </label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                value={radiusMiles}
                onChange={(e) => setRadiusMiles(Number(e.target.value))}
                min={5}
                max={200}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Max Leads/Day
              </label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                value={maxLeadsPerDay}
                onChange={(e) => setMaxLeadsPerDay(Number(e.target.value))}
                min={1}
                max={500}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Min Lead Score
              </label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                value={minLeadScore}
                onChange={(e) => setMinLeadScore(Number(e.target.value))}
                min={0}
                max={100}
              />
            </div>
          </div>
        </div>

        <div className="mt-6 flex items-center gap-4">
          <button
            onClick={handleSave}
            disabled={saving}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Settings"}
          </button>
          {saved && (
            <span className="text-sm text-green-600">
              Settings saved successfully.
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
