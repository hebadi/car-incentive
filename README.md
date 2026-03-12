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

- Node.js 20+
- Python 3.12+
- Docker & Docker Compose

## Local Development Setup

### 1. Start infrastructure

```bash
docker compose up -d
```

This starts PostgreSQL 16 on port 5432 and Redis 7 on port 6379.

### 2. Set up environment

```bash
cp .env.example .env
```

### 3. Install frontend dependencies

```bash
npm install
```

### 4. Install backend dependencies

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Run database migration

```bash
psql $DATABASE_URL -f apps/api/app/migrations/001_initial_schema.sql
```

### 6. Start development servers

In separate terminals:

```bash
# Consumer web app (port 3000)
npm run dev:web

# Dealer portal (port 3001)
npm run dev:dealer

# API server (port 8000)
npm run dev:api
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
