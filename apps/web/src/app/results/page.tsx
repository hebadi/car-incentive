"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import LeadCaptureModal from "@/components/LeadCaptureModal";
import CarImage from "@/components/CarImage";

interface ClaimStepData {
  step: number;
  title: string;
  description: string;
  documents?: string[];
  url?: string;
}

interface IncentiveSummary {
  id: string;
  name: string;
  type: string;
  amount: number;
  claimMechanism: string;
  confidenceScore: number;
  sourceUrl?: string | null;
  fundingStatus?: string | null;
  endDate?: string | null;
  lastVerified?: string | null;
  eligiblePurchaseTypes?: string[];
  claimSteps?: ClaimStepData[];
}

interface IncentiveResults {
  incentives: IncentiveSummary[];
  totalSavings: number;
  confidence: number;
  disclaimers: string[];
}

interface StoredCalculatorData {
  zipCode: string;
  fuelType?: string;
  newOrUsed?: string;
  make?: string;
  model?: string;
  incomeRange?: string;
  filingStatus?: string;
  affinityGroups?: string[];
}

const TYPE_LABELS: Record<string, string> = {
  state: "State Rebate",
  manufacturer: "Manufacturer Rebate",
  utility: "Utility Rebate",
  federal: "Federal Credit",
  affinity: "Affinity Discount",
};

const TYPE_COLORS: Record<string, string> = {
  state: "bg-green-100 text-green-800",
  manufacturer: "bg-blue-100 text-blue-800",
  utility: "bg-yellow-100 text-yellow-800",
  federal: "bg-purple-100 text-purple-800",
  affinity: "bg-pink-100 text-pink-800",
};

const TYPE_BORDER_COLORS: Record<string, string> = {
  state: "border-l-green-500",
  manufacturer: "border-l-blue-500",
  utility: "border-l-yellow-500",
  federal: "border-l-purple-500",
  affinity: "border-l-pink-500",
};

function incentiveAmount(incentive: IncentiveSummary): number {
  return incentive.amount || 0;
}

function ClaimStepsLight({ steps }: { steps: ClaimStepData[] }) {
  return (
    <div className="mt-3 space-y-2 rounded-lg border border-gray-100 bg-gray-50 px-4 py-3">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-gray-500">
        How to Claim
      </p>
      <ol className="space-y-2">
        {steps.map((s) => (
          <li key={s.step} className="flex gap-2.5">
            <span className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-indigo-100 text-[10px] font-bold text-indigo-700">
              {s.step}
            </span>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-gray-800">{s.title}</p>
              <p className="text-[11px] leading-relaxed text-gray-600">{s.description}</p>
              {s.documents && s.documents.length > 0 && (
                <p className="mt-0.5 text-[10px] text-gray-500">
                  Docs needed: {s.documents.join(", ")}
                </p>
              )}
              {s.url && (
                <a
                  href={s.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-0.5 inline-flex items-center gap-1 text-[10px] font-medium text-indigo-600 hover:text-indigo-500"
                >
                  Apply here
                  <svg className="h-2.5 w-2.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                  </svg>
                </a>
              )}
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}

function IncentiveItem({ inc }: { inc: IncentiveSummary }) {
  const [showClaim, setShowClaim] = useState(false);
  const hasClaimSteps = inc.claimSteps && inc.claimSteps.length > 0;
  return (
    <div className="px-5 py-4 transition-colors hover:bg-gray-50/50">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-semibold text-gray-900">
            {inc.name}
          </p>
          <p className="mt-0.5 text-xs text-gray-500">
            {inc.claimMechanism === "point_of_sale" && "Applied at purchase"}
            {inc.claimMechanism === "tax_return" && "Claimed on tax return"}
            {inc.claimMechanism === "post_purchase_rebate" && "Post-purchase rebate"}
            {inc.claimMechanism === "lease_reduction" && "Lease reduction"}
          </p>
        </div>
        <span className="rounded-lg bg-green-50 px-3 py-1 text-sm font-bold text-green-700">
          ${incentiveAmount(inc).toLocaleString()}
        </span>
      </div>
      <div className="mt-2 flex items-center gap-2">
        {inc.endDate && (() => {
          const exp = getExpirationInfo(inc.endDate);
          return (
            <span className={`rounded-full px-2 py-0.5 text-[10px] ${exp.color}`}>
              {exp.label}
            </span>
          );
        })()}
        {inc.lastVerified && (
          <span className="text-[10px] text-gray-400">
            {formatVerifiedDate(inc.lastVerified)}
          </span>
        )}
      </div>
      {inc.fundingStatus !== "open" && (
        <p className="mt-1 text-xs text-red-600">
          Funding status: {inc.fundingStatus}
        </p>
      )}
      <div className="mt-2 flex items-center gap-3">
        {inc.sourceUrl && (
          <a
            href={inc.sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs font-medium text-indigo-600 transition-colors hover:text-indigo-500"
          >
            See more info
            <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
            </svg>
          </a>
        )}
        {hasClaimSteps && (
          <button
            type="button"
            onClick={() => setShowClaim(!showClaim)}
            className="inline-flex items-center gap-1 text-xs font-medium text-indigo-600 transition-colors hover:text-indigo-500"
          >
            {showClaim ? "Hide steps" : "How to claim"}
            <svg
              className={`h-3 w-3 transition-transform ${showClaim ? "rotate-180" : ""}`}
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
            </svg>
          </button>
        )}
      </div>
      {showClaim && hasClaimSteps && (
        <ClaimStepsLight steps={inc.claimSteps!} />
      )}
    </div>
  );
}

function formatVerifiedDate(iso: string): string {
  const d = new Date(iso);
  return `Verified ${d.toLocaleDateString("en-US", { month: "short", year: "numeric" })}`;
}

function getExpirationInfo(endDateIso: string): { label: string; color: string } {
  const now = new Date();
  const end = new Date(endDateIso);
  const diffMs = end.getTime() - now.getTime();
  const daysLeft = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

  if (daysLeft < 0) {
    return { label: "Expired", color: "text-red-700 bg-red-50" };
  }
  if (daysLeft < 7) {
    return { label: `Expires in ${daysLeft} day${daysLeft !== 1 ? "s" : ""}!`, color: "text-red-700 bg-red-50 font-semibold" };
  }
  if (daysLeft <= 30) {
    return { label: `Expires in ${daysLeft} days`, color: "text-yellow-700 bg-yellow-50" };
  }
  return {
    label: `Expires ${end.toLocaleDateString("en-US", { month: "short", day: "numeric" })}`,
    color: "text-green-700 bg-green-50",
  };
}

const PURCHASE_TYPE_LABELS: Record<string, string> = {
  cash: "Cash Purchase",
  finance: "Finance",
  lease: "Lease",
};

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<IncentiveResults | null>(null);
  const [calcData, setCalcData] = useState<StoredCalculatorData | null>(null);
  const [showLeadModal, setShowLeadModal] = useState(false);
  const [activePurchaseType, setActivePurchaseType] = useState("cash");

  useEffect(() => {
    const stored = sessionStorage.getItem("incentiveResults");
    const storedCalc = sessionStorage.getItem("calculatorData");
    if (!stored || !storedCalc) {
      router.replace("/calculator");
      return;
    }
    setResults(JSON.parse(stored));
    setCalcData(JSON.parse(storedCalc));
  }, [router]);

  if (!results || !calcData) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
          <p className="mt-4 text-sm text-gray-500">Loading results...</p>
        </div>
      </div>
    );
  }

  // Filter out incentives with unreliable/generic sources
  const BLOCKED_SOURCES = ["https://www.marketcheck.com", "https://www.marketcheck.com/"];
  const filteredIncentives = results.incentives.filter(
    (inc) => !inc.sourceUrl || !BLOCKED_SOURCES.includes(inc.sourceUrl)
  );

  // Group by purchase type
  const byPurchaseType: Record<string, IncentiveSummary[]> = { cash: [], finance: [], lease: [] };
  for (const inc of filteredIncentives) {
    const pts = inc.eligiblePurchaseTypes || ["cash", "finance", "lease"];
    for (const pt of pts) {
      if (byPurchaseType[pt]) {
        byPurchaseType[pt].push(inc);
      }
    }
  }

  const activeIncentives = byPurchaseType[activePurchaseType] || [];
  const activeTotal = activeIncentives.reduce((sum, inc) => sum + incentiveAmount(inc), 0);

  // Group active incentives by type for display
  const grouped: Record<string, IncentiveSummary[]> = {};
  for (const inc of activeIncentives) {
    if (!grouped[inc.type]) grouped[inc.type] = [];
    grouped[inc.type].push(inc);
  }

  // Order: state, manufacturer, utility, federal, affinity
  const typeOrder = ["state", "manufacturer", "utility", "federal", "affinity"];
  const orderedTypes = typeOrder.filter((t) => grouped[t]);

  // Purchase type totals for tabs
  const purchaseTypeTotals: Record<string, { total: number; count: number }> = {};
  for (const pt of ["cash", "finance", "lease"]) {
    const incs = byPurchaseType[pt] || [];
    if (incs.length > 0) {
      purchaseTypeTotals[pt] = {
        total: incs.reduce((sum, inc) => sum + incentiveAmount(inc), 0),
        count: incs.length,
      };
    }
  }

  const hasCarSelection = calcData.make && calcData.model;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Hero banner with car and savings */}
      <div className="bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-900 px-4 py-12">
        <div className="mx-auto max-w-3xl">
          <div className={`flex flex-col items-center gap-8 ${hasCarSelection ? "sm:flex-row" : ""}`}>
            {/* Car image */}
            {hasCarSelection && (
              <div className="flex-shrink-0">
                <CarImage
                  make={calcData.make!}
                  model={calcData.model!}
                  size="lg"
                />
              </div>
            )}

            {/* Savings amount */}
            <div className={`text-center ${hasCarSelection ? "sm:text-left" : ""}`}>
              {hasCarSelection && (
                <p className="text-sm font-medium text-indigo-300">
                  Your {calcData.make} {calcData.model}
                </p>
              )}
              <p className="mt-1 text-sm font-medium text-slate-400">
                Estimated Savings — {PURCHASE_TYPE_LABELS[activePurchaseType]}
              </p>
              <p className="mt-2 animate-count-up bg-gradient-to-r from-emerald-400 to-green-300 bg-clip-text text-6xl font-black text-transparent sm:text-7xl">
                ${activeTotal.toLocaleString()}
              </p>
              <p className="mt-3 text-sm text-slate-400">
                Based on {activeIncentives.length} incentive
                {activeIncentives.length !== 1 ? "s" : ""} you may qualify for
              </p>
              {results.confidence < 0.8 && (
                <p className="mt-2 rounded-lg bg-yellow-500/10 px-3 py-1.5 text-xs text-yellow-300">
                  Some incentives have lower confidence scores. Verify with official
                  sources before making decisions.
                </p>
              )}
            </div>
          </div>

          {/* Purchase type tabs */}
          <div className="mt-8 flex gap-2 rounded-xl bg-white/5 p-1.5">
            {(["cash", "finance", "lease"] as const).map((pt) => {
              const data = purchaseTypeTotals[pt];
              if (!data) return null;
              const isActive = activePurchaseType === pt;
              return (
                <button
                  key={pt}
                  type="button"
                  onClick={() => setActivePurchaseType(pt)}
                  className={`flex flex-1 flex-col items-center gap-1 rounded-lg px-4 py-3 transition-all ${
                    isActive
                      ? "bg-white/15 text-white shadow-sm"
                      : "text-slate-400 hover:bg-white/5 hover:text-slate-300"
                  }`}
                >
                  <span className="text-xs font-semibold uppercase tracking-wider">
                    {PURCHASE_TYPE_LABELS[pt]}
                  </span>
                  <span className={`text-xl font-black ${isActive ? "text-emerald-400" : "text-emerald-400/50"}`}>
                    ${data.total.toLocaleString()}
                  </span>
                  <span className="text-[10px] text-slate-500">
                    {data.count} incentive{data.count !== 1 ? "s" : ""}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-3xl px-4 py-10">
        {/* Savings breakdown */}
        <div className="space-y-6">
          <h3 className="text-xl font-bold text-gray-900">
            Savings Breakdown
          </h3>

          {orderedTypes.map((type) => {
            const incentives = grouped[type];
            const subtotal = incentives.reduce(
              (sum, inc) => sum + incentiveAmount(inc),
              0
            );
            return (
              <div
                key={type}
                className={`overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-md border-l-4 ${
                  TYPE_BORDER_COLORS[type] || "border-l-gray-400"
                }`}
              >
                <div className="flex items-center justify-between border-b border-gray-100 px-5 py-4">
                  <div className="flex items-center gap-3">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${
                        TYPE_COLORS[type] || "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {TYPE_LABELS[type] || type}
                    </span>
                    <span className="text-sm text-gray-500">
                      {incentives.length} program
                      {incentives.length !== 1 ? "s" : ""}
                    </span>
                  </div>
                  <span className="text-lg font-bold text-gray-900">
                    ${subtotal.toLocaleString()}
                  </span>
                </div>
                <div className="divide-y divide-gray-50">
                  {incentives.map((inc) => (
                    <IncentiveItem key={inc.id} inc={inc} />
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Disclaimers */}
        {results.disclaimers.length > 0 && (
          <div className="mt-8 rounded-2xl border border-yellow-200 bg-yellow-50 p-5">
            <h4 className="flex items-center gap-2 text-sm font-semibold text-yellow-800">
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
              Important Notes
            </h4>
            <ul className="mt-3 list-disc space-y-1.5 pl-5 text-xs leading-relaxed text-yellow-700">
              {results.disclaimers.map((d, i) => (
                <li key={i}>{d}</li>
              ))}
            </ul>
          </div>
        )}

        {/* CTA */}
        <div className="mt-10 overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-600 to-blue-700 p-8 text-center shadow-2xl shadow-indigo-500/20">
          <h3 className="text-2xl font-bold text-white">
            Ready to claim your savings?
          </h3>
          <p className="mt-3 text-sm text-indigo-200">
            Connect with a local dealer who can help you take advantage of these
            incentives.
          </p>
          <button
            onClick={() => setShowLeadModal(true)}
            className="mt-6 inline-flex items-center gap-2 rounded-xl bg-white px-8 py-4 text-sm font-bold text-indigo-700 shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600"
          >
            Connect with a Dealer
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </button>
        </div>

        {/* Start over */}
        <div className="mt-8 text-center">
          <Link
            href="/calculator"
            className="inline-flex items-center gap-2 text-sm font-medium text-indigo-600 transition-colors hover:text-indigo-500"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
            Start a new calculation
          </Link>
        </div>

        <LeadCaptureModal
          open={showLeadModal}
          onClose={() => setShowLeadModal(false)}
          calculatorData={{
            zipCode: calcData.zipCode,
            fuelType: calcData.fuelType as never,
            newOrUsed: calcData.newOrUsed as never,
            make: calcData.make,
            model: calcData.model,
            incomeRange: calcData.incomeRange,
            filingStatus: calcData.filingStatus,
            affinityGroups: calcData.affinityGroups as never,
          }}
        />
      </div>
    </div>
  );
}
