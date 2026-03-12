"""
Base spider class for incentive program scraping.

Provides common patterns: rate limiting, user-agent rotation, retry logic,
and output formatting matching the IncentiveProgram schema.
"""

import random
from datetime import datetime, timezone

import scrapy
from scrapy.exceptions import IgnoreRequest

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
]


class IncentiveSpider(scrapy.Spider):
    """Base spider with common configuration for scraping incentive programs."""

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "CONCURRENT_REQUESTS": 1,
        "RETRY_TIMES": 3,
        "RETRY_HTTP_CODES": [429, 500, 502, 503, 504],
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 2,
        "AUTOTHROTTLE_MAX_DELAY": 30,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "ROBOTSTXT_OBEY": True,
        "HTTPCACHE_ENABLED": True,
        "HTTPCACHE_EXPIRATION_SECS": 86400,
        "HTTPCACHE_DIR": "httpcache",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request_count = 0

    def _rotate_user_agent(self) -> str:
        return random.choice(USER_AGENTS)

    def make_request(self, url: str, callback, **kwargs):
        """Create a request with a rotated user-agent header."""
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self._rotate_user_agent()
        return scrapy.Request(url, callback=callback, headers=headers, **kwargs)

    def build_incentive_item(
        self,
        *,
        name: str,
        type: str,
        source_authority: str,
        geographic_scope: str,
        eligible_states: list[str] | None = None,
        vehicle_criteria: dict | None = None,
        buyer_criteria: dict | None = None,
        incentive_value_type: str,
        incentive_amount: float | None = None,
        incentive_max_amount: float | None = None,
        incentive_percentage: float | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        funding_status: str = "open",
        claim_mechanism: str,
        source_url: str,
        confidence_score: float = 0.7,
    ) -> dict:
        """Build a dict matching the IncentiveProgram schema."""
        return {
            "name": name,
            "type": type,
            "source_authority": source_authority,
            "geographic_scope": geographic_scope,
            "eligible_states": eligible_states or [],
            "eligible_zips": [],
            "vehicle_criteria": vehicle_criteria or {},
            "buyer_criteria": buyer_criteria or {},
            "incentive_value_type": incentive_value_type,
            "incentive_amount": incentive_amount,
            "incentive_max_amount": incentive_max_amount,
            "incentive_percentage": incentive_percentage,
            "stackable_with": [],
            "mutually_exclusive_with": [],
            "start_date": start_date,
            "end_date": end_date,
            "application_deadline": None,
            "funding_status": funding_status,
            "claim_mechanism": claim_mechanism,
            "last_verified": datetime.now(timezone.utc).isoformat(),
            "source_url": source_url,
            "confidence_score": confidence_score,
            "is_active": funding_status not in ("depleted", "suspended"),
        }
