"""
Sales domain — Pydantic schemas for API request/response validation.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from src.common.enums import CustomerSegment, OrderStatus
from src.common.schemas import BaseSchema, IDSchema


# ── Customer Schemas ──────────────────────────────────────────────

class CustomerCreate(BaseSchema):
    """Request schema for creating a customer."""
    name: str
    name_bn: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    company_bn: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    segment: Optional[CustomerSegment] = None
    notes: Optional[str] = None


class CustomerUpdate(BaseSchema):
    """Request schema for updating a customer (all fields optional)."""
    name: Optional[str] = None
    name_bn: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    segment: Optional[CustomerSegment] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class CustomerResponse(IDSchema):
    """Response schema for a customer."""
    name: str
    name_bn: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    company_bn: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    segment: Optional[str] = None
    lifetime_value: Decimal
    total_orders: int
    first_purchase: Optional[date] = None
    last_purchase: Optional[date] = None
    is_active: bool


# ── Product Schemas ───────────────────────────────────────────────

class ProductCreate(BaseSchema):
    """Request schema for creating a product."""
    name: str
    name_bn: Optional[str] = None
    sku: str
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    unit: str = "pcs"
    price: Decimal
    cost: Decimal
    tax_rate: Decimal = Decimal("0")
    stock_quantity: int = 0
    reorder_level: int = 10
    supplier_id: Optional[uuid.UUID] = None


class ProductUpdate(BaseSchema):
    """Request schema for updating a product."""
    name: Optional[str] = None
    name_bn: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    reorder_level: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(IDSchema):
    """Response schema for a product."""
    name: str
    name_bn: Optional[str] = None
    sku: str
    category: Optional[str] = None
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
    discount: Decimal = Decimal("0")


class OrderCreate(BaseSchema):
    """Request schema for creating an order."""
    customer_id: uuid.UUID
    order_date: date
    delivery_date: Optional[date] = None
    shipping_address: Optional[str] = None
    notes: Optional[str] = None
    payment_method: Optional[str] = None
    items: List[OrderItemCreate]


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
    delivery_date: Optional[date] = None
    payment_status: str
    items: List[OrderItemResponse] = []


# ── Supplier Schemas ──────────────────────────────────────────────

class SupplierCreate(BaseSchema):
    name: str
    name_bn: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None


class SupplierResponse(IDSchema):
    name: str
    name_bn: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    rating: Decimal
    total_orders: int
    is_active: bool


# ── Warehouse Schemas ─────────────────────────────────────────────

class WarehouseCreate(BaseSchema):
    name: str
    name_bn: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    capacity: int = 10000


class WarehouseResponse(IDSchema):
    name: str
    name_bn: Optional[str] = None
    location: Optional[str] = None
    capacity: int
    current_stock: int
    is_active: bool
