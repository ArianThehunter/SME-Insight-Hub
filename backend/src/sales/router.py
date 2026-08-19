"""
Sales domain — API router for customers, products, orders, suppliers, warehouses.
All endpoints require authentication. All data is org-scoped.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, require_permission
from src.auth.models import User
from src.common.schemas import PaginatedResponse, SuccessResponse
from src.database import get_db
from src.sales.schemas import (
    CustomerCreate, CustomerResponse, CustomerUpdate,
    OrderCreate, OrderResponse,
    ProductCreate, ProductResponse, ProductUpdate,
    SupplierCreate, SupplierResponse,
    WarehouseCreate, WarehouseResponse,
)
from src.sales.service import SalesService

router = APIRouter(prefix="/sales", tags=["Sales"])


def _svc(db: AsyncSession, user: User) -> SalesService:
    return SalesService(db, user.org_id)


# ── Customers ────────────────────────────────────────────────────

@router.get("/customers", response_model=SuccessResponse[PaginatedResponse[CustomerResponse]])
async def list_customers(
    search: Optional[str] = Query(None),
    segment: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all customers for the current organization."""
    svc = _svc(db, user)
    customers, total = await svc.list_customers(search, segment, page, page_size)
    return SuccessResponse(data=PaginatedResponse.create(
        [CustomerResponse.model_validate(c) for c in customers], total, page, page_size
    ))


@router.post("/customers", response_model=SuccessResponse[CustomerResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("customers", "create"))])
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new customer."""
    customer = await _svc(db, user).create_customer(data)
    return SuccessResponse(message="Customer created", data=CustomerResponse.model_validate(customer))


@router.get("/customers/{customer_id}", response_model=SuccessResponse[CustomerResponse])
async def get_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    customer = await _svc(db, user).get_customer(customer_id)
    return SuccessResponse(data=CustomerResponse.model_validate(customer))


@router.patch("/customers/{customer_id}", response_model=SuccessResponse[CustomerResponse], dependencies=[Depends(require_permission("customers", "update"))])
async def update_customer(
    customer_id: uuid.UUID,
    data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    customer = await _svc(db, user).update_customer(customer_id, data)
    return SuccessResponse(message="Customer updated", data=CustomerResponse.model_validate(customer))


@router.delete("/customers/{customer_id}", response_model=SuccessResponse, dependencies=[Depends(require_permission("customers", "delete"))])
async def delete_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await _svc(db, user).delete_customer(customer_id)
    return SuccessResponse(message="Customer deactivated")


# ── Products ─────────────────────────────────────────────────────

@router.get("/products", response_model=SuccessResponse[PaginatedResponse[ProductResponse]])
async def list_products(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    low_stock: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all products."""
    svc = _svc(db, user)
    products, total = await svc.list_products(search, category, low_stock, page, page_size)
    return SuccessResponse(data=PaginatedResponse.create(
        [ProductResponse.model_validate(p) for p in products], total, page, page_size
    ))


@router.post("/products", response_model=SuccessResponse[ProductResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("products", "create"))])
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = await _svc(db, user).create_product(data)
    return SuccessResponse(message="Product created", data=ProductResponse.model_validate(product))


@router.patch("/products/{product_id}", response_model=SuccessResponse[ProductResponse], dependencies=[Depends(require_permission("products", "update"))])
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = await _svc(db, user).update_product(product_id, data)
    return SuccessResponse(message="Product updated", data=ProductResponse.model_validate(product))


# ── Orders ───────────────────────────────────────────────────────

@router.get("/orders", response_model=SuccessResponse[PaginatedResponse[OrderResponse]])
async def list_orders(
    status_filter: Optional[str] = Query(None, alias="status"),
    customer_id: Optional[uuid.UUID] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all orders."""
    svc = _svc(db, user)
    orders, total = await svc.list_orders(status_filter, customer_id, page, page_size)
    return SuccessResponse(data=PaginatedResponse.create(
        [OrderResponse.model_validate(o) for o in orders], total, page, page_size
    ))


@router.post("/orders", response_model=SuccessResponse[OrderResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("orders", "create"))])
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = await _svc(db, user).create_order(data, user.id)
    return SuccessResponse(message="Order created", data=OrderResponse.model_validate(order))


@router.get("/orders/{order_id}", response_model=SuccessResponse[OrderResponse])
async def get_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = await _svc(db, user).get_order(order_id)
    return SuccessResponse(data=OrderResponse.model_validate(order))


# ── Suppliers ────────────────────────────────────────────────────

@router.get("/suppliers", response_model=SuccessResponse[PaginatedResponse[SupplierResponse]])
async def list_suppliers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = _svc(db, user)
    suppliers, total = await svc.list_suppliers(page, page_size)
    return SuccessResponse(data=PaginatedResponse.create(
        [SupplierResponse.model_validate(s) for s in suppliers], total, page, page_size
    ))


@router.post("/suppliers", response_model=SuccessResponse[SupplierResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("suppliers", "create"))])
async def create_supplier(
    data: SupplierCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    supplier = await _svc(db, user).create_supplier(data)
    return SuccessResponse(message="Supplier created", data=SupplierResponse.model_validate(supplier))


# ── Warehouses ───────────────────────────────────────────────────

@router.get("/warehouses", response_model=SuccessResponse[list[WarehouseResponse]])
async def list_warehouses(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    warehouses = await _svc(db, user).list_warehouses()
    return SuccessResponse(data=[WarehouseResponse.model_validate(w) for w in warehouses])


@router.post("/warehouses", response_model=SuccessResponse[WarehouseResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("warehouses", "create"))])
async def create_warehouse(
    data: WarehouseCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    warehouse = await _svc(db, user).create_warehouse(data)
    return SuccessResponse(message="Warehouse created", data=WarehouseResponse.model_validate(warehouse))
