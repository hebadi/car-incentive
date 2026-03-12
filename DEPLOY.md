# IncentiveDrive — Production Deployment

## Recommended Stack

| Component | Service | Cost |
|-----------|---------|------|
| Web (Next.js) | Vercel | Free tier |
| API (FastAPI) | Fly.io | ~$5/mo |
| PostgreSQL | Fly Postgres | ~$7/mo |
| Redis | Upstash | Free tier |
| Email (ADF) | SendGrid | Free tier (100/day) |
| **Total** | | **~$12/mo** |

---

## Step 1: Deploy API to Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Create app + Postgres
cd apps/api
fly launch --name incentivedrive-api --region ewr --no-deploy
fly postgres create --name incentivedrive-db --region ewr --initial-cluster-size 1 --vm-size shared-cpu-1x
fly postgres attach incentivedrive-db

# Create Upstash Redis (free) at https://console.upstash.com
# Copy the redis:// URL

# Set secrets
fly secrets set \
  API_SECRET_KEY=$(openssl rand -hex 32) \
  JWT_SECRET_KEY=$(openssl rand -hex 32) \
  SENDGRID_API_KEY=SG.your-key-here \
  REDIS_URL=redis://default:xxx@your-upstash-url:6379

# Deploy
fly deploy

# Run migrations + seed data
fly ssh console -C "python -m scripts.migrate_leads"
fly ssh console -C "python -m scripts.seed_incentives"
fly ssh console -C "python -m scripts.seed_dealers"
```

API will be live at: `https://incentivedrive-api.fly.dev`

## Step 2: Deploy Web to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from repo root
cd /path/to/car-incentive
vercel --prod

# When prompted:
#   - Root directory: apps/web
#   - Framework: Next.js
#   - Build command: (default)
#   - Output directory: (default)

# Set environment variable in Vercel dashboard:
#   NEXT_PUBLIC_API_BASE_URL = https://incentivedrive-api.fly.dev/api/v1
```

Web will be live at: `https://incentivedrive.vercel.app`

## Step 3: Get a SendGrid API Key

1. Create account at https://sendgrid.com (free: 100 emails/day)
2. Settings → API Keys → Create API Key (Full Access)
3. Verify a sender: Settings → Sender Authentication → Single Sender
   - Use `leads@yourdomain.com` or verify your domain
4. Set in Fly.io: `fly secrets set SENDGRID_API_KEY=SG.xxxxx`

## Step 4: Custom Domain (Optional)

```bash
# Fly.io (API)
fly certs add api.incentivedrive.com
# → Add the CNAME record shown to your DNS

# Vercel (Web)
vercel domains add incentivedrive.com
# → Add the A/CNAME records shown to your DNS

# Update API URL
vercel env add NEXT_PUBLIC_API_BASE_URL
# → Enter: https://api.incentivedrive.com/api/v1
```

---

## Alternative: Docker Compose (Single Server)

For a VPS deployment (DigitalOcean, Hetzner, etc.):

```bash
# Copy and configure env
cp .env.production.example .env.production
# Edit .env.production with your values

# Deploy
./scripts/deploy.sh compose
```

## CI/CD

Push to `main` auto-deploys the API via `.github/workflows/deploy.yml`.
Set `FLY_API_TOKEN` in GitHub repo secrets:

```bash
fly tokens create deploy -x 999999h
# → Copy token to GitHub: Settings → Secrets → FLY_API_TOKEN
```

Vercel auto-deploys on push if connected to the GitHub repo.
