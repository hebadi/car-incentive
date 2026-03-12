"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEALER_ID = "demo";

interface Subscription {
  has_subscription: boolean;
  id?: string;
  status?: string;
  tier?: string;
  current_period_start?: number;
  current_period_end?: number;
  cancel_at_period_end?: boolean;
}

interface Invoice {
  id: string;
  number: string | null;
  amount_paid: number;
  status: string;
  created: number;
  hosted_invoice_url: string | null;
  invoice_pdf: string | null;
}

const tierInfo: Record<string, { name: string; base: number; perLead: number; leads: number }> = {
  starter: { name: "Starter", base: 299, perLead: 40, leads: 25 },
  growth: { name: "Growth", base: 599, perLead: 35, leads: 50 },
  enterprise: { name: "Enterprise", base: 999, perLead: 30, leads: 100 },
};

export default function BillingPage() {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/api/v1/billing/subscription/${DEALER_ID}`)
        .then((r) => r.json())
        .catch(() => ({ has_subscription: false, tier: "starter" })),
      fetch(`${API_BASE}/api/v1/billing/invoices/${DEALER_ID}`)
        .then((r) => r.json())
        .catch(() => ({ invoices: [] })),
    ]).then(([sub, inv]) => {
      setSubscription(sub);
      setInvoices(inv.invoices || []);
      setLoading(false);
    });
  }, []);

  const currentTier = subscription?.tier || "starter";
  const tier = tierInfo[currentTier] || tierInfo.starter;

  const handleUpgrade = async (newTier: string) => {
    const resp = await fetch(`${API_BASE}/api/v1/billing/checkout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        dealer_id: DEALER_ID,
        tier: newTier,
      }),
    });
    if (resp.ok) {
      const data = await resp.json();
      if (data.url) window.location.href = data.url;
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 text-center text-gray-400">
        Loading...
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <h2 className="text-2xl font-bold text-gray-900">Billing</h2>
      <p className="mt-1 text-gray-600">
        Manage your subscription and view invoices.
      </p>

      {/* Current Plan */}
      <div className="mt-6 rounded-lg border border-gray-200 bg-white p-6">
        <h3 className="text-lg font-semibold text-gray-900">Current Plan</h3>
        <div className="mt-4 flex items-center justify-between">
          <div>
            <p className="text-2xl font-bold text-gray-900">{tier.name}</p>
            <p className="text-gray-600">
              ${tier.base}/mo base + ${tier.perLead}/lead
            </p>
            <p className="mt-1 text-sm text-gray-500">
              Up to {tier.leads} leads/mo included
            </p>
          </div>
          <div className="text-right">
            {subscription?.has_subscription ? (
              <span className="inline-flex rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
                Active
              </span>
            ) : (
              <span className="inline-flex rounded-full bg-gray-100 px-3 py-1 text-sm font-medium text-gray-600">
                No subscription
              </span>
            )}
            {subscription?.cancel_at_period_end && (
              <p className="mt-1 text-sm text-red-600">Cancels at period end</p>
            )}
          </div>
        </div>
        {subscription?.current_period_end && (
          <p className="mt-2 text-sm text-gray-500">
            Current period ends:{" "}
            {new Date(subscription.current_period_end * 1000).toLocaleDateString()}
          </p>
        )}
      </div>

      {/* Pricing Tiers */}
      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900">Available Plans</h3>
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">
          {Object.entries(tierInfo).map(([key, t]) => (
            <div
              key={key}
              className={`rounded-lg border p-6 ${
                key === currentTier
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 bg-white"
              }`}
            >
              <h4 className="text-lg font-semibold">{t.name}</h4>
              <p className="mt-2 text-3xl font-bold">${t.base}</p>
              <p className="text-sm text-gray-500">/month base</p>
              <ul className="mt-4 space-y-1 text-sm text-gray-600">
                <li>+ ${t.perLead}/lead</li>
                <li>Up to {t.leads} leads/mo included</li>
                {key === "growth" && <li>CRM integration</li>}
                {key === "enterprise" && <li>White-label tools</li>}
                {key === "enterprise" && <li>Dedicated account manager</li>}
              </ul>
              {key === currentTier ? (
                <p className="mt-4 text-center text-sm font-medium text-blue-700">
                  Current Plan
                </p>
              ) : (
                <button
                  onClick={() => handleUpgrade(key)}
                  className="mt-4 w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                >
                  {Object.keys(tierInfo).indexOf(key) >
                  Object.keys(tierInfo).indexOf(currentTier)
                    ? "Upgrade"
                    : "Downgrade"}
                </button>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Invoices */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold text-gray-900">Invoices</h3>
        {invoices.length === 0 ? (
          <p className="mt-4 text-sm text-gray-400">No invoices yet.</p>
        ) : (
          <div className="mt-4 overflow-x-auto rounded-lg border border-gray-200 bg-white">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                    Date
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                    Invoice
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                    Amount
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                    Status
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {invoices.map((inv) => (
                  <tr key={inv.id}>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-600">
                      {new Date(inv.created * 1000).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3 text-sm">{inv.number || inv.id}</td>
                    <td className="px-4 py-3 text-sm font-medium">
                      ${(inv.amount_paid / 100).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-sm capitalize">{inv.status}</td>
                    <td className="px-4 py-3 text-sm">
                      {inv.hosted_invoice_url && (
                        <a
                          href={inv.hosted_invoice_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline"
                        >
                          View
                        </a>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
