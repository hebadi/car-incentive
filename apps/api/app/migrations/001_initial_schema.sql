-- IncentiveDrive Initial Schema Migration
-- Version: 001
-- Date: 2026-03-05

-- Enums
CREATE TYPE incentive_type_enum AS ENUM ('federal', 'state', 'manufacturer', 'utility', 'affinity');
CREATE TYPE geographic_scope_enum AS ENUM ('national', 'state', 'county', 'zip', 'utility_territory');
CREATE TYPE incentive_value_type_enum AS ENUM ('fixed', 'percentage', 'tax_credit', 'rate_reduction');
CREATE TYPE funding_status_enum AS ENUM ('open', 'waitlisted', 'depleted', 'suspended');
CREATE TYPE claim_mechanism_enum AS ENUM ('point_of_sale', 'tax_return', 'post_purchase_rebate', 'lease_reduction');
CREATE TYPE lead_tier_enum AS ENUM ('hot', 'warm', 'nurture', 'unqualified');
CREATE TYPE delivery_method_enum AS ENUM ('adf_email', 'crm_api', 'email_plain');
CREATE TYPE delivery_status_enum AS ENUM ('pending', 'sent', 'delivered', 'failed', 'bounced');
CREATE TYPE dealer_subscription_tier_enum AS ENUM ('starter', 'growth', 'enterprise');
CREATE TYPE consent_method_enum AS ENUM ('web_form', 'api');

-- Incentive Programs
CREATE TABLE incentive_programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    type incentive_type_enum NOT NULL,
    source_authority VARCHAR(255) NOT NULL,
    geographic_scope geographic_scope_enum NOT NULL,
    eligible_states VARCHAR(2)[] DEFAULT '{}',
    eligible_zips VARCHAR(10)[] DEFAULT '{}',
    vehicle_criteria JSONB NOT NULL DEFAULT '{}',
    buyer_criteria JSONB NOT NULL DEFAULT '{}',
    incentive_value_type incentive_value_type_enum NOT NULL,
    incentive_amount NUMERIC(12, 2),
    incentive_max_amount NUMERIC(12, 2),
    incentive_percentage NUMERIC(5, 2),
    stackable_with UUID[] DEFAULT '{}',
    mutually_exclusive_with UUID[] DEFAULT '{}',
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ,
    application_deadline TIMESTAMPTZ,
    funding_status funding_status_enum NOT NULL DEFAULT 'open',
    claim_mechanism claim_mechanism_enum NOT NULL,
    last_verified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_url VARCHAR(512) NOT NULL,
    confidence_score FLOAT NOT NULL DEFAULT 0.5,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_incentive_programs_type ON incentive_programs (type);
CREATE INDEX ix_incentive_programs_eligible_states ON incentive_programs USING GIN (eligible_states);
CREATE INDEX ix_incentive_programs_funding_status ON incentive_programs (funding_status);
CREATE INDEX ix_incentive_programs_active ON incentive_programs (is_active);

-- Dealers
CREATE TABLE dealers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    crm_email VARCHAR(255),
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(500) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    makes VARCHAR(50)[] DEFAULT '{}',
    subscription_tier dealer_subscription_tier_enum NOT NULL DEFAULT 'starter',
    stripe_customer_id VARCHAR(100),
    stripe_subscription_id VARCHAR(100),
    max_leads_per_day INTEGER NOT NULL DEFAULT 50,
    min_lead_score INTEGER NOT NULL DEFAULT 20,
    radius_miles INTEGER NOT NULL DEFAULT 25,
    vehicle_type_preferences VARCHAR(50)[] DEFAULT '{}',
    exclusive_leads BOOLEAN NOT NULL DEFAULT FALSE,
    crm_type VARCHAR(50),
    crm_api_config JSONB,
    monthly_budget NUMERIC(10, 2),
    budget_spent_this_month NUMERIC(10, 2) NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_dealers_state ON dealers (state);
CREATE INDEX ix_dealers_zip_code ON dealers (zip_code);
CREATE INDEX ix_dealers_makes ON dealers USING GIN (makes);
CREATE INDEX ix_dealers_active ON dealers (is_active);
CREATE INDEX ix_dealers_subscription_tier ON dealers (subscription_tier);

-- Leads
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    zip_code VARCHAR(10) NOT NULL,
    full_address VARCHAR(500),
    income_range VARCHAR(50),
    vehicle_interest JSONB NOT NULL DEFAULT '{}',
    affinity_groups VARCHAR(50)[] DEFAULT '{}',
    purchase_timeline VARCHAR(50),
    has_trade_in BOOLEAN NOT NULL DEFAULT FALSE,
    score INTEGER NOT NULL DEFAULT 0,
    tier lead_tier_enum NOT NULL DEFAULT 'unqualified',
    matched_incentive_ids UUID[] DEFAULT '{}',
    total_savings_estimate NUMERIC(12, 2) NOT NULL DEFAULT 0,
    source VARCHAR(100) NOT NULL DEFAULT 'web',
    source_ip VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_leads_zip_code ON leads (zip_code);
CREATE INDEX ix_leads_tier ON leads (tier);
CREATE INDEX ix_leads_score ON leads (score);
CREATE INDEX ix_leads_created_at ON leads (created_at);
CREATE INDEX ix_leads_email ON leads (email);

-- Consent Records (TCPA audit trail)
CREATE TABLE consent_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    dealer_id UUID NOT NULL REFERENCES dealers(id) ON DELETE CASCADE,
    consent_timestamp TIMESTAMPTZ NOT NULL,
    consent_ip VARCHAR(45) NOT NULL,
    consent_user_agent VARCHAR(500) NOT NULL,
    consent_page_url VARCHAR(512) NOT NULL,
    consent_language_version VARCHAR(64) NOT NULL,
    consent_method consent_method_enum NOT NULL DEFAULT 'web_form',
    trustedform_cert_url VARCHAR(512),
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revocation_timestamp TIMESTAMPTZ,
    revocation_method VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_consent_records_lead_id ON consent_records (lead_id);
CREATE INDEX ix_consent_records_dealer_id ON consent_records (dealer_id);
CREATE INDEX ix_consent_records_timestamp ON consent_records (consent_timestamp);

-- Lead Deliveries (ADF XML tracking)
CREATE TABLE lead_deliveries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    dealer_id UUID NOT NULL REFERENCES dealers(id) ON DELETE CASCADE,
    delivery_method delivery_method_enum NOT NULL DEFAULT 'adf_email',
    status delivery_status_enum NOT NULL DEFAULT 'pending',
    adf_xml TEXT,
    delivery_email VARCHAR(255),
    error_message TEXT,
    retry_count INTEGER NOT NULL DEFAULT 0,
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_lead_deliveries_lead_id ON lead_deliveries (lead_id);
CREATE INDEX ix_lead_deliveries_dealer_id ON lead_deliveries (dealer_id);
CREATE INDEX ix_lead_deliveries_status ON lead_deliveries (status);

-- Lead-Dealer Matches (many-to-many with routing metadata)
CREATE TABLE lead_dealer_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    dealer_id UUID NOT NULL REFERENCES dealers(id) ON DELETE CASCADE,
    distance_miles DOUBLE PRECISION NOT NULL,
    match_score INTEGER NOT NULL DEFAULT 0,
    is_exclusive BOOLEAN NOT NULL DEFAULT FALSE,
    accepted BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_lead_dealer_matches_lead_id ON lead_dealer_matches (lead_id);
CREATE INDEX ix_lead_dealer_matches_dealer_id ON lead_dealer_matches (dealer_id);
