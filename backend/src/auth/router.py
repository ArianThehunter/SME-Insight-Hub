"""
Auth domain — API endpoints for authentication.
"""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.auth.schemas import (
    AuthInfoResponse,
    LoginRequest,
    OrganizationBriefResponse,
    RefreshTokenRequest,
    RegisterRequest,
    RoleResponse,
    TokenResponse,
    UserResponse,
)
from src.auth.service import AuthService
from src.common.schemas import SuccessResponse
from src.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user and organization",
)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Create a new user account and organization."""
    service = AuthService(db)
    tokens = await service.register(data)
    return SuccessResponse(
        message="Registration successful",
        data=tokens,
    )


@router.post(
    "/login",
    response_model=SuccessResponse[TokenResponse],
    summary="Authenticate and get tokens",
)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate with email and password."""
    service = AuthService(db)
    tokens = await service.login(data)
    return SuccessResponse(
        message="Login successful",
        data=tokens,
    )


@router.post(
    "/refresh",
    response_model=SuccessResponse[TokenResponse],
    summary="Refresh access token",
)
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Get a new access token using a refresh token."""
    service = AuthService(db)
    tokens = await service.refresh(data.refresh_token)
    return SuccessResponse(
        message="Token refreshed",
        data=tokens,
    )


@router.post(
    "/logout",
    response_model=SuccessResponse,
    summary="Logout and revoke tokens",
)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Revoke all refresh tokens for the current user."""
    service = AuthService(db)
    await service.logout(current_user.id)
    return SuccessResponse(message="Logged out successfully")


@router.get(
    "/me",
    response_model=SuccessResponse[UserResponse],
    summary="Get current user profile",
)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    user_response = UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        full_name_bn=current_user.full_name_bn,
        phone=current_user.phone,
        avatar_url=current_user.avatar_url,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        last_login=current_user.last_login,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        role=RoleResponse.model_validate(current_user.role),
        organization=OrganizationBriefResponse(
            id=current_user.organization.id,
            name=current_user.organization.name,
            name_bn=current_user.organization.name_bn,
            slug=current_user.organization.slug,
            logo_url=current_user.organization.logo_url,
            currency=current_user.organization.currency,
        ),
    )
    return SuccessResponse(data=user_response)


@router.get(
    "/health",
    summary="Auth service health check",
)
async def health():
    """Simple health check for the auth service."""
    return {"status": "healthy", "service": "auth"}
