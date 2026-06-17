"""
Auth domain — Business logic for authentication and user management.
"""

import hashlib
import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.models import AuditLog, Organization, RefreshToken, Role, User
from src.auth.schemas import (
    LoginRequest,
    OrganizationBriefResponse,
    RegisterRequest,
    RoleResponse,
    TokenResponse,
    UserResponse,
)
from src.common.enums import UserRole
from src.common.exceptions import (
    AlreadyExistsError,
    AuthenticationError,
    NotFoundError,
)
from src.common.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    verify_token_type,
)
from src.config import get_settings

settings = get_settings()


class AuthService:
    """Handles authentication, registration, and token management."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: RegisterRequest) -> TokenResponse:
        """Register a new user and create their organization."""
        # Check if email exists
        existing = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        if existing.scalar_one_or_none():
            raise AlreadyExistsError("User", "email")

        # Get or create org_owner role
        role = await self._get_or_create_role(UserRole.ORG_OWNER)

        # Create organization
        slug = self._generate_slug(data.organization_name)
        org = Organization(
            name=data.organization_name,
            name_bn=data.organization_name_bn,
            slug=slug,
            currency="BDT",
            locale="en",
        )
        self.db.add(org)
        await self.db.flush()

        # Create user
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            full_name_bn=data.full_name_bn,
            phone=data.phone,
            org_id=org.id,
            role_id=role.id,
            is_active=True,
            is_verified=True,  # Auto-verify for demo
        )
        self.db.add(user)
        await self.db.flush()

        # Generate tokens
        tokens = await self._create_token_pair(user)

        # Audit log
        await self._log_action(org.id, user.id, "register", "user", str(user.id))

        return tokens

    async def login(self, data: LoginRequest) -> TokenResponse:
        """Authenticate user and return token pair."""
        # Find user with role loaded
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role), selectinload(User.organization))
            .where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            raise AuthenticationError("Account has been deactivated")

        # Update last login
        user.last_login = datetime.now(timezone.utc)

        # Generate tokens
        tokens = await self._create_token_pair(user)

        # Audit log
        await self._log_action(user.org_id, user.id, "login", "user", str(user.id))

        return tokens

    async def refresh(self, refresh_token_str: str) -> TokenResponse:
        """Refresh access token using a valid refresh token."""
        try:
            payload = decode_token(refresh_token_str)
            if not verify_token_type(payload, "refresh"):
                raise AuthenticationError("Invalid token type")
        except Exception:
            raise AuthenticationError("Invalid or expired refresh token")

        user_id = uuid.UUID(payload["sub"])
        token_hash = self._hash_token(refresh_token_str)

        # Verify token exists and is not revoked
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.is_revoked == False,
            )
        )
        stored_token = result.scalar_one_or_none()
        if not stored_token:
            raise AuthenticationError("Token has been revoked")

        # Revoke old token
        stored_token.is_revoked = True

        # Get user
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role), selectinload(User.organization))
            .where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")

        # Generate new token pair
        return await self._create_token_pair(user)

    async def logout(self, user_id: uuid.UUID) -> None:
        """Revoke all refresh tokens for a user."""
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False,
            )
        )
        tokens = result.scalars().all()
        for token in tokens:
            token.is_revoked = True

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID with role and org loaded."""
        result = await self.db.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(Role.permissions),
                selectinload(User.organization),
            )
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    # ── Private Helpers ────────────────────────────────────────────
    async def _create_token_pair(self, user: User) -> TokenResponse:
        """Create access + refresh token pair."""
        access_token = create_access_token(
            user_id=user.id,
            org_id=user.org_id,
            role=user.role.name if user.role else "viewer",
        )
        refresh_token = create_refresh_token(user_id=user.id)

        # Store refresh token hash
        token_record = RefreshToken(
            token_hash=self._hash_token(refresh_token),
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        )
        self.db.add(token_record)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def _get_or_create_role(self, role_enum: UserRole) -> Role:
        """Get a role by name, creating it if it doesn't exist."""
        result = await self.db.execute(
            select(Role).where(Role.name == role_enum.value)
        )
        role = result.scalar_one_or_none()
        if not role:
            role = Role(
                name=role_enum.value,
                display_name=role_enum.value.replace("_", " ").title(),
                is_system=True,
            )
            self.db.add(role)
            await self.db.flush()
        return role

    async def _log_action(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        action: str,
        resource: str,
        resource_id: str,
    ) -> None:
        """Create an audit log entry."""
        log = AuditLog(
            org_id=org_id,
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
        )
        self.db.add(log)

    @staticmethod
    def _hash_token(token: str) -> str:
        """Hash a token for secure storage."""
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def _generate_slug(name: str) -> str:
        """Generate a URL-safe slug from a name."""
        slug = re.sub(r"[^\w\s-]", "", name.lower())
        slug = re.sub(r"[-\s]+", "-", slug).strip("-")
        return f"{slug}-{uuid.uuid4().hex[:8]}"
