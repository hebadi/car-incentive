"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import Link from "next/link";
import LeadCaptureModal from "@/components/LeadCaptureModal";
import {
  getTopIncentivesByZip,
  type TopIncentiveResult,
  type IncentiveDetail,
  type PurchaseTypeBreakdown,
  type ClaimStep,
} from "@/lib/api";
import { getExpirationInfo } from "@/lib/expiration";

const TYPE_COLORS: Record<string, string> = {
  state: "text-green-700 bg-green-50",
  manufacturer: "text-blue-700 bg-blue-50",
  utility: "text-yellow-700 bg-yellow-50",
  federal: "text-purple-700 bg-purple-50",
  affinity: "text-pink-700 bg-pink-50",
};

const PURCHASE_TYPE_LABELS: Record<string, string> = {
  cash: "Cash Purchase",
  finance: "Finance",
  lease: "Lease",
};

const PURCHASE_TYPE_ICONS: Record<string, JSX.Element> = {
  cash: (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
    </svg>
  ),
  finance: (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
    </svg>
  ),
  lease: (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
};

function formatVerifiedDate(iso: string): string {
  const d = new Date(iso);
  return `Verified ${d.toLocaleDateString("en-US", { month: "short", year: "numeric" })}`;
}

function buildLogoUrl(make: string): string {
  const slug = make.toLowerCase().replace(/\s+/g, "-");
  return `https://www.carlogos.org/car-logos/${slug}-logo.png`;
}

function ClaimStepsDark({ steps }: { steps: ClaimStep[] }) {
  return (
    <div className="mt-2 space-y-2 rounded-lg bg-white/5 px-3 py-2">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
        Steps to Claim
      </p>
      <ol className="space-y-1.5">
        {steps.map((s) => (
          <li key={s.step} className="flex gap-2">
            <span className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-[10px] font-bold text-emerald-400">
              {s.step}
            </span>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-slate-200">{s.title}</p>
              <p className="text-[11px] leading-relaxed text-slate-400">{s.description}</p>
              {s.documents && s.documents.length > 0 && (
                <p className="mt-0.5 text-[10px] text-slate-500">
                  Docs needed: {s.documents.join(", ")}
                </p>
              )}
              {s.url && (
                <a
                  href={s.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-0.5 inline-flex items-center gap-1 text-[10px] font-medium text-blue-400 hover:text-blue-300"
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

function IncentiveRow({ inc }: { inc: IncentiveDetail }) {
  const [showClaim, setShowClaim] = useState(false);
  const expiration = inc.endDate ? getExpirationInfo(inc.endDate, "dark") : null;
  const hasClaimSteps = inc.claimSteps && inc.claimSteps.length > 0;

  // Safety net: don't render expired incentives that slipped through
  if (inc.endDate && new Date(inc.endDate) < new Date()) return null;

  return (
    <div className="rounded-lg bg-white/5 px-3 py-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span
            className={`rounded-full px-2 py-0.5 text-[10px] font-semibold ${TYPE_COLORS[inc.type] || "text-gray-700 bg-gray-50"}`}
          >
            {inc.type}
          </span>
          <span className="text-sm text-slate-300">{inc.name}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm font-bold text-emerald-400">
            ${inc.amount.toLocaleString()}
          </span>
          {inc.sourceUrl && (
            <a
              href={inc.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 transition-colors hover:text-blue-400"
              title="Verify source"
            >
              <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
              </svg>
            </a>
          )}
        </div>
      </div>
      <div className="mt-1 flex items-center gap-2">
        {expiration && (
          <span className={`rounded-full px-2 py-0.5 text-[10px] ${expiration.color}`}>
            {expiration.label}
          </span>
        )}
        {inc.lastVerified && (
          <span className="text-[10px] text-slate-500">
            {formatVerifiedDate(inc.lastVerified)}
          </span>
        )}
        {hasClaimSteps && (
          <button
            type="button"
            onClick={() => setShowClaim(!showClaim)}
            className="text-[10px] font-medium text-blue-400 hover:text-blue-300 transition-colors"
          >
            {showClaim ? "Hide steps" : "How to claim"}
          </button>
        )}
      </div>
      {showClaim && hasClaimSteps && (
        <ClaimStepsDark steps={inc.claimSteps!} />
      )}
    </div>
  );
}

function PurchaseTypeTabs({
  byPurchaseType,
  activePurchaseType,
  onSelect,
}: {
  byPurchaseType: TopIncentiveResult["byPurchaseType"];
  activePurchaseType: string;
  onSelect: (pt: string) => void;
}) {
  const types = ["cash", "finance", "lease"].filter(
    (pt) => byPurchaseType[pt as keyof typeof byPurchaseType]
  );

  return (
    <div className="flex gap-1 rounded-lg bg-white/5 p-1">
      {types.map((pt) => {
        const data = byPurchaseType[pt as keyof typeof byPurchaseType]!;
        const isActive = activePurchaseType === pt;
        return (
          <button
            key={pt}
            type="button"
            onClick={() => onSelect(pt)}
            className={`flex flex-1 flex-col items-center gap-0.5 rounded-md px-3 py-2 text-center transition-all ${
              isActive
                ? "bg-white/15 text-white shadow-sm"
                : "text-slate-400 hover:bg-white/5 hover:text-slate-300"
            }`}
          >
            <div className="flex items-center gap-1.5">
              {PURCHASE_TYPE_ICONS[pt]}
              <span className="text-xs font-semibold">
                {PURCHASE_TYPE_LABELS[pt]}
              </span>
            </div>
            <span
              className={`text-lg font-black ${isActive ? "text-emerald-400" : "text-emerald-400/60"}`}
            >
              ${data.total.toLocaleString()}
            </span>
            <span className="text-[10px] text-slate-500">
              {data.count} incentive{data.count !== 1 ? "s" : ""}
            </span>
          </button>
        );
      })}
    </div>
  );
}

export default function TopIncentivesSearch() {
  const [zipCode, setZipCode] = useState("");
  const [results, setResults] = useState<TopIncentiveResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedMake, setExpandedMake] = useState<string | null>(null);
  const [activePurchaseTypes, setActivePurchaseTypes] = useState<Record<string, string>>({});
  const [detectedLocation, setDetectedLocation] = useState<string | null>(null);
  const [showLeadModal, setShowLeadModal] = useState(false);
  const [selectedMake, setSelectedMake] = useState<string | null>(null);
  const hasAutoSearched = useRef(false);

  const runSearch = useCallback(async (zip: string) => {
    if (!/^\d{5}$/.test(zip)) return;
    setLoading(true);
    setError(null);
    setExpandedMake(null);
    setActivePurchaseTypes({});
    try {
      const data = await getTopIncentivesByZip(zip);
      setResults(data.results);
      const defaults: Record<string, string> = {};
      for (const r of data.results) {
        const bp = r.byPurchaseType;
        let bestPt = "cash";
        let bestTotal = 0;
        for (const pt of ["cash", "finance", "lease"] as const) {
          if (bp[pt] && bp[pt]!.total > bestTotal) {
            bestTotal = bp[pt]!.total;
            bestPt = pt;
          }
        }
        defaults[r.make] = bestPt;
      }
      setActivePurchaseTypes(defaults);
    } catch {
      setError("Could not load incentives. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Auto-detect ZIP from IP geolocation on mount
  useEffect(() => {
    if (hasAutoSearched.current) return;
    hasAutoSearched.current = true;

    async function detectZip() {
      try {
        const res = await fetch("https://ipapi.co/json/", { signal: AbortSignal.timeout(4000) });
        if (!res.ok) return;
        const data = await res.json();
        const zip = data.postal;
        const city = data.city;
        const region = data.region_code;
        if (zip && /^\d{5}$/.test(zip)) {
          setZipCode(zip);
          if (city && region) setDetectedLocation(`${city}, ${region}`);
          runSearch(zip);
        }
      } catch {
        // Silently fail — user can enter ZIP manually
      }
    }

    detectZip();
  }, [runSearch]);

  async function handleSearch() {
    if (!/^\d{5}$/.test(zipCode)) {
      setError("Enter a valid 5-digit ZIP code");
      return;
    }
    setDetectedLocation(null); // Clear auto-detect label on manual search
    runSearch(zipCode);
  }

  function getActiveBreakdown(item: TopIncentiveResult): PurchaseTypeBreakdown | null {
    const pt = activePurchaseTypes[item.make] || "cash";
    return item.byPurchaseType[pt as keyof typeof item.byPurchaseType] || null;
  }

  const topResult = results?.[0];
  const restResults = results?.slice(1);

  return (
    <div>
      {/* Search bar */}
      <div className="flex flex-col items-center gap-3">
        {detectedLocation && results && (
          <p className="text-sm text-slate-400">
            Showing deals near{" "}
            <span className="font-semibold text-white">{detectedLocation}</span>
          </p>
        )}
        <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
          <div className="relative">
            <input
              type="text"
              maxLength={5}
              placeholder="Enter ZIP code"
              value={zipCode}
              onChange={(e) => setZipCode(e.target.value.replace(/\D/g, ""))}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="w-48 rounded-xl border border-white/20 bg-white/10 px-5 py-3.5 text-center text-lg font-semibold text-white placeholder-slate-400 backdrop-blur-sm transition-all focus:border-blue-400 focus:bg-white/15 focus:outline-none focus:ring-2 focus:ring-blue-400/30"
            />
          </div>
          <button
            type="button"
            onClick={handleSearch}
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-emerald-500 to-green-500 px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-emerald-500/25 transition-all hover:shadow-emerald-500/40 hover:scale-[1.02] disabled:opacity-50 disabled:hover:scale-100"
          >
            {loading ? (
              <>
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Searching...
              </>
            ) : (
              <>
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                </svg>
                {results ? "Update" : "Find Top Deals"}
              </>
            )}
          </button>
        </div>
      </div>

      {error && (
        <p className="mt-4 text-center text-sm text-red-300">{error}</p>
      )}

      {/* Results */}
      {results !== null && (
        <div className="mt-10">
          {results.length === 0 ? (
            <p className="text-center text-slate-400">
              No incentives found for this ZIP code. Try a different location.
            </p>
          ) : (
            <>
              {/* Top result — hero card */}
              {topResult && (() => {
                const activeData = getActiveBreakdown(topResult);
                return (
                  <div className="mx-auto max-w-2xl">
                    <p className="mb-3 text-center text-xs font-semibold uppercase tracking-widest text-emerald-400">
                      Best Deal in Your Area
                    </p>
                    <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/10 to-white/5 p-6 backdrop-blur-sm transition-all hover:border-white/20">
                      <div className="flex flex-col items-center gap-6 sm:flex-row">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img
                          src={buildLogoUrl(topResult.make)}
                          alt={topResult.make}
                          className="h-20 w-20 object-contain drop-shadow-2xl transition-transform duration-500 group-hover:scale-105"
                        />
                        <div className="flex-1 text-center sm:text-left">
                          <h4 className="text-2xl font-bold text-white">
                            {topResult.make}
                          </h4>
                          <p className="mt-1 text-xs text-slate-400">
                            {topResult.incentiveCount} incentive{topResult.incentiveCount !== 1 ? "s" : ""} available
                          </p>
                        </div>
                      </div>

                      {/* Purchase type tabs */}
                      <div className="mt-5">
                        <PurchaseTypeTabs
                          byPurchaseType={topResult.byPurchaseType}
                          activePurchaseType={activePurchaseTypes[topResult.make] || "cash"}
                          onSelect={(pt) =>
                            setActivePurchaseTypes((prev) => ({ ...prev, [topResult.make]: pt }))
                          }
                        />
                      </div>

                      {/* Incentive breakdown for active purchase type */}
                      {activeData && (
                        <div className="mt-4 space-y-2">
                          <div className="flex items-center justify-between px-1">
                            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                              {PURCHASE_TYPE_LABELS[activePurchaseTypes[topResult.make] || "cash"]} Incentives
                            </p>
                            <p className="bg-gradient-to-r from-emerald-400 to-green-300 bg-clip-text text-2xl font-black text-transparent">
                              ${activeData.total.toLocaleString()}
                            </p>
                          </div>
                          {activeData.incentives.map((inc) => (
                            <IncentiveRow key={inc.id} inc={inc} />
                          ))}
                        </div>
                      )}

                      <div className="mt-4 flex flex-col items-center gap-2 sm:flex-row sm:justify-center">
                        <Link
                          href="/calculator"
                          className="inline-flex items-center gap-1.5 rounded-lg bg-white/10 px-4 py-2 text-xs font-semibold text-white transition-all hover:bg-white/20"
                        >
                          Get personalized savings
                          <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                          </svg>
                        </Link>
                        <button
                          type="button"
                          onClick={() => {
                            setSelectedMake(topResult.make);
                            setShowLeadModal(true);
                          }}
                          className="inline-flex items-center gap-1.5 rounded-lg bg-gradient-to-r from-emerald-500 to-green-500 px-4 py-2 text-xs font-bold text-white shadow-lg shadow-emerald-500/20 transition-all hover:shadow-emerald-500/30 hover:scale-[1.02]"
                        >
                          <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                          </svg>
                          Connect with a Dealer
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })()}

              {/* Rest of results */}
              {restResults && restResults.length > 0 && (
                <div className="mx-auto mt-6 max-w-2xl">
                  <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-slate-500">
                    More deals near you
                  </p>
                  <div className="space-y-2">
                    {restResults.map((item) => {
                      const activeData = getActiveBreakdown(item);
                      return (
                        <div key={item.make}>
                          <button
                            type="button"
                            onClick={() =>
                              setExpandedMake(expandedMake === item.make ? null : item.make)
                            }
                            className="flex w-full items-center justify-between rounded-xl border border-white/10 bg-white/5 px-5 py-4 text-left transition-all hover:bg-white/10"
                          >
                            <div className="flex items-center gap-4">
                              {/* eslint-disable-next-line @next/next/no-img-element */}
                              <img
                                src={buildLogoUrl(item.make)}
                                alt={item.make}
                                className="h-10 w-10 object-contain"
                              />
                              <div>
                                <p className="font-bold text-white">{item.make}</p>
                                <p className="text-xs text-slate-400">
                                  {item.incentiveCount} incentive{item.incentiveCount !== 1 ? "s" : ""}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-3">
                              <span className="text-lg font-bold text-emerald-400">
                                ${item.totalSavings.toLocaleString()}
                              </span>
                              <svg
                                className={`h-4 w-4 text-slate-400 transition-transform ${expandedMake === item.make ? "rotate-180" : ""}`}
                                fill="none"
                                viewBox="0 0 24 24"
                                strokeWidth={2}
                                stroke="currentColor"
                              >
                                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                              </svg>
                            </div>
                          </button>

                          {expandedMake === item.make && (
                            <div className="mt-1 rounded-xl border border-white/5 bg-white/5 p-3">
                              {/* Purchase type tabs */}
                              <PurchaseTypeTabs
                                byPurchaseType={item.byPurchaseType}
                                activePurchaseType={activePurchaseTypes[item.make] || "cash"}
                                onSelect={(pt) =>
                                  setActivePurchaseTypes((prev) => ({
                                    ...prev,
                                    [item.make]: pt,
                                  }))
                                }
                              />
                              {activeData && (
                                <div className="mt-3 space-y-1">
                                  {activeData.incentives.map((inc) => (
                                    <IncentiveRow key={inc.id} inc={inc} />
                                  ))}
                                  <div className="flex justify-center pt-2">
                                    <button
                                      type="button"
                                      onClick={() => {
                                        setSelectedMake(item.make);
                                        setShowLeadModal(true);
                                      }}
                                      className="inline-flex items-center gap-1.5 rounded-lg bg-emerald-500/20 px-3 py-1.5 text-[11px] font-semibold text-emerald-400 transition-all hover:bg-emerald-500/30"
                                    >
                                      <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                                      </svg>
                                      Connect with a {item.make} dealer
                                    </button>
                                  </div>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      <LeadCaptureModal
        open={showLeadModal}
        onClose={() => setShowLeadModal(false)}
        calculatorData={{
          zipCode: zipCode,
          make: selectedMake || undefined,
        }}
      />
    </div>
  );
}
