# IncentiveDrive

Incentive-aware automotive lead generation platform.

## Project Structure

```
apps/
  web/             Next.js consumer app (incentive calculator)
  dealer-portal/   Next.js dealer dashboard
  api/             Python/FastAPI backend
packages/
  shared/          Shared TypeScript types and API contracts
```

## Prerequisites

Install these before you start — all have official installers for Mac/Windows/Linux:

- **Node.js 20+**
- **Python 3.9+**
- **Docker Desktop** (provides `docker` and `docker compose`)

## Quick Start (recommended)

This gets the whole app running with two commands. No prior experience with
this repo needed.

### 1. Clone the repo

```bash
git clone https://github.com/hebadi/car-incentive.git
cd car-incentive
```

### 2. Run the setup script

```bash
./scripts/setup.sh
```

This one command starts Postgres + Redis, creates your `.env` files,
installs all frontend and backend dependencies, runs the database
migrations, and seeds sample incentive/dealer data. It only needs to be
run once (or again later if a new migration is added).

### 3. Start the app

```bash
./scripts/dev.sh
```

This starts both the API (port 8000) and the consumer web app (port 3000)
and streams their logs to your terminal. Press `Ctrl+C` to stop both.

### 4. Open it

Go to **http://localhost:3000** in your browser. API docs are at
**http://localhost:8000/docs**.

> Some features (e.g. live vehicle catalog sync, OEM incentive monitoring)
> need real API keys. Add `MARKETCHECK_API_KEY` and `GEMINI_API_KEY` to
> `apps/api/.env` if you want those to run — everything else works out of
> the box with the seeded sample data.

## Manual Setup (advanced)

If you'd rather run each step yourself instead of `./scripts/setup.sh`:

```bash
# 1. Start infrastructure (Postgres on 5432, Redis on 6379)
docker compose up -d

# 2. Set up environment files
cp .env.example .env
cp apps/api/.env.example apps/api/.env

# 3. Install frontend dependencies
npm install

# 4. Install backend dependencies
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ../..

# 5. Run database migrations (in order)
docker compose exec -T postgres psql -U postgres -d incentive_drive -f - < apps/api/app/migrations/001_initial_schema.sql
docker compose exec -T postgres psql -U postgres -d incentive_drive -f - < apps/api/app/migrations/002_vehicle_catalog.sql

# 6. Seed sample data
cd apps/api && source .venv/bin/activate
python scripts/seed_incentives.py
python scripts/seed_dealers.py
cd ../..
```

Then start each server in its own terminal:

```bash
npm run dev:web     # Consumer web app (port 3000)
npm run dev:dealer  # Dealer portal (port 3001)
npm run dev:api     # API server (port 8000)
```

## Testing

```bash
# Frontend
npm run test

# Backend
cd apps/api && python -m pytest
```

## Type Checking

```bash
npm run typecheck
```
