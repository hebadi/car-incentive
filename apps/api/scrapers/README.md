# Incentive Scrapers

Scrapy-based web scrapers for keeping incentive program data current.

## Architecture

- **`base_spider.py`** -- Base class with rate limiting, user-agent rotation, retry logic, and `build_incentive_item()` helper that outputs data matching the `incentive_programs` table schema.
- **`nyserda_spider.py`** -- Example spider for New York's Drive Clean Rebate program.

## Adding a New Spider

1. Create `scrapers/<state_or_source>_spider.py`
2. Subclass `IncentiveSpider` from `base_spider.py`
3. Set `start_urls` to the program's official page(s)
4. Implement `parse()` to extract:
   - Rebate/credit amount(s)
   - Funding status (open, suspended, depleted)
   - Any eligibility changes
5. Yield items via `self.build_incentive_item(...)` -- all required fields are listed in the method signature
6. Test with: `scrapy runspider scrapers/<your_spider>.py -o output/test.json`

## Running

```bash
# Single spider
scrapy runspider scrapers/nyserda_spider.py -o output/nyserda.json

# All spiders via Celery task (see app/tasks/refresh_incentives.py)
python -m app.tasks.refresh_incentives
```

## Output Format

Each spider yields dicts matching the `incentive_programs` table columns. The Celery refresh task handles upserting results into the database and detecting diffs from the previous run.

## Rate Limiting

All spiders inherit these defaults from `IncentiveSpider`:
- 3-second download delay (randomized)
- Auto-throttle with max 30s delay
- Robots.txt compliance
- HTTP response caching (24h)
- Retry on 429/5xx codes

Override `custom_settings` in your spider subclass if a source requires different behavior.
