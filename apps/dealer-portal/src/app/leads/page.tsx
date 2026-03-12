"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEALER_ID = "demo";

interface LeadSummary {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string | null;
  vehicle_interest: { make?: string; model?: string; year?: number };
  score: number;
  tier: string;
  total_savings: number;
  delivery_status: string;
  created_at: string;
}

const tierColors: Record<string, string> = {
  hot: "bg-red-100 text-red-800",
  warm: "bg-amber-100 text-amber-800",
  nurture: "bg-blue-100 text-blue-800",
  unqualified: "bg-gray-100 text-gray-600",
};

export default function LeadsPage() {
  const [leads, setLeads] = useState<LeadSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [tierFilter, setTierFilter] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (tierFilter) params.set("tier", tierFilter);
    params.set("sort_by", sortBy);

    fetch(`${API_BASE}/api/v1/portal/leads/${DEALER_ID}?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setLeads(data.leads || []);
        setTotal(data.total || 0);
      })
      .catch(() => {
        setLeads([]);
        setTotal(0);
      })
      .finally(() => setLoading(false));
  }, [tierFilter, sortBy]);

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Leads</h2>
        <span className="text-sm text-gray-500">{total} total</span>
      </div>

      <div className="mt-4 flex gap-4">
        <select
          className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
          value={tierFilter}
          onChange={(e) => setTierFilter(e.target.value)}
        >
          <option value="">All Tiers</option>
          <option value="hot">Hot</option>
          <option value="warm">Warm</option>
          <option value="nurture">Nurture</option>
        </select>
        <select
          className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <option value="date">Sort by Date</option>
          <option value="score">Sort by Score</option>
        </select>
      </div>

      <div className="mt-6 overflow-x-auto rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                Date
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                Name
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                Vehicle
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                Score
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                Savings
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                Status
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {loading ? (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-gray-400">
                  Loading...
                </td>
              </tr>
            ) : leads.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-gray-400">
                  No leads found.
                </td>
              </tr>
            ) : (
              leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-gray-50">
                  <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-600">
                    {new Date(lead.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3">
                    <a
                      href={`/leads/${lead.id}`}
                      className="text-sm font-medium text-blue-600 hover:underline"
                    >
                      {lead.first_name} {lead.last_name}
                    </a>
                    <p className="text-xs text-gray-500">{lead.email}</p>
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700">
                    {[
                      lead.vehicle_interest?.year,
                      lead.vehicle_interest?.make,
                      lead.vehicle_interest?.model,
                    ]
                      .filter(Boolean)
                      .join(" ") || "Not specified"}
                  </td>
                  <td className="whitespace-nowrap px-4 py-3">
                    <span
                      className={`inline-flex rounded-full px-2 py-0.5 text-xs font-semibold ${
                        tierColors[lead.tier] || tierColors.unqualified
                      }`}
                    >
                      {lead.score} - {lead.tier}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 text-sm font-medium text-green-700">
                    ${lead.total_savings.toLocaleString()}
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 text-sm capitalize text-gray-600">
                    {lead.delivery_status || "pending"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
