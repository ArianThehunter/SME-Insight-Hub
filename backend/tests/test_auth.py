"""
Unit tests for authentication security utilities and JWT helpers.
"""

import uuid
from src.common.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type,
)
from src.auth.models import User, Role, Permission


def test_password_hashing():
    """Verify bcrypt password hashing and verification."""
    password = "SuperSecretPassword123!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_lifecycle():
    """Verify JWT access and refresh token creation, decoding, and type verification."""
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()

    # Access token
    token = create_access_token(
        user_id=user_id,
        org_id=org_id,
        role="org_owner",
    )
    assert isinstance(token, str)

    payload = decode_token(token)
    assert payload["sub"] == str(user_id)
    assert payload["org_id"] == str(org_id)
    assert payload["role"] == "org_owner"
    assert verify_token_type(payload, "access") is True
    assert verify_token_type(payload, "refresh") is False

    # Refresh token
    refresh_token = create_refresh_token(user_id=user_id)
    refresh_payload = decode_token(refresh_token)
    assert refresh_payload["sub"] == str(user_id)
    assert verify_token_type(refresh_payload, "refresh") is True


def test_rbac_permission_matching():
    """Verify fine-grained permission matching on User model."""
    role_id = uuid.uuid4()
    user = User(
        id=uuid.uuid4(),
        org_id=uuid.uuid4(),
        role_id=role_id,
        email="owner@sme.com.bd",
        full_name="Test Owner",
        password_hash="hash",
    )
    
    # Org owner has full privileges
    role_owner = Role(name="org_owner", description="Owner")
    user.role = role_owner
    assert user.has_permission("customers", "create") is True
    assert user.has_permission("invoices", "delete") is True

    # Staff role with specific permissions
    role_staff = Role(name="sales_rep", description="Sales Representative")
    perm1 = Permission(resource="customers", action="read")
    perm2 = Permission(resource="orders", action="create")
    role_staff.permissions = [perm1, perm2]
    user.role = role_staff

    assert user.has_permission("customers", "read") is True
    assert user.has_permission("orders", "create") is True
    assert user.has_permission("invoices", "delete") is False
