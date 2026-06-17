"""
Sales domain — SQLAlchemy models for orders, customers, and products.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, Numeric,
    String, Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import TenantModel


class Customer(TenantModel):
    """Customer entity for sales and CRM."""

    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name_bn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company_bn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address_bn: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    segment: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    lifetime_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    total_orders: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    first_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    last_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)

    # Relationships
    orders: Mapped[List["Order"]] = relationship(back_populates="customer", cascade="all, delete-orphan")
    invoices: Mapped[List["Invoice"]] = relationship(back_populates="customer")


class Product(TenantModel):
    """Product catalog item."""

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name_bn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_bn: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    unit: Mapped[str] = mapped_column(String(50), default="pcs", nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reorder_level: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    max_stock: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Foreign keys
    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    supplier: Mapped[Optional["Supplier"]] = relationship(back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
    stock_movements: Mapped[List["StockMovement"]] = relationship(back_populates="product")


class Order(TenantModel):
    """Sales order."""

    __tablename__ = "orders"

    order_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    subtotal: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="BDT", nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    delivery_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class OrderItem(TenantModel):
    """Line item in a sales order."""

    __tablename__ = "order_items"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    discount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    tax: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")


# ── Inventory Models ──────────────────────────────────────────────
class Supplier(TenantModel):
    """Product supplier/vendor."""

    __tablename__ = "suppliers"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name_bn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_person: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address_bn: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=0, nullable=False)
    total_orders: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    on_time_delivery_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=100, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    products: Mapped[List["Product"]] = relationship(back_populates="supplier")


class Warehouse(TenantModel):
    """Inventory warehouse/location."""

    __tablename__ = "warehouses"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_bn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=10000, nullable=False)
    current_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    stock_movements: Mapped[List["StockMovement"]] = relationship(back_populates="warehouse")


class StockMovement(TenantModel):
    """Inventory stock movement record."""

    __tablename__ = "stock_movements"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False
    )
    movement_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    movement_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    product: Mapped["Product"] = relationship(back_populates="stock_movements")
    warehouse: Mapped["Warehouse"] = relationship(back_populates="stock_movements")


# ── Finance Models ────────────────────────────────────────────────
class Invoice(TenantModel):
    """Financial invoice."""

    __tablename__ = "invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="BDT", nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    paid_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    vendor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    customer: Mapped[Optional["Customer"]] = relationship(back_populates="invoices")


class Expense(TenantModel):
    """Business expense record."""

    __tablename__ = "expenses"

    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    description_bn: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="BDT", nullable=False)
    expense_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    vendor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    vendor_bn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    receipt_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)


# ── Document Models ───────────────────────────────────────────────
class Document(TenantModel):
    """Uploaded document for OCR processing."""

    __tablename__ = "documents"

    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), default="other", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="uploaded", nullable=False, index=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 4), nullable=True)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)

    # Relationships
    extraction_results: Mapped[List["ExtractionResult"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class ExtractionResult(TenantModel):
    """Extracted field from a document."""

    __tablename__ = "extraction_results"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    field_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    field_type: Mapped[str] = mapped_column(String(50), default="text", nullable=False)
    confidence: Mapped[float] = mapped_column(Numeric(5, 4), default=0.0, nullable=False)
    is_validated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validated_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bounding_box: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    document: Mapped["Document"] = relationship(back_populates="extraction_results")
