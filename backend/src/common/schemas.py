"""
Shared Pydantic schemas for pagination, responses, and common patterns.
"""

import uuid
from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

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
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")
    search: Optional[str] = Field(default=None, description="Search query")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper."""

    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(
        cls, items: List[T], total: int, page: int, page_size: int
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
class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response wrapper."""

    success: bool = True
    message: str = "Success"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    message: str
    detail: dict = {}
    path: Optional[str] = None


# ── Filter Schema ────────────────────────────────────────────────
class DateRangeFilter(BaseModel):
    """Date range filter parameters."""

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AmountRangeFilter(BaseModel):
    """Amount range filter parameters."""

    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
