#!/usr/bin/env python3
"""
Bangladesh SME Seed Data — Populates database with realistic demo data.
Run: python seed.py

Creates:
- 1 demo organization (Acme Corporation Ltd.)
- 1 org_owner user (admin@acmecorp.com / password: Demo@1234)
- 15 customers (Bangladesh businesses)
- 20 products (electronics, textiles, food)
- 5 suppliers
- 2 warehouses (Dhaka, Chittagong)
- 30 sales orders
- 15 expenses
- 10 invoices
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date, datetime, timezone, timedelta
from decimal import Decimal
import random

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_factory, engine, Base
from src.auth.models import Organization, Role, User, Permission
from src.common.security import hash_password
from src.common.enums import UserRole
from src.sales.models import (
    Customer, Product, Order, OrderItem, Supplier, Warehouse, Expense, Invoice
)


DEMO_EMAIL = "admin@acmecorp.com"
DEMO_PASSWORD = "Demo@1234"


async def create_tables():
    """Create all tables from models."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created")


async def seed(db: AsyncSession):
    print("🌱 Seeding Bangladesh SME demo data...")

    # ── Organization ─────────────────────────────────────────────
    org = Organization(
        name="Acme Corporation Ltd.",
        name_bn="একমি কর্পোরেশন লিমিটেড",
        slug="acme-corp-demo",
        description="A leading trading company in Dhaka",
        email="info@acmecorp.com.bd",
        phone="+8801712000000",
        address="House 42, Road 11, Banani, Dhaka-1213",
        address_bn="বাড়ি ৪২, রাস্তা ১১, বনানী, ঢাকা-১২১৩",
        locale="en",
        currency="BDT",
        timezone="Asia/Dhaka",
        fiscal_year_start=7,  # July (Bangladesh fiscal year)
        is_active=True,
    )
    db.add(org)
    await db.flush()
    print(f"  ✓ Organization: {org.name}")

    # ── Roles ─────────────────────────────────────────────────────
    role = Role(
        name=UserRole.ORG_OWNER.value,
        display_name="Organization Owner",
        display_name_bn="প্রতিষ্ঠান মালিক",
        is_system=True,
    )
    db.add(role)
    await db.flush()

    # ── Admin User ────────────────────────────────────────────────
    user = User(
        email=DEMO_EMAIL,
        password_hash=hash_password(DEMO_PASSWORD),
        full_name="Rafiq Ahmed",
        full_name_bn="রফিক আহমেদ",
        phone="+8801712345678",
        org_id=org.id,
        role_id=role.id,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.flush()
    print(f"  ✓ User: {user.email} / {DEMO_PASSWORD}")

    # ── Suppliers ─────────────────────────────────────────────────
    supplier_data = [
        ("Chittagong Port Traders", "চট্টগ্রাম বন্দর ব্যবসায়ী", "Mr. Karim", "+8801812345678", "Chittagong"),
        ("Narayanganj Textile Mills", "নারায়ণগঞ্জ বস্ত্র মিলস", "Mrs. Sultana", "+8801912345678", "Narayanganj"),
        ("Gazipur Electronics Hub", "গাজীপুর ইলেকট্রনিক্স হাব", "Mr. Rahman", "+8801512345678", "Gazipur"),
        ("Rajshahi Agro Products", "রাজশাহী কৃষি পণ্য", "Mr. Islam", "+8801612345678", "Rajshahi"),
        ("Bogura Steel Industries", "বগুড়া স্টিল ইন্ডাস্ট্রিজ", "Mr. Hossain", "+8801712999888", "Bogura"),
    ]
    suppliers = []
    for name, name_bn, contact, phone, city in supplier_data:
        s = Supplier(
            org_id=org.id, name=name, name_bn=name_bn,
            contact_person=contact, phone=phone, city=city,
            rating=Decimal(str(round(random.uniform(3.5, 5.0), 2))),
            is_active=True,
        )
        db.add(s)
        suppliers.append(s)
    await db.flush()
    print(f"  ✓ {len(suppliers)} suppliers")

    # ── Warehouses ────────────────────────────────────────────────
    warehouses_data = [
        ("Dhaka Central Warehouse", "ঢাকা কেন্দ্রীয় গুদাম", "Tejgaon, Dhaka", 50000),
        ("Chittagong Port Depot", "চট্টগ্রাম বন্দর ডিপো", "Agrabad, Chittagong", 30000),
    ]
    for name, name_bn, location, capacity in warehouses_data:
        w = Warehouse(
            org_id=org.id, name=name, name_bn=name_bn,
            location=location, capacity=capacity,
            current_stock=random.randint(5000, capacity // 2),
            is_active=True,
        )
        db.add(w)
    await db.flush()
    print(f"  ✓ 2 warehouses")

    # ── Customers ─────────────────────────────────────────────────
    customers_data = [
        ("Rahman Textiles Ltd.", "রহমান টেক্সটাইলস লি.", "info@rahman.com.bd", "+8801712111111", "Narsingdi", "enterprise"),
        ("Dhaka Electronics Hub", "ঢাকা ইলেকট্রনিক্স হাব", "sales@dhaka-elec.com", "+8801812111111", "Dhaka", "mid_market"),
        ("Chittagong Spice Co.", "চট্টগ্রাম মশলা কোং", "spice@ctgco.com", "+8801912111111", "Chittagong", "small_business"),
        ("Sylhet Tea Gardens", "সিলেট চা বাগান", "tea@sylhetgardens.com", "+8801512111111", "Sylhet", "enterprise"),
        ("Rajshahi Mangoes Inc.", "রাজশাহী আম ইনকর্পোরেটেড", "mangoes@rajshahi.com", "+8801612111111", "Rajshahi", "small_business"),
        ("Khulna Fisheries Ltd.", "খুলনা মৎস্য লি.", "fish@khulna.com.bd", "+8801712222222", "Khulna", "mid_market"),
        ("Narayanganj Jute Works", "নারায়ণগঞ্জ পাট কারখানা", "jute@njworks.com", "+8801812222222", "Narayanganj", "enterprise"),
        ("Comilla Ceramics", "কুমিল্লা সিরামিক্স", "ceramics@comilla.com", "+8801912222222", "Comilla", "small_business"),
        ("Bogura Steel Corp.", "বগুড়া স্টিল কর্পোরেশন", "steel@bogura.com", "+8801512222222", "Bogura", "enterprise"),
        ("Gazipur Garments Ltd.", "গাজীপুর পোশাক লি.", "garments@gazipur.com", "+8801612222222", "Gazipur", "mid_market"),
        ("Jessore Food Products", "যশোর খাদ্য পণ্য", "food@jessore.com", "+8801712333333", "Jessore", "small_business"),
        ("Mymensingh Dairy Farm", "ময়মনসিংহ ডেইরি ফার্ম", "dairy@mymensingh.com", "+8801812333333", "Mymensingh", "small_business"),
        ("Rangpur Agro Solutions", "রংপুর কৃষি সমাধান", "agro@rangpur.com", "+8801912333333", "Rangpur", "mid_market"),
        ("Barishal Marine Co.", "বরিশাল মেরিন কোং", "marine@barishal.com", "+8801512333333", "Barishal", "mid_market"),
        ("Tangail Handicrafts", "টাঙ্গাইল হস্তশিল্প", "crafts@tangail.com", "+8801612333333", "Tangail", "small_business"),
    ]
    customers = []
    for name, name_bn, email, phone, city, segment in customers_data:
        ltv = Decimal(str(random.randint(50000, 5000000)))
        c = Customer(
            org_id=org.id, name=name, name_bn=name_bn, email=email,
            phone=phone, city=city, district=city, segment=segment,
            lifetime_value=ltv, total_orders=random.randint(1, 50),
            first_purchase=date(2024, random.randint(1, 6), random.randint(1, 28)),
            last_purchase=date(2026, random.randint(6, 8), random.randint(1, 15)),
            is_active=True,
        )
        db.add(c)
        customers.append(c)
    await db.flush()
    print(f"  ✓ {len(customers)} customers")

    # ── Products ──────────────────────────────────────────────────
    products_data = [
        ("Laptop 15\" Core i5", "ল্যাপটপ ১৫\" কোর আই৫", "LAP-I5-001", "Electronics", "pcs", 65000, 52000),
        ("Wireless Mouse MX-200", "ওয়ারলেস মাউস এমএক্স-২০০", "MSE-WL-200", "Electronics", "pcs", 1500, 900),
        ("Cotton Fabric (per yard)", "তুলার কাপড় (প্রতি গজ)", "FAB-CTN-001", "Textiles", "yard", 250, 180),
        ("Silk Saree Premium", "সিল্ক শাড়ি প্রিমিয়াম", "SAR-SLK-001", "Textiles", "pcs", 8500, 6000),
        ("Basmati Rice (50kg bag)", "বাসমতি চাল (৫০কেজি বস্তা)", "RCE-BAS-050", "Food & Agriculture", "bag", 3500, 2800),
        ("Mustard Oil (5L)", "সরিষার তেল (৫ লিটার)", "OIL-MST-005", "Food & Agriculture", "bottle", 850, 680),
        ("Steel Rod 12mm (per ton)", "স্টিল রড ১২মিমি (প্রতি টন)", "STL-ROD-012", "Construction", "ton", 95000, 88000),
        ("Cement (50kg bag)", "সিমেন্ট (৫০কেজি বস্তা)", "CMT-STD-050", "Construction", "bag", 580, 520),
        ("Rechargeable LED Light", "রিচার্জেবল এলইডি লাইট", "LGT-LED-001", "Electronics", "pcs", 1200, 750),
        ("Water Pump 1HP", "পানির পাম্প ১ এইচপি", "PMP-H01-001", "Machinery", "pcs", 8500, 6500),
        ("Smartphone Android 5G", "স্মার্টফোন অ্যান্ড্রয়েড ৫জি", "PHN-AND-5G", "Electronics", "pcs", 28000, 22000),
        ("Jute Bags (set of 100)", "পাটের ব্যাগ (১০০টির সেট)", "JUT-BAG-100", "Packaging", "set", 4500, 3200),
        ("Sugar (50kg bag)", "চিনি (৫০কেজি বস্তা)", "SGR-WHT-050", "Food & Agriculture", "bag", 4200, 3800),
        ("Power Strip 6-outlet", "পাওয়ার স্ট্রিপ ৬-আউটলেট", "PWR-STR-006", "Electronics", "pcs", 650, 420),
        ("Mosquito Net (Double)", "মশারি (ডাবল)", "NET-MOS-DBL", "Household", "pcs", 380, 250),
        ("A4 Paper (500 sheets)", "এ৪ কাগজ (৫০০ শিট)", "PPR-A4-500", "Stationery", "ream", 420, 340),
        ("Hand Sanitizer (1L)", "হ্যান্ড স্যানিটাইজার (১ লিটার)", "SAN-HAD-001", "Healthcare", "bottle", 280, 200),
        ("Ceramic Floor Tile (sqft)", "সিরামিক মেঝের টাইল (বর্গফুট)", "TIL-CRM-001", "Construction", "sqft", 120, 90),
        ("Bicycle (Mountain)", "সাইকেল (মাউন্টেন)", "BCY-MTN-001", "Sports", "pcs", 15000, 11000),
        ("Cooking Pot (Aluminum 5L)", "রান্নার পাত্র (অ্যালুমিনিয়াম ৫লি)", "POT-ALU-05L", "Household", "pcs", 650, 450),
    ]
    products = []
    for name, name_bn, sku, category, unit, price, cost in products_data:
        p = Product(
            org_id=org.id, name=name, name_bn=name_bn, sku=sku,
            category=category, unit=unit,
            price=Decimal(str(price)), cost=Decimal(str(cost)),
            tax_rate=Decimal("15"),  # Standard VAT in Bangladesh
            stock_quantity=random.randint(10, 500),
            reorder_level=random.randint(5, 50),
            supplier_id=random.choice(suppliers).id,
            is_active=True,
        )
        db.add(p)
        products.append(p)
    await db.flush()
    print(f"  ✓ {len(products)} products")

    # ── Orders ────────────────────────────────────────────────────
    statuses = ["completed", "completed", "completed", "processing", "shipped", "pending", "cancelled"]
    payment_statuses = ["paid", "paid", "partial", "unpaid", "refunded"]
    orders_count = 0

    for i in range(30):
        customer = random.choice(customers)
        order_date = date(2026, random.randint(1, 8), random.randint(1, 28))
        num_items = random.randint(1, 5)
        chosen_products = random.sample(products, num_items)

        order = Order(
            org_id=org.id,
            order_number=f"ORD-2026-{str(i+1).zfill(3)}",
            customer_id=customer.id,
            order_date=order_date,
            delivery_date=order_date + timedelta(days=random.randint(3, 14)),
            status=random.choice(statuses),
            payment_status=random.choice(payment_statuses),
            currency="BDT",
        )
        db.add(order)
        await db.flush()

        subtotal = Decimal("0")
        for product in chosen_products:
            qty = random.randint(1, 20)
            line_total = qty * product.price
            subtotal += line_total
            item = OrderItem(
                org_id=org.id,
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                unit_price=product.price,
                discount=Decimal("0"),
                tax=Decimal("0"),
                total_price=line_total,
            )
            db.add(item)

        order.subtotal = subtotal
        order.total_amount = subtotal
        orders_count += 1

    await db.flush()
    print(f"  ✓ {orders_count} orders")

    # ── Expenses ──────────────────────────────────────────────────
    expense_data = [
        ("Utilities", "Electricity", "DESCO electricity bill", "DESCO", 12500, "bank_transfer"),
        ("Utilities", "Internet", "Grameenphone business internet", "Grameenphone", 8500, "bank_transfer"),
        ("Rent", "Office", "Banani office monthly rent", "Building Management", 85000, "bank_transfer"),
        ("Salaries", "Staff", "Monthly staff payroll", "Payroll", 450000, "bank_transfer"),
        ("Transport", "Delivery", "Delivery van fuel costs", "Padma Oil", 25000, "cash"),
        ("Marketing", "Digital", "Facebook ads campaign", "Meta Platforms", 15000, "card"),
        ("Utilities", "Water", "WASA water bill", "WASA", 3500, "bank_transfer"),
        ("Office Supplies", "Stationery", "Office stationery monthly", "Ananya Stationers", 8000, "cash"),
        ("Maintenance", "Equipment", "AC servicing and repair", "Cool Air BD", 12000, "bkash"),
        ("Insurance", "Business", "Business insurance premium", "Green Delta Insurance", 35000, "bank_transfer"),
        ("Training", "Staff Development", "Employee training workshop", "BRAC Training", 22000, "bank_transfer"),
        ("Legal", "Compliance", "Trade license renewal fee", "DNCC", 15000, "bank_transfer"),
        ("Transport", "Courier", "DHL courier charges", "DHL Bangladesh", 8500, "card"),
        ("Cleaning", "Office", "Office cleaning service", "CleanBD", 4500, "bkash"),
        ("Banking", "Charges", "Bank service charges", "BRAC Bank", 2500, "bank_transfer"),
    ]
    for i, (category, subcategory, desc, vendor, amount, payment_method) in enumerate(expense_data):
        e = Expense(
            org_id=org.id,
            category=category, subcategory=subcategory,
            description=desc, vendor=vendor,
            amount=Decimal(str(amount)),
            expense_date=date(2026, random.randint(6, 8), random.randint(1, 28)),
            payment_method=payment_method,
            is_recurring=i < 6,  # First 6 are recurring
        )
        db.add(e)
    await db.flush()
    print(f"  ✓ 15 expenses")

    # ── Invoices ──────────────────────────────────────────────────
    invoice_statuses = ["paid", "paid", "sent", "partially_paid", "overdue", "draft"]
    for i in range(10):
        customer = random.choice(customers)
        subtotal = Decimal(str(random.randint(50000, 500000)))
        tax = subtotal * Decimal("0.15")
        total = subtotal + tax
        paid = total if random.random() > 0.4 else Decimal("0")
        issue_date = date(2026, random.randint(5, 8), random.randint(1, 20))
        inv = Invoice(
            org_id=org.id,
            invoice_number=f"INV-2026-{str(i+1).zfill(4)}",
            customer_id=customer.id,
            status=random.choice(invoice_statuses),
            subtotal=subtotal,
            tax_amount=tax,
            total_amount=total,
            amount_paid=paid,
            issue_date=issue_date,
            due_date=issue_date + timedelta(days=30),
            paid_date=issue_date + timedelta(days=random.randint(1, 25)) if paid > 0 else None,
        )
        db.add(inv)
    await db.flush()
    print(f"  ✓ 10 invoices")

    print("\n🎉 Seed data complete!")
    print(f"   Login: {DEMO_EMAIL}")
    print(f"   Password: {DEMO_PASSWORD}")


async def main():
    print("Creating database tables...")
    await create_tables()

    async with async_session_factory() as db:
        try:
            # Check if already seeded
            from sqlalchemy import select
            from src.auth.models import User as UserModel
            result = await db.execute(select(UserModel).where(UserModel.email == DEMO_EMAIL))
            existing = result.scalar_one_or_none()
            if existing:
                print(f"⚠️  Seed data already exists (user: {DEMO_EMAIL}). Skipping.")
                return

            await seed(db)
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(f"❌ Seed failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
