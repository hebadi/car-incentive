#!/usr/bin/env bash
set -euo pipefail

# IncentiveDrive Local Dev Setup
# One-shot bootstrap: starts infra, installs deps, runs migrations, seeds data.
# Usage:
#   ./scripts/setup.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

check_cmd() {
  if ! command -v "$1" &>/dev/null; then
    echo "Error: '$1' is not installed (or not on your PATH)."
    echo "$2"
    echo "Install it, restart your terminal, then re-run ./scripts/setup.sh"
    exit 1
  fi
}

check_cmd docker "Install Docker Desktop: https://www.docker.com/products/docker-desktop/"
check_cmd node "Install Node.js 20+: https://nodejs.org/"
check_cmd npm "npm ships with Node.js — install Node.js 20+: https://nodejs.org/"
check_cmd python3 "Install Python 3.9+: https://www.python.org/downloads/"

echo "=== 1/6: Starting Postgres + Redis ==="
docker compose up -d

echo ""
echo "=== 2/6: Waiting for Postgres to be healthy ==="
until docker compose exec -T postgres pg_isready -U postgres &>/dev/null; do
  sleep 1
done
echo "Postgres is ready."

echo ""
echo "=== 3/6: Setting up env files ==="
[ -f .env ] || { cp .env.example .env; echo "Created .env"; }
[ -f apps/api/.env ] || { cp apps/api/.env.example apps/api/.env; echo "Created apps/api/.env"; }

echo ""
echo "=== 4/6: Installing frontend dependencies ==="
npm install

echo ""
echo "=== 5/6: Installing backend dependencies ==="
cd apps/api
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
cd "$ROOT_DIR"

echo ""
echo "=== 6/6: Running migrations and seeding data ==="
for migration in apps/api/app/migrations/*.sql; do
  echo "Applying $(basename "$migration")..."
  docker compose exec -T postgres psql -U postgres -d incentive_drive -f - < "$migration"
done

cd apps/api
source .venv/bin/activate
python scripts/seed_incentives.py
python scripts/seed_dealers.py
cd "$ROOT_DIR"

echo ""
echo "=== Setup complete! ==="
echo "Next: run ./scripts/dev.sh to start the app."
