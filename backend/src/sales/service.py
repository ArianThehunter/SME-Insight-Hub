"""
Sales domain — CRUD service layer.
All queries are org-scoped (multi-tenant via org_id).
"""

import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.common.exceptions import NotFoundError
from src.sales.models import Customer, Order, OrderItem, Product, Supplier, Warehouse
from src.sales.schemas import (
    CustomerCreate,
    CustomerUpdate,
    OrderCreate,
    ProductCreate,
    ProductUpdate,
    SupplierCreate,
    WarehouseCreate,
)


class SalesService:
    """Handles sales domain business logic with org-scoped queries."""

    def __init__(self, db: AsyncSession, org_id: uuid.UUID):
        self.db = db
        self.org_id = org_id

    # ── Customers ─────────────────────────────────────────────────

    async def list_customers(
        self,
        search: str | None = None,
        segment: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Customer], int]:
        query = select(Customer).where(Customer.org_id == self.org_id, Customer.is_active)
        if search:
            query = query.where(
                Customer.name.ilike(f"%{search}%") |
                Customer.email.ilike(f"%{search}%") |
                Customer.phone.ilike(f"%{search}%")
            )
        if segment:
            query = query.where(Customer.segment == segment)

        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        query = query.order_by(Customer.name).offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total or 0

    async def get_customer(self, customer_id: uuid.UUID) -> Customer:
        result = await self.db.execute(
            select(Customer).where(Customer.id == customer_id, Customer.org_id == self.org_id)
        )
        customer = result.scalar_one_or_none()
        if not customer:
            raise NotFoundError("Customer", str(customer_id))
        return customer

    async def create_customer(self, data: CustomerCreate) -> Customer:
        customer = Customer(org_id=self.org_id, **data.model_dump())
        self.db.add(customer)
        await self.db.flush()
        return customer

    async def update_customer(self, customer_id: uuid.UUID, data: CustomerUpdate) -> Customer:
        customer = await self.get_customer(customer_id)
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(customer, key, value)
        await self.db.flush()
        return customer

    async def delete_customer(self, customer_id: uuid.UUID) -> None:
        customer = await self.get_customer(customer_id)
        customer.is_active = False
        await self.db.flush()

    # ── Products ──────────────────────────────────────────────────

    async def list_products(
        self,
        search: str | None = None,
        category: str | None = None,
        low_stock_only: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Product], int]:
        query = select(Product).where(Product.org_id == self.org_id, Product.is_active)
        if search:
            query = query.where(Product.name.ilike(f"%{search}%") | Product.sku.ilike(f"%{search}%"))
        if category:
            query = query.where(Product.category == category)
        if low_stock_only:
            query = query.where(Product.stock_quantity <= Product.reorder_level)

        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        query = query.order_by(Product.name).offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total or 0

    async def get_product(self, product_id: uuid.UUID) -> Product:
        result = await self.db.execute(
            select(Product).where(Product.id == product_id, Product.org_id == self.org_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise NotFoundError("Product", str(product_id))
        return product

    async def create_product(self, data: ProductCreate) -> Product:
        product = Product(org_id=self.org_id, **data.model_dump())
        self.db.add(product)
        await self.db.flush()
        return product

    async def update_product(self, product_id: uuid.UUID, data: ProductUpdate) -> Product:
        product = await self.get_product(product_id)
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(product, key, value)
        await self.db.flush()
        return product

    # ── Orders ────────────────────────────────────────────────────

    async def list_orders(
        self,
        status: str | None = None,
        customer_id: uuid.UUID | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Order], int]:
        query = (
            select(Order)
            .where(Order.org_id == self.org_id)
            .options(selectinload(Order.items))
        )
        if status:
            query = query.where(Order.status == status)
        if customer_id:
            query = query.where(Order.customer_id == customer_id)

        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        query = query.order_by(Order.order_date.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total or 0

    async def get_order(self, order_id: uuid.UUID) -> Order:
        result = await self.db.execute(
            select(Order)
            .where(Order.id == order_id, Order.org_id == self.org_id)
            .options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()
        if not order:
            raise NotFoundError("Order", str(order_id))
        return order

    async def create_order(self, data: OrderCreate, created_by: uuid.UUID) -> Order:
        # Generate order number
        count = await self.db.scalar(select(func.count(Order.id)).where(Order.org_id == self.org_id)) or 0
        order_number = f"ORD-{uuid.uuid4().hex[:4].upper()}-{str(count + 1).zfill(4)}"

        subtotal = Decimal(0)
        items_data = []
        for item in data.items:
            line_total = item.quantity * item.unit_price - item.discount
            subtotal += line_total
            items_data.append((item, line_total))

        order = Order(
            org_id=self.org_id,
            order_number=order_number,
            customer_id=data.customer_id,
            order_date=data.order_date,
            delivery_date=data.delivery_date,
            shipping_address=data.shipping_address,
            notes=data.notes,
            payment_method=data.payment_method,
            subtotal=subtotal,
            total_amount=subtotal,
        )
        self.db.add(order)
        await self.db.flush()

        for item_data, line_total in items_data:
            order_item = OrderItem(
                org_id=self.org_id,
                order_id=order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                discount=item_data.discount,
                tax=Decimal(0),
                total_price=line_total,
            )
            self.db.add(order_item)

        await self.db.flush()
        return order

    # ── Suppliers ─────────────────────────────────────────────────

    async def list_suppliers(self, page: int = 1, page_size: int = 20) -> tuple[list[Supplier], int]:
        query = select(Supplier).where(Supplier.org_id == self.org_id, Supplier.is_active)
        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        query = query.order_by(Supplier.name).offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total or 0

    async def create_supplier(self, data: SupplierCreate) -> Supplier:
        supplier = Supplier(org_id=self.org_id, **data.model_dump())
        self.db.add(supplier)
        await self.db.flush()
        return supplier

    # ── Warehouses ────────────────────────────────────────────────

    async def list_warehouses(self) -> list[Warehouse]:
        result = await self.db.execute(
            select(Warehouse).where(Warehouse.org_id == self.org_id, Warehouse.is_active)
        )
        return list(result.scalars().all())

    async def create_warehouse(self, data: WarehouseCreate) -> Warehouse:
        warehouse = Warehouse(org_id=self.org_id, **data.model_dump())
        self.db.add(warehouse)
        await self.db.flush()
        return warehouse
