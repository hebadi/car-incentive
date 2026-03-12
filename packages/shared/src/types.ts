// Enums

export type IncentiveType = "federal" | "state" | "manufacturer" | "utility" | "affinity";

export type GeographicScope = "national" | "state" | "county" | "zip" | "utility_territory";

export type FuelType = "BEV" | "PHEV" | "FCEV" | "ICE";

export type NewOrUsed = "new" | "used" | "both";

export type IncomeType = "AGI" | "MAGI" | "FPL_percentage";

export type IncentiveValueType = "fixed" | "percentage" | "tax_credit" | "rate_reduction";

export type FundingStatus = "open" | "waitlisted" | "depleted" | "suspended";

export type ClaimMechanism = "point_of_sale" | "tax_return" | "post_purchase_rebate" | "lease_reduction";

export type AffinityGroup = "military" | "educator" | "first_responder" | "college_grad" | "first_time_buyer" | "loyalty" | "other";

export type LeadTier = "hot" | "warm" | "nurture" | "unqualified";

export type LeadDeliveryStatus = "pending" | "sent" | "delivered" | "failed" | "bounced";

export type DealerSubscriptionTier = "starter" | "growth" | "enterprise";

export type ConsentMethod = "web_form" | "api";

// Core Models

export interface IncentiveProgram {
  id: string;
  name: string;
  type: IncentiveType;
  sourceAuthority: string;
  geographicScope: GeographicScope;
  eligibleStates: string[];
  eligibleZips: string[];
  vehicleCriteria: {
    fuelTypes: FuelType[];
    makes: string[];
    models: string[];
    yearMin?: number;
    yearMax?: number;
    msrpCap?: number;
    newOrUsed: NewOrUsed;
  };
  buyerCriteria: {
    incomeMax?: number;
    incomeType?: IncomeType;
    filingStatusLimits?: Record<string, number>;
    residencyRequired: boolean;
    tradeInRequired: boolean;
    affinityGroup?: AffinityGroup;
  };
  incentiveValue: {
    type: IncentiveValueType;
    amount?: number;
    maxAmount?: number;
    percentage?: number;
  };
  stackingRules: {
    stackableWith: string[];
    mutuallyExclusiveWith: string[];
  };
  startDate: string;
  endDate?: string;
  applicationDeadline?: string;
  fundingStatus: FundingStatus;
  claimMechanism: ClaimMechanism;
  lastVerified: string;
  sourceUrl: string;
  confidenceScore: number;
}

export interface Lead {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  zipCode: string;
  fullAddress?: string;
  incomeRange?: string;
  vehicleInterest: {
    make?: string;
    model?: string;
    year?: number;
    fuelType?: FuelType;
    newOrUsed?: NewOrUsed;
  };
  affinityGroups: AffinityGroup[];
  purchaseTimeline?: string;
  hasTradeIn: boolean;
  score: number;
  tier: LeadTier;
  matchedIncentives: string[];
  totalSavingsEstimate: number;
  source: string;
  createdAt: string;
  updatedAt: string;
}

export interface Dealer {
  id: string;
  name: string;
  contactEmail: string;
  crmEmail?: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  latitude: number;
  longitude: number;
  makes: string[];
  subscriptionTier: DealerSubscriptionTier;
  maxLeadsPerDay: number;
  minLeadScore: number;
  radiusMiles: number;
  vehicleTypePreferences: string[];
  exclusiveLeads: boolean;
  crmType?: string;
  crmApiConfig?: Record<string, unknown>;
  isActive: boolean;
  createdAt: string;
}

export interface ConsentRecord {
  id: string;
  leadId: string;
  dealerId: string;
  consentTimestamp: string;
  consentIp: string;
  consentUserAgent: string;
  consentPageUrl: string;
  consentLanguageVersion: string;
  consentMethod: ConsentMethod;
  trustedformCertUrl?: string;
  revoked: boolean;
  revocationTimestamp?: string;
  revocationMethod?: string;
}

// API Request/Response Types

export interface CalculateIncentivesRequest {
  zipCode: string;
  vehicleInterest: {
    make?: string;
    model?: string;
    year?: number;
    fuelType?: FuelType;
    newOrUsed?: NewOrUsed;
  };
  buyerProfile: {
    incomeRange?: string;
    filingStatus?: string;
    affinityGroups?: AffinityGroup[];
    hasTradeIn?: boolean;
  };
}

export interface CalculateIncentivesResponse {
  incentives: IncentiveProgram[];
  totalSavings: number;
  confidence: number;
  disclaimers: string[];
}

export interface LeadSubmissionRequest {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  zipCode: string;
  fullAddress?: string;
  incomeRange?: string;
  vehicleInterest: {
    make?: string;
    model?: string;
    year?: number;
    fuelType?: FuelType;
    newOrUsed?: NewOrUsed;
  };
  affinityGroups?: AffinityGroup[];
  purchaseTimeline?: string;
  hasTradeIn?: boolean;
  consentText: string;
  trustedformCertUrl?: string;
}

export interface LeadSubmissionResponse {
  leadId: string;
  score: number;
  tier: LeadTier;
  matchedIncentives: IncentiveProgram[];
  totalSavingsEstimate: number;
  matchedDealerCount: number;
}
