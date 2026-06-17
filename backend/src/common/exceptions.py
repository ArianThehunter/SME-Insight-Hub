"""
Custom exception hierarchy and FastAPI exception handlers.
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


# ── Base Exceptions ───────────────────────────────────────────────
class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str = "Resource", resource_id: Any = None):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class AlreadyExistsError(AppException):
    """Resource already exists."""

    def __init__(self, resource: str = "Resource", field: str = ""):
        message = f"{resource} already exists"
        if field:
            message = f"{resource} with this {field} already exists"
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )


class AuthenticationError(AppException):
    """Authentication failed."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(AppException):
    """Insufficient permissions."""

    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class ValidationError(AppException):
    """Validation failed."""

    def __init__(self, message: str = "Validation error", errors: Optional[Dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors or {},
        )


class RateLimitError(AppException):
    """Rate limit exceeded."""

    def __init__(self):
        super().__init__(
            message="Rate limit exceeded. Please try again later.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


class FileProcessingError(AppException):
    """File processing failed."""

    def __init__(self, message: str = "File processing failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class TenantAccessError(AppException):
    """Cross-tenant data access attempt."""

    def __init__(self):
        super().__init__(
            message="Access denied: cross-organization data access",
            status_code=status.HTTP_403_FORBIDDEN,
        )


# ── Exception Handlers ───────────────────────────────────────────
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions with consistent JSON response format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "detail": exc.detail,
            "path": str(request.url),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle standard HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "detail": {},
            "path": str(request.url),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions — don't leak internals."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An internal server error occurred",
            "detail": {},
            "path": str(request.url),
        },
    )
