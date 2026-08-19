"""
Unit tests for Sales and Inventory schemas and calculation logic.
"""

from decimal import Decimal
from src.sales.schemas import (
    CustomerCreate,
    ProductCreate,
    OrderCreate,
    OrderItemCreate,
    SupplierCreate,
    WarehouseCreate,
)


def test_customer_schema_validation():
    """Test customer creation schema with bilingual fields."""
    cust_data = CustomerCreate(
        name="Rahman Textiles Ltd.",
        name_bn="রহমান টেক্সটাইলস লি.",
        email="info@rahmantextiles.com",
        phone="+8801711223344",
        city="Dhaka",
        district="Dhaka",
        segment="enterprise",
    )
    assert cust_data.name == "Rahman Textiles Ltd."
    assert cust_data.city == "Dhaka"


def test_product_schema_validation():
    """Test product schema creation and margin pricing."""
    prod = ProductCreate(
        name="Wireless Keyboard K-100",
        sku="SKU-KB-100",
        category="Electronics",
        cost=Decimal("1200.00"),
        price=Decimal("1800.00"),
        stock_quantity=50,
        reorder_level=10,
    )
    assert prod.sku == "SKU-KB-100"
    assert prod.price > prod.cost


def test_order_creation_schema():
    """Test order creation schema with nested line items."""
    import uuid
    from datetime import date

    prod_id = uuid.uuid4()
    cust_id = uuid.uuid4()

    item1 = OrderItemCreate(
        product_id=prod_id,
        quantity=2,
        unit_price=Decimal("1800.00"),
        discount=Decimal("100.00"),
    )
    order = OrderCreate(
        customer_id=cust_id,
        order_date=date(2026, 7, 1),
        items=[item1],
        payment_method="bKash",
        shipping_address="Dhaka, Bangladesh",
    )
    assert len(order.items) == 1
    assert order.items[0].quantity == 2
