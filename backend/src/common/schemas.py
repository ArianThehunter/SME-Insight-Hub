"""
Shared Pydantic schemas for pagination, responses, and common patterns.
"""

import uuid
from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ── Base Schemas ──────────────────────────────────────────────────
class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""

    created_at: datetime
    updated_at: datetime


class IDSchema(TimestampSchema):
    """Schema with UUID id and timestamps."""

    id: uuid.UUID


# ── Pagination ────────────────────────────────────────────────────
class PaginationParams(BaseModel):
    """Query parameters for pagination."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")
    sort_by: str | None = Field(default=None, description="Field to sort by")
    sort_order: str | None = Field(default="desc", pattern="^(asc|desc)$")
    search: str | None = Field(default=None, description="Search query")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse[T](BaseModel):
    """Standard paginated response wrapper."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(
        cls, items: list[T], total: int, page: int, page_size: int
    ) -> "PaginatedResponse[T]":
        total_pages = max(1, (total + page_size - 1) // page_size)
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


# ── API Response Wrappers ────────────────────────────────────────
class SuccessResponse[T](BaseModel):
    """Standard success response wrapper."""

    success: bool = True
    message: str = "Success"
    data: T | None = None


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    message: str
    detail: dict = {}
    path: str | None = None


# ── Filter Schema ────────────────────────────────────────────────
class DateRangeFilter(BaseModel):
    """Date range filter parameters."""

    start_date: datetime | None = None
    end_date: datetime | None = None


class AmountRangeFilter(BaseModel):
    """Amount range filter parameters."""

    min_amount: float | None = None
    max_amount: float | None = None
