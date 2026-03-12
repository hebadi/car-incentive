"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import ProgressBar from "@/components/ProgressBar";
import CarImage from "@/components/CarImage";
import {
  VEHICLE_MAKES,
  VEHICLE_MODELS,
  INCOME_RANGES,
  FILING_STATUSES,
  AFFINITY_OPTIONS,
  type FuelTypeKey,
} from "@/lib/constants";
import { calculateIncentives } from "@/lib/api";
import type { FuelType, NewOrUsed, AffinityGroup } from "@incentive-drive/shared";

interface CalculatorFormData {
  zipCode: string;
  fuelType: FuelType | "";
  newOrUsed: NewOrUsed | "";
  make: string;
  model: string;
  budgetMin: number;
  budgetMax: number;
  incomeRange: string;
  filingStatus: string;
  affinityGroups: AffinityGroup[];
}

const STEP_INFO = [
  {
    number: 1,
    title: "Location & Vehicle Type",
    subtitle: "Where you live determines which incentives are available",
  },
  {
    number: 2,
    title: "Vehicle Preferences",
    subtitle: "Help us find model-specific incentives",
  },
  {
    number: 3,
    title: "Eligibility Information",
    subtitle: "Some incentives have income requirements",
  },
  {
    number: 4,
    title: "Special Affiliations",
    subtitle: "Unlock exclusive discounts for qualifying groups",
  },
];

export default function CalculatorPage() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const {
    register,
    handleSubmit,
    watch,
    trigger,
    getValues,
    formState: { errors },
  } = useForm<CalculatorFormData>({
    defaultValues: {
      zipCode: "",
      fuelType: "",
      newOrUsed: "",
      make: "",
      model: "",
      budgetMin: 25000,
      budgetMax: 50000,
      incomeRange: "",
      filingStatus: "",
      affinityGroups: [],
    },
  });

  const selectedMake = watch("make");
  const selectedModel = watch("model");
  const selectedFuelType = watch("fuelType");
  const budgetMax = watch("budgetMax");

  async function goNext() {
    const fieldsToValidate: (keyof CalculatorFormData)[][] = [
      ["zipCode", "fuelType", "newOrUsed"],
      [],
      [],
      [],
    ];
    const valid = await trigger(fieldsToValidate[step - 1]);
    if (valid) setStep((s) => Math.min(s + 1, 4));
  }

  function goBack() {
    setStep((s) => Math.max(s - 1, 1));
  }

  async function onSubmit(data: CalculatorFormData) {
    setLoading(true);
    setError(null);
    try {
      const result = await calculateIncentives({
        zipCode: data.zipCode,
        vehicleInterest: {
          make: data.make || undefined,
          model: data.model || undefined,
          fuelType: (data.fuelType as FuelType) || undefined,
          newOrUsed: (data.newOrUsed as NewOrUsed) || undefined,
        },
        buyerProfile: {
          incomeRange: data.incomeRange || undefined,
          filingStatus: data.filingStatus || undefined,
          affinityGroups: data.affinityGroups.length
            ? data.affinityGroups
            : undefined,
        },
      });

      // Store results and form data in sessionStorage for the results page
      sessionStorage.setItem(
        "incentiveResults",
        JSON.stringify(result)
      );
      sessionStorage.setItem(
        "calculatorData",
        JSON.stringify(data)
      );
      router.push("/results");
    } catch {
      setError("Failed to calculate incentives. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  const currentStepInfo = STEP_INFO[step - 1];

  return (
    <div className="min-h-[80vh] bg-gradient-to-b from-slate-50 to-white">
      <div className="mx-auto max-w-2xl px-4 py-10">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900">
            Incentive Calculator
          </h2>
          <p className="mt-2 text-sm text-gray-500">
            Answer a few questions to find all the savings you qualify for.
          </p>
        </div>

        <div className="mt-8">
          <ProgressBar currentStep={step} />
        </div>

        {/* Step info card */}
        <div className="mb-2 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 p-4 text-white shadow-lg shadow-indigo-500/20">
          <div className="flex items-center gap-3">
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white/20 text-sm font-bold">
              {currentStepInfo.number}
            </span>
            <div>
              <h3 className="font-semibold">{currentStepInfo.title}</h3>
              <p className="text-xs text-indigo-200">{currentStepInfo.subtitle}</p>
            </div>
          </div>
        </div>

        <form
          onSubmit={(e) => e.preventDefault()}
          className="mt-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-lg shadow-gray-100/50 transition-all duration-300"
        >
          {/* Step 1: Location & Vehicle Type */}
          <div className={`transition-all duration-300 ${step === 1 ? "block" : "hidden"}`}>
            <fieldset className="space-y-5">
              <legend className="sr-only">
                Location &amp; Vehicle Type
              </legend>
              <div>
                <label
                  htmlFor="calc-zipCode"
                  className="block text-sm font-medium text-gray-700"
                >
                  ZIP Code *
                </label>
                <input
                  id="calc-zipCode"
                  type="text"
                  maxLength={5}
                  placeholder="e.g. 90210"
                  {...register("zipCode", {
                    required: "ZIP code is required",
                    pattern: {
                      value: /^\d{5}$/,
                      message: "Enter a valid 5-digit ZIP code",
                    },
                  })}
                  className="mt-1 block w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                />
                {errors.zipCode && (
                  <p className="mt-1 text-xs text-red-600" role="alert">
                    {errors.zipCode.message}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="calc-fuelType"
                  className="block text-sm font-medium text-gray-700"
                >
                  Vehicle Type *
                </label>
                <select
                  id="calc-fuelType"
                  {...register("fuelType", {
                    required: "Please select a vehicle type",
                  })}
                  className="mt-1 block w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                >
                  <option value="">Select type</option>
                  <option value="BEV">Battery Electric (BEV)</option>
                  <option value="PHEV">Plug-in Hybrid (PHEV)</option>
                  <option value="FCEV">Fuel Cell (FCEV)</option>
                  <option value="ICE">Gas / Diesel (ICE)</option>
                </select>
                {errors.fuelType && (
                  <p className="mt-1 text-xs text-red-600" role="alert">
                    {errors.fuelType.message}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="calc-newOrUsed"
                  className="block text-sm font-medium text-gray-700"
                >
                  New or Used *
                </label>
                <select
                  id="calc-newOrUsed"
                  {...register("newOrUsed", {
                    required: "Please select new or used",
                  })}
                  className="mt-1 block w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                >
                  <option value="">Select</option>
                  <option value="new">New</option>
                  <option value="used">Used</option>
                  <option value="both">Either / Not Sure</option>
                </select>
                {errors.newOrUsed && (
                  <p className="mt-1 text-xs text-red-600" role="alert">
                    {errors.newOrUsed.message}
                  </p>
                )}
              </div>
            </fieldset>
          </div>

          {/* Step 2: Make/Model & Budget */}
          <div className={`transition-all duration-300 ${step === 2 ? "block" : "hidden"}`}>
            <fieldset className="space-y-5">
              <legend className="sr-only">
                Vehicle Preferences
              </legend>
              <p className="text-sm text-gray-500">
                These are optional but help us find more specific incentives.
              </p>

              <div>
                <label
                  htmlFor="calc-make"
                  className="block text-sm font-medium text-gray-700"
                >
                  Make
                </label>
                <select
                  id="calc-make"
                  {...register("make")}
                  className="mt-1 block w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                >
                  <option value="">Any / Not sure</option>
                  {VEHICLE_MAKES.map((make) => (
                    <option key={make} value={make}>
                      {make}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label
                  htmlFor="calc-model"
                  className="block text-sm font-medium text-gray-700"
                >
                  Model
                </label>
                <select
                  id="calc-model"
                  {...register("model")}
                  disabled={!selectedMake}
                  className="mt-1 block w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:bg-gray-100 disabled:text-gray-400"
                >
                  <option value="">{selectedMake ? "Select model" : "Select a make first"}</option>
                  {selectedMake && VEHICLE_MODELS[selectedMake]?.map((m) => {
                    const matchesFuelType = !selectedFuelType || m.fuelTypes.includes(selectedFuelType as FuelTypeKey);
                    return (
                      <option
                        key={m.name}
                        value={m.name}
                        disabled={!matchesFuelType}
                        className={matchesFuelType ? "" : "text-gray-400"}
                      >
                        {m.name}{!matchesFuelType ? " (not available as " + selectedFuelType + ")" : ""}
                      </option>
                    );
                  })}
                </select>
              </div>

              {/* Car image preview */}
              {selectedMake && selectedModel && (
                <div className="relative overflow-hidden rounded-2xl">
                  <CarImage make={selectedMake} model={selectedModel} size="lg" className="w-full" />
                </div>
              )}

              <div>
                <label
                  htmlFor="calc-budget"
                  className="block text-sm font-medium text-gray-700"
                >
                  Budget Range: up to ${budgetMax?.toLocaleString() || "50,000"}
                </label>
                <input
                  id="calc-budget"
                  type="range"
                  min={15000}
                  max={150000}
                  step={5000}
                  {...register("budgetMax", { valueAsNumber: true })}
                  className="mt-2 w-full accent-indigo-600"
                />
                <div className="mt-1 flex justify-between text-xs text-gray-400">
                  <span>$15,000</span>
                  <span>$150,000</span>
                </div>
              </div>
            </fieldset>
          </div>

          {/* Step 3: Income & Filing Status */}
          <div className={`transition-all duration-300 ${step === 3 ? "block" : "hidden"}`}>
            <fieldset className="space-y-5">
              <legend className="sr-only">
                Eligibility Information
              </legend>
              <p className="text-sm text-gray-500">
                Some incentives have income limits. This helps us check your
                eligibility.
              </p>

              <div>
                <label
                  htmlFor="calc-income"
                  className="block text-sm font-medium text-gray-700"
                >
                  Annual Household Income
                </label>
                <select
                  id="calc-income"
                  {...register("incomeRange")}
                  className="mt-1 block w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                >
                  <option value="">Prefer not to say</option>
                  {INCOME_RANGES.map((range) => (
                    <option key={range.value} value={range.value}>
                      {range.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label
                  htmlFor="calc-filing"
                  className="block text-sm font-medium text-gray-700"
                >
                  Tax Filing Status
                </label>
                <select
                  id="calc-filing"
                  {...register("filingStatus")}
                  className="mt-1 block w-full rounded-xl border border-gray-300 px-4 py-3 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                >
                  <option value="">Prefer not to say</option>
                  {FILING_STATUSES.map((status) => (
                    <option key={status.value} value={status.value}>
                      {status.label}
                    </option>
                  ))}
                </select>
              </div>
            </fieldset>
          </div>

          {/* Step 4: Affinities */}
          <div className={`transition-all duration-300 ${step === 4 ? "block" : "hidden"}`}>
            <fieldset className="space-y-5">
              <legend className="sr-only">
                Special Affiliations
              </legend>
              <p className="text-sm text-gray-500">
                Many manufacturers and programs offer extra discounts for these
                groups. Check all that apply.
              </p>

              <div className="space-y-3">
                {AFFINITY_OPTIONS.map((option) => (
                  <label
                    key={option.value}
                    className="flex items-center gap-3 rounded-xl border border-gray-200 p-4 transition-all hover:border-indigo-300 hover:bg-indigo-50/50 has-[:checked]:border-indigo-400 has-[:checked]:bg-indigo-50"
                  >
                    <input
                      type="checkbox"
                      value={option.value}
                      {...register("affinityGroups")}
                      className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    <span className="text-sm font-medium text-gray-700">{option.label}</span>
                  </label>
                ))}
              </div>
            </fieldset>
          </div>

          {error && (
            <p className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600" role="alert">{error}</p>
          )}

          {/* Navigation */}
          <div className="mt-8 flex items-center justify-between">
            {step > 1 ? (
              <button
                type="button"
                onClick={goBack}
                className="inline-flex items-center gap-2 rounded-xl border border-gray-300 px-5 py-2.5 text-sm font-medium text-gray-700 transition-all hover:bg-gray-50 hover:border-gray-400"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
                </svg>
                Back
              </button>
            ) : (
              <div />
            )}

            {step < 4 ? (
              <button
                type="button"
                onClick={goNext}
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/20 transition-all hover:shadow-indigo-500/30 hover:from-indigo-500 hover:to-blue-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                Next
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
              </button>
            ) : (
              <button
                type="button"
                disabled={loading}
                onClick={() => handleSubmit(onSubmit)()}
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-green-600 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-emerald-500/20 transition-all hover:shadow-emerald-500/30 hover:from-emerald-500 hover:to-green-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    Calculating...
                  </>
                ) : (
                  <>
                    See My Savings
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </>
                )}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
