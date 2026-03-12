"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1";

interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  zip_code: string;
  vehicle_interest: { make?: string; model?: string; fuel_type?: string; new_or_used?: string } | string;
  score: number;
  tier: string;
  total_savings: number;
  delivery_status: string;
  sent_at: string | null;
  created_at: string;
}

interface LeadDetail extends Lead {
  incentive_breakdown?: {
    name: string;
    type: string;
    amount: number;
  }[];
}

const TIER_COLORS: Record<string, string> = {
  hot: "bg-red-100 text-red-700",
  warm: "bg-yellow-100 text-yellow-700",
  nurture: "bg-blue-100 text-blue-700",
};

export default function PortalLeadsPage() {
  const router = useRouter();
  const [leads, setLeads] = useState<Lead[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [tierFilter, setTierFilter] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [expandedLeadId, setExpandedLeadId] = useState<string | null>(null);
  const [leadDetail, setLeadDetail] = useState<LeadDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const dealerId =
    typeof window !== "undefined"
      ? sessionStorage.getItem("portal_dealer_id")
      : null;

  const fetchLeads = useCallback(async () => {
    if (!dealerId) return;
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams({ skip: "0", limit: "50", sort_by: sortBy });
      if (tierFilter) params.set("tier", tierFilter);
      const res = await fetch(
        `${API_BASE}/portal/leads/${dealerId}?${params.toString()}`,
        { headers: { "Content-Type": "application/json" } }
      );
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const data = await res.json();
      setLeads(data.leads);
      setTotal(data.total);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leads");
    } finally {
      setLoading(false);
    }
  }, [dealerId, tierFilter, sortBy]);

  useEffect(() => {
    if (!dealerId) {
      router.replace("/portal");
      return;
    }
    fetchLeads();
  }, [dealerId, fetchLeads, router]);

  async function toggleLeadDetail(leadId: string) {
    if (expandedLeadId === leadId) {
      setExpandedLeadId(null);
      setLeadDetail(null);
      return;
    }
    setExpandedLeadId(leadId);
    setDetailLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/portal/leads/${dealerId}/${leadId}`,
        { headers: { "Content-Type": "application/json" } }
      );
      if (!res.ok) throw new Error(`Error ${res.status}`);
      setLeadDetail(await res.json());
    } catch {
      setLeadDetail(null);
    } finally {
      setDetailLoading(false);
    }
  }

  if (!dealerId) return null;

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
        <p className="text-sm text-gray-500">{total} total</p>
      </div>

      {/* Filters */}
      <div className="mt-6 flex flex-wrap items-center gap-4">
        <div>
          <label htmlFor="tier-filter" className="mr-2 text-sm text-gray-600">
            Tier:
          </label>
          <select
            id="tier-filter"
            value={tierFilter}
            onChange={(e) => setTierFilter(e.target.value)}
            className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="hot">Hot</option>
            <option value="warm">Warm</option>
            <option value="nurture">Nurture</option>
          </select>
        </div>
        <div>
          <label htmlFor="sort-by" className="mr-2 text-sm text-gray-600">
            Sort:
          </label>
          <select
            id="sort-by"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="date">Date</option>
            <option value="score">Score</option>
          </select>
        </div>
      </div>

      {loading && (
        <div className="mt-10 flex justify-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
        </div>
      )}

      {error && (
        <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-center text-sm text-red-700">
          {error}
        </div>
      )}

      {!loading && !error && (
        <div className="mt-6 overflow-x-auto rounded-xl border border-gray-200">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-4 py-3 font-medium text-gray-600">Name</th>
                <th className="px-4 py-3 font-medium text-gray-600">Email</th>
                <th className="px-4 py-3 font-medium text-gray-600">Phone</th>
                <th className="px-4 py-3 font-medium text-gray-600">Vehicle Interest</th>
                <th className="px-4 py-3 font-medium text-gray-600">Score</th>
                <th className="px-4 py-3 font-medium text-gray-600">Tier</th>
                <th className="px-4 py-3 font-medium text-gray-600">Savings</th>
                <th className="px-4 py-3 font-medium text-gray-600">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {leads.map((lead) => (
                <>
                  <tr
                    key={lead.id}
                    onClick={() => toggleLeadDetail(lead.id)}
                    className="cursor-pointer hover:bg-gray-50"
                  >
                    <td className="whitespace-nowrap px-4 py-3 font-medium text-gray-900">
                      {lead.first_name} {lead.last_name}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{lead.email}</td>
                    <td className="px-4 py-3 text-gray-600">{lead.phone}</td>
                    <td className="px-4 py-3 text-gray-600">
                      {typeof lead.vehicle_interest === "string"
                        ? lead.vehicle_interest
                        : [lead.vehicle_interest.make, lead.vehicle_interest.model].filter(Boolean).join(" ") || "—"}
                    </td>
                    <td className="px-4 py-3 text-gray-900">{lead.score}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${
                          TIER_COLORS[lead.tier] || "bg-gray-100 text-gray-700"
                        }`}
                      >
                        {lead.tier}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-900">
                      ${lead.total_savings.toLocaleString()}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-gray-600">
                      {new Date(lead.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                  {expandedLeadId === lead.id && (
                    <tr key={`${lead.id}-detail`}>
                      <td colSpan={8} className="bg-gray-50 px-6 py-4">
                        {detailLoading ? (
                          <div className="flex justify-center py-4">
                            <div className="h-6 w-6 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
                          </div>
                        ) : leadDetail ? (
                          <div className="space-y-3">
                            <div className="grid grid-cols-2 gap-4 text-sm sm:grid-cols-4">
                              <div>
                                <span className="text-gray-500">ZIP:</span>{" "}
                                <span className="font-medium">{leadDetail.zip_code}</span>
                              </div>
                              <div>
                                <span className="text-gray-500">Status:</span>{" "}
                                <span className="font-medium">{leadDetail.delivery_status}</span>
                              </div>
                              {leadDetail.sent_at && (
                                <div>
                                  <span className="text-gray-500">Sent:</span>{" "}
                                  <span className="font-medium">
                                    {new Date(leadDetail.sent_at).toLocaleString()}
                                  </span>
                                </div>
                              )}
                            </div>
                            {leadDetail.incentive_breakdown &&
                              leadDetail.incentive_breakdown.length > 0 && (
                                <div>
                                  <p className="text-sm font-medium text-gray-700">
                                    Incentive Breakdown
                                  </p>
                                  <div className="mt-2 space-y-1">
                                    {leadDetail.incentive_breakdown.map((inc, i) => (
                                      <div
                                        key={i}
                                        className="flex items-center justify-between rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm"
                                      >
                                        <div>
                                          <span className="font-medium text-gray-900">
                                            {inc.name}
                                          </span>
                                          <span className="ml-2 text-xs text-gray-500">
                                            {inc.type}
                                          </span>
                                        </div>
                                        <span className="font-semibold text-gray-900">
                                          ${inc.amount.toLocaleString()}
                                        </span>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500">
                            Could not load lead details.
                          </p>
                        )}
                      </td>
                    </tr>
                  )}
                </>
              ))}
              {leads.length === 0 && (
                <tr>
                  <td
                    colSpan={8}
                    className="px-4 py-8 text-center text-sm text-gray-500"
                  >
                    No leads found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
