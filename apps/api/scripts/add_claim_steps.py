"""Add claim_steps JSONB column to incentive_programs and populate data."""

import asyncio
import json

from sqlalchemy import text

from app.database import engine


CLAIM_STEPS_BY_CATEGORY = {
    # Federal tax credits (Section 30D new, 25E used)
    "federal_30d": [
        {"step": 1, "title": "Check Eligibility", "description": "Confirm the vehicle is on the IRS qualified list and meets the MSRP cap ($55,000 for sedans, $80,000 for SUVs/trucks). Your Modified Adjusted Gross Income must be under $150,000 (single) or $300,000 (married filing jointly)."},
        {"step": 2, "title": "Decide: Tax Credit or Point-of-Sale Transfer", "description": "You can either claim the full credit on your tax return, or transfer it to the dealer at purchase to get an instant price reduction. Ask the dealer if they participate in the IRS transfer program."},
        {"step": 3, "title": "Get the Seller Report", "description": "The dealer must submit a seller report to the IRS and provide you with a copy (IRS Time of Sale Report). You need the vehicle's VIN.", "documents": ["VIN", "Dealer time-of-sale report", "Purchase agreement"]},
        {"step": 4, "title": "File IRS Form 8936", "description": "If claiming on your tax return, attach Form 8936 (Qualified Plug-in Electric Drive Motor Vehicle Credit) when you file. The credit is nonrefundable — it reduces your tax owed, up to $7,500.", "url": "https://www.irs.gov/forms-pubs/about-form-8936", "documents": ["IRS Form 8936", "Copy of seller report"]},
        {"step": 5, "title": "Receive Credit", "description": "If transferred to dealer, the discount is applied at purchase. If claimed on tax return, you receive it when your return is processed (typically within 3 weeks of e-filing)."},
    ],
    "federal_25e": [
        {"step": 1, "title": "Check Eligibility", "description": "The used EV must be at least 2 model years old, priced at $25,000 or less, and purchased from a licensed dealer (not private sale). Your income must be under $75,000 (single) or $150,000 (married filing jointly)."},
        {"step": 2, "title": "Get Dealer Documentation", "description": "The dealer must submit a seller report to the IRS. You receive a copy as proof of the qualified sale.", "documents": ["VIN", "Dealer time-of-sale report", "Bill of sale showing price under $25,000"]},
        {"step": 3, "title": "File IRS Form 8936", "description": "Attach Form 8936 to your tax return. The used EV credit is up to $4,000 or 30% of the sale price, whichever is less.", "url": "https://www.irs.gov/forms-pubs/about-form-8936", "documents": ["IRS Form 8936"]},
        {"step": 4, "title": "Receive Credit", "description": "Credit is applied when your tax return is processed. If transferred to dealer at point of sale, discount is immediate."},
    ],
    # California Clean Cars 4 All (CC4A)
    "ca_cc4a": [
        {"step": 1, "title": "Check Eligibility", "description": "You must live in an eligible air district (South Coast, San Joaquin Valley, Bay Area, or Sacramento). Household income must be at or below 400% of the federal poverty level. You must own and scrap an older, high-polluting vehicle."},
        {"step": 2, "title": "Contact Your Local Air District", "description": "Each air district administers CC4A differently. Contact your district office or visit their website to start an application and check for available funding."},
        {"step": 3, "title": "Gather Documents", "description": "You will need proof of income, vehicle registration for the car being scrapped, and proof of residency in the air district.", "documents": ["Proof of income (tax return or pay stubs)", "Vehicle registration for scrap vehicle", "Proof of residency", "Valid driver's license", "Smog check certificate for scrap vehicle"]},
        {"step": 4, "title": "Get Vehicle Appraised and Scrapped", "description": "Your old vehicle must pass a smog check (to prove it runs) and then be scrapped at an authorized dismantler. The air district coordinates this."},
        {"step": 5, "title": "Purchase or Lease Replacement Vehicle", "description": "Choose an eligible clean vehicle (BEV, PHEV, or FCEV). Grants range from $9,500 to $12,000 depending on the vehicle type and your income level."},
        {"step": 6, "title": "Receive Funds", "description": "The grant is typically applied as a voucher or direct payment after purchase. Processing times vary by district but expect 4-8 weeks."},
    ],
    # California DCAP (Disadvantaged Communities)
    "ca_dcap": [
        {"step": 1, "title": "Check Eligibility", "description": "Similar to CC4A but specifically for residents of disadvantaged communities as defined by CalEnviroScreen. Income limits may differ by district."},
        {"step": 2, "title": "Apply Through Your Air District", "description": "Contact your local air district. DCAP may have separate funding and different income tiers than CC4A."},
        {"step": 3, "title": "Gather Documents", "description": "Prepare proof of income, proof of residency in a disadvantaged community, and vehicle registration for the car being scrapped.", "documents": ["Proof of income", "Proof of residency in disadvantaged community", "Vehicle registration for scrap vehicle", "Valid driver's license"]},
        {"step": 4, "title": "Complete Scrap and Purchase", "description": "Scrap your old vehicle at an authorized dismantler and purchase an eligible clean vehicle."},
        {"step": 5, "title": "Receive Funds", "description": "Expect the incentive as a voucher or check within 4-8 weeks of completing the process."},
    ],
    # California CVRP
    "ca_cvrp": [
        {"step": 1, "title": "Check Eligibility", "description": "CVRP is available statewide in California. Income must be under $135,000 (single) or $200,000 (household). The vehicle must be new and eligible (BEV, PHEV, or FCEV). Check the current waitlist status."},
        {"step": 2, "title": "Purchase or Lease Your Vehicle", "description": "Buy or lease an eligible vehicle first. You apply for the rebate after purchase, not before."},
        {"step": 3, "title": "Apply Online Within 3 Months", "description": "Submit your application at cleanvehiclerebate.org within 3 months of the purchase/lease date.", "url": "https://cleanvehiclerebate.org/en/apply", "documents": ["Vehicle purchase/lease agreement", "Vehicle registration", "Proof of California residency", "Most recent tax return (for income verification)"]},
        {"step": 4, "title": "Wait for Processing", "description": "Applications are processed in the order received. Standard rebates are $2,000 for BEVs and $1,000 for PHEVs. Increased rebates available for lower-income applicants. Note: CVRP may have a waitlist when funding is limited."},
        {"step": 5, "title": "Receive Rebate Check", "description": "Once approved, expect a rebate check within 2-3 months. If waitlisted, you'll be notified when funding becomes available."},
    ],
    # Utility rebates (generic template)
    "utility_rebate": [
        {"step": 1, "title": "Verify Your Utility Provider", "description": "Confirm you are a current customer of the utility offering the rebate. Your account must be in good standing."},
        {"step": 2, "title": "Purchase an Eligible Vehicle", "description": "Buy or lease a qualifying electric vehicle. Most utility rebates require a new BEV or PHEV."},
        {"step": 3, "title": "Apply Online", "description": "Visit your utility's EV rebate page and submit the online application. Most utilities require you to apply within 90 days of purchase.", "documents": ["Utility account number", "Vehicle purchase/lease agreement", "Vehicle registration", "Copy of driver's license"]},
        {"step": 4, "title": "Receive Rebate", "description": "Rebates are typically issued as a bill credit or check within 4-8 weeks of approval."},
    ],
    # Manufacturer cash rebates
    "manufacturer_rebate": [
        {"step": 1, "title": "Confirm Offer Availability", "description": "Check the manufacturer's website or ask your dealer to confirm the rebate is currently active for your selected vehicle and trim."},
        {"step": 2, "title": "Purchase Vehicle", "description": "The rebate is applied automatically at the point of sale. It will appear as a line item on your purchase agreement reducing the price."},
        {"step": 3, "title": "No Separate Application Needed", "description": "Manufacturer cash rebates are handled entirely by the dealer. You do not need to file any paperwork separately."},
    ],
    # 0% APR financing
    "apr_financing": [
        {"step": 1, "title": "Check Credit Qualification", "description": "0% APR offers typically require excellent credit (usually 700+ FICO score). The offer is through the manufacturer's captive lender (e.g., Toyota Financial, Hyundai Capital)."},
        {"step": 2, "title": "Choose Your Term", "description": "0% APR may only be available on specific loan terms (e.g., 36, 48, or 60 months). Longer terms may have a low but non-zero rate. Ask the dealer for all available terms."},
        {"step": 3, "title": "Apply at the Dealer", "description": "The finance manager will run your credit application through the captive lender. If approved, the 0% rate is applied to your loan.", "documents": ["Valid driver's license", "Proof of income", "Proof of residency"]},
        {"step": 4, "title": "Note: May Not Stack with Cash Rebate", "description": "Many manufacturers make you choose between 0% APR and a cash rebate. Compare the total cost of each option to see which saves more."},
    ],
    # Affinity discounts (military, first responder, etc.)
    "affinity_discount": [
        {"step": 1, "title": "Verify Eligibility", "description": "Check which affinity groups qualify (e.g., military, first responder, educator, college graduate, loyalty/conquest). Requirements vary by manufacturer."},
        {"step": 2, "title": "Gather Proof of Eligibility", "description": "Bring documentation proving your affinity group membership to the dealer.", "documents": ["Military: DD-214, Leave & Earnings Statement, or military ID", "First Responder: badge, department ID, or pay stub", "Educator: school ID or pay stub", "College Grad: diploma or transcript (within last 2 years)", "Loyalty: current registration of qualifying brand vehicle"]},
        {"step": 3, "title": "Present at Dealer", "description": "The discount is applied at the point of sale. Inform the dealer before negotiating the price so it can be included in the deal."},
        {"step": 4, "title": "Receive Discount", "description": "Typically $500-$1,000 off. This usually stacks with other manufacturer offers and is deducted directly from the purchase price."},
    ],
    # Lease-specific incentives
    "lease_incentive": [
        {"step": 1, "title": "Understand Lease Incentive Structure", "description": "Lease incentives are applied by the dealer during lease structuring. They may appear as a reduced capitalized cost, lower money factor, or bonus cash applied to the lease."},
        {"step": 2, "title": "Ask Dealer for Lease Worksheet", "description": "Request a full lease breakdown showing how incentives are applied. The dealer should show the cap cost reduction separately."},
        {"step": 3, "title": "No Separate Application", "description": "Lease incentives are handled entirely between the dealer and the manufacturer's leasing company. You do not need to apply separately."},
        {"step": 4, "title": "Note on Federal Tax Credit", "description": "On a lease, the federal EV tax credit goes to the leasing company (not you), but it is typically passed through as a cap cost reduction, lowering your monthly payment."},
    ],
}


async def run_migration():
    """Add claim_steps column and populate data."""
    async with engine.begin() as conn:
        # Add the column
        await conn.execute(text(
            "ALTER TABLE incentive_programs ADD COLUMN IF NOT EXISTS claim_steps JSONB DEFAULT '[]'"
        ))
        print("Added claim_steps column")

        # Populate based on incentive characteristics
        # Federal tax credits (30D)
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'federal'
              AND claim_mechanism = 'tax_return'
              AND name ILIKE '%new%clean%vehicle%'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["federal_30d"])})

        # Federal used EV credit (25E)
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'federal'
              AND claim_mechanism = 'tax_return'
              AND name ILIKE '%used%'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["federal_25e"])})

        # Remaining federal credits get 30D steps as default
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'federal'
              AND claim_mechanism = 'tax_return'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["federal_30d"])})

        # California CC4A
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE name ILIKE '%clean cars 4 all%'
              OR name ILIKE '%cc4a%'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["ca_cc4a"])})

        # California DCAP
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE (name ILIKE '%dcap%' OR name ILIKE '%disadvantaged communit%')
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["ca_dcap"])})

        # California CVRP
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE (name ILIKE '%cvrp%' OR name ILIKE '%clean vehicle rebate%')
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["ca_cvrp"])})

        # Utility rebates
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'utility'
              AND claim_mechanism = 'post_purchase_rebate'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["utility_rebate"])})

        # Manufacturer cash rebates (point of sale)
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'manufacturer'
              AND claim_mechanism = 'point_of_sale'
              AND incentive_value_type IN ('fixed', 'percentage')
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["manufacturer_rebate"])})

        # 0% APR / rate reduction financing
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE incentive_value_type = 'rate_reduction'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["apr_financing"])})

        # Affinity discounts
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'affinity'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["affinity_discount"])})

        # Lease-specific incentives
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE claim_mechanism = 'lease_reduction'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["lease_incentive"])})

        # State post-purchase rebates that haven't been categorized yet
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'state'
              AND claim_mechanism = 'post_purchase_rebate'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["ca_cvrp"])})

        # Manufacturer point-of-sale that weren't caught above
        await conn.execute(text("""
            UPDATE incentive_programs
            SET claim_steps = :steps
            WHERE type = 'manufacturer'
              AND claim_steps = '[]'::jsonb
        """), {"steps": json.dumps(CLAIM_STEPS_BY_CATEGORY["manufacturer_rebate"])})

        print("Populated claim_steps data")


if __name__ == "__main__":
    asyncio.run(run_migration())
