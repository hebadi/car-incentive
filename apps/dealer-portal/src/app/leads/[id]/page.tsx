"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEALER_ID = "demo";

interface LeadDetail {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string | null;
  zip_code: string;
  full_address: string | null;
  income_range: string | null;
  vehicle_interest: Record<string, string | number>;
  affinity_groups: string[];
  purchase_timeline: string | null;
  has_trade_in: boolean;
  score: number;
  tier: string;
  total_savings: number;
  incentives: {
    id: string;
    name: string;
    type: string;
    amount: number;
    claim_mechanism: string;
  }[];
  delivery: {
    status: string;
    method: string;
    sent_at: string | null;
    error: string | null;
  };
  consent: {
    timestamp: string | null;
    method: string | null;
    revoked: boolean | null;
  } | null;
  created_at: string;
}

const tierColors: Record<string, string> = {
  hot: "bg-red-100 text-red-800",
  warm: "bg-amber-100 text-amber-800",
  nurture: "bg-blue-100 text-blue-800",
};

export default function LeadDetailPage() {
  const params = useParams();
  const leadId = params.id as string;
  const [lead, setLead] = useState<LeadDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [notes, setNotes] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/portal/leads/${DEALER_ID}/${leadId}`)
      .then((r) => {
        if (!r.ok) throw new Error("Not found");
        return r.json();
      })
      .then(setLead)
      .catch(() => setLead(null))
      .finally(() => setLoading(false));
  }, [leadId]);

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 text-center text-gray-400">
        Loading...
      </div>
    );
  }

  if (!lead) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8">
        <a href="/leads" className="text-sm text-blue-600 hover:underline">
          &larr; Back to leads
        </a>
        <p className="mt-4 text-gray-500">Lead not found.</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <a href="/leads" className="text-sm text-blue-600 hover:underline">
        &larr; Back to leads
      </a>

      <div className="mt-4 flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            {lead.first_name} {lead.last_name}
          </h2>
          <p className="text-gray-600">{lead.email}</p>
          {lead.phone && <p className="text-gray-600">{lead.phone}</p>}
        </div>
        <span
          className={`rounded-full px-3 py-1 text-sm font-semibold capitalize ${
            tierColors[lead.tier] || "bg-gray-100 text-gray-600"
          }`}
        >
          Score: {lead.score} ({lead.tier})
        </span>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Contact & Vehicle Info */}
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Consumer Details
          </h3>
          <dl className="mt-4 space-y-3 text-sm">
            <Row label="ZIP Code" value={lead.zip_code} />
            {lead.full_address && (
              <Row label="Address" value={lead.full_address} />
            )}
            {lead.income_range && (
              <Row label="Income Range" value={lead.income_range} />
            )}
            <Row
              label="Vehicle Interest"
              value={
                [
                  lead.vehicle_interest?.year,
                  lead.vehicle_interest?.make,
                  lead.vehicle_interest?.model,
                ]
                  .filter(Boolean)
                  .join(" ") || "Not specified"
              }
            />
            <Row
              label="Purchase Timeline"
              value={lead.purchase_timeline || "Not specified"}
            />
            <Row label="Has Trade-In" value={lead.has_trade_in ? "Yes" : "No"} />
            {lead.affinity_groups.length > 0 && (
              <Row
                label="Affinity Groups"
                value={lead.affinity_groups.join(", ")}
              />
            )}
          </dl>
        </div>

        {/* Incentive Breakdown */}
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Incentive Breakdown
          </h3>
          <p className="mt-1 text-2xl font-bold text-green-700">
            ${lead.total_savings.toLocaleString()} total savings
          </p>
          {lead.incentives.length > 0 ? (
            <ul className="mt-4 space-y-2">
              {lead.incentives.map((inc) => (
                <li
                  key={inc.id}
                  className="flex items-center justify-between rounded border border-gray-100 p-3"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {inc.name}
                    </p>
                    <p className="text-xs capitalize text-gray-500">
                      {inc.type} &middot; {inc.claim_mechanism.replace(/_/g, " ")}
                    </p>
                  </div>
                  <span className="font-semibold text-green-700">
                    ${inc.amount.toLocaleString()}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-4 text-sm text-gray-400">
              No incentive details available.
            </p>
          )}
        </div>

        {/* ADF Delivery Status */}
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Delivery Status
          </h3>
          <dl className="mt-4 space-y-3 text-sm">
            <Row label="Method" value={lead.delivery.method.replace(/_/g, " ")} />
            <Row
              label="Status"
              value={
                <span
                  className={`capitalize ${
                    lead.delivery.status === "sent" || lead.delivery.status === "delivered"
                      ? "text-green-700"
                      : lead.delivery.status === "failed"
                        ? "text-red-600"
                        : "text-gray-600"
                  }`}
                >
                  {lead.delivery.status}
                </span>
              }
            />
            {lead.delivery.sent_at && (
              <Row
                label="Sent At"
                value={new Date(lead.delivery.sent_at).toLocaleString()}
              />
            )}
            {lead.delivery.error && (
              <Row label="Error" value={lead.delivery.error} />
            )}
          </dl>
        </div>

        {/* Consent & Notes */}
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Consent Record
          </h3>
          {lead.consent ? (
            <dl className="mt-4 space-y-3 text-sm">
              <Row
                label="Consent Given"
                value={
                  lead.consent.timestamp
                    ? new Date(lead.consent.timestamp).toLocaleString()
                    : "Unknown"
                }
              />
              <Row label="Method" value={lead.consent.method || "web_form"} />
              <Row
                label="Revoked"
                value={lead.consent.revoked ? "Yes" : "No"}
              />
            </dl>
          ) : (
            <p className="mt-4 text-sm text-gray-400">
              No consent record found.
            </p>
          )}

          <h3 className="mt-6 text-lg font-semibold text-gray-900">
            Dealer Notes
          </h3>
          <textarea
            className="mt-2 w-full rounded-lg border border-gray-300 p-3 text-sm"
            rows={3}
            placeholder="Add notes about this lead..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>
      </div>
    </div>
  );
}

function Row({
  label,
  value,
}: {
  label: string;
  value: React.ReactNode;
}) {
  return (
    <div className="flex justify-between">
      <dt className="text-gray-500">{label}</dt>
      <dd className="font-medium text-gray-900">{value}</dd>
    </div>
  );
}
