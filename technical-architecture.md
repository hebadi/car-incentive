# MVP Technical Architecture: Automotive Incentive-Based Lead Generation Platform

**Version:** 1.0
**Date:** March 2026

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Lead Sourcing Strategy](#2-lead-sourcing-strategy)
3. [Incentive Matching Engine](#3-incentive-matching-engine)
4. [Lead Scoring and Qualification Pipeline](#4-lead-scoring-and-qualification-pipeline)
5. [CRM/DMS Integrations](#5-crmdms-integrations)
6. [Data Pipeline Architecture](#6-data-pipeline-architecture)
7. [Minimum Viable Tech Stack](#7-minimum-viable-tech-stack)
8. [Build vs Buy Decisions](#8-build-vs-buy-decisions)
9. [MVP Scope and Phased Roadmap](#9-mvp-scope-and-phased-roadmap)
10. [Infrastructure and Scalability](#10-infrastructure-and-scalability)
11. [Security and Compliance](#11-security-and-compliance)
12. [Cost Estimates](#12-cost-estimates)
13. [Sources](#13-sources)

---

## 1. System Overview

### Value Proposition

The platform matches car buyers with the maximum available incentives (state rebates, manufacturer cash, OEM financing, utility rebates, affinity discounts) and delivers these high-intent, incentive-qualified leads to dealerships. With federal EV credits terminated as of September 30, 2025, consumers face a fragmented landscape of state, manufacturer, and utility incentives that is difficult to navigate -- creating a clear opportunity for an aggregation and matching service.

### Architecture Diagram

```
                              +---------------------------+
                              |    Consumer-Facing Web    |
                              |    (Next.js / React SPA)  |
                              |                           |
                              |  - Incentive Calculator   |
                              |  - Vehicle Finder         |
                              |  - Savings Estimator      |
                              +------------+--------------+
                                           |
                                      HTTPS/REST
                                           |
                         +-----------------v------------------+
                         |          API Gateway               |
                         |     (AWS API Gateway / Kong)       |
                         +-----------------+------------------+
                                           |
              +----------------------------+----------------------------+
              |                            |                            |
   +----------v----------+    +------------v-----------+    +-----------v-----------+
   |   Lead Capture &    |    |   Incentive Matching   |    |   Dealer Portal       |
   |   Qualification     |    |   Engine               |    |   & Lead Delivery     |
   |   Service           |    |                        |    |                       |
   |  (Python/FastAPI)   |    |  (Python/FastAPI)      |    |  (Next.js + API)      |
   +----------+----------+    +------------+-----------+    +-----------+-----------+
              |                            |                            |
              +----------------------------+----------------------------+
                                           |
                              +------------v-----------+
                              |   PostgreSQL (Primary)  |
                              |   + Redis (Cache/Queue) |
                              +------------+-----------+
                                           |
              +----------------------------+----------------------------+
              |                            |                            |
   +----------v----------+    +------------v-----------+    +-----------v-----------+
   |  Incentive Data     |    |  Inventory Data        |    |  CRM/DMS Integration  |
   |  Pipeline           |    |  Pipeline              |    |  Layer                |
   |                     |    |                        |    |                       |
   |  - State programs   |    |  - Dealer feeds        |    |  - ADF XML leads      |
   |  - OEM incentives   |    |  - MarketCheck API     |    |  - Fortellis APIs     |
   |  - Utility rebates  |    |  - Scraping fallback   |    |  - VinSolutions API   |
   |  - AFDC data        |    |                        |    |  - Email fallback     |
   +---------------------+    +------------------------+    +-----------------------+

   +-----------------------------------------------------------------------+
   |                    Background Workers (Celery / ARQ)                   |
   |                                                                        |
   |  - Incentive data refresh (daily/weekly)                               |
   |  - Lead scoring model execution                                        |
   |  - CRM delivery + retry logic                                          |
   |  - Consent audit logging                                               |
   +-----------------------------------------------------------------------+

   +-----------------------------------------------------------------------+
   |                    Observability & Analytics                           |
   |                                                                        |
   |  - PostHog (product analytics)      - Sentry (error tracking)          |
   |  - Grafana + Prometheus (infra)     - Lead attribution tracking        |
   +-----------------------------------------------------------------------+
```

### Core Data Flow

1. **Consumer** visits site, enters ZIP code, vehicle preferences, and basic financial info
2. **Incentive Engine** computes all applicable federal (30C charger credit), state, OEM, utility, and affinity incentives
3. **Savings Estimator** presents total potential savings, broken down by source
4. **Lead Capture** collects contact info with TCPA-compliant consent
5. **Lead Scoring** qualifies the lead based on intent signals and incentive match quality
6. **Lead Delivery** routes the scored lead to matched dealer(s) via ADF XML, CRM API, or email
7. **Dealer Portal** provides lead management, performance analytics, and ROI tracking

---

## 2. Lead Sourcing Strategy

### Phase 1: Organic Inbound (Months 1-6)

The primary strategy is to generate inbound leads by providing genuine value -- an incentive calculator that consumers cannot easily find elsewhere.

**Content-Driven Acquisition:**
- SEO-optimized pages for every state incentive program (50 states x multiple programs)
- Long-tail keyword targeting: "EV rebate [state] 2026", "how to stack car incentives", "[vehicle model] incentives near me"
- Incentive calculator as the primary conversion tool (ZIP code entry -> personalized savings)
- Blog content on incentive changes, seasonal buying guides, model-specific savings breakdowns

**Estimated Cost:** $2,000-5,000/month (content writers + SEO tools)
**Expected CPL:** $15-40 (organic traffic converts at higher rates due to intent)

### Phase 2: Paid Acquisition (Months 4-9)

**Google Ads:**
- Target high-intent keywords: "best car deals [city]", "[model] rebates 2026", "EV incentives [state]"
- Google Vehicle Ads integration for inventory-specific ads
- Expected CPL: $25-45 (in line with automotive SEM benchmarks)

**Facebook/Meta:**
- Lead form ads with instant incentive estimate as the hook
- Lookalike audiences based on converted leads
- Expected CPL: $20-30

**Programmatic/Geofenced:**
- Geofence competitor dealerships and auto shows
- Retarget site visitors who used the calculator but did not submit contact info

### Phase 3: Partnerships & Scale (Months 6-12)

**Affiliate/Widget Strategy:**
- Embeddable incentive calculator widget for financial blogs, automotive review sites, credit unions
- Revenue share on leads generated through partner widgets

**Credit Union & Financial Institution Partnerships:**
- Pre-purchase incentive check integrated into auto loan applications
- White-label calculator for credit union websites

**Data Partnerships:**
- Purchase in-market shopper intent data from Polk/S&P Global Mobility or Oracle Data Cloud
- Enrich existing leads with purchase likelihood scores

### Lead Volume Projections (Year 1)

| Quarter | Monthly Leads | Primary Source | Estimated CPL |
|---------|--------------|----------------|---------------|
| Q1 | 500-1,000 | SEO + beta dealers | $30-50 |
| Q2 | 1,500-3,000 | SEO + paid ads | $25-40 |
| Q3 | 3,000-6,000 | SEO + paid + affiliates | $20-35 |
| Q4 | 6,000-12,000 | All channels | $15-30 |

---

## 3. Incentive Matching Engine

### Data Model

```
IncentiveProgram
  - id (UUID)
  - name (string)
  - type (enum: federal, state, manufacturer, utility, affinity)
  - source_authority (string)             # e.g., "California CARB", "Hyundai USA"
  - geographic_scope (enum + details)     # national, state, county, zip, utility_territory
  - eligible_states[] / eligible_zips[]
  - vehicle_criteria:
      - fuel_types[] (BEV, PHEV, FCEV, ICE)
      - make[], model[], year_range
      - msrp_cap (decimal)
      - new_or_used (enum)
  - buyer_criteria:
      - income_max (decimal)
      - income_type (enum: AGI, MAGI, FPL_percentage)
      - filing_status_limits{}
      - residency_requirements
      - trade_in_required (boolean)
      - affinity_group (enum: military, educator, first_responder, etc.)
  - incentive_value:
      - type (enum: fixed, percentage, tax_credit, rate_reduction)
      - amount (decimal)
      - max_amount (decimal)
      - percentage (decimal)
  - stacking_rules:
      - stackable_with[] (program IDs)
      - mutually_exclusive_with[] (program IDs)
  - timing:
      - start_date, end_date
      - application_deadline
      - funding_status (enum: open, waitlisted, depleted, suspended)
  - claim_mechanism (enum: point_of_sale, tax_return, post_purchase_rebate, lease_reduction)
  - last_verified (timestamp)
  - source_url (string)
  - confidence_score (0-1)
```

### Matching Algorithm

```python
def match_incentives(buyer_profile, vehicle, zip_code):
    """
    Returns ranked list of applicable incentives with total savings estimate.
    """
    # 1. Geographic filter: state, county, zip, utility territory
    candidates = filter_by_geography(all_active_incentives, zip_code)

    # 2. Vehicle filter: fuel type, make/model, MSRP, new/used
    candidates = filter_by_vehicle(candidates, vehicle)

    # 3. Buyer filter: income, filing status, residency, affinity groups
    candidates = filter_by_buyer(candidates, buyer_profile)

    # 4. Stacking resolver: handle mutual exclusions, choose optimal combo
    optimal_stack = resolve_stacking(candidates)

    # 5. Compute total savings
    total = sum(compute_value(i, vehicle) for i in optimal_stack)

    return IncentiveResult(
        incentives=optimal_stack,
        total_savings=total,
        confidence=min(i.confidence_score for i in optimal_stack),
        disclaimers=generate_disclaimers(optimal_stack)
    )
```

### Stacking Resolution

The stacking resolver handles mutual exclusions (e.g., 0% APR vs cash rebate). For each set of mutually exclusive incentives, it computes the net present value of each option and recommends the financially optimal choice. This is critical -- as noted in our research, "taking the cash + credit union financing saves more than 0% APR" in many cases.

### Incentive Data Sources and Refresh

| Source | Method | Refresh Frequency | Data Quality |
|--------|--------|-------------------|--------------|
| State program websites | Structured scraping + manual verification | Weekly | High (verified) |
| AFDC (afdc.energy.gov) | Data download / scraping | Weekly | High (government source) |
| MarketCheck OEM Incentive Feed | API ($) | Weekly (real-time available) | High (sourced from OEM sites) |
| JD Power ChromeData API | API ($$) | Real-time | Highest (industry standard) |
| OEM websites | Structured scraping | Weekly | Medium-High |
| Utility company programs | Manual + scraping | Monthly | Medium (fragmented) |
| Manufacturer incentive bulletins | Industry contacts + scraping | Weekly | Medium-High |

**MVP approach:** Start with manual curation of top 15 states (covering ~80% of EV sales) + MarketCheck API for OEM incentives. Expand automated scraping and premium APIs as revenue supports.

### Confidence Scoring

Each incentive gets a confidence score based on:
- **1.0**: Verified via official API or government data feed within last 7 days
- **0.8-0.9**: Scraped from official source within last 14 days
- **0.6-0.7**: Scraped from third-party source or manually entered within last 30 days
- **Below 0.5**: Stale data, flagged for re-verification

Consumer-facing results show disclaimers for anything below 0.8, with links to official sources.

---

## 4. Lead Scoring and Qualification Pipeline

### Scoring Model

```
LeadScore (0-100) = weighted sum of:

  Intent Signals (40%):
    - Used incentive calculator: +15
    - Viewed specific vehicle: +10
    - Used trade-in estimator: +10
    - Visited pricing/payment page: +10
    - Return visit within 7 days: +10
    - Shared results / saved calculation: +5

  Incentive Match Quality (30%):
    - Total savings >= $5,000: +15
    - Eligible for 3+ stacking incentives: +10
    - Time-sensitive incentive (expiring within 60 days): +10
    - Depleting program (funding running low): +10

  Buyer Readiness (20%):
    - Provided phone number: +10
    - Provided full address (not just ZIP): +5
    - Indicated purchase timeline < 30 days: +10
    - Has trade-in vehicle: +5

  Data Completeness (10%):
    - All required fields filled: +5
    - Income range provided: +3
    - Vehicle preference specified (make/model): +5
```

### Lead Tiers

| Tier | Score | Delivery | Dealer SLA | Pricing Model |
|------|-------|----------|------------|---------------|
| Hot | 80-100 | Real-time push (< 60 seconds) | Contact within 5 min | Premium CPL |
| Warm | 50-79 | Batched (every 15 min) | Contact within 30 min | Standard CPL |
| Nurture | 20-49 | Daily digest | Contact within 24 hours | Discounted CPL or subscription |
| Unqualified | 0-19 | Not delivered | -- | Recycled via email nurture |

### Lead Routing Logic

```
1. Match lead to dealers by:
   - ZIP code radius (configurable per dealer, default 25 miles)
   - Makes/models the dealer carries (franchise filter)
   - Dealer's active subscription status and budget remaining

2. Apply dealer preferences:
   - Max leads per day cap
   - Vehicle type preferences (new, used, EV, truck, etc.)
   - Minimum lead score threshold

3. Distribution rules:
   - Exclusive leads: sent to one dealer only (premium pricing)
   - Shared leads: sent to 2-3 dealers max (standard pricing)
   - Never more than 3 dealers per lead (quality commitment)

4. Failover:
   - If no matched dealer accepts within SLA, expand radius
   - If still unmatched, route to nurture queue
```

---

## 5. CRM/DMS Integrations

### Integration Landscape

The CRM/DMS market is dominated by a few players with varying levels of openness to third-party integration:

| System | Market Share | Integration Approach | Cost to Integrate | Difficulty |
|--------|-------------|---------------------|-------------------|------------|
| **VinSolutions** (Cox) | ~25% franchise | ADF XML email (universal); Connect CRM API (partnership required) | $0 (ADF) / negotiable (API) | Low (ADF) / Medium (API) |
| **Elead** (CDK) | ~20% franchise | ADF XML; Fortellis Marketplace APIs (Lead Delivery API, Sales Customer API) | $0 (ADF) / $50-150/store/month (Fortellis) | Low (ADF) / Medium-High (Fortellis) |
| **DriveCentric** | Growing | ADF XML; Partner API program (3 tiers: data providers, strategic integrations, add-ons) | $0 (ADF) / negotiable | Low (ADF) / Medium (API) |
| **DealerSocket** | ~15% | ADF XML; proprietary API | $0 (ADF) / custom | Low (ADF) / High |
| **CDK Drive DMS** | ~40% DMS | Fortellis Marketplace APIs (6.7B transactions/year, 82K dealer integrations) | $50-150/store/month | High (certification required) |
| **Reynolds & Reynolds DMS** | ~30% DMS | Reynolds Certified Interface (RCI) -- STAR-compliant | $50-150/store/month + certification | Very High (restrictive) |
| **Dealertrack DMS** (Cox) | ~16% DMS | More open API; Cox ecosystem integration | Negotiable | Medium |

### MVP Integration Strategy

**Phase 1 (MVP): ADF XML via Email -- Universal Compatibility**

ADF (Auto-lead Data Format) 1.0 is the industry standard XML format for lead delivery. Every CRM system accepts it. This is the fastest path to market.

```xml
<?ADF VERSION "1.0"?>
<?XML VERSION "1.0"?>
<adf>
  <prospect status="new">
    <requestdate>2026-03-05T10:30:00-05:00</requestdate>
    <vehicle interest="buy" status="new">
      <year>2026</year>
      <make>Hyundai</make>
      <model>IONIQ 5</model>
      <trim>SEL</trim>
    </vehicle>
    <customer>
      <contact>
        <name part="first">Jane</name>
        <name part="last">Smith</name>
        <email>jane.smith@email.com</email>
        <phone type="cellphone">555-123-4567</phone>
      </contact>
      <comments>
        Qualified for $2,000 NYSERDA Drive Clean Rebate +
        $500 Hyundai military discount +
        0% APR 60mo available.
        Total estimated savings: $2,500+ off MSRP.
        Lead Score: 85 (Hot). Source: IncentiveMatch.
      </comments>
    </customer>
    <vendor>
      <contact>
        <name part="full">ABC Hyundai</name>
      </contact>
    </vendor>
    <provider>
      <name part="full">IncentiveMatch</name>
      <url>https://www.incentivematch.com</url>
    </provider>
  </prospect>
</adf>
```

**Delivery:** SMTP to dealer's CRM intake email address. Every CRM has one. Zero integration cost.

**Phase 2 (Month 6+): Direct CRM API Integration**

Priority order based on market share and API accessibility:
1. **VinSolutions Connect CRM API** -- largest market share, Cox ecosystem is relatively open
2. **Elead via Fortellis Lead Delivery API** -- CDK's marketplace is growing (NADA 2026 showed new tools)
3. **DriveCentric Partner API** -- growing CRM with modern API-first approach
4. **Tekion** -- cloud-native, API-friendly, but smaller installed base

Benefits of direct API over ADF email:
- Real-time delivery (vs 1-5 min email delay)
- Structured data fields (not free-text comments)
- Bi-directional: receive lead status updates, disposition codes, close rates
- Better attribution and ROI reporting

**Phase 3 (Year 2+): DMS Integration via Fortellis**

Publish as a Fortellis Marketplace app to access CDK Drive DMS stores directly. This enables:
- Inventory feed integration (real-time stock awareness)
- Deal outcome tracking (closed/lost attribution)
- Service customer data for equity mining partnerships

### Integration Cost Summary

| Phase | Method | Per-Store Cost | Dev Effort | Coverage |
|-------|--------|---------------|------------|----------|
| 1 | ADF XML email | $0 | 2 weeks | ~95% of dealers |
| 2 | CRM APIs (top 3) | $0-150/store/mo | 2-3 months | ~60% of franchise dealers |
| 3 | Fortellis DMS | $50-150/store/mo | 3-6 months | ~40% DMS market (CDK) |

---

## 6. Data Pipeline Architecture

### Pipeline Overview

```
+-------------------+     +-------------------+     +-------------------+
|  Data Ingestion   | --> |  Processing &     | --> |  Serving Layer    |
|                   |     |  Normalization    |     |                   |
|  - API pulls      |     |  - Validation     |     |  - REST API       |
|  - Web scrapers   |     |  - Dedup          |     |  - Cached lookups |
|  - Manual entry   |     |  - Enrichment     |     |  - Real-time calc |
|  - File imports   |     |  - Scoring        |     |  - Exports        |
+-------------------+     +-------------------+     +-------------------+
        |                         |                         |
        v                         v                         v
  +----------+            +-----------+              +----------+
  | Raw Store|            | Processed |              | Read     |
  | (S3)     |            | (Postgres)|              | Replicas |
  +----------+            +-----------+              +----------+
```

### Key Data Pipelines

**1. Incentive Data Pipeline (Daily/Weekly)**

```
Source websites/APIs
    --> Scrapy spiders / API clients (Python)
    --> Raw JSON/HTML stored in S3 (audit trail)
    --> Parsing + normalization (standardize to IncentiveProgram schema)
    --> Validation rules (amount ranges, date sanity, geographic consistency)
    --> Diff detection (flag changes from previous run)
    --> Human review queue for significant changes
    --> PostgreSQL upsert
    --> Redis cache invalidation
    --> Slack/email alert for funding status changes (depleted, suspended)
```

**2. Inventory Data Pipeline (Daily)**

```
MarketCheck API / Dealer feeds
    --> Vehicle listings with pricing, VIN, stock status
    --> Normalize to internal vehicle schema
    --> Match to incentive eligibility rules
    --> Pre-compute "max savings" per listing
    --> PostgreSQL + Elasticsearch (for search)
```

**3. Lead Processing Pipeline (Real-time)**

```
Form submission / API call
    --> Input validation + sanitization
    --> Consent record creation (TCPA audit log)
    --> Fraud detection (rate limiting, email validation, phone verification)
    --> Incentive matching (real-time)
    --> Lead scoring
    --> Dealer matching + routing
    --> CRM delivery (ADF XML or API)
    --> Delivery confirmation logging
    --> Billing event creation
```

### Data Quality Controls

- **Incentive staleness monitor**: Alerts when any incentive hasn't been verified in 30+ days
- **Funding tracker**: Monitors state program pages for "funding depleted" / "suspended" signals
- **Price anomaly detection**: Flags incentive amounts that deviate >50% from historical norms
- **Human-in-the-loop**: All new incentive entries and significant changes require manual verification before going live

---

## 7. Minimum Viable Tech Stack

### Languages & Frameworks

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Consumer Web App** | Next.js 14+ (React, TypeScript) | SSR for SEO (critical for organic strategy), fast page loads, API routes |
| **API Services** | Python 3.12+ / FastAPI | Fastest Python framework, async support, auto-generated OpenAPI docs, strong data validation with Pydantic |
| **Background Jobs** | Celery + Redis (or ARQ for lighter weight) | Reliable task queuing for scrapers, lead delivery, notifications |
| **Web Scraping** | Scrapy + Playwright (for JS-rendered pages) | Industry standard, middleware ecosystem, handles anti-bot measures |
| **Dealer Portal** | Next.js (shared codebase with consumer app) | Reduces maintenance burden, shared component library |

### Data Stores

| Store | Technology | Use Case |
|-------|-----------|----------|
| **Primary DB** | PostgreSQL 16 (AWS RDS or Supabase) | Incentives, leads, dealers, users, billing -- relational integrity is critical |
| **Cache** | Redis 7 (AWS ElastiCache or Upstash) | Session cache, incentive lookup cache, rate limiting, Celery broker |
| **Search** | PostgreSQL full-text search (MVP) -> Elasticsearch (scale) | Vehicle/incentive search with faceting |
| **File Storage** | AWS S3 | Raw scraper output, ADF XML archives, consent records |
| **Analytics** | PostHog (self-hosted or cloud) | Product analytics, funnel tracking, A/B testing |

### Infrastructure

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Hosting** | AWS (ECS Fargate or App Runner) | Managed containers, auto-scaling, no server management |
| **CDN** | CloudFront | Static asset delivery, edge caching for consumer site |
| **DNS/Domain** | Route 53 + CloudFlare | DDoS protection, SSL, edge caching |
| **CI/CD** | GitHub Actions | Simple, integrated with repo, free tier generous |
| **Monitoring** | Sentry (errors) + Grafana Cloud (metrics) | Fast setup, good free tiers |
| **Email/SMS** | SendGrid (transactional email) + Twilio (SMS) | Reliable delivery, TCPA compliance tools |
| **Auth** | Clerk or Auth0 | Dealer portal authentication, SSO support |

### Why This Stack

- **Python backend**: The incentive matching engine is data-heavy logic. Python excels at data processing, has mature scraping libraries, and FastAPI is production-ready with excellent performance.
- **Next.js frontend**: SEO is the primary acquisition channel. Server-side rendering is non-negotiable for ranking state-specific incentive pages.
- **PostgreSQL over NoSQL**: Incentive data has complex relational structure (programs -> eligibility rules -> stacking rules -> geographic scopes). Relational queries are cleaner and more maintainable.
- **AWS over alternatives**: Broadest service ecosystem, ECS Fargate eliminates ops overhead while keeping costs reasonable for a startup.

---

## 8. Build vs Buy Decisions

| Component | Decision | Rationale | Estimated Cost |
|-----------|----------|-----------|----------------|
| **Incentive data aggregation** | BUILD | Core IP -- this is the moat. No existing API covers all incentive types (federal + state + OEM + utility + affinity + stacking rules) | Dev time only |
| **Incentive matching engine** | BUILD | Core IP -- stacking optimization and buyer-specific matching is the differentiator | Dev time only |
| **OEM incentive data** | BUY (MarketCheck) | Comprehensive, real-time, covers 35+ makes. Building this from scratch is months of scraping work | $500-2,000/mo |
| **Vehicle data / VIN decoding** | BUY (NHTSA free + DataOne or MarketCheck) | NHTSA VIN decoder is free. Supplement with commercial API for enriched data | $0-500/mo |
| **Consumer website** | BUILD | Custom -- the incentive calculator UX is the product | Dev time only |
| **Dealer portal** | BUILD | Relatively simple dashboard. Off-the-shelf doesn't fit our specific lead + incentive model | Dev time only |
| **CRM integration (ADF)** | BUILD | Simple XML template generation + SMTP. A few days of work | Dev time only |
| **CRM integration (APIs)** | BUILD (with vendor SDKs) | Must own integration logic for reliability and customization | Dev time only |
| **Lead scoring** | BUILD | Simple weighted model initially. ML can come later with data | Dev time only |
| **Web scraping infrastructure** | BUILD | Scrapy framework handles 90% of complexity. Custom spiders per source | Dev time only |
| **Email delivery** | BUY (SendGrid) | Transactional email is a commodity. Deliverability matters | $20-100/mo |
| **SMS / phone** | BUY (Twilio) | Regulatory compliance (TCPA) is critical -- use a proven platform | $100-500/mo |
| **Consent management** | BUILD + BUY | Build consent capture UI, buy TrustedForm ($0.50-2/cert) for third-party verification | $200-1,000/mo |
| **Analytics** | BUY (PostHog) | Self-hosted is free up to scale, then reasonable cloud pricing | $0-450/mo |
| **Authentication** | BUY (Clerk) | Not a differentiator. Clerk handles MFA, SSO, user management | $25-100/mo |
| **Fraud detection** | BUILD (basic) | Rate limiting + email/phone validation initially. Buy later at scale | Dev time + $50/mo (validation APIs) |
| **Payment/billing** | BUY (Stripe) | Industry standard for B2B SaaS billing | 2.9% + $0.30/txn |

### Key Principle

Build what is core to the value proposition (incentive data, matching engine, consumer experience). Buy commodity infrastructure (email, SMS, auth, payments). The incentive aggregation + matching engine is the defensible moat.

---

## 9. MVP Scope and Phased Roadmap

### Phase 1: MVP (Months 1-3) -- "Incentive Calculator + Lead Delivery"

**Goal:** Prove that incentive-informed leads convert at higher rates than generic third-party leads.

**Scope:**
- Consumer web app with incentive calculator (ZIP + vehicle preferences + basic financial info)
- Manual/semi-automated incentive database covering top 15 states
- OEM incentive data via MarketCheck API
- Lead capture form with TCPA-compliant consent
- Basic lead scoring (rule-based, not ML)
- ADF XML lead delivery to dealers via email
- Simple dealer onboarding (manual setup)
- Basic dealer dashboard (lead list, contact info, incentive summary)

**NOT in MVP:**
- Direct CRM API integration
- Inventory-level matching
- Mobile app
- Equity mining
- AI chatbot
- Self-service dealer signup

**Team:** 2-3 full-stack engineers, 1 incentive data analyst/researcher, 1 designer (contract)

**Key Metrics:**
- Consumer calculator completion rate (target: 40%+)
- Lead capture conversion rate (target: 15-25% of calculator completions)
- Lead delivery success rate (target: 99%+)
- Dealer lead response time (target: < 30 min for 80% of leads)
- Close rate (target: 8-12% -- above industry average of 5-8%)

### Phase 2: Growth (Months 4-6) -- "Scale Acquisition + Dealer Tools"

**Additions:**
- Paid acquisition channels (Google Ads, Facebook)
- Expand incentive coverage to all 50 states
- Automated scraping pipeline for state incentive programs
- Dealer self-service signup and billing (Stripe)
- Enhanced dealer portal: lead analytics, ROI dashboard, conversion tracking
- Embeddable widget for partner sites
- Lead deduplication (prevent same consumer going to 4+ dealers)
- Phone verification for lead quality

### Phase 3: Platform (Months 7-12) -- "Integrations + Intelligence"

**Additions:**
- Direct CRM API integration (VinSolutions, Elead, DriveCentric)
- Inventory feed integration (match leads to specific in-stock vehicles)
- ML-based lead scoring (trained on Phase 1-2 conversion data)
- Bi-directional CRM sync (receive close/disposition data)
- Affiliate/widget program launch
- Mobile-optimized progressive web app
- A/B testing framework for incentive presentation

### Phase 4: Expansion (Year 2) -- "Data Moat + New Products"

**Additions:**
- Fortellis Marketplace listing (CDK DMS integration)
- Equity mining product (partner with dealers to target service customers)
- Used vehicle incentive matching
- Lease vs buy optimizer with incentive comparison
- White-label for dealer groups and OEMs
- API product (sell incentive data to other platforms)

---

## 10. Infrastructure and Scalability

### MVP Infrastructure (Supports ~10K leads/month)

```
AWS Region: us-east-1

Consumer Web:
  - Vercel (Next.js hosting) -- serverless, auto-scaling, global CDN
  - Cost: $0-20/mo (hobby/pro tier)

API Services:
  - AWS App Runner (2 services: lead API, incentive API)
  - 1 vCPU, 2 GB RAM each
  - Auto-scales 1-5 instances
  - Cost: ~$50-100/mo

Database:
  - AWS RDS PostgreSQL (db.t4g.medium: 2 vCPU, 4 GB RAM)
  - 50 GB storage, daily backups
  - Cost: ~$70/mo

Cache:
  - AWS ElastiCache Redis (cache.t4g.micro)
  - Cost: ~$15/mo

Background Workers:
  - AWS ECS Fargate (1 task, 0.5 vCPU, 1 GB)
  - Cost: ~$20/mo

Storage:
  - S3: ~$5/mo

Total: ~$160-230/mo
```

### Scaling Strategy

| Load Level | Monthly Leads | Infrastructure Changes |
|-----------|--------------|----------------------|
| MVP | Up to 10K | As described above |
| Growth | 10K-50K | RDS upgrade to db.r6g.large, add read replica, Redis cluster mode, 3-10 App Runner instances |
| Scale | 50K-200K | Multi-AZ RDS, Elasticsearch for search, dedicated scraping cluster, CDN optimization |
| Enterprise | 200K+ | Microservice decomposition, event-driven architecture (SQS/SNS), data warehouse (Redshift/BigQuery) for analytics |

### Performance Targets

| Metric | Target |
|--------|--------|
| Incentive calculation response time | < 500ms (p95) |
| Lead submission to CRM delivery | < 60 seconds (Hot leads) |
| Consumer site page load (LCP) | < 2.5 seconds |
| API uptime | 99.9% |
| Scraper success rate | > 95% per run |

---

## 11. Security and Compliance

### TCPA Compliance (Critical)

TCPA violations carry penalties of **$500-$1,500 per text or call**, with average settlements exceeding **$6 million**. This is an existential risk.

**Requirements:**
1. **One-to-one consent**: Each lead must explicitly consent to contact from each specific dealer (not blanket consent)
2. **Consent record retention**: Store full consent record (timestamp, IP, form version, exact language displayed, user agent)
3. **Opt-out processing**: Honor within 10 business days (April 2025 rule). Must apply across all channels
4. **Consent verification**: Consider TrustedForm certificates for third-party proof
5. **Do Not Call registry**: Check against national DNC list before delivery

**Implementation:**
```
ConsentRecord
  - id (UUID)
  - lead_id (FK)
  - dealer_id (FK)            # One-to-one: consent per dealer
  - consent_timestamp (ISO 8601)
  - consent_ip (string)
  - consent_user_agent (string)
  - consent_page_url (string)
  - consent_language_version (string)  # Hash of exact disclosure text shown
  - consent_method (enum: web_form, api)
  - trustedform_cert_url (string, optional)
  - revoked (boolean)
  - revocation_timestamp (timestamp, nullable)
  - revocation_method (string, nullable)
```

### FTC Safeguards Rule

As a company handling consumer financial information (income, purchase intent), compliance is likely required:
- Encryption at rest (RDS encryption, S3 encryption) and in transit (TLS 1.3)
- Multi-factor authentication for all internal systems
- Access controls with least-privilege principle
- Annual penetration testing
- Employee security training
- Breach notification plan (30 days for 500+ affected individuals)
- Penalties: up to $11,000/day for non-compliance

### State Privacy Laws

With 20 state consumer privacy laws in effect by January 2026:
- **Privacy policy**: Clear disclosure of data collection, use, sharing, and sale
- **"Do Not Sell" mechanism**: Required in California (CCPA/CPRA) and others
- **Data minimization**: Collect only what is necessary for the service
- **Right to delete**: Must support consumer data deletion requests within 45 days
- **Consent for targeted advertising**: Required in several states

**Implementation approach:** Build to California (CCPA/CPRA) standard -- it is the most restrictive and satisfies most other states.

### Data Security Architecture

```
Consumer Data Flow:
  Browser --> CloudFlare (DDoS, WAF) --> TLS 1.3 --> API Gateway
    --> Input validation/sanitization --> Application logic
    --> Encrypted at rest (AES-256) in PostgreSQL/S3

Access Controls:
  - Role-based access (RBAC): admin, dealer, support, system
  - Dealers can only see their own leads
  - PII fields encrypted at application level (not just DB-level)
  - Audit log for all PII access

Key Management:
  - AWS KMS for encryption keys
  - Secrets in AWS Secrets Manager (not env vars)
  - Rotate credentials quarterly
```

### Lead Fraud Prevention

Per research, **30% of third-party vendor leads are estimated to be fraudulent**. Our controls:

1. **Rate limiting**: Max 3 submissions per IP per hour
2. **Email validation**: Real-time MX record check + disposable email detection
3. **Phone validation**: Twilio Lookup API (carrier type, line type)
4. **Honeypot fields**: Hidden form fields that bots fill in
5. **Behavioral analysis**: Time-on-page, scroll depth, mouse movement (distinguish humans from bots)
6. **reCAPTCHA v3**: Invisible bot scoring on form submissions
7. **Post-delivery monitoring**: Track dealer feedback on lead quality, flag patterns

---

## 12. Cost Estimates

### Monthly Infrastructure Costs

| Component | MVP (Mo 1-3) | Growth (Mo 4-6) | Scale (Mo 7-12) |
|-----------|-------------|-----------------|-----------------|
| Hosting (Vercel + AWS) | $230 | $500 | $1,200 |
| Database (RDS + Redis) | $85 | $250 | $600 |
| Email (SendGrid) | $20 | $50 | $100 |
| SMS (Twilio) | $100 | $300 | $800 |
| MarketCheck API | $500 | $1,000 | $2,000 |
| TrustedForm | $200 | $500 | $1,500 |
| Analytics (PostHog) | $0 | $0 | $450 |
| Auth (Clerk) | $25 | $25 | $100 |
| Monitoring (Sentry + Grafana) | $0 | $30 | $100 |
| Domain + DNS | $20 | $20 | $20 |
| **Subtotal Infrastructure** | **$1,180** | **$2,675** | **$6,870** |

### Operational Costs

| Component | MVP (Mo 1-3) | Growth (Mo 4-6) | Scale (Mo 7-12) |
|-----------|-------------|-----------------|-----------------|
| Ad spend (paid acquisition) | $0 | $5,000 | $15,000 |
| Content/SEO | $2,000 | $3,000 | $5,000 |
| Incentive data analyst (contract) | $4,000 | $4,000 | $6,000 |
| Legal/compliance | $2,000 | $1,000 | $1,000 |
| **Subtotal Operational** | **$8,000** | **$13,000** | **$27,000** |

### Total Monthly Burn (Excluding Engineering Salaries)

| Phase | Monthly Cost |
|-------|-------------|
| MVP (Mo 1-3) | ~$9,200 |
| Growth (Mo 4-6) | ~$15,700 |
| Scale (Mo 7-12) | ~$33,900 |
| **Year 1 Total** | **~$240,000** |

### Revenue Breakeven Estimate

Assuming average CPL to dealers of $40 (shared leads) to $100 (exclusive hot leads):

| Scenario | Avg Revenue/Lead | Monthly Leads Needed | Breakeven Month |
|----------|-----------------|---------------------|-----------------|
| Conservative ($40/lead) | $40 | 850 | Month 8-10 |
| Moderate ($60/lead) | $60 | 565 | Month 6-8 |
| Optimistic ($80/lead) | $80 | 425 | Month 5-6 |

---

## 13. Sources

### CRM & DMS Integration
- [VinSolutions Developer Portal](http://developer.vinsolutions.com/)
- [VinSolutions CRM Integrations](https://www.vinsolutions.com/dealership-software/integrations/)
- [CDK Global API Solutions](https://www.cdkglobal.com/cdk-global-api-solutions)
- [CDK Global Elead APIs (4 New APIs)](https://www.businesswire.com/news/home/20210209005197/en/CDK-Global-Launches-Advanced-CRM-Data-Capabilities-with-Four-New-Elead-APIs)
- [ActivEngage Elead Lead Delivery API](https://www.globenewswire.com/news-release/2023/10/24/2765777/0/en/ActivEngage-Develops-Advanced-Chat-and-CRM-Integration-with-New-Elead-Lead-Delivery-API.html)
- [Fortellis Marketplace](https://fortellis.io/)
- [DriveCentric CRM Integrations](https://drivecentric.com/integrations)
- [DriveCentric Integration Strategy](https://www.autosuccessonline.com/drivecentri-automotive-crm-integration-strategy/)
- [DriveCentric Future of CRM](https://www.prnewswire.com/news-releases/drivecentric-introduces-the-future-of-crm-intelligent-integrated-built-for-dealers-302551066.html)
- [Reynolds Certified Interface Program](https://www.reyrey.com/partners/reynolds-certified-interface)
- [CDK-Reynolds $100M Antitrust Settlement](https://www.classaction.org/news/another-class-action-alleges-cdk-global-reynolds-and-reynolds-co.-fixed-market-for-auto-dealer-data-systems)

### Data Standards
- [ADF XML Specification](https://adfxml.info/)
- [ADF XML Format Example (GitHub)](https://github.com/manuganji/ADF-XML-format-example)
- [STAR Standards for Automotive Retail](https://xml.coverpages.org/star.html)
- [STAR XML Standards](https://www.starstandard.org/)

### Incentive Data APIs
- [JD Power ChromeData Digital Retailing API](https://www.jdpower.com/business/chromedata-automotive-digital-retailing-api)
- [MarketCheck OEM Incentive Data Feed](https://www.marketcheck.com/data_feed/oem-incentives/)
- [MarketCheck APIs](https://www.marketcheck.com/apis/)
- [AFDC Federal and State Laws and Incentives](https://afdc.energy.gov/laws)
- [AFDC Tools](https://afdc.energy.gov/tools)
- [DataOne Software Vehicle Data](https://www.dataonesoftware.com/vehicle-data-vin-decoding/mapping-and-3rd-party-validation-data)

### TCPA & Compliance
- [TCPA Consent Rule Changes 2026](https://www.tratta.io/blog/tcpa-consent-rule-changes)
- [TCPA Compliance for Lead Generation 2026](https://stealthlabz.com/topics/lead-gen-infrastructure/tcpa-compliance)
- [FCC Lead Generation Ruling (ActiveProspect)](https://activeprospect.com/blog/fcc-lead-generation/)
- [TCPA Compliance Guide for Lead Generators 2026](https://www.leadgen-economy.com/blog/tcpa-compliance-guide-lead-generators/)
- [NADA FTC Safeguards Rule](https://www.nada.org/safeguardsrule)
- [State Privacy Law Deadline January 2026 (ComplyAuto)](https://complyauto.com/state-privacy-law-deadline-january-1-2026/)

### Lead Generation & Industry Data
- [TradePending: Data-Driven Lead Generation Guide](https://tradepending.com/blog/data-driven-lead-generation-automotive-dealerships-guide/)
- [TradePending: Best Car Sales Lead Generation Tools 2025](https://tradepending.com/blog/best-car-sales-lead-generation-tools/)
- [Edmunds Developer Portal](https://developer.edmunds.com/)
- [Gryphon AI: Obtaining Consent Under New FCC Rules](https://gryphon.ai/how-to-obtain-consent-with-new-fcc-lead-generator-laws/)

### Research Files (Internal)
- [Incentive Research](/Users/hamid.ebadi/car-incentive/incentive-research.md)
- [Leads Research](/Users/hamid.ebadi/car-incentive/leads-research.md)
