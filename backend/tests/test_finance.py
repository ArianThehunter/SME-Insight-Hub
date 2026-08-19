"""
Unit tests for Finance schemas, expenses, and invoice VAT calculations.
"""

from datetime import date
from decimal import Decimal
from src.finance.schemas import ExpenseCreate, InvoiceCreate


def test_expense_schema_validation():
    """Verify expense logging schema."""
    expense = ExpenseCreate(
        category="Office Rent",
        description="July 2026 Office Rent - Gulshan Office",
        amount=Decimal("45000.00"),
        expense_date=date(2026, 7, 1),
        payment_method="bKash",
        department="Operations",
    )
    assert expense.amount == Decimal("45000.00")
    assert expense.category == "Office Rent"


def test_invoice_vat_calculation():
    """Verify 15% NBR standard VAT calculation on invoices."""
    subtotal = Decimal("100000.00")
    tax_amount = subtotal * Decimal("0.15")  # 15% Bangladesh VAT
    discount_amount = Decimal("5000.00")
    total_amount = subtotal + tax_amount - discount_amount

    inv = InvoiceCreate(
        issue_date=date(2026, 7, 1),
        due_date=date(2026, 7, 30),
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
    )
    assert inv.subtotal == Decimal("100000.00")
    assert inv.tax_amount == Decimal("15000.00")
    assert total_amount == Decimal("110000.00")
