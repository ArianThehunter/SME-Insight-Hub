"""
Pytest fixtures and configuration for backend testing.
"""

import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Set test environment variables
os.environ["ENVIRONMENT"] = "testing"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-key-minimum-32-chars-length"
os.environ["DATABASE_URL"] = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
)

from src.database import Base, get_db
from src.main import create_app

app = create_app()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing API endpoints."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac
