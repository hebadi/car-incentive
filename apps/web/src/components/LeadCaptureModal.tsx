"use client";

import { useForm } from "react-hook-form";
import { useState } from "react";
import { submitLead } from "@/lib/api";
import { TCPA_CONSENT_TEXT } from "@/lib/constants";
import type { AffinityGroup, FuelType, NewOrUsed } from "@incentive-drive/shared";

interface LeadFormData {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  purchaseTimeline: string;
  hasTradeIn: string;
  consent: boolean;
}

interface LeadCaptureModalProps {
  open: boolean;
  onClose: () => void;
  calculatorData: {
    zipCode: string;
    fuelType?: FuelType;
    newOrUsed?: NewOrUsed;
    make?: string;
    model?: string;
    incomeRange?: string;
    filingStatus?: string;
    affinityGroups?: AffinityGroup[];
    hasTradeIn?: boolean;
  };
}

export default function LeadCaptureModal({
  open,
  onClose,
  calculatorData,
}: LeadCaptureModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LeadFormData>();
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!open) return null;

  async function onSubmit(data: LeadFormData) {
    setSubmitting(true);
    setError(null);
    try {
      await submitLead({
        firstName: data.firstName,
        lastName: data.lastName,
        email: data.email,
        phone: data.phone || undefined,
        zipCode: calculatorData.zipCode,
        incomeRange: calculatorData.incomeRange,
        vehicleInterest: {
          make: calculatorData.make,
          model: calculatorData.model,
          fuelType: calculatorData.fuelType,
          newOrUsed: calculatorData.newOrUsed,
        },
        affinityGroups: calculatorData.affinityGroups,
        purchaseTimeline: data.purchaseTimeline || undefined,
        hasTradeIn: data.hasTradeIn === "yes" ? true : data.hasTradeIn === "no" ? false : undefined,
        consentText: TCPA_CONSENT_TEXT,
      });
      setSubmitted(true);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Connect with a dealer"
    >
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
        {submitted ? (
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
              <svg className="h-6 w-6 text-green-600" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900">
              You&apos;re all set!
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              A dealer in your area will reach out shortly to help you maximize
              your savings.
            </p>
            <button
              onClick={onClose}
              className="mt-6 rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500"
            >
              Close
            </button>
          </div>
        ) : (
          <>
            <div className="flex items-start justify-between">
              <h3 className="text-lg font-semibold text-gray-900">
                Connect with a Dealer
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
                aria-label="Close"
              >
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <p className="mt-1 text-sm text-gray-500">
              Share your contact info so a dealer can help you claim your
              savings.
            </p>

            <form onSubmit={handleSubmit(onSubmit)} className="mt-4 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label htmlFor="lead-firstName" className="block text-sm font-medium text-gray-700">
                    First Name
                  </label>
                  <input
                    id="lead-firstName"
                    type="text"
                    {...register("firstName", { required: "Required" })}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                  {errors.firstName && (
                    <p className="mt-1 text-xs text-red-600" role="alert">
                      {errors.firstName.message}
                    </p>
                  )}
                </div>
                <div>
                  <label htmlFor="lead-lastName" className="block text-sm font-medium text-gray-700">
                    Last Name
                  </label>
                  <input
                    id="lead-lastName"
                    type="text"
                    {...register("lastName", { required: "Required" })}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                  {errors.lastName && (
                    <p className="mt-1 text-xs text-red-600" role="alert">
                      {errors.lastName.message}
                    </p>
                  )}
                </div>
              </div>

              <div>
                <label htmlFor="lead-email" className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  id="lead-email"
                  type="email"
                  {...register("email", {
                    required: "Required",
                    pattern: {
                      value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                      message: "Invalid email address",
                    },
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                {errors.email && (
                  <p className="mt-1 text-xs text-red-600" role="alert">
                    {errors.email.message}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="lead-phone" className="block text-sm font-medium text-gray-700">
                  Phone Number
                </label>
                <input
                  id="lead-phone"
                  type="tel"
                  {...register("phone", {
                    pattern: {
                      value: /^[\d\s\-().+]{7,15}$/,
                      message: "Invalid phone number",
                    },
                  })}
                  placeholder="(555) 123-4567"
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                {errors.phone && (
                  <p className="mt-1 text-xs text-red-600" role="alert">
                    {errors.phone.message}
                  </p>
                )}
              </div>

              {/* Optional fields */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label htmlFor="lead-timeline" className="block text-sm font-medium text-gray-700">
                    Purchase Timeline
                    <span className="ml-1 text-xs font-normal text-gray-400">(optional)</span>
                  </label>
                  <select
                    id="lead-timeline"
                    {...register("purchaseTimeline")}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="">Not sure</option>
                    <option value="immediate">Ready now</option>
                    <option value="within_30_days">Within 30 days</option>
                    <option value="1_3_months">1-3 months</option>
                    <option value="3_6_months">3-6 months</option>
                    <option value="just_browsing">Just browsing</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="lead-tradein" className="block text-sm font-medium text-gray-700">
                    Have a Trade-In?
                    <span className="ml-1 text-xs font-normal text-gray-400">(optional)</span>
                  </label>
                  <select
                    id="lead-tradein"
                    {...register("hasTradeIn")}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="">Not sure</option>
                    <option value="yes">Yes</option>
                    <option value="no">No</option>
                  </select>
                </div>
              </div>

              <div className="rounded-md border border-gray-200 bg-gray-50 p-3">
                <label className="flex items-start gap-2">
                  <input
                    type="checkbox"
                    {...register("consent", {
                      required: "You must consent to be contacted",
                    })}
                    className="mt-0.5 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-xs leading-relaxed text-gray-600">
                    {TCPA_CONSENT_TEXT}
                  </span>
                </label>
                {errors.consent && (
                  <p className="mt-1 text-xs text-red-600" role="alert">
                    {errors.consent.message}
                  </p>
                )}
              </div>

              {error && (
                <p className="text-sm text-red-600" role="alert">{error}</p>
              )}

              <button
                type="submit"
                disabled={submitting}
                className="w-full rounded-md bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
              >
                {submitting ? "Submitting..." : "Submit"}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
