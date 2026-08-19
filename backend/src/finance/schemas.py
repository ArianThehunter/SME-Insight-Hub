"""
Finance domain — Pydantic schemas for expenses, invoices, and cash flow / financial metrics.
"""

import uuid
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional

from src.common.schemas import BaseSchema, IDSchema


# ── Expense Schemas ───────────────────────────────────────────────

class ExpenseCreate(BaseSchema):
    category: str
    subcategory: Optional[str] = None
    description: str
    description_bn: Optional[str] = None
    amount: Decimal
    expense_date: date
    vendor: Optional[str] = None
    vendor_bn: Optional[str] = None
    payment_method: Optional[str] = None
    department: Optional[str] = None
    is_recurring: bool = False


class ExpenseUpdate(BaseSchema):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    description_bn: Optional[str] = None
    amount: Optional[Decimal] = None
    expense_date: Optional[date] = None
    vendor: Optional[str] = None
    vendor_bn: Optional[str] = None
    payment_method: Optional[str] = None
    department: Optional[str] = None
    is_recurring: Optional[bool] = None


class ExpenseResponse(IDSchema):
    category: str
    subcategory: Optional[str] = None
    description: str
    description_bn: Optional[str] = None
    amount: Decimal
    currency: str
    expense_date: date
    vendor: Optional[str] = None
    vendor_bn: Optional[str] = None
    payment_method: Optional[str] = None
    department: Optional[str] = None
    is_recurring: bool


# ── Invoice Schemas ───────────────────────────────────────────────

class InvoiceCreate(BaseSchema):
    invoice_number: Optional[str] = None
    customer_id: Optional[uuid.UUID] = None
    issue_date: date
    due_date: date
    subtotal: Decimal
    tax_amount: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    vendor_name: Optional[str] = None
    notes: Optional[str] = None
    status: str = "draft"


class InvoiceUpdate(BaseSchema):
    status: Optional[str] = None
    subtotal: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    amount_paid: Optional[Decimal] = None
    paid_date: Optional[date] = None
    notes: Optional[str] = None


class InvoiceResponse(IDSchema):
    invoice_number: str
    customer_id: Optional[uuid.UUID] = None
    status: str
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    currency: str
    issue_date: date
    due_date: date
    paid_date: Optional[date] = None
    vendor_name: Optional[str] = None
    notes: Optional[str] = None


# ── Financial Analytics & Summary Schemas ─────────────────────────

class FinanceOverview(BaseSchema):
    total_revenue: Decimal
    total_expenses: Decimal
    net_profit: Decimal
    profit_margin_pct: Decimal
    cash_inflow: Decimal
    cash_outflow: Decimal
    net_cash_flow: Decimal
    outstanding_invoices_amount: Decimal
    outstanding_invoices_count: int
    overdue_invoices_amount: Decimal
    overdue_invoices_count: int
    expense_by_category: Dict[str, Decimal]
