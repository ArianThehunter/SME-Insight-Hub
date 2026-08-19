"""
Finance domain — API router for expenses, invoices, cashflow, and P&L financial metrics.
All data is org-scoped with multi-tenancy.
"""

import uuid
from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, require_permission
from src.auth.models import User
from src.common.exceptions import NotFoundError
from src.common.schemas import PaginatedResponse, SuccessResponse
from src.database import get_db
from src.finance.schemas import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
    FinanceOverview,
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdate,
)
from src.sales.models import Expense, Invoice, Order

router = APIRouter(prefix="/finance", tags=["Finance"])


# ── Expenses ──────────────────────────────────────────────────────

@router.get("/expenses", response_model=SuccessResponse[PaginatedResponse[ExpenseResponse]])
async def list_expenses(
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all business expenses for the current organization."""
    query = select(Expense).where(Expense.org_id == user.org_id)
    if category:
        query = query.where(Expense.category == category)
    if start_date:
        query = query.where(Expense.expense_date >= start_date)
    if end_date:
        query = query.where(Expense.expense_date <= end_date)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.order_by(Expense.expense_date.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    expenses = result.scalars().all()

    return SuccessResponse(
        data=PaginatedResponse.create(
            [ExpenseResponse.model_validate(e) for e in expenses],
            total or 0,
            page,
            page_size,
        )
    )


@router.post("/expenses", response_model=SuccessResponse[ExpenseResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("expenses", "create"))])
async def create_expense(
    data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new business expense record."""
    expense = Expense(org_id=user.org_id, **data.model_dump())
    db.add(expense)
    await db.flush()
    return SuccessResponse(message="Expense created", data=ExpenseResponse.model_validate(expense))


@router.get("/expenses/{expense_id}", response_model=SuccessResponse[ExpenseResponse])
async def get_expense(
    expense_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Expense).where(Expense.id == expense_id, Expense.org_id == user.org_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise NotFoundError("Expense", str(expense_id))
    return SuccessResponse(data=ExpenseResponse.model_validate(expense))


@router.patch("/expenses/{expense_id}", response_model=SuccessResponse[ExpenseResponse], dependencies=[Depends(require_permission("expenses", "update"))])
async def update_expense(
    expense_id: uuid.UUID,
    data: ExpenseUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Expense).where(Expense.id == expense_id, Expense.org_id == user.org_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise NotFoundError("Expense", str(expense_id))

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(expense, key, value)
    await db.flush()
    return SuccessResponse(message="Expense updated", data=ExpenseResponse.model_validate(expense))


@router.delete("/expenses/{expense_id}", response_model=SuccessResponse, dependencies=[Depends(require_permission("expenses", "delete"))])
async def delete_expense(
    expense_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Expense).where(Expense.id == expense_id, Expense.org_id == user.org_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise NotFoundError("Expense", str(expense_id))
    await db.delete(expense)
    await db.flush()
    return SuccessResponse(message="Expense deleted")


# ── Invoices ──────────────────────────────────────────────────────

@router.get("/invoices", response_model=SuccessResponse[PaginatedResponse[InvoiceResponse]])
async def list_invoices(
    status_filter: Optional[str] = Query(None, alias="status"),
    customer_id: Optional[uuid.UUID] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all invoices."""
    query = select(Invoice).where(Invoice.org_id == user.org_id)
    if status_filter:
        query = query.where(Invoice.status == status_filter)
    if customer_id:
        query = query.where(Invoice.customer_id == customer_id)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.order_by(Invoice.issue_date.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    invoices = result.scalars().all()

    return SuccessResponse(
        data=PaginatedResponse.create(
            [InvoiceResponse.model_validate(inv) for inv in invoices],
            total or 0,
            page,
            page_size,
        )
    )


@router.post("/invoices", response_model=SuccessResponse[InvoiceResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("invoices", "create"))])
async def create_invoice(
    data: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new invoice."""
    invoice_number = data.invoice_number
    if not invoice_number:
        count = await db.scalar(select(func.count(Invoice.id)).where(Invoice.org_id == user.org_id)) or 0
        invoice_number = f"INV-2026-{str(count + 1).zfill(4)}"

    total_amount = data.subtotal + data.tax_amount - data.discount_amount

    inv_data = data.model_dump(exclude={"invoice_number"})
    invoice = Invoice(
        org_id=user.org_id,
        invoice_number=invoice_number,
        total_amount=total_amount,
        amount_paid=Decimal("0"),
        **inv_data,
    )
    db.add(invoice)
    await db.flush()
    return SuccessResponse(message="Invoice created", data=InvoiceResponse.model_validate(invoice))


@router.get("/invoices/{invoice_id}", response_model=SuccessResponse[InvoiceResponse])
async def get_invoice(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id, Invoice.org_id == user.org_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise NotFoundError("Invoice", str(invoice_id))
    return SuccessResponse(data=InvoiceResponse.model_validate(invoice))


@router.patch("/invoices/{invoice_id}/status", response_model=SuccessResponse[InvoiceResponse], dependencies=[Depends(require_permission("invoices", "update"))])
async def update_invoice_status(
    invoice_id: uuid.UUID,
    data: InvoiceUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id, Invoice.org_id == user.org_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise NotFoundError("Invoice", str(invoice_id))

    if data.status:
        invoice.status = data.status
    if data.paid_amount is not None:
        invoice.paid_amount = data.paid_amount

    await db.flush()
    return SuccessResponse(message="Invoice status updated", data=InvoiceResponse.model_validate(invoice))


@router.delete("/invoices/{invoice_id}", response_model=SuccessResponse, dependencies=[Depends(require_permission("invoices", "delete"))])
async def delete_invoice(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id, Invoice.org_id == user.org_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise NotFoundError("Invoice", str(invoice_id))
    await db.delete(invoice)
    await db.flush()
    return SuccessResponse(message="Invoice deleted")


# ── Financial Overview / P&L / Cash Flow ─────────────────────────

@router.get("/overview", response_model=SuccessResponse[FinanceOverview])
async def get_finance_overview(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Aggregate financial health metrics: revenue, expenses, net profit, cashflow, and breakdown."""
    total_rev = await db.scalar(
        select(func.coalesce(func.sum(Order.total_amount), 0)).where(
            Order.org_id == user.org_id,
            Order.status.in_(["completed", "shipped", "processing"]),
        )
    )
    total_exp = await db.scalar(
        select(func.coalesce(func.sum(Expense.amount), 0)).where(Expense.org_id == user.org_id)
    )

    revenue = Decimal(str(total_rev or 0))
    expenses = Decimal(str(total_exp or 0))
    net_profit = revenue - expenses
    profit_margin = (net_profit / revenue * 100) if revenue > 0 else Decimal("0")

    # Invoices stats
    outstanding_res = await db.execute(
        select(
            func.coalesce(func.sum(Invoice.total_amount - Invoice.amount_paid), 0),
            func.count(Invoice.id),
        ).where(Invoice.org_id == user.org_id, Invoice.status.in_(["sent", "partially_paid"]))
    )
    out_amt, out_cnt = outstanding_res.one()

    overdue_res = await db.execute(
        select(
            func.coalesce(func.sum(Invoice.total_amount - Invoice.amount_paid), 0),
            func.count(Invoice.id),
        ).where(Invoice.org_id == user.org_id, Invoice.status == "overdue")
    )
    ovd_amt, ovd_cnt = overdue_res.one()

    # Expenses by category
    exp_cat_res = await db.execute(
        select(Expense.category, func.sum(Expense.amount))
        .where(Expense.org_id == user.org_id)
        .group_by(Expense.category)
    )
    exp_by_cat = {cat: Decimal(str(amt)) for cat, amt in exp_cat_res.all()}

    overview = FinanceOverview(
        total_revenue=revenue,
        total_expenses=expenses,
        net_profit=net_profit,
        profit_margin_pct=round(profit_margin, 2),
        cash_inflow=revenue,
        cash_outflow=expenses,
        net_cash_flow=net_profit,
        outstanding_invoices_amount=Decimal(str(out_amt)),
        outstanding_invoices_count=out_cnt,
        overdue_invoices_amount=Decimal(str(ovd_amt)),
        overdue_invoices_count=ovd_cnt,
        expense_by_category=exp_by_cat,
    )
    return SuccessResponse(data=overview)
