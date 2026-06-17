"""
Auth domain — Pydantic schemas for authentication requests and responses.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

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
    full_name_bn: Optional[str] = None
    organization_name: str = Field(min_length=2, max_length=255)
    organization_name_bn: Optional[str] = None
    phone: Optional[str] = None

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
    full_name_bn: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None
    role: "RoleResponse"
    organization: "OrganizationBriefResponse"


class UserBriefResponse(BaseSchema):
    """Brief user info for lists and references."""
    id: uuid.UUID
    email: str
    full_name: str
    avatar_url: Optional[str] = None
    role_name: Optional[str] = None


# ── Role Schemas ──────────────────────────────────────────────────
class PermissionResponse(IDSchema):
    """Permission details."""
    resource: str
    action: str
    description: Optional[str] = None


class RoleResponse(IDSchema):
    """Role with permissions."""
    name: str
    display_name: str
    display_name_bn: Optional[str] = None
    description: Optional[str] = None
    is_system: bool
    permissions: List[PermissionResponse] = []


class RoleCreateRequest(BaseSchema):
    """Create a custom role."""
    name: str = Field(min_length=2, max_length=100)
    display_name: str = Field(min_length=2, max_length=100)
    display_name_bn: Optional[str] = None
    description: Optional[str] = None
    permission_ids: List[uuid.UUID] = []


# ── Organization Schemas ──────────────────────────────────────────
class OrganizationBriefResponse(BaseSchema):
    """Brief org info included in user responses."""
    id: uuid.UUID
    name: str
    name_bn: Optional[str] = None
    slug: str
    logo_url: Optional[str] = None
    currency: str = "BDT"


class OrganizationResponse(IDSchema):
    """Full organization details."""
    name: str
    name_bn: Optional[str] = None
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    address_bn: Optional[str] = None
    locale: str
    currency: str
    timezone: str
    fiscal_year_start: int
    settings: Optional[Dict] = None
    branding: Optional[Dict] = None
    is_active: bool


class OrganizationUpdateRequest(BaseSchema):
    """Update organization settings."""
    name: Optional[str] = None
    name_bn: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    address_bn: Optional[str] = None
    locale: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    fiscal_year_start: Optional[int] = Field(default=None, ge=1, le=12)
    settings: Optional[Dict] = None
    branding: Optional[Dict] = None


# ── Auth Info ─────────────────────────────────────────────────────
class AuthInfoResponse(BaseSchema):
    """Current authenticated user info."""
    user: UserResponse
    permissions: List[str]
