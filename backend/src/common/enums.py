"""
Shared enumerations used across the application.
"""

from enum import StrEnum


class UserRole(StrEnum):
    """User roles with hierarchical permissions."""
    SUPER_ADMIN = "super_admin"
    ORG_OWNER = "org_owner"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"
    SALES_OFFICER = "sales_officer"
    INVENTORY_OFFICER = "inventory_officer"
    VIEWER = "viewer"


class DocumentStatus(StrEnum):
    """Document processing pipeline statuses."""
    UPLOADED = "uploaded"
    QUEUED = "queued"
    PROCESSING = "processing"
    OCR_COMPLETE = "ocr_complete"
    EXTRACTING = "extracting"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    REVIEW_NEEDED = "review_needed"


class DocumentType(StrEnum):
    """Types of documents that can be uploaded."""
    INVOICE = "invoice"
    RECEIPT = "receipt"
    PURCHASE_ORDER = "purchase_order"
    FINANCIAL_STATEMENT = "financial_statement"
    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"
    OTHER = "other"


class OrderStatus(StrEnum):
    """Sales order statuses."""
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class InvoiceStatus(StrEnum):
    """Invoice payment statuses."""
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    VOID = "void"


class StockMovementType(StrEnum):
    """Types of inventory stock movements."""
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"
    WRITE_OFF = "write_off"


class LeadStatus(StrEnum):
    """CRM lead pipeline statuses."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class CustomerSegment(StrEnum):
    """Customer segmentation categories."""
    ENTERPRISE = "enterprise"
    MID_MARKET = "mid_market"
    SMALL_BUSINESS = "small_business"
    STARTUP = "startup"
    INDIVIDUAL = "individual"


class Currency(StrEnum):
    """Supported currencies."""
    BDT = "BDT"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class ReportType(StrEnum):
    """Report generation types."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    CUSTOM = "custom"


class ReportFormat(StrEnum):
    """Report export formats."""
    PDF = "pdf"
    CSV = "csv"
    EXCEL = "excel"


class AuditAction(StrEnum):
    """Audit trail action types."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    UPLOAD = "upload"
    PROCESS = "process"
