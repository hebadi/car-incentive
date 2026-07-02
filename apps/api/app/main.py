from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import incentives, leads, dealers, health, admin, billing, dealer_portal, vehicles

app = FastAPI(
    title="IncentiveDrive API",
    description="Automotive incentive-based lead generation platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(incentives.router, prefix="/api/v1/incentives", tags=["incentives"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["leads"])
app.include_router(dealers.router, prefix="/api/v1/dealers", tags=["dealers"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["billing"])
app.include_router(dealer_portal.router, prefix="/api/v1/portal", tags=["dealer-portal"])
app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["vehicles"])

# Convenience alias for the spec endpoint path
app.include_router(incentives.router, prefix="/api/v1/calculate-incentives", tags=["incentives"], include_in_schema=False)
