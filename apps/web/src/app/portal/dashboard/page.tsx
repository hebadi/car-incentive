"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1";

interface DashboardData {
  dealer_name: string;
  subscription_tier: string;
  total_leads_this_month: number;
  avg_lead_score: number;
  leads_by_tier: { hot: number; warm: number; nurture: number };
  max_leads_per_day: number;
  radius_miles: number;
}

export default function PortalDashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const dealerId = sessionStorage.getItem("portal_dealer_id");
    if (!dealerId) {
      router.replace("/portal");
      return;
    }

    fetch(`${API_BASE}/portal/dashboard/${dealerId}`, {
      headers: { "Content-Type": "application/json" },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return res.json();
      })
      .then((d: DashboardData) => {
        setData(d);
        sessionStorage.setItem("portal_dealer_name", d.dealer_name);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
          <p className="mt-4 text-sm text-gray-500">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-10">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
          <p className="text-sm font-medium text-red-700">Failed to load dashboard</p>
          <p className="mt-1 text-xs text-red-600">{error}</p>
          <button
            onClick={() => router.push("/portal")}
            className="mt-4 text-sm font-medium text-blue-600 hover:text-blue-500"
          >
            Back to login
          </button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const tierBadgeColor: Record<string, string> = {
    free: "bg-gray-100 text-gray-700",
    basic: "bg-blue-100 text-blue-700",
    premium: "bg-purple-100 text-purple-700",
    enterprise: "bg-yellow-100 text-yellow-700",
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{data.dealer_name}</h1>
          <span
            className={`mt-1 inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${
              tierBadgeColor[data.subscription_tier] || "bg-gray-100 text-gray-700"
            }`}
          >
            {data.subscription_tier} plan
          </span>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <p className="text-sm text-gray-500">Leads This Month</p>
          <p className="mt-1 text-3xl font-bold text-gray-900">
            {data.total_leads_this_month}
          </p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <p className="text-sm text-gray-500">Avg Lead Score</p>
          <p className="mt-1 text-3xl font-bold text-gray-900">
            {data.avg_lead_score.toFixed(1)}
          </p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <p className="text-sm text-gray-500">Max Leads / Day</p>
          <p className="mt-1 text-3xl font-bold text-gray-900">
            {data.max_leads_per_day}
          </p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <p className="text-sm text-gray-500">Radius</p>
          <p className="mt-1 text-3xl font-bold text-gray-900">
            {data.radius_miles} mi
          </p>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-lg font-semibold text-gray-900">Leads by Tier</h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="rounded-xl border border-red-200 bg-red-50 p-5">
            <p className="text-sm font-medium text-red-700">Hot</p>
            <p className="mt-1 text-3xl font-bold text-red-800">
              {data.leads_by_tier.hot}
            </p>
          </div>
          <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-5">
            <p className="text-sm font-medium text-yellow-700">Warm</p>
            <p className="mt-1 text-3xl font-bold text-yellow-800">
              {data.leads_by_tier.warm}
            </p>
          </div>
          <div className="rounded-xl border border-blue-200 bg-blue-50 p-5">
            <p className="text-sm font-medium text-blue-700">Nurture</p>
            <p className="mt-1 text-3xl font-bold text-blue-800">
              {data.leads_by_tier.nurture}
            </p>
          </div>
        </div>
      </div>

      <div className="mt-8 text-center">
        <Link
          href="/portal/leads"
          className="inline-block rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          View All Leads
        </Link>
      </div>
    </div>
  );
}
