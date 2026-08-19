"""
Finance domain — Schemas for expenses, invoices, and cash flow.
"""

import uuid
from datetime import date
from decimal import Decimal

from src.common.enums import InvoiceStatus
from src.common.schemas import BaseSchema, IDSchema

# ── Expense Schemas ────────────────────────────────────────────────

class ExpenseCreate(BaseSchema):
    category: str
    subcategory: str | None = None
    description: str
    description_bn: str | None = None
    amount: Decimal
    expense_date: date
    vendor: str | None = None
    vendor_bn: str | None = None
    payment_method: str | None = None
    department: str | None = None
    is_recurring: bool = False


class ExpenseUpdate(BaseSchema):
    category: str | None = None
    description: str | None = None
    amount: Decimal | None = None
    expense_date: date | None = None
    vendor: str | None = None
    payment_method: str | None = None


class ExpenseResponse(IDSchema):
    category: str
    subcategory: str | None = None
    description: str
    description_bn: str | None = None
    amount: Decimal
    currency: str
    expense_date: date
    vendor: str | None = None
    payment_method: str | None = None
    department: str | None = None
    is_recurring: bool


# ── Invoice Schemas ────────────────────────────────────────────────

class InvoiceCreate(BaseSchema):
    customer_id: uuid.UUID | None = None
    issue_date: date
    due_date: date
    subtotal: Decimal
    tax_amount: Decimal = Decimal(0)
    discount_amount: Decimal = Decimal(0)
    vendor_name: str | None = None
    notes: str | None = None


class InvoiceUpdate(BaseSchema):
    status: InvoiceStatus | None = None
    amount_paid: Decimal | None = None
    paid_date: date | None = None
    notes: str | None = None


class InvoiceResponse(IDSchema):
    invoice_number: str
    customer_id: uuid.UUID | None = None
    status: str
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    currency: str
    issue_date: date
    due_date: date
    paid_date: date | None = None
    vendor_name: str | None = None


# ── Summary Schemas ────────────────────────────────────────────────

class FinanceSummaryResponse(BaseSchema):
    total_revenue: Decimal
    total_expenses: Decimal
    net_profit: Decimal
    outstanding_invoices: Decimal
    overdue_invoices: Decimal
    expense_by_category: dict
