"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function PortalLoginPage() {
  const router = useRouter();
  const [dealerId, setDealerId] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = dealerId.trim();
    if (!trimmed) {
      setError("Please enter a dealer ID.");
      return;
    }
    sessionStorage.setItem("portal_dealer_id", trimmed);
    router.push("/portal/dashboard");
  }

  return (
    <div className="flex min-h-[60vh] items-center justify-center px-4">
      <div className="w-full max-w-md rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">Dealer Portal</h1>
        <p className="mt-2 text-sm text-gray-600">
          Enter your dealer ID to access the portal.
        </p>
        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label htmlFor="dealer-id" className="block text-sm font-medium text-gray-700">
              Dealer ID
            </label>
            <input
              id="dealer-id"
              type="text"
              value={dealerId}
              onChange={(e) => {
                setDealerId(e.target.value);
                setError("");
              }}
              placeholder="e.g. 550e8400-e29b-41d4-a716-446655440000"
              className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
            {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
          </div>
          <button
            type="submit"
            className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            View Portal
          </button>
        </form>
      </div>
    </div>
  );
}
