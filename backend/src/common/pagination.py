"""
Pagination utilities for database queries.
"""

from typing import Any, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.schemas import PaginatedResponse, PaginationParams

T = TypeVar("T")


async def paginate(
    session: AsyncSession,
    query: Select,
    params: PaginationParams,
    response_model: Optional[Type] = None,
) -> PaginatedResponse:
    """
    Apply pagination to a SQLAlchemy query and return a PaginatedResponse.

    Args:
        session: Database session
        query: Base SQLAlchemy select query
        params: Pagination parameters (page, page_size, sort)
        response_model: Optional Pydantic model to convert results
    """
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    # Apply sorting
    if params.sort_by:
        from sqlalchemy import asc, desc

        sort_func = desc if params.sort_order == "desc" else asc
        # We trust sort_by is validated at the schema level
        query = query.order_by(sort_func(params.sort_by))

    # Apply pagination
    query = query.offset(params.offset).limit(params.page_size)

    # Execute
    result = await session.execute(query)
    items = list(result.scalars().all())

    # Convert to response models if provided
    if response_model:
        items = [response_model.model_validate(item) for item in items]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=params.page,
        page_size=params.page_size,
    )
