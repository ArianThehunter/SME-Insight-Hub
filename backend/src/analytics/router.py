"""
Analytics domain — Dashboard data, KPIs, and chart data endpoints.
Serves both real (from DB) and demo data for showcasing.
"""

import random
import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.common.schemas import BaseSchema, SuccessResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ── Schemas ───────────────────────────────────────────────────────
class KPICard(BaseSchema):
    """Single KPI metric card data."""
    id: str
    title: str
    title_bn: Optional[str] = None
    value: float
    formatted_value: str
    change_percent: float
    change_direction: str  # "up", "down", "neutral"
    trend_data: List[float] = []
    currency: Optional[str] = None
    icon: str
    color: str


class ChartData(BaseSchema):
    """Chart data with labels and datasets."""
    id: str
    title: str
    title_bn: Optional[str] = None
    chart_type: str
    labels: List[str]
    datasets: List[Dict[str, Any]]


class AIInsight(BaseSchema):
    """AI-generated business insight."""
    id: str
    title: str
    title_bn: Optional[str] = None
    description: str
    description_bn: Optional[str] = None
    severity: str  # "info", "success", "warning", "critical"
    category: str
    action_url: Optional[str] = None
    metric_value: Optional[str] = None
    icon: str


class ActivityItem(BaseSchema):
    """Activity feed item."""
    id: str
    title: str
    title_bn: Optional[str] = None
    description: str
    type: str  # "invoice", "report", "customer", "stock", "user", "alert"
    icon: str
    timestamp: datetime
    user_name: Optional[str] = None
    url: Optional[str] = None


class DashboardResponse(BaseSchema):
    """Complete dashboard data."""
    kpis: List[KPICard]
    charts: List[ChartData]
    insights: List[AIInsight]
    activities: List[ActivityItem]
    summary: Dict[str, Any]


# ── Demo Data Generator ──────────────────────────────────────────
def _generate_sparkline(base: float, variance: float = 0.1, points: int = 12) -> List[float]:
    """Generate a realistic sparkline trend."""
    data = [base]
    for _ in range(points - 1):
        change = random.uniform(-variance, variance) * base
        data.append(round(max(0, data[-1] + change), 2))
    return data


def _generate_months(count: int = 12) -> List[str]:
    """Generate month labels for the last N months."""
    today = date.today()
    months = []
    for i in range(count - 1, -1, -1):
        d = today.replace(day=1) - timedelta(days=i * 30)
        months.append(d.strftime("%b %Y"))
    return months


def _get_demo_kpis() -> List[KPICard]:
    """Generate demo KPI data."""
    return [
        KPICard(
            id="revenue", title="Revenue", title_bn="রাজস্ব",
            value=28450000, formatted_value="৳2,84,50,000",
            change_percent=12.5, change_direction="up",
            trend_data=_generate_sparkline(2400000, 0.08),
            currency="BDT", icon="TrendingUp", color="emerald",
        ),
        KPICard(
            id="expenses", title="Expenses", title_bn="ব্যয়",
            value=18200000, formatted_value="৳1,82,00,000",
            change_percent=8.3, change_direction="up",
            trend_data=_generate_sparkline(1500000, 0.06),
            currency="BDT", icon="Receipt", color="rose",
        ),
        KPICard(
            id="profit", title="Profit", title_bn="মুনাফা",
            value=10250000, formatted_value="৳1,02,50,000",
            change_percent=18.2, change_direction="up",
            trend_data=_generate_sparkline(850000, 0.1),
            currency="BDT", icon="Wallet", color="blue",
        ),
        KPICard(
            id="cashflow", title="Cash Flow", title_bn="নগদ প্রবাহ",
            value=5800000, formatted_value="৳58,00,000",
            change_percent=5.1, change_direction="up",
            trend_data=_generate_sparkline(480000, 0.12),
            currency="BDT", icon="Banknote", color="violet",
        ),
        KPICard(
            id="customers", title="Customers", title_bn="গ্রাহক",
            value=1247, formatted_value="1,247",
            change_percent=15.3, change_direction="up",
            trend_data=_generate_sparkline(100, 0.05),
            icon="Users", color="cyan",
        ),
        KPICard(
            id="inventory_value", title="Inventory Value", title_bn="মজুদ মূল্য",
            value=12500000, formatted_value="৳1,25,00,000",
            change_percent=-3.2, change_direction="down",
            trend_data=_generate_sparkline(1050000, 0.04),
            currency="BDT", icon="Package", color="amber",
        ),
        KPICard(
            id="outstanding_invoices", title="Outstanding Invoices", title_bn="বকেয়া চালান",
            value=3200000, formatted_value="৳32,00,000",
            change_percent=-6.8, change_direction="down",
            trend_data=_generate_sparkline(270000, 0.1),
            currency="BDT", icon="FileText", color="orange",
        ),
        KPICard(
            id="growth", title="Growth", title_bn="প্রবৃদ্ধি",
            value=12.5, formatted_value="12.5%",
            change_percent=2.1, change_direction="up",
            trend_data=_generate_sparkline(10, 0.15),
            icon="TrendingUp", color="teal",
        ),
    ]


def _get_demo_charts() -> List[ChartData]:
    """Generate demo chart data."""
    months = _generate_months()

    return [
        ChartData(
            id="revenue_trend", title="Revenue Trend", title_bn="রাজস্ব প্রবণতা",
            chart_type="area",
            labels=months,
            datasets=[{
                "name": "Revenue",
                "data": [round(random.uniform(2000000, 3000000)) for _ in months],
                "color": "#10b981",
            }, {
                "name": "Target",
                "data": [2500000] * len(months),
                "color": "#6366f1",
                "lineStyle": "dashed",
            }],
        ),
        ChartData(
            id="expense_breakdown", title="Expense Breakdown", title_bn="ব্যয় বিশ্লেষণ",
            chart_type="donut",
            labels=["Operations", "Salaries", "Marketing", "Rent", "Utilities", "Other"],
            datasets=[{
                "name": "Expenses",
                "data": [4200000, 6500000, 2100000, 1800000, 900000, 2700000],
            }],
        ),
        ChartData(
            id="sales_by_category", title="Sales by Category", title_bn="বিভাগ অনুযায়ী বিক্রয়",
            chart_type="bar",
            labels=["Electronics", "Clothing", "Food", "Furniture", "Stationery", "Healthcare"],
            datasets=[{
                "name": "Current Period",
                "data": [8500000, 5200000, 4100000, 3800000, 2200000, 4650000],
                "color": "#3b82f6",
            }, {
                "name": "Previous Period",
                "data": [7200000, 4800000, 3900000, 4200000, 1900000, 3800000],
                "color": "#94a3b8",
            }],
        ),
        ChartData(
            id="monthly_comparison", title="Monthly Comparison", title_bn="মাসিক তুলনা",
            chart_type="bar",
            labels=months[-6:],
            datasets=[{
                "name": "Revenue",
                "data": [round(random.uniform(2000000, 3000000)) for _ in range(6)],
                "color": "#10b981",
            }, {
                "name": "Expenses",
                "data": [round(random.uniform(1500000, 2000000)) for _ in range(6)],
                "color": "#f43f5e",
            }],
        ),
        ChartData(
            id="geographic", title="Sales by Region", title_bn="অঞ্চল ভিত্তিক বিক্রয়",
            chart_type="bar",
            labels=["Dhaka", "Chittagong", "Rajshahi", "Khulna", "Sylhet", "Rangpur", "Barisal", "Mymensingh"],
            datasets=[{
                "name": "Sales",
                "data": [12000000, 5500000, 2800000, 2200000, 1800000, 1200000, 900000, 800000],
                "color": "#8b5cf6",
            }],
        ),
        ChartData(
            id="customer_acquisition", title="Customer Acquisition", title_bn="গ্রাহক অধিগ্রহণ",
            chart_type="line",
            labels=months,
            datasets=[{
                "name": "New Customers",
                "data": [round(random.uniform(30, 80)) for _ in months],
                "color": "#06b6d4",
            }, {
                "name": "Churned",
                "data": [round(random.uniform(5, 20)) for _ in months],
                "color": "#f43f5e",
            }],
        ),
        ChartData(
            id="inventory_movement", title="Inventory Movement", title_bn="মজুদ চলাচল",
            chart_type="bar",
            labels=months[-6:],
            datasets=[{
                "name": "Stock In",
                "data": [round(random.uniform(500, 1200)) for _ in range(6)],
                "color": "#10b981",
            }, {
                "name": "Stock Out",
                "data": [round(random.uniform(400, 1000)) for _ in range(6)],
                "color": "#f59e0b",
            }],
        ),
        ChartData(
            id="cashflow_forecast", title="Cash Flow Forecast", title_bn="নগদ প্রবাহ পূর্বাভাস",
            chart_type="area",
            labels=months,
            datasets=[{
                "name": "Actual",
                "data": [round(random.uniform(400000, 700000)) for _ in months[:9]] + [None, None, None],
                "color": "#3b82f6",
            }, {
                "name": "Forecast",
                "data": [None] * 8 + [round(random.uniform(450000, 650000)) for _ in range(4)],
                "color": "#8b5cf6",
                "lineStyle": "dashed",
            }],
        ),
    ]


def _get_demo_insights() -> List[AIInsight]:
    """Generate AI business insights."""
    return [
        AIInsight(
            id="insight_1", title="Revenue Growth Acceleration",
            title_bn="রাজস্ব বৃদ্ধি ত্বরান্বিত",
            description="Revenue increased by 12.5% compared to last quarter, driven primarily by electronics and healthcare categories. The growth rate is accelerating month over month.",
            description_bn="গত প্রান্তিকের তুলনায় রাজস্ব ১২.৫% বৃদ্ধি পেয়েছে, প্রধানত ইলেকট্রনিক্স এবং স্বাস্থ্যসেবা বিভাগের কারণে।",
            severity="success", category="revenue",
            metric_value="+12.5%", icon="TrendingUp",
            action_url="/sales/analytics",
        ),
        AIInsight(
            id="insight_2", title="Customer Retention Alert",
            title_bn="গ্রাহক ধরে রাখার সতর্কতা",
            description="Customer retention rate has declined by 6.2% this month. 23 enterprise customers haven't placed orders in the last 60 days. Recommend reaching out with targeted offers.",
            description_bn="এই মাসে গ্রাহক ধরে রাখার হার ৬.২% কমেছে। ২৩টি এন্টারপ্রাইজ গ্রাহক গত ৬০ দিনে অর্ডার দেননি।",
            severity="warning", category="customers",
            metric_value="-6.2%", icon="UserMinus",
            action_url="/crm/retention",
        ),
        AIInsight(
            id="insight_3", title="Critical Stock Level",
            title_bn="মজুদের সংকটপূর্ণ স্তর",
            description="Inventory for 'Samsung Galaxy A54' is critically low — only 12 units remaining with an average daily sale of 8 units. Reorder immediately from Supplier: TechBD Ltd.",
            description_bn="'Samsung Galaxy A54'-এর মজুদ সংকটপূর্ণ পর্যায়ে — মাত্র ১২ ইউনিট অবশিষ্ট, দৈনিক গড় বিক্রি ৮ ইউনিট।",
            severity="critical", category="inventory",
            metric_value="12 units", icon="AlertTriangle",
            action_url="/inventory/stock-alerts",
        ),
        AIInsight(
            id="insight_4", title="Supplier Delivery Delays",
            title_bn="সরবরাহকারী বিলম্ব",
            description="Supplier 'Global Trade BD' has delayed deliveries 3 months in a row. Average delay: 5.2 days. Consider diversifying supply chain or renegotiating terms.",
            description_bn="সরবরাহকারী 'Global Trade BD' পরপর ৩ মাস ডেলিভারি বিলম্ব করেছে। গড় বিলম্ব: ৫.২ দিন।",
            severity="warning", category="supply_chain",
            metric_value="5.2 days avg", icon="Truck",
            action_url="/inventory/suppliers",
        ),
        AIInsight(
            id="insight_5", title="Sales Peak Pattern Detected",
            title_bn="বিক্রয় শীর্ষ প্যাটার্ন",
            description="Sales consistently peak on Friday afternoons (2-6 PM) and Saturday mornings. Consider increasing staff and inventory during these periods for optimal conversion.",
            description_bn="বিক্রয় নিয়মিতভাবে শুক্রবার বিকেলে (২-৬ PM) এবং শনিবার সকালে সর্বোচ্চ হয়।",
            severity="info", category="sales",
            metric_value="Fri-Sat Peak", icon="BarChart3",
            action_url="/sales/analytics",
        ),
        AIInsight(
            id="insight_6", title="Marketing ROI Improvement",
            title_bn="বিপণন ROI উন্নতি",
            description="Marketing ROI improved by 18.3% this quarter. Social media campaigns generated 340 new leads, with a conversion rate of 12.4%. Digital ads outperform traditional channels by 3.2x.",
            description_bn="এই প্রান্তিকে বিপণন ROI ১৮.৩% উন্নতি হয়েছে। সোশ্যাল মিডিয়া ক্যাম্পেইন ৩৪০টি নতুন লিড তৈরি করেছে।",
            severity="success", category="marketing",
            metric_value="+18.3%", icon="Megaphone",
            action_url="/crm/leads",
        ),
    ]


def _get_demo_activities() -> List[ActivityItem]:
    """Generate demo activity feed."""
    now = datetime.now(timezone.utc)
    return [
        ActivityItem(
            id="act_1", title="New Invoice Uploaded",
            title_bn="নতুন চালান আপলোড করা হয়েছে",
            description="Invoice #INV-2024-0847 from Rahman Enterprise — ৳125,000",
            type="invoice", icon="FileText",
            timestamp=now - timedelta(minutes=12),
            user_name="Fatima Begum",
        ),
        ActivityItem(
            id="act_2", title="Monthly Report Generated",
            title_bn="মাসিক প্রতিবেদন তৈরি হয়েছে",
            description="May 2024 Executive Summary report has been generated successfully",
            type="report", icon="FileBarChart",
            timestamp=now - timedelta(minutes=45),
            user_name="System",
        ),
        ActivityItem(
            id="act_3", title="New Customer Registered",
            title_bn="নতুন গ্রাহক নিবন্ধিত",
            description="ABC Trading Co. (মোঃ করিম ট্রেডিং) — Enterprise segment",
            type="customer", icon="UserPlus",
            timestamp=now - timedelta(hours=1),
            user_name="Karim Ahmed",
        ),
        ActivityItem(
            id="act_4", title="Low Stock Alert",
            title_bn="মজুদ কম সতর্কতা",
            description="Product 'Wireless Mouse MX-200' stock below reorder level (8 remaining)",
            type="stock", icon="AlertTriangle",
            timestamp=now - timedelta(hours=2),
            user_name="System",
        ),
        ActivityItem(
            id="act_5", title="Bulk Import Completed",
            title_bn="বাল্ক ইমপোর্ট সম্পন্ন",
            description="Successfully imported 156 product records from CSV file",
            type="import", icon="Upload",
            timestamp=now - timedelta(hours=3),
            user_name="Rahul Hasan",
        ),
        ActivityItem(
            id="act_6", title="Order Delivered",
            title_bn="অর্ডার বিতরণ করা হয়েছে",
            description="Order #ORD-2024-1234 delivered to Dhaka — ৳85,500",
            type="order", icon="CheckCircle",
            timestamp=now - timedelta(hours=4),
            user_name="Delivery System",
        ),
        ActivityItem(
            id="act_7", title="Payment Received",
            title_bn="পেমেন্ট গৃহীত",
            description="Invoice #INV-2024-0839 — ৳250,000 received via bank transfer",
            type="payment", icon="Banknote",
            timestamp=now - timedelta(hours=5),
            user_name="Finance System",
        ),
        ActivityItem(
            id="act_8", title="OCR Processing Complete",
            title_bn="OCR প্রক্রিয়াকরণ সম্পন্ন",
            description="3 invoices processed with 94.2% average confidence score",
            type="processing", icon="Scan",
            timestamp=now - timedelta(hours=6),
            user_name="OCR System",
        ),
    ]


# ── Endpoints ─────────────────────────────────────────────────────
@router.get(
    "/overview",
    response_model=SuccessResponse[DashboardResponse],
    summary="Get complete dashboard overview",
)
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
):
    """Get all dashboard data including KPIs, charts, insights, and activities."""
    dashboard = DashboardResponse(
        kpis=_get_demo_kpis(),
        charts=_get_demo_charts(),
        insights=_get_demo_insights(),
        activities=_get_demo_activities(),
        summary={
            "total_revenue": 28450000,
            "total_expenses": 18200000,
            "net_profit": 10250000,
            "profit_margin": 36.0,
            "total_customers": 1247,
            "active_orders": 89,
            "pending_invoices": 34,
            "low_stock_items": 7,
        },
    )
    return SuccessResponse(data=dashboard)


@router.get(
    "/kpis",
    response_model=SuccessResponse[List[KPICard]],
    summary="Get KPI cards data",
)
async def get_kpis(
    current_user: User = Depends(get_current_user),
):
    """Get all KPI card data for the dashboard."""
    return SuccessResponse(data=_get_demo_kpis())


@router.get(
    "/charts/{chart_id}",
    response_model=SuccessResponse[ChartData],
    summary="Get specific chart data",
)
async def get_chart_data(
    chart_id: str,
    period: str = Query(default="12m", regex="^(1m|3m|6m|12m|ytd|all)$"),
    current_user: User = Depends(get_current_user),
):
    """Get data for a specific chart."""
    charts = {c.id: c for c in _get_demo_charts()}
    chart = charts.get(chart_id)
    if not chart:
        from src.common.exceptions import NotFoundError
        raise NotFoundError("Chart", chart_id)
    return SuccessResponse(data=chart)


@router.get(
    "/insights",
    response_model=SuccessResponse[List[AIInsight]],
    summary="Get AI business insights",
)
async def get_insights(
    current_user: User = Depends(get_current_user),
):
    """Get AI-generated business insights and recommendations."""
    return SuccessResponse(data=_get_demo_insights())


@router.get(
    "/activities",
    response_model=SuccessResponse[List[ActivityItem]],
    summary="Get recent activity feed",
)
async def get_activities(
    limit: int = Query(default=20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
):
    """Get recent activity feed items."""
    return SuccessResponse(data=_get_demo_activities()[:limit])
