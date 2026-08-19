"""
Auth domain — Pydantic schemas for authentication requests and responses.
"""

import uuid
from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from src.common.schemas import BaseSchema, IDSchema


# ── Auth Requests ─────────────────────────────────────────────────
class LoginRequest(BaseSchema):
    """Login credentials."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisterRequest(BaseSchema):
    """Registration data including org creation."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    full_name_bn: str | None = None
    organization_name: str = Field(min_length=2, max_length=255)
    organization_name_bn: str | None = None
    phone: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class RefreshTokenRequest(BaseSchema):
    """Request to refresh access token."""
    refresh_token: str


class ChangePasswordRequest(BaseSchema):
    """Change password request."""
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


# ── Auth Responses ────────────────────────────────────────────────
class TokenResponse(BaseSchema):
    """JWT token pair response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(IDSchema):
    """User profile response."""
    email: str
    full_name: str
    full_name_bn: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    is_active: bool
    is_verified: bool
    last_login: datetime | None = None
    role: "RoleResponse"
    organization: "OrganizationBriefResponse"


class UserBriefResponse(BaseSchema):
    """Brief user info for lists and references."""
    id: uuid.UUID
    email: str
    full_name: str
    avatar_url: str | None = None
    role_name: str | None = None


# ── Role Schemas ──────────────────────────────────────────────────
class PermissionResponse(IDSchema):
    """Permission details."""
    resource: str
    action: str
    description: str | None = None


class RoleResponse(IDSchema):
    """Role with permissions."""
    name: str
    display_name: str
    display_name_bn: str | None = None
    description: str | None = None
    is_system: bool
    permissions: list[PermissionResponse] = []


class RoleCreateRequest(BaseSchema):
    """Create a custom role."""
    name: str = Field(min_length=2, max_length=100)
    display_name: str = Field(min_length=2, max_length=100)
    display_name_bn: str | None = None
    description: str | None = None
    permission_ids: list[uuid.UUID] = []


# ── Organization Schemas ──────────────────────────────────────────
class OrganizationBriefResponse(BaseSchema):
    """Brief org info included in user responses."""
    id: uuid.UUID
    name: str
    name_bn: str | None = None
    slug: str
    logo_url: str | None = None
    currency: str = "BDT"


class OrganizationResponse(IDSchema):
    """Full organization details."""
    name: str
    name_bn: str | None = None
    slug: str
    description: str | None = None
    logo_url: str | None = None
    website: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    address_bn: str | None = None
    locale: str
    currency: str
    timezone: str
    fiscal_year_start: int
    settings: dict | None = None
    branding: dict | None = None
    is_active: bool


class OrganizationUpdateRequest(BaseSchema):
    """Update organization settings."""
    name: str | None = None
    name_bn: str | None = None
    description: str | None = None
    logo_url: str | None = None
    website: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    address_bn: str | None = None
    locale: str | None = None
    currency: str | None = None
    timezone: str | None = None
    fiscal_year_start: int | None = Field(default=None, ge=1, le=12)
    settings: dict | None = None
    branding: dict | None = None


# ── Auth Info ─────────────────────────────────────────────────────
class AuthInfoResponse(BaseSchema):
    """Current authenticated user info."""
    user: UserResponse
    permissions: list[str]
