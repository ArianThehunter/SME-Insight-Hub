"""
SME Insight Hub — FastAPI Application Entry Point.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.config import get_settings
from src.common.exceptions import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
)
from src.middleware.logging import RequestLoggingMiddleware

settings = get_settings()

# ── Logging Configuration ────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("sme_insight_hub")

# ── Rate Limiter ──────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT_DEFAULT])


# ── Lifespan ──────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📦 Environment: {settings.ENVIRONMENT}")
    yield
    logger.info(f"🛑 Shutting down {settings.APP_NAME}")


# ── Application Factory ──────────────────────────────────────────
def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-Powered Business Management & Intelligence Platform for SMEs. "
            "Combines business operations, analytics, document processing, "
            "reporting, and business intelligence into a unified platform."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        openapi_tags=[
            {"name": "Health", "description": "Health check endpoints"},
            {"name": "Authentication", "description": "User registration, login, and token management"},
            {"name": "Dashboard", "description": "Executive dashboard and KPI data"},
            {"name": "Analytics", "description": "Business analytics and data exploration"},
            {"name": "Sales", "description": "Sales orders, revenue, and customer management"},
            {"name": "Inventory", "description": "Products, warehouses, stock management"},
            {"name": "Finance", "description": "Expenses, invoices, cash flow"},
            {"name": "Documents", "description": "PDF upload, OCR processing, data extraction"},
            {"name": "Reports", "description": "Report generation and scheduling"},
            {"name": "CRM", "description": "Customer relationship management"},
            {"name": "BI", "description": "Business Intelligence and custom dashboards"},
            {"name": "AI", "description": "AI business assistant"},
            {"name": "Admin", "description": "User, role, and permission management"},
            {"name": "Settings", "description": "Organization and system settings"},
        ],
    )

    # ── Middleware ─────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Response-Time"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    # Rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ── Exception Handlers ────────────────────────────────────
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # ── Routers ───────────────────────────────────────────────
    from src.auth.router import router as auth_router
    from src.analytics.router import router as analytics_router

    app.include_router(auth_router, prefix=settings.API_PREFIX)
    app.include_router(analytics_router, prefix=settings.API_PREFIX)

    # ── Health Check ──────────────────────────────────────────
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Application health check endpoint."""
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.get("/", tags=["Health"])
    async def root():
        """API root — redirects to documentation."""
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": "/health",
        }

    return app


# Create the app instance
app = create_app()
