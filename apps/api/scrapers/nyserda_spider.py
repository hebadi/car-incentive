"""
Example spider: scrapes the NYSERDA Drive Clean Rebate page for current
incentive amounts and program status.

Usage:
    cd apps/api
    scrapy runspider scrapers/nyserda_spider.py -o output/nyserda.json
"""

from scrapers.base_spider import IncentiveSpider


class NYSERDASpider(IncentiveSpider):
    name = "nyserda_drive_clean"
    allowed_domains = ["www.nyserda.ny.gov"]
    start_urls = [
        "https://www.nyserda.ny.gov/All-Programs/Drive-Clean-Rebate-For-Electric-Cars-Program",
    ]

    def parse(self, response):
        # Look for rebate amount in page content.
        # NYSERDA typically shows the rebate in a prominent heading or table.
        # This selector may need updating if the page structure changes.
        body_text = response.css("div.field-content ::text, div.page-content ::text").getall()
        body_text = " ".join(t.strip() for t in body_text if t.strip())

        # Default amount from research; override if we can parse from page
        rebate_amount = 2000.0

        # Try to extract dollar amounts near "rebate" text
        import re
        amounts = re.findall(r"\$(\d{1,3}(?:,\d{3})*)", body_text)
        for raw in amounts:
            val = float(raw.replace(",", ""))
            if 500 <= val <= 5000:
                rebate_amount = val
                break

        # Detect if funding is suspended or depleted
        funding_status = "open"
        lower_text = body_text.lower()
        if "suspended" in lower_text or "paused" in lower_text:
            funding_status = "suspended"
        elif "depleted" in lower_text or "exhausted" in lower_text or "no longer accepting" in lower_text:
            funding_status = "depleted"

        yield self.build_incentive_item(
            name="New York Drive Clean Rebate (NYSERDA)",
            type="state",
            source_authority="NYSERDA",
            geographic_scope="state",
            eligible_states=["NY"],
            vehicle_criteria={
                "fuel_types": ["BEV", "PHEV"],
                "new_or_used": "new",
            },
            buyer_criteria={},
            incentive_value_type="fixed",
            incentive_amount=rebate_amount,
            incentive_max_amount=rebate_amount,
            funding_status=funding_status,
            claim_mechanism="point_of_sale",
            source_url=response.url,
            confidence_score=0.85,
        )
