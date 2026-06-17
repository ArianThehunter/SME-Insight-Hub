"""
Auth domain — FastAPI dependencies for authentication and authorization.
"""

import uuid
from typing import List, Optional

import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.service import AuthService
from src.common.enums import UserRole
from src.common.exceptions import AuthenticationError, AuthorizationError
from src.common.security import decode_token, verify_token_type
from src.database import get_db


async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extract and validate JWT from Authorization header.
    Returns the authenticated User with role and org loaded.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise AuthenticationError("Missing or invalid authorization header")

    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_token(token)
        if not verify_token_type(payload, "access"):
            raise AuthenticationError("Invalid token type")
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")

    user_id = uuid.UUID(payload["sub"])
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(user_id)

    if not user:
        raise AuthenticationError("User not found")
    if not user.is_active:
        raise AuthenticationError("Account has been deactivated")

    return user


def require_role(*roles: UserRole):
    """
    Dependency factory that checks if the current user has one of the specified roles.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_role(UserRole.SUPER_ADMIN))])
    """

    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        role_names = [r.value for r in roles]
        if current_user.role.name not in role_names:
            raise AuthorizationError(
                f"Requires one of these roles: {', '.join(role_names)}"
            )
        return current_user

    return role_checker


def require_permission(resource: str, action: str):
    """
    Dependency factory that checks if the current user has a specific permission.

    Usage:
        @router.delete("/items/{id}", dependencies=[Depends(require_permission("items", "delete"))])
    """

    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.has_permission(resource, action):
            raise AuthorizationError(
                f"Missing permission: {resource}:{action}"
            )
        return current_user

    return permission_checker


def get_org_id(current_user: User = Depends(get_current_user)) -> uuid.UUID:
    """Extract the organization ID from the current user for tenant-scoped queries."""
    return current_user.org_id
