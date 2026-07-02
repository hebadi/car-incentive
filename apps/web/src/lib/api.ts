import type {
  CalculateIncentivesRequest,
  CalculateIncentivesResponse,
  LeadSubmissionRequest,
  LeadSubmissionResponse,
} from "@incentive-drive/shared";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1";

async function apiFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${body}`);
  }
  return res.json();
}

export function calculateIncentives(
  data: CalculateIncentivesRequest
): Promise<CalculateIncentivesResponse> {
  return apiFetch("/incentives/calculate", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function submitLead(
  data: LeadSubmissionRequest
): Promise<LeadSubmissionResponse> {
  return apiFetch("/leads", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export interface ClaimStep {
  step: number;
  title: string;
  description: string;
  documents?: string[];
  url?: string;
}

export interface IncentiveDetail {
  id: string;
  name: string;
  type: string;
  amount: number;
  sourceUrl: string;
  claimMechanism: string;
  lastVerified?: string;
  endDate?: string | null;
  claimSteps?: ClaimStep[];
}

export interface PurchaseTypeBreakdown {
  incentives: IncentiveDetail[];
  total: number;
  count: number;
}

export interface TopIncentiveResult {
  make: string;
  totalSavings: number;
  incentiveCount: number;
  incentives: IncentiveDetail[];
  byPurchaseType: {
    cash?: PurchaseTypeBreakdown;
    finance?: PurchaseTypeBreakdown;
    lease?: PurchaseTypeBreakdown;
  };
}

export interface TopIncentivesResponse {
  zipCode: string;
  results: TopIncentiveResult[];
}

export function getTopIncentivesByZip(
  zipCode: string
): Promise<TopIncentivesResponse> {
  return apiFetch(`/incentives/top-by-zip?zip_code=${zipCode}`);
}

// ---- Vehicle catalog (dynamic makes/models) ----

export interface VehicleModelInfo2 {
  name: string;
  fuelTypes: string[];
}

export interface VehicleMakesResponse {
  makes: string[];
  source: string;
}

export interface VehicleModelsResponse {
  make: string;
  models: VehicleModelInfo2[];
  source: string;
}

export function getVehicleMakes(): Promise<VehicleMakesResponse> {
  return apiFetch("/vehicles/makes");
}

export function getVehicleModels(
  make: string,
  fuelType?: string
): Promise<VehicleModelsResponse> {
  const params = new URLSearchParams({ make });
  if (fuelType) params.set("fuel_type", fuelType);
  return apiFetch(`/vehicles/models?${params.toString()}`);
}

export interface VehiclePhotoResponse {
  photoUrl: string | null;
}

export function getVehiclePhoto(
  make: string,
  model: string
): Promise<VehiclePhotoResponse> {
  return apiFetch(
    `/incentives/vehicle-photo?make=${encodeURIComponent(make)}&model=${encodeURIComponent(model)}`
  );
}
