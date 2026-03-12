"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface DashboardData {
  dealer_name: string;
  subscription_tier: string;
  total_leads_this_month: number;
  avg_lead_score: number;
  leads_by_tier: { hot: number; warm: number; nurture: number };
  max_leads_per_day: number;
  radius_miles: number;
}

// MVP: hardcoded dealer ID. Replace with auth context in production.
const DEALER_ID = "demo";

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/portal/dashboard/${DEALER_ID}`)
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load dashboard");
        return r.json();
      })
      .then(setData)
      .catch(() => setError("Could not connect to API"));
  }, []);

  const stats = data || {
    total_leads_this_month: 0,
    avg_lead_score: 0,
    leads_by_tier: { hot: 0, warm: 0, nurture: 0 },
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
          <p className="mt-1 text-gray-600">
            {data
              ? `Welcome back, ${data.dealer_name}`
              : "Welcome to your IncentiveDrive dealer portal."}
          </p>
        </div>
        {data && (
          <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium capitalize text-blue-800">
            {data.subscription_tier} Plan
          </span>
        )}
      </div>

      {error && (
        <div className="mt-4 rounded-lg bg-yellow-50 p-4 text-sm text-yellow-800">
          {error} — showing placeholder data.
        </div>
      )}

      <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <p className="text-sm font-medium text-gray-500">
            Leads This Month
          </p>
          <p className="mt-2 text-3xl font-bold text-gray-900">
            {stats.total_leads_this_month}
          </p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <p className="text-sm font-medium text-gray-500">Avg Lead Score</p>
          <p className="mt-2 text-3xl font-bold text-gray-900">
            {stats.avg_lead_score || "--"}
          </p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <p className="text-sm font-medium text-gray-500">Hot Leads</p>
          <p className="mt-2 text-3xl font-bold text-red-600">
            {stats.leads_by_tier.hot}
          </p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <p className="text-sm font-medium text-gray-500">Warm Leads</p>
          <p className="mt-2 text-3xl font-bold text-amber-600">
            {stats.leads_by_tier.warm}
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Leads by Tier
          </h3>
          <div className="mt-4 space-y-3">
            <TierBar label="Hot (80-100)" count={stats.leads_by_tier.hot} color="bg-red-500" total={stats.total_leads_this_month} />
            <TierBar label="Warm (50-79)" count={stats.leads_by_tier.warm} color="bg-amber-500" total={stats.total_leads_this_month} />
            <TierBar label="Nurture (20-49)" count={stats.leads_by_tier.nurture} color="bg-blue-500" total={stats.total_leads_this_month} />
          </div>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
          <div className="mt-4 space-y-2">
            <a
              href="/leads"
              className="block rounded-lg border border-gray-200 p-3 text-sm hover:bg-gray-50"
            >
              View all leads &rarr;
            </a>
            <a
              href="/settings"
              className="block rounded-lg border border-gray-200 p-3 text-sm hover:bg-gray-50"
            >
              Update lead preferences &rarr;
            </a>
            <a
              href="/billing"
              className="block rounded-lg border border-gray-200 p-3 text-sm hover:bg-gray-50"
            >
              View billing &amp; invoices &rarr;
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

function TierBar({
  label,
  count,
  color,
  total,
}: {
  label: string;
  count: number;
  color: string;
  total: number;
}) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div>
      <div className="flex justify-between text-sm">
        <span className="text-gray-600">{label}</span>
        <span className="font-medium">{count}</span>
      </div>
      <div className="mt-1 h-2 w-full rounded-full bg-gray-100">
        <div
          className={`h-2 rounded-full ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
