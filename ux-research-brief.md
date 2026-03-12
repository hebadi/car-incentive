# UX Research Brief: Savings-Motivated Car Buyers on Incentive Aggregation Sites

**Product:** IncentiveDrive -- Car Incentive Discovery & Stacking Platform
**Date:** March 12, 2026
**Prepared by:** UX Research

---

## Executive Summary

Savings-motivated car buyers represent a large and growing segment: 43% of consumers say they would switch brands to get a lower price, and 62% feel vehicle ownership is too costly. These buyers spend 14+ hours researching online before purchase, with 61% of that traffic coming from mobile devices. They demand **price transparency** (65% call it the most important factor), **trustworthy data sources**, and **low-friction tools** that help them understand exactly how much they can save.

The opportunity for IncentiveDrive is clear: no single platform today aggregates all incentive types (federal, state, utility, manufacturer, military/educator) into a unified, personalized savings view. Existing sites like Edmunds, TrueCar, KBB, and CarsDirect each cover partial incentive data but none stack them comprehensively. Users are left to manually cross-reference multiple sources -- a painful, error-prone process.

This brief synthesizes findings from industry studies (Cox Automotive Car Buyer Journey, Shift Digital Pulse Report), competitive analysis, and user behavior data to provide actionable recommendations for the IncentiveDrive product.

---

## Key Findings

### 1. What Savings-Motivated Buyers Want

**Primary needs (in order of priority):**

1. **Total out-of-pocket cost clarity** -- Buyers want to know exactly what they will pay after all incentives, not just MSRP or individual rebate amounts. The #1 frustration is finding that final numbers differ from advertised prices.
2. **Personalized incentive eligibility** -- Incentives vary by ZIP code, income, military status, trade-in, and purchase type. Users want to enter their info once and see everything they qualify for.
3. **Comparison across purchase types** -- Cash, finance, and lease deals carry different incentives. Users need to compare total cost across these options side-by-side.
4. **Source credibility** -- Users are skeptical of deal claims. They trust platforms that show where data comes from (e.g., "based on manufacturer announcement dated X" or "data from state rebate program Y").
5. **Timeliness** -- Incentive programs change quarterly or monthly. Users need to know when deals expire and whether the data is current.

**Buyer persona -- The Bargain Hunter:**
- Extremely price-sensitive; purchase timing is often driven by financial triggers (tax season, high rebates, low interest rates)
- Uses aggressive research and comparison across multiple sites
- Will sacrifice brand loyalty for savings (43% of consumers)
- Spends above-average time on research (14h 19m online average)
- Wants to feel confident they are getting the best possible deal before contacting a dealer

### 2. UX Patterns That Work on Competitor Sites

**TrueCar (7M+ monthly unique visitors):**
- Shows "what others paid" as a price anchor -- creates trust through social proof
- Clean, free-to-use interface with no upselling or hidden fees
- Real-time market data with local pricing
- ZIP code entry as the primary personalization mechanism
- A+ BBB rating prominently displayed

**Edmunds:**
- Strong editorial content (expert reviews, comparison tools) alongside deals
- "True Market Value" pricing based on actual transaction data
- Calculators that auto-populate data once a vehicle is selected (minimizes user input)
- Low APR vs. Cash Back calculator -- helps users decide which incentive path saves more
- Ownership cost calculators that factor in incentives

**CarsDirect:**
- Separates deals into three clear categories: Lease / Finance / Cash Rebate
- Users can toggle between "Payment" and "Cash Rebate" views
- Brand-specific incentive pages updated monthly
- Editorial articles contextualizing the deals (e.g., "Best Lease Deals in March 2026")

**Key pattern:** All successful sites use **ZIP code as the entry point** for personalization, separate deals by purchase type (cash/finance/lease), and provide editorial context alongside raw numbers.

### 3. Pain Points and Unmet Needs

**From user research and forums:**

| Pain Point | Severity | Current State |
|---|---|---|
| No single source aggregates ALL incentive types (federal + state + utility + manufacturer + special eligibility) | Critical | Users must visit 3-5 sites to find all incentives |
| Incentive eligibility is confusing (income limits, residency requirements, vehicle eligibility) | High | Most sites list incentives without checking eligibility |
| Stacking rules are opaque (which incentives can combine?) | High | Almost no site explains combinability |
| Expired or outdated deal information | High | Many sites show stale data; TrueCar checks daily but others lag |
| Paperwork burden for claiming rebates is unclear upfront | Medium | Users discover complexity only after committing |
| Cash vs. finance vs. lease comparison is fragmented | Medium | Sites show one type well but rarely compare across all three |
| Mobile experience is slow or cluttered | Medium | 61% of traffic is mobile but many deals pages are desktop-optimized |

**Unmet needs identified:**
- A "total savings calculator" that stacks all eligible incentives into one number
- Clear explanation of which incentives stack and which are mutually exclusive
- Timeline visibility (when incentives expire, application deadlines)
- Step-by-step guidance on how to claim each incentive after purchase
- Alerts/notifications when new incentives become available for a saved vehicle

### 4. Lead Generation & Conversion Patterns

**What works in automotive lead gen:**

- **Progressive disclosure**: Don't ask for all info upfront. Start with ZIP code and vehicle interest, then gradually request name/email/phone as users go deeper.
- **Minimal form fields**: Name + email or phone is optimal. Every additional field reduces conversion. Requiring all four fields (name, address, email, phone) significantly drops completion rates.
- **Value-first CTAs**: "See Your Total Savings" or "Get Your Personalized Deal" outperform "Submit" or "Contact Dealer." Action-oriented CTAs like "Get Our Best Price Today" are top performers.
- **Avoid feeling pushy**: Users flee when they sense the site exists primarily to collect their info for dealer leads. Trust is built by providing genuine value before asking for anything.
- **Timely offers**: Behavior-tracked incentive pop-ups at salient moments (e.g., after a user has spent 30+ seconds on a vehicle page) convert better than immediate pop-ups.
- **Live chat**: Increases conversion 20-30% vs. static forms.
- **Speed of follow-up**: Leads contacted within 5 minutes convert at dramatically higher rates.

**Trust signals that improve conversion:**
- SSL/security badges near forms
- "We never share your info with dealers without your permission"
- Customer testimonials and delivery-day photos
- BBB ratings and partner logos
- Transparent explanation of how the site makes money

### 5. Mobile-First Considerations

**Traffic data:**
- 61% of automotive website traffic is from mobile
- 54% of car shoppers use phones more than desktops
- 70%+ use smartphones as their primary research device
- 78% of mobile local searches result in business visits within 24 hours

**Mobile UX requirements:**
- Thumb-friendly navigation (large tap targets, bottom-anchored CTAs)
- Fast load times (mobile users are less tolerant; slow sites lose the majority before engagement)
- Simplified incentive display (collapsible cards rather than dense tables)
- Sticky "total savings" bar that updates as users explore incentives
- One-tap ZIP code entry via location services
- Swipeable comparison between purchase types (cash / finance / lease)

**Mobile conversion note:** Mobile conversion rates average 3.48% vs. higher desktop rates, and mobile cost-per-conversion runs 60% higher. This means the mobile funnel must be especially frictionless -- every unnecessary step costs more on mobile.

---

## Competitive Analysis Summary

| Feature | TrueCar | Edmunds | KBB | CarsDirect | IncentiveDrive (Opportunity) |
|---|---|---|---|---|---|
| Manufacturer incentives | Yes | Yes | Yes | Yes | Yes |
| State rebates (EV) | Partial | Partial | Yes | No | **Full coverage** |
| Utility rebates | No | No | No | No | **Yes -- key differentiator** |
| Federal tax credits | Partial | Yes | Yes | Partial | **Yes, with eligibility check** |
| Military/educator/first-responder discounts | Listed | Listed | Listed | Listed | **Stacked into total** |
| Incentive stacking calculator | No | No | No | No | **Primary feature** |
| Cash vs. finance vs. lease comparison | Partial | Yes (calculator) | Partial | Yes (tabs) | **Side-by-side with stacked incentives** |
| Personalized eligibility | ZIP only | ZIP only | ZIP only | ZIP only | **ZIP + income + status + utility** |
| Expiration/timeline visibility | Limited | Limited | Limited | Limited | **Prominent countdown + alerts** |
| How-to-claim guidance | No | No | No | No | **Step-by-step per incentive** |
| Mobile-first design | Responsive | Responsive | Responsive | Responsive | **Mobile-native** |

---

## Recommendations

### P0 -- Must Have (Launch Blockers)

1. **Incentive Stacking Calculator as Hero Feature**
   Show a single, bold "total savings" number that combines all eligible incentives. This is the core value proposition and must be above the fold. Users should see something like "You could save up to $12,350 on a 2026 Chevy Equinox EV" within seconds of entering their ZIP code and selecting a vehicle.

2. **ZIP Code as Primary Entry Point**
   Every competitor uses ZIP code as the personalization gate. IncentiveDrive should auto-detect location (with permission) or prompt ZIP code entry immediately. All incentive data must be localized.

3. **Cash / Finance / Lease Toggle**
   Display incentive stacks for each purchase type with a clear toggle or tab UI. Different incentives apply to different purchase types -- this is a top user need and every competitor separates them.

4. **Source Attribution on Every Incentive**
   Each listed incentive must show its source (e.g., "California Clean Vehicle Rebate Project," "Toyota Motor Sales") and last-verified date. This is the #1 trust builder for deal-skeptical users.

5. **Mobile-First Responsive Design**
   With 61% mobile traffic, the site must be designed mobile-first. Key elements: sticky savings bar, collapsible incentive cards, thumb-friendly CTAs, fast load times (<3s), and location-based ZIP auto-fill.

### P1 -- High Priority (First 30 Days Post-Launch)

6. **Eligibility Questionnaire (Progressive)**
   After ZIP code, progressively ask: income range, military/educator/first-responder status, current vehicle (for trade-in incentives), and utility provider. Each answer should immediately update the savings total -- creating a satisfying "watch it grow" experience.

7. **Incentive Expiration Countdown**
   Show expiration dates prominently with countdown indicators (e.g., "Expires in 12 days"). Color-code urgency: green (30+ days), yellow (7-30 days), red (<7 days). This creates urgency without feeling manipulative.

8. **"How to Claim" Guides**
   For each incentive, provide a collapsible section explaining: required documents, application process, timeline to receive funds, and any gotchas. This is a major unmet need -- users currently discover paperwork complexity only after committing.

9. **Value-First Lead Capture**
   Primary CTA should be "See Your Full Savings Breakdown" (not "Get a Quote" or "Contact Dealer"). Require only ZIP code and email to deliver the full breakdown. Phone number should be optional. Explain clearly: "We'll email your personalized savings report."

10. **Editorial Deal Context**
    Alongside raw incentive data, provide brief editorial notes (e.g., "This is the largest Toyota cash rebate we've seen since 2024" or "California's CVRP funds are running low -- apply soon"). This builds trust and creates urgency through expertise rather than sales pressure.

### P2 -- Important (60-90 Days Post-Launch)

11. **Savings Alerts & Notifications**
    Allow users to save a vehicle and receive email/SMS alerts when new incentives become available or existing ones are about to expire. This is a retention mechanism and re-engagement channel.

12. **Comparison Tool**
    Let users compare total savings across 2-3 vehicles side-by-side, including all stacked incentives. This helps undecided buyers and increases time on site.

13. **Live Chat / AI Assistant**
    Implement chat that can answer incentive eligibility questions in real time. Live chat increases conversion 20-30% over static forms. An AI chatbot trained on incentive data could scale this cost-effectively.

14. **Community Trust Signals**
    Add user testimonials focused on savings achieved (e.g., "I saved $11,200 on my Bolt EUV thanks to IncentiveDrive"). Feature real savings amounts and locations. Delivery-day photos perform well as social proof.

15. **Dealer Transparency**
    When connecting users to dealers, clearly state: "This dealer has agreed to honor these incentives" or show dealer ratings. Users' top complaint about lead-gen sites is feeling "sold" to a dealer who then changes the deal.

---

## Key Metrics to Track

| Metric | Target | Rationale |
|---|---|---|
| ZIP code entry rate | >60% of visitors | Gate to personalization; low rate = unclear value prop |
| Savings calculator completion | >40% of ZIP entrants | Core engagement metric |
| Lead form submission rate | >8% of calculator completers | Industry avg is 2-5%; value-first approach should exceed |
| Mobile bounce rate | <45% | Below industry avg of 50%+ for auto sites |
| Time to first meaningful interaction | <10 seconds | Users must see value immediately |
| Incentive data freshness | <7 days stale | Trust depends on accuracy |

---

## Sources

- [Cox Automotive Car Buyer Journey Study](https://www.coxautoinc.com/insights/cox-automotive-car-buyer-journey-study-finds-efficiency-digital-tools-and-ai-drive-record-satisfaction/)
- [Consumer Behavior in Car Buying Statistics 2025](https://www.demandlocal.com/blog/consumer-behavior-car-buying-statistics/)
- [Car Buyer Behavior Trends Statistics](https://www.demandlocal.com/blog/car-buyer-behavior-trends-statistics/)
- [Dealership Outlook: Consumer Shopping Trends 2025](https://www.recallmasters.com/dealership-outlook-consumer-shopping-trends-for-2025/)
- [CTA Optimization for Automotive Websites](https://dealerknows.com/cta-optimization-automotive-website-conversion-rates/)
- [Automotive Conversion Rate Optimization Guide](https://www.spyne.ai/blogs/car-dealership-conversion-rates)
- [Edmunds vs TrueCar Comparison](https://www.rydeshopper.com/car-buying-tips/edmunds-vs-truecar)
- [Car Buyer Personas](https://www.cbtnews.com/decoding-car-buyer-personas-understanding-emotional-triggers-and-decision-making-factors/)
- [Automotive Digital Marketing Statistics 2025](https://www.demandlocal.com/blog/automotive-digital-marketing-statistics/)
- [Auto Shopper Behavior Statistics](https://www.demandlocal.com/blog/auto-shopper-behavior-statistics/)
- [Pain Points: Buyers Have Changed](https://www.cbtnews.com/pain-points-buyers-have-changed-and-dealers-should-too/)
- [CarsDirect Deals](https://www.carsdirect.com/deals)
- [Edmunds Auto Calculators](https://www.edmunds.com/calculators/)
- [Electric Vehicle Incentives by State](https://www.kbb.com/car-advice/electric-vehicle-rebates-by-state/)
- [EV Incentives - Electric For All](https://www.electricforall.org/rebates-incentives/)
- [Shift Digital 2025 Pulse Report](https://www.shiftdigital.com/2025-Digital-Automotive-Shopping-Trends)
