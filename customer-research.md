# Dealer Pain Points & Customer Research

**Last updated:** March 2026

---

## Table of Contents

1. [Consumer Buyer Research](#1-consumer-buyer-research)
2. [Dealer Pain Points (Ranked by Severity)](#2-dealer-pain-points-ranked-by-severity)
3. [Current Spending Patterns & Budget Allocation](#3-current-spending-patterns--budget-allocation)
4. [Ideal Customer Profile](#4-ideal-customer-profile)
5. [What Dealers Value Most in a Lead Provider](#5-what-dealers-value-most-in-a-lead-provider)
6. [Switching Triggers](#6-switching-triggers--what-makes-dealers-change-providers)
7. [The Incentive Angle](#7-the-incentive-angle--would-dealers-pay-for-incentive-qualified-leads)
8. [Interview-Style Insights from Web Sources](#8-interview-style-insights-from-web-sources)
9. [Customer Acquisition Strategy Recommendations](#9-customer-acquisition-strategy-recommendations)
10. [Sources](#10-sources)

---

## 1. Consumer Buyer Research

*Source: UX Research Brief (March 2026) -- see [ux-research-brief.md](ux-research-brief.md) for full findings and sources.*

### The Savings-Motivated Buyer Persona

Savings-motivated car buyers are a large and growing segment. Key characteristics:

- **43% of consumers would switch brands** for a lower price; **62% feel vehicle ownership is too costly**
- Spend **14+ hours researching online** before purchase, with **61% of traffic from mobile**
- **65% cite price transparency** as the most important factor in their research experience
- Purchase timing often driven by financial triggers (tax season, high rebates, low interest rates)
- Will sacrifice brand loyalty for savings; want to feel confident they have the best deal before contacting a dealer

### What Consumers Want (Prioritized)

1. **Total out-of-pocket cost clarity** -- final price after all incentives, not just MSRP or individual rebates
2. **Personalized eligibility** -- enter info once and see everything they qualify for (varies by ZIP, income, military status, purchase type)
3. **Purchase type comparison** -- cash, finance, and lease carry different incentives; users need side-by-side comparison
4. **Source credibility** -- users trust platforms that show where data comes from (e.g., "California Clean Vehicle Rebate Project")
5. **Timeliness** -- incentives change monthly/quarterly; users need to know data is current and when deals expire

### Consumer Pain Points

| Pain Point | Severity |
|---|---|
| No single source aggregates all incentive types (federal + state + utility + manufacturer + eligibility-based) | Critical |
| Incentive eligibility is confusing (income limits, residency, vehicle eligibility) | High |
| Stacking rules are opaque (which incentives combine?) | High |
| Expired or outdated deal information | High |
| Cash vs. finance vs. lease comparison is fragmented across sites | Medium |
| Mobile experience is slow or cluttered (61% of traffic is mobile) | Medium |

### Unmet Consumer Needs

- A total savings calculator that stacks all eligible incentives into one number
- Clear explanation of which incentives stack and which are mutually exclusive
- Timeline visibility (expiration dates, application deadlines)
- Step-by-step guidance on how to claim each incentive after purchase
- Alerts when new incentives become available for a saved vehicle

### What Works on Competitor Sites

**Key UX patterns from TrueCar, Edmunds, CarsDirect:**
- ZIP code as the primary personalization entry point (universal pattern)
- Separation of deals by purchase type (cash / finance / lease)
- Social proof and price anchoring ("what others paid" on TrueCar)
- Calculators that auto-populate data to minimize user input (Edmunds)
- Editorial context alongside raw numbers builds trust and urgency

**Lead generation best practices from competitive analysis:**
- Progressive disclosure (start with ZIP, gradually request more info)
- Value-first CTAs ("See Your Total Savings" outperforms "Submit" or "Contact Dealer")
- Minimal form fields (name + email/phone optimal; every additional field reduces conversion)
- Trust signals: source attribution, BBB ratings, "we never share your info without permission"
- Live chat increases conversion 20-30% vs. static forms
- Leads contacted within 5 minutes convert at dramatically higher rates

### Mobile Considerations

- **61% of automotive traffic** is from mobile; **70%+ use smartphones** as primary research device
- **78% of mobile local searches** result in business visits within 24 hours
- Mobile conversion rates average 3.48% (lower than desktop) with 60% higher cost-per-conversion -- the mobile funnel must be especially frictionless
- Key mobile UX requirements: thumb-friendly navigation, fast load times (<3s), collapsible incentive cards, sticky savings bar, one-tap ZIP via location services

---

## 2. Dealer Pain Points (Ranked by Severity)

### Tier 1: Critical (Universal, high-impact)

#### 1.1 Lead Quality Degradation
- **30% of third-party vendor leads are estimated to be fraudulent** (bot submissions, hired form-fillers, aged-lead recycling)
- **70%+ of leads from third parties result in zero return communication** -- the customer never responds to any outreach
- Dealers using proven follow-up processes (averaging 9.3 call attempts) still see minimal engagement
- Customers often didn't realize they submitted a lead -- they thought they were getting a "free price quote" or even "free movie tickets" (deceptive lead generation by downstream aggregators)
- Lead sources are opaque: dealers trace leads back to sponsored link sites like MyCarQuote.com and CarsBelowInvoice.com that use bait-and-switch tactics

**Impact:** Dealerships waste an average of **11 hours per person per month** chasing fraudulent or unresponsive leads. With 3 BDC agents, that's 33 hours/month of pure waste. At $25/hour fully loaded, that's ~$10,000/year per store in labor alone -- not counting the lead acquisition cost.

#### 1.2 Poor ROI Visibility / Attribution Gap
- **92% of vehicle sales are untraceable** to a specific lead source in CRM (Clarivoy data)
- Last-touch attribution misallocates budgets -- AutoTrader influences 55% of sales via multi-touch but gets credit for far fewer
- Salespeople override or fail to log lead sources in CRM
- Dealers make budget decisions on incomplete data, leading to chronic overspending on some channels and underspending on others
- One dealer reported: sold only **4 vehicles from AutoTrader over 9 months while paying $3,700/month** ($8,325 cost per sale from that source)

**Impact:** Dealers cannot confidently say which marketing dollars are working, creating fear of cutting any channel. This keeps incumbents entrenched even with poor performance.

#### 1.3 Lead Non-Exclusivity / Bid Wars
- A single customer can blast their information to **12+ competing dealers** within minutes from third-party sites
- Leads are sent to multiple dealers simultaneously, creating price wars where the lowest bidder wins
- Dealers report that shared leads commoditize the sales process -- "it becomes all about who quotes the lowest price, not who provides the best experience"
- CRM deduplication is imperfect: different phone, email, or spelling creates multiple records for the same buyer

**Impact:** Destroys margins. Dealers compete on price rather than service, driving down gross profit per vehicle. Exclusive leads command a significant premium precisely because this problem is so painful.

### Tier 2: Severe (Widespread, significant cost)

#### 1.4 Rising Costs with Declining Perceived Value
- AutoTrader pricing: $450/month (entry) to $2,000+/month (enterprise), with dealers questioning uniform "rooftop pricing" regardless of inventory size
- Annual price increases have widened the gap between cost and perceived value
- Total annual spend on listing sites alone: **$109,487** (NADA 2024 average)
- Dealers ask why they're "charged the same rooftop pricing regardless of whether I have 23 vehicles or 300 at my lot"
- One dealer explicitly stated: "They should charge per vehicle uploaded instead"

#### 1.5 Vendor Lock-In and Integration Friction
- CDK and Reynolds lock dealers into **5-7 year DMS contracts**
- Third-party vendors pay **$50-$150+/month per store** for API access to DMS data
- **$100 million antitrust settlement** (Feb 2025) over CDK-Reynolds price-fixing and blocking third-party data access
- Having to "log into a separate account to retrieve a finance application not in the dealer's format" is a persistent frustration
- Dealers feel they don't fully control their own customer data

#### 1.6 Slow Lead Response (Self-Inflicted but Systemic)
- OEM-mandated response time: 30 minutes. Best practice: under 5 minutes
- **78% of customers buy from the first responder**, yet many dealerships respond in hours or days
- Root causes: understaffed BDCs, after-hours leads, CRM alert fatigue, no accountability tracking
- AI tools are helping (50% adoption by end of 2025) but many dealers still struggle

### Tier 3: Significant (Segment-specific or emerging)

#### 1.7 TCPA Compliance Risk from Bad Leads
- Every bot-submitted lead that a dealer calls is a **TCPA compliance risk at $1,500 per violation**
- "Lead generator loophole" (selling one consumer's consent to multiple businesses) is being closed
- New consent revocation rules (April 2025): must honor opt-out within **10 business days**
- Texas SB 140: $10,000 security bond for telephone solicitation
- Dealers face liability for contacting people who never actually consented

#### 1.8 Incentive Complexity (The Gap We Fill)
- With federal EV credits terminated (Sept 2025) and **20+ state programs** with different rules, income limits, and deadlines, neither dealers nor consumers can easily navigate the incentive landscape
- Programs run out of funding unpredictably (Oregon suspended, Maryland FY26 depleted)
- No existing lead provider qualifies leads based on incentive eligibility
- Dealers lose sales when customers don't realize they qualify for $5,000-$15,000 in combined incentives
- Manufacturer incentives (0% APR, rebates, loyalty/conquest) change monthly and interact with state programs in complex ways

#### 1.9 EV-Specific Challenges
- Dealer EV outlook weakening: Q4 2025 Cox Automotive Dealer Sentiment Index shows declining EV profit expectations
- Many franchise dealers required to stock EVs but lack tools to sell them effectively
- Consumer confusion about range, charging, and total cost of ownership
- DealerOn/Lyteflo partnership shows market recognizes need for EV-specific merchandising tools on dealer websites

---

## 3. Current Spending Patterns & Budget Allocation

### Average Annual Dealership Spend (NADA 2024)

| Category | Annual Spend | % of Total |
|----------|-------------|-----------|
| Third-party listing sites (AutoTrader, Cars.com, etc.) | $109,487 | 20% |
| Search engine marketing (SEM/PPC) | $105,256 | 19% |
| SEO / website optimization | $103,140 | 19% |
| Social media advertising | $64,000 | 12% |
| Local television | $59,246 | 11% |
| Radio | $40,765 | 7% |
| Direct mail | $26,446 | 5% |
| Newspaper | $11,636 | 2% |
| Other digital | ~$23,563 | 4% |
| **Total advertising** | **$543,539** | **100%** |

### Total Technology + Marketing Spend by Dealership Size

| Category | Small (50 units/mo) | Mid-Size (150 units/mo) | Large (500+ units/mo) |
|----------|--------------------|-----------------------|----------------------|
| DMS | $180K-$200K | $250K-$360K | $360K+ per store |
| CRM | $12K-$24K | $24K-$36K | $36K+ per store |
| Advertising | $250K-$350K | $500K-$650K | $800K+ per store |
| BDC Operations | $75K-$150K | $200K-$250K | $300K+ per store |
| Third-party leads | $50K-$100K | $100K-$200K | $200K+ per store |
| **Estimated Total** | **$567K-$824K** | **$1.07M-$1.5M** | **$1.7M+ per store** |

### Key Cost Metrics

| Metric | Value |
|--------|-------|
| Average ad spend per vehicle sold (H1 2025) | **$722** |
| Industry average CPL (all sources) | **$283** |
| Third-party CPL range | **$20-$150** |
| Average cost per sale (third-party leads) | **$250-$350** (well-run processes) to **$1,000+** (poor processes) |
| Digital share of ad budget | **73%** (up from 65% in 2023) |
| NADA recommended ad spend (% of gross profit) | **6-7%** |

### Budget Pressure Points
- Dealers spend the most on channels with the **worst attribution** (third-party sites, broad SEM)
- The shift to digital is accelerating but dealers struggle to measure which digital channels actually work
- AI tools ($300-$3,000/month) are a new budget line item but show strong ROI ($8-$12 per $1 spent)
- Compliance costs rising: FTC Safeguards Rule, state privacy laws, TCPA -- all require investment

---

## 4. Ideal Customer Profile

### Primary Target: Mid-Size Franchise Dealers in Incentive-Rich States

| Attribute | Ideal Profile |
|-----------|--------------|
| **Dealer type** | Franchise (new + used) -- they have the most incentive complexity |
| **Size** | 100-300 units/month (large enough to invest, small enough to lack dedicated analytics) |
| **Geography** | States with active incentive programs: CA, CO, NY, NJ, MA, CT, IL, PA |
| **Brand mix** | OEMs with aggressive incentive programs: Stellantis, GM, Ford, Hyundai/Kia, Nissan |
| **EV inventory** | Dealers carrying EVs/PHEVs (especially those struggling to move EV inventory) |
| **Tech-savviness** | Moderate: uses CRM and digital marketing but hasn't adopted AI tools yet (the 50% who haven't) |
| **Pain level** | Frustrated with third-party lead ROI, looking for differentiation |
| **Budget** | $50K-$200K/year on third-party leads (willing to reallocate a portion) |

### Secondary Target: Independent Dealers in Competitive Markets

| Attribute | Profile |
|-----------|---------|
| **Dealer type** | Independent (used vehicles) |
| **Size** | 30-100 units/month |
| **Geography** | Competitive metro markets where differentiation is hard |
| **Pain level** | Lower margins than franchise, need every edge. Used EV market growing |
| **Opportunity** | Used EV incentives (some state programs cover used EVs: CT up to $5,000, MA $3,500, IL $4,000) |
| **Budget** | $30K-$100K/year on leads (price-sensitive, need clear ROI) |
| **Note** | Independent dealer sentiment even lower than franchise (profit sentiment: 33 vs 44, Q4 2025 Cox CADSI) |

### Tertiary Target: Large Dealer Groups (Enterprise)

| Attribute | Profile |
|-----------|---------|
| **Type** | Multi-rooftop groups (AutoNation, Lithia, Penske, Group 1, etc.) |
| **Size** | 500+ units/month per store, 10-200+ stores |
| **Opportunity** | API integration, bulk data, cross-store incentive optimization |
| **Approach** | Enterprise sales, pilot at 2-3 stores then roll out |
| **Challenge** | Longer sales cycles, established vendor relationships, custom integration requirements |

### Anti-Targets (Avoid Initially)

- **Buy-Here-Pay-Here (BHPH) dealers**: Different business model, subprime focus, less incentive relevance
- **Single-car-per-week micro dealers**: Too small to justify acquisition cost
- **Luxury-only dealers**: Incentives less relevant for $80K+ buyers (income limits disqualify many)
- **Rural dealers with no EV inventory**: Limited incentive applicability until EV adoption grows

---

## 5. What Dealers Value Most in a Lead Provider

Ranked by importance based on forum discussions, surveys, and industry data:

### 1. Lead Quality Over Quantity
- Dealers overwhelmingly prefer fewer, higher-quality leads over volume
- Key quality indicators: **connection rate (70%+)**, **close rate (7%+)**, **cost per sale ($350 or lower)**
- One dealer who reallocated their $1,000/month lead budget elsewhere reported "similar sales volume but improved profit margins per vehicle sold"
- Forums consistently show: removing low-quality lead sources reduces volume but **increases profit**

### 2. Transparent, Measurable ROI
- Dealers want to know exactly how many leads they received, how many they sold, and at what cost
- "The purest form of ROI" -- clear attribution from lead to sold vehicle
- Performance-based or pay-per-sale models (like TrueCar at $299-$399/sale) are preferred over flat subscriptions with opaque results

### 3. Lead Exclusivity
- Exclusive leads eliminate bid wars and preserve margins
- Dealers will pay a premium for leads not simultaneously sent to competitors
- Phone leads (74% appointment set rate) vastly outperform internet form fills (40%) partly because they're typically more exclusive

### 4. Speed and Integration
- Leads must flow into existing CRM instantly (VinSolutions, Elead, DriveCentric)
- No separate logins or manual processes
- Real-time delivery matters: **78% of customers buy from the first responder**

### 5. Fair, Flexible Pricing
- Per-vehicle or per-lead pricing preferred over flat "rooftop" fees
- Ability to scale up/down based on inventory and season
- No long-term contracts (the DMS model of 5-7 year lock-in is universally hated)
- Month-to-month with performance guarantees

### 6. Compliance Built-In
- TCPA-compliant consent documentation
- Privacy law compliance (20 state laws by Jan 2026)
- FTC Safeguards Rule compatibility
- Dealers don't want to be the ones liable for contacting non-consenting consumers

---

## 6. Switching Triggers -- What Makes Dealers Change Providers

### Immediate Triggers (Action within 30 days)

1. **Price increase without performance improvement**: Annual increases from AutoTrader/Cars.com without corresponding lead quality improvement. "Dealers have accepted annual price rises for years, but recently the gap between cost and perceived value has widened dramatically."

2. **Provable poor ROI**: When a dealer can show their GM or owner that a channel costs $3,700/month and produced only 4 sales in 9 months ($8,325/sale), cancellation follows quickly.

3. **Compliance incident**: A TCPA violation traced to a third-party lead triggers immediate review of all lead sources.

4. **New management/ownership**: Dealership acquisitions (at record pace) bring new decision-makers who audit all vendor relationships.

### Gradual Triggers (Build over 3-6 months)

5. **Declining lead volume or quality**: Slow erosion in connection rates or close rates.

6. **Better alternative demonstrated**: A competitor dealer in the same market visibly succeeding with a different approach.

7. **OEM program changes**: New co-op requirements or certified vendor mandates shift budgets.

8. **Industry peer influence**: DealerRefresh forum discussions, 20 Group meetings, NADA conference demos.

### What Overcomes Switching Inertia

- **Risk-free trial or pilot**: No-commitment test period with measurable outcomes
- **Integration ease**: Works with existing CRM without disruption
- **Social proof from similar dealers**: "A dealer my size in my market grew sales 20% with this"
- **Pay-for-performance**: Aligns incentives -- dealer only pays when value is delivered
- **Data portability**: Unlike DMS lock-in, dealer keeps their data if they leave

---

## 7. The Incentive Angle -- Would Dealers Pay for Incentive-Qualified Leads?

### The Market Gap

No major lead provider currently qualifies leads based on incentive eligibility. This is a significant gap because:

1. **Incentive complexity is at an all-time high**: Federal credits terminated, 20+ state programs with varying rules, manufacturer incentives changing monthly, utility rebates, and stacking possibilities
2. **Neither dealers nor consumers understand the full picture**: A buyer in Colorado could qualify for $15,000+ in combined incentives but not know it
3. **Incentives directly drive purchase decisions**: 71% of survey respondents said a $35 test-drive incentive alone would compel them to test drive an EV -- imagine the impact of knowing you qualify for $5,000-$15,000 in savings
4. **DealerOn/Lyteflo partnership validates the concept**: Their EV merchandising tool highlights "federal, state and local tax savings, automated for easy integration" -- but only on dealer websites, not as a lead generation tool

### Why Dealers Would Pay Premium Pricing

**Higher intent = higher close rates:**
- A lead that says "I want a Hyundai Ioniq 5 and I qualify for $8,500 in combined incentives" is dramatically more valuable than a generic "send me a price quote" lead
- Incentive-qualified leads have built-in urgency (many programs have funding deadlines or caps)
- The lead comes pre-educated about affordability, reducing the sales cycle

**Solves the EV inventory problem:**
- Many dealers are sitting on EV inventory they can't move (Q4 2025: EV profit outlook declining)
- Matching incentive-eligible buyers with EV inventory creates a win-win
- Addresses the #1 consumer barrier to EV adoption: perceived cost

**Differentiation from every other lead source:**
- No one else is doing this at scale
- Incentive data is complex enough to create a meaningful moat
- Dealers get something they literally cannot get elsewhere

### Pricing Power Estimate

| Lead Type | Market CPL | Premium Justification | Estimated CPL |
|-----------|-----------|----------------------|---------------|
| Generic third-party lead | $20-$50 | Baseline | $20-$50 |
| Incentive-aware lead (knows general savings) | -- | Higher intent, pre-educated | $50-$75 |
| Incentive-qualified lead (verified eligibility) | -- | Income-verified, program-matched, high urgency | $75-$150 |
| Incentive-qualified + exclusive | -- | No competition, highest close rate | $150-$300 |

At $150-$300 per exclusive incentive-qualified lead with a projected 15-20% close rate (vs 5-8% for generic leads), the **cost per sale of $750-$2,000** compares favorably to:
- Industry average cost per sale: $722 ad spend alone (not counting all other costs)
- AutoTrader at $8,325/sale in the worst-case dealer example above
- TrueCar at $299-$399/sale (but no incentive qualification)

### Revenue Model Possibilities

1. **Per-lead pricing**: $75-$300 per incentive-qualified lead (tiered by exclusivity and qualification depth)
2. **Per-sale commission**: $400-$600 per closed deal (higher than TrueCar but with incentive qualification)
3. **Monthly subscription + per-lead**: $500-$1,500/month base + $50-$100 per lead (covers platform access + leads)
4. **Consumer freemium + dealer monetization**: Free incentive calculator for consumers, monetize the high-intent leads generated

---

## 8. Interview-Style Insights from Web Sources

### On Third-Party Lead Quality

> "For years I have been watching dealers pour money into 3rd party lead providers. It frustrates me because the deal always seems so one sided."
> -- Elizabeth Apps, DealerRefresh Forum

> "I'm finding the quality of the leads are becoming more and more substandard... 70%+ of the leads result in absolutely no return communication of any kind."
> -- Anonymous dealer, DealerRefresh "Are Your 3rd Party Leads Junk?"

> "I was filling out a form to get free movie tickets."
> -- Customer who unknowingly became a car lead, reported by dealer on DealerRefresh

### On AutoTrader Specifically

> "[AutoTrader is] the worst lead source we have by far, hard to appoint... I sold 4 vehicles from AutoTrader over a 9-month period while paying $3,700/month."
> -- Eley Duke, DealerRefresh Forum

> "Platforms giving customers the 'option' to supply phone numbers don't have dealerships' best interests in mind."
> -- John H., DealerRefresh Forum

> "Why am I charged the same rooftop pricing regardless of inventory size -- 23 vehicles at one location versus 300 at another? They should charge per vehicle uploaded."
> -- Anonymous dealer, DealerRefresh Forum

### On Lead Exclusivity and Bid Wars

> "Shared leads create all-out bid wars where the lowest-priced vehicle wins, not the best sales pitch."
> -- John H., DealerRefresh Forum

> "It becomes all about who quotes the lowest price, not who provides the best experience."
> -- Multiple dealers, paraphrased from DealerRefresh discussions

### On What Dealers Would Do Differently

> "[After dropping third-party leads] I'd put the money into Google Ads using dynamic inventory ads to drive more in-market used traffic directly to my website."
> -- Adam Stone, DealerRefresh Forum

> "[I'd invest in] Facebook advertising to target in-market shoppers through creative angles without emphasizing price, allowing salespeople to command better margins."
> -- John H., DealerRefresh Forum

> "One dealer reallocated their $1,000 monthly lead budget elsewhere, reporting similar sales volume but improved profit margins per vehicle sold."
> -- DealerRefresh, "Are Your 3rd Party Leads Junk?"

### On the Market Sentiment (Q4 2025)

> "Market sentiment for both current and future conditions fell below the positive threshold in the fourth quarter, signaling caution as dealers face rising costs, higher prices and economic uncertainty."
> -- Cox Automotive Dealer Sentiment Index, Q4 2025

> Independent dealer profit sentiment: **33** (out of 100). Franchise dealer profit sentiment: **44**. Both well below the positive threshold of 50.
> -- Cox Automotive CADSI, Q4 2025 (919 dealers surveyed)

### On EV-Specific Challenges

> "DealerOn and Lyteflo [are] joining forces to elevate EV merchandising for car dealerships... tools transform how dealerships connect with buyers by addressing key questions and highlighting benefits to EV ownership."
> -- DealerOn/Lyteflo press release, 2025

> "71% of respondents report a $35 incentive would compel them to test drive an EV."
> -- DealerOn Lead Accelerator research

---

## 9. Customer Acquisition Strategy Recommendations

### Phase 1: Prove Value (Months 1-3)

**Target:** 10-20 franchise dealers in California and Colorado (richest incentive landscapes)

**Approach:**
1. **Free incentive calculator widget** for dealer websites -- like Lyteflo but focused on lead capture
2. **Risk-free pilot**: provide 50-100 incentive-qualified leads per dealer per month at no cost
3. **Measure everything**: track connection rate, appointment rate, close rate, gross profit per lead
4. **Build case studies**: document ROI vs their existing third-party leads

**Why CA and CO first:**
- California: CC4A up to $14,000, DCAP, utility rebates ($700-$4,200), no federal credits = state programs matter more
- Colorado: Up to $15,000 combined (state tax credit + VXC), point-of-sale rebates at dealership

### Phase 2: Scale with Social Proof (Months 4-8)

**Target:** Expand to 100-200 dealers across top 8 incentive states

**Approach:**
1. **Introduce paid tiers** based on Phase 1 results
2. **DealerRefresh and 20 Group presence**: get early adopters talking about results
3. **OEM co-op certification**: become eligible for co-op advertising funds (Hyundai tripled co-op in 2025)
4. **CRM integrations**: VinSolutions, Elead, DriveCentric (covers ~70% of franchise dealers)
5. **Referral program**: existing dealer customers refer peers for bonus leads

### Phase 3: National Expansion (Months 9-18)

**Target:** 500-1,000 dealers nationwide

**Approach:**
1. **Enterprise sales** to large dealer groups (pilot at 2-3 stores, roll out to all)
2. **Consumer-facing brand**: SEO and content marketing around "how much can I save on a car" -- capture intent at the top of funnel
3. **API/data licensing**: sell incentive data to other platforms (CRMs, DMS, dealer websites)
4. **Expand beyond EVs**: manufacturer cash rebates, 0% APR offers, loyalty/conquest programs, affinity discounts

### Key Channels for Dealer Acquisition

| Channel | Cost | Effectiveness | Notes |
|---------|------|---------------|-------|
| DealerRefresh forum presence | Free | High credibility | Authentic participation, not ads |
| NADA Show / Digital Dealer conference | $10K-$50K per event | High for enterprise | Demo and relationship building |
| 20 Group referrals | Free | Highest conversion | Peer recommendation is #1 influence |
| LinkedIn outreach to dealer principals | Low | Moderate | Target Internet Directors and GMs |
| Industry publications (WardsAuto, Automotive News) | $5K-$20K | Brand building | Thought leadership on incentives |
| OEM co-op program inclusion | Effort-intensive | Very high | Unlocks OEM marketing budgets |
| Free tools/calculators (SEO) | Dev cost only | Long-term compounding | Content moat around incentive data |

### Pricing Strategy Recommendation

**Start with pay-per-performance** to overcome switching inertia:
- No upfront cost, no long-term contract
- Charge per qualified lead or per closed sale
- Once proven, introduce subscription tiers with volume discounts
- Never lock dealers into multi-year contracts (position as the anti-DMS)

---

## 10. Sources

### UX Research and Consumer Behavior
- [UX Research Brief](ux-research-brief.md) -- IncentiveDrive UX Research, March 2026
- [Cox Automotive Car Buyer Journey Study](https://www.coxautoinc.com/insights/cox-automotive-car-buyer-journey-study-finds-efficiency-digital-tools-and-ai-drive-record-satisfaction/)
- [Consumer Behavior in Car Buying Statistics 2025](https://www.demandlocal.com/blog/consumer-behavior-car-buying-statistics/)
- [Shift Digital 2025 Pulse Report](https://www.shiftdigital.com/2025-Digital-Automotive-Shopping-Trends)
- [Auto Shopper Behavior Statistics](https://www.demandlocal.com/blog/auto-shopper-behavior-statistics/)

### Dealer Forums and Direct Insights
- [DealerRefresh: 3rd Party Lead Providers](https://forum.dealerrefresh.com/threads/3rd-party-lead-providers.5578/)
- [DealerRefresh: Are Your 3rd Party Leads Junk?](https://www.dealerrefresh.com/are-your-3rd-party-leads-junk/)
- [DealerRefresh: If You Dropped AutoTrader - Where Would You Put the Money](https://forum.dealerrefresh.com/threads/if-you-dropped-autotrader-where-would-you-put-the-money.6541/)
- [DealerRefresh: Blueprint Series - Third-Party Lead Providers](https://www.dealerrefresh.com/blueprint-series-third-party-lead-providers/)
- [DealerRefresh: Pop-Ups on Your Dealer Website in 2025](https://forum.dealerrefresh.com/threads/pop-ups-on-your-dealer-website-in-2025-lead-generators-or-traffic-killers.11188/)
- [DealerRefresh: Cost for Leads?](https://forum.dealerrefresh.com/threads/cost-for-leads.9461/)

### Industry Reports and Surveys
- [Cox Automotive: Q4 2025 Dealer Sentiment Index](https://www.coxautoinc.com/insights-hub/q4-2025-cadsi/)
- [Cox Automotive: Q3 2025 Dealer Sentiment Index](https://www.coxautoinc.com/insights-hub/q3-2025-cadsi/)
- [Cox Automotive: The High Cost of Poor-Quality Leads](https://coxautoinc.com/learning-center/the-high-cost-of-poor-quality-leads)
- [WardsAuto: Studies, Reports Reveal Persistent Dealer Pain Points](https://www.wardsauto.com/news/studies-reports-reveal-persistent-dealer-pain-points/798929/)
- [WardsAuto: Bad Digital Sales Leads That Bog Down Car Dealers](https://www.wardsauto.com/news/archive-wards-bad-digital-sales-leads-that-bog-down-car-dealers/793837/)
- [Kerrigan Advisors: Dealer Survey - Gauging Dealer Sentiment](https://www.kerriganadvisors.com/our-reports/dealer-survey)
- [CBT News: Auto Dealer Sentiment Turns Positive in 2025](https://www.cbtnews.com/auto-dealer-sentiment-turns-positive-in-2025-as-survey-reveals-profit-and-valuation-expectations-improve-for-the-first-time-since-2021/)

### Lead Generation and Cost Data
- [Demand Local: 22 Auto Dealer Lead Generation Statistics 2025](https://www.demandlocal.com/blog/auto-dealer-lead-generation-statistics/)
- [Invoca: Calculate Your Dealership's Cost Per Lead](https://www.invoca.com/blog/calculate-dealership-cost-per-lead)
- [First Page Sage: Average Cost Per Lead by Industry 2026](https://firstpagesage.com/reports/average-cost-per-lead-by-industry/)
- [Turbo Marketing Solutions: Impact of Purchased Leads in Automotive](https://www.turbomarketingsolutions.com/single-post/the-impact-of-purchased-leads-in-the-automotive-industry-a-comprehensive-cost-analysis)
- [DealerOn: The Real Cost of 3rd Party Leads](https://www.dealeron.com/blog/the-real-cost-of-3rd-party-leads/)
- [AutoLeadPro: How to Get Car Leads Without Overpaying](https://autoleadpro.com/how-to-get-car-leads/)
- [LeadLocate: Pay-As-You-Go Sales Leads for Car Dealers](https://leadlocate.com/sales-leads/automotive-pay-per-sales-lead)

### Dealer Switching and Provider Criticism
- [DrivingSales: Third Party Lead Providers - Some Are Just Saying No](https://www.drivingsales.com/jeremy-patterson/blog/20150618-third-party-lead-providers-some-just-saying-no)
- [WardsAuto: Third-Party Lead Providers - Friend or Foe?](https://www.wardsauto.com/dealers/third-party-lead-providers-friend-or-foe-)
- [Agilita Digital: Why Car Dealers Are Leaving Auto Trader](https://www.agilitadigital.co.uk/news/why-car-dealers-are-walking-away-from-autotrader)
- [AM Online: AutoTrader Responds to Deal Builder Criticism](https://www.am-online.com/news/autotrader-responds-to-deal-builder-criticism-after-facing-threat-of-mass-cancellations)
- [DealerRefresh: Why It Is Impossible to Cancel AutoTrader](https://forum.dealerrefresh.com/threads/why-it-is-impossible-to-cancel-autotrader.3466/)

### Lead Fraud and Compliance
- [ActiveProspect: A Challenging Type of Lead Fraud](https://activeprospect.com/blog/lead-fraud-bot-detection/)
- [ActiveProspect: Fake Leads - How to Mitigate Risk](https://activeprospect.com/blog/fake-leads/)
- [Spider AF: Lead Fraud Protection Guide 2025](https://spideraf.com/articles/what-is-lead-fraud)
- [LeadsHook: Lead Generation Fraud Guide 2026](https://www.leadshook.com/blog/lead-generation-fraud/)
- [FraudBlocker: Lead Generation Fraud - 7 Ways to Prevent Bot Leads](https://fraudblocker.com/articles/lead-generation-fraud)

### EV Incentives and Merchandising
- [DealerOn: DealerOn and Lyteflo Partner to Electrify EV Merchandising](https://www.dealeron.com/blog/dealeron-and-lyteflo-partner-to-electrify-ev-merchandising-on-dealer-websites/)
- [DealerOn: Lead Accelerator - Incentive Management System](https://www.dealeron.com/features-and-upgrades/lead-accelerator/)
- [Lyteflo: EV Sales and Service Tools](https://www.lyteflo.com/)

### Independent vs Franchise Dealers
- [Carketa: Franchise vs Independent Dealership Software Comparison](https://carketa.com/franchise-vs-independent-dealership-software/)
- [Spyne: Differences Between Franchised and Independent Car Dealerships](https://www.spyne.ai/blogs/independent-car-dealerships-differences)
- [Dealr: 10 Ways Independent Dealers Can Outperform Franchises](https://dealr.cloud/blog/how-independent-dealers-outperform-franchises)
- [DealershipGuy: From Corporate to Rural Dealer](https://news.dealershipguy.com/p/from-corporate-to-rural-dealer-what-it-takes-to-win-today-in-every-market-2025-11-28)

### Regional and Market Data
- [CBT News: The Impact of Urbanization on Dealerships](https://www.cbtnews.com/the-impact-of-urbanization-on-dealerships/)
- [Automotive Mastermind: How Dealers Can Ditch Third-Party Auto Leads](https://www.automotivemastermind.com/blog/car-sales/ditch-third-party-auto-leads/)
- [VisQuanta: Top 7 Third-Party Lead Providers for Dealerships](https://www.visquanta.com/blog-details/third-party-lead-providers-dealerships)
