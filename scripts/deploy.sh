#!/usr/bin/env bash
set -euo pipefail

# IncentiveDrive Production Deployment Script
# Usage:
#   ./scripts/deploy.sh [fly|compose]
#
# Options:
#   fly      - Deploy API to Fly.io (recommended)
#   compose  - Deploy full stack with docker-compose

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

command="${1:-}"

case "$command" in
  fly)
    echo "=== Deploying API to Fly.io ==="
    cd "$ROOT_DIR/apps/api"

    # Check fly CLI is installed
    if ! command -v fly &>/dev/null; then
      echo "Error: Install flyctl first: https://fly.io/docs/hands-on/install-flyctl/"
      exit 1
    fi

    # Check if app exists, create if not
    if ! fly status &>/dev/null 2>&1; then
      echo "Creating Fly.io app..."
      fly launch --no-deploy --region ewr
    fi

    # Set secrets if not already set
    echo "Checking secrets..."
    fly secrets list 2>/dev/null | grep -q DATABASE_URL || {
      echo ""
      echo "You need to set secrets. Run:"
      echo "  cd apps/api"
      echo "  fly postgres create --name incentivedrive-db --region ewr"
      echo "  fly postgres attach incentivedrive-db"
      echo "  fly secrets set API_SECRET_KEY=\$(openssl rand -hex 32)"
      echo "  fly secrets set JWT_SECRET_KEY=\$(openssl rand -hex 32)"
      echo "  fly secrets set SENDGRID_API_KEY=your-key-here"
      echo "  fly secrets set REDIS_URL=your-redis-url"
      echo ""
      echo "Then re-run: ./scripts/deploy.sh fly"
      exit 1
    }

    # Deploy
    fly deploy
    echo ""
    echo "=== API deployed! ==="
    fly status
    echo ""
    echo "API URL: https://$(fly info --json 2>/dev/null | python3 -c 'import sys,json; print(json.load(sys.stdin)["Hostname"])' 2>/dev/null || echo 'incentivedrive-api.fly.dev')"
    ;;

  compose)
    echo "=== Deploying with Docker Compose ==="
    cd "$ROOT_DIR"

    if [ ! -f .env.production ]; then
      echo "Error: .env.production not found."
      echo "Copy .env.production.example to .env.production and fill in values."
      exit 1
    fi

    # Build and start
    docker compose -f docker-compose.prod.yml --env-file .env.production up -d --build

    echo ""
    echo "Waiting for services to be healthy..."
    sleep 10

    # Run migrations
    echo "Running database migrations..."
    docker compose -f docker-compose.prod.yml exec api python -m scripts.migrate_leads

    # Seed data
    echo "Seeding incentive programs..."
    docker compose -f docker-compose.prod.yml exec api python -m scripts.seed_incentives

    echo "Seeding dealers..."
    docker compose -f docker-compose.prod.yml exec api python -m scripts.seed_dealers

    echo ""
    echo "=== Deployment complete! ==="
    echo "API: http://localhost:${API_PORT:-8000}"
    echo "Web: http://localhost:${WEB_PORT:-3000}"
    docker compose -f docker-compose.prod.yml ps
    ;;

  *)
    echo "IncentiveDrive Deploy Script"
    echo ""
    echo "Usage: ./scripts/deploy.sh [fly|compose]"
    echo ""
    echo "  fly      Deploy API to Fly.io (recommended for production)"
    echo "  compose  Deploy full stack locally with docker-compose"
    echo ""
    echo "Prerequisites:"
    echo "  fly:     Install flyctl, create account at fly.io"
    echo "  compose: Docker Desktop running, .env.production configured"
    ;;
esac
