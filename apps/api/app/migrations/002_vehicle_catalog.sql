-- Vehicle catalog: dynamic make/model/year inventory synced from MarketCheck API.
-- Replaces hardcoded frontend constants with a database-backed source of truth.

CREATE TABLE vehicle_catalog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    fuel_types VARCHAR(10)[] NOT NULL DEFAULT '{}',
    body_style VARCHAR(50),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source VARCHAR(50) NOT NULL DEFAULT 'marketcheck',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (make, model, year)
);

CREATE INDEX ix_vehicle_catalog_make ON vehicle_catalog (make);
CREATE INDEX ix_vehicle_catalog_make_year ON vehicle_catalog (make, year);
CREATE INDEX ix_vehicle_catalog_active ON vehicle_catalog (is_active);
CREATE INDEX ix_vehicle_catalog_fuel_types ON vehicle_catalog USING GIN (fuel_types);
