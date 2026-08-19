"""
Sales domain — Pydantic schemas for API request/response validation.
"""

import uuid
from datetime import date
from decimal import Decimal

from src.common.enums import CustomerSegment
from src.common.schemas import BaseSchema, IDSchema

# ── Customer Schemas ──────────────────────────────────────────────

class CustomerCreate(BaseSchema):
    """Request schema for creating a customer."""
    name: str
    name_bn: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    company_bn: str | None = None
    address: str | None = None
    city: str | None = None
    district: str | None = None
    segment: CustomerSegment | None = None
    notes: str | None = None


class CustomerUpdate(BaseSchema):
    """Request schema for updating a customer (all fields optional)."""
    name: str | None = None
    name_bn: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    city: str | None = None
    district: str | None = None
    segment: CustomerSegment | None = None
    notes: str | None = None
    is_active: bool | None = None


class CustomerResponse(IDSchema):
    """Response schema for a customer."""
    name: str
    name_bn: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    company_bn: str | None = None
    city: str | None = None
    district: str | None = None
    segment: str | None = None
    lifetime_value: Decimal
    total_orders: int
    first_purchase: date | None = None
    last_purchase: date | None = None
    is_active: bool


# ── Product Schemas ───────────────────────────────────────────────

class ProductCreate(BaseSchema):
    """Request schema for creating a product."""
    name: str
    name_bn: str | None = None
    sku: str
    description: str | None = None
    category: str | None = None
    subcategory: str | None = None
    unit: str = "pcs"
    price: Decimal
    cost: Decimal
    tax_rate: Decimal = Decimal(0)
    stock_quantity: int = 0
    reorder_level: int = 10
    supplier_id: uuid.UUID | None = None


class ProductUpdate(BaseSchema):
    """Request schema for updating a product."""
    name: str | None = None
    name_bn: str | None = None
    description: str | None = None
    category: str | None = None
    price: Decimal | None = None
    cost: Decimal | None = None
    stock_quantity: int | None = None
    reorder_level: int | None = None
    is_active: bool | None = None


class ProductResponse(IDSchema):
    """Response schema for a product."""
    name: str
    name_bn: str | None = None
    sku: str
    category: str | None = None
    unit: str
    price: Decimal
    cost: Decimal
    tax_rate: Decimal
    stock_quantity: int
    reorder_level: int
    is_active: bool


# ── Order Schemas ─────────────────────────────────────────────────

class OrderItemCreate(BaseSchema):
    """Line item for order creation."""
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal
    discount: Decimal = Decimal(0)


class OrderCreate(BaseSchema):
    """Request schema for creating an order."""
    customer_id: uuid.UUID
    order_date: date
    delivery_date: date | None = None
    shipping_address: str | None = None
    notes: str | None = None
    payment_method: str | None = None
    items: list[OrderItemCreate]


class OrderItemResponse(BaseSchema):
    """Response schema for an order line item."""
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal
    discount: Decimal
    tax: Decimal
    total_price: Decimal


class OrderResponse(IDSchema):
    """Response schema for an order."""
    order_number: str
    status: str
    customer_id: uuid.UUID
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    currency: str
    order_date: date
    delivery_date: date | None = None
    payment_status: str
    items: list[OrderItemResponse] = []


# ── Supplier Schemas ──────────────────────────────────────────────

class SupplierCreate(BaseSchema):
    name: str
    name_bn: str | None = None
    contact_person: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None


class SupplierResponse(IDSchema):
    name: str
    name_bn: str | None = None
    contact_person: str | None = None
    email: str | None = None
    phone: str | None = None
    city: str | None = None
    rating: Decimal
    total_orders: int
    is_active: bool


# ── Warehouse Schemas ─────────────────────────────────────────────

class WarehouseCreate(BaseSchema):
    name: str
    name_bn: str | None = None
    location: str | None = None
    address: str | None = None
    capacity: int = 10000


class WarehouseResponse(IDSchema):
    name: str
    name_bn: str | None = None
    location: str | None = None
    capacity: int
    current_stock: int
    is_active: bool
