"""
PRAMAN AI - Legal Metrology Compliance Inspection Platform
FastAPI Application Entrypoint
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import engine, Base
from .seed import seed_database
from .routes.auth_routes import router as auth_router
from .routes.scan_routes import router as scan_router
from .routes.inspection_routes import router as inspection_router
from .routes.product_routes import product_router, rule_router
from .routes.analytics_routes import router as analytics_router
from .routes.report_routes import report_router, audit_router

# Create database tables and seed initial users and sample data
Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(
    title="PRAMAN AI - Packaging Regulations & Automated Metrology Audit Network",
    description="Statutory Legal Metrology Compliance & Inspection API for packaged commodities in India.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded and sample images
uploads_dir = os.path.abspath("backend/uploads")
samples_dir = os.path.abspath("backend/samples")
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(samples_dir, exist_ok=True)

app.mount("/api/static/uploads", StaticFiles(directory=uploads_dir), name="uploads")
app.mount("/api/static/samples", StaticFiles(directory=samples_dir), name="samples")

# Register routes
app.include_router(auth_router)
app.include_router(scan_router)
app.include_router(inspection_router)
app.include_router(product_router)
app.include_router(rule_router)
app.include_router(analytics_router)
app.include_router(report_router)
app.include_router(audit_router)

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "PRAMAN AI Legal Metrology Engine",
        "version": "1.0.0",
        "dataset_rules_count": 12,
        "mode": "Enforcement Production Ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
