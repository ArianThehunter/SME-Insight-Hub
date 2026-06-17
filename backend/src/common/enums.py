"""
Shared enumerations used across the application.
"""

from enum import Enum


class UserRole(str, Enum):
    """User roles with hierarchical permissions."""
    SUPER_ADMIN = "super_admin"
    ORG_OWNER = "org_owner"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"
    SALES_OFFICER = "sales_officer"
    INVENTORY_OFFICER = "inventory_officer"
    VIEWER = "viewer"


class DocumentStatus(str, Enum):
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


class DocumentType(str, Enum):
    """Types of documents that can be uploaded."""
    INVOICE = "invoice"
    RECEIPT = "receipt"
    PURCHASE_ORDER = "purchase_order"
    FINANCIAL_STATEMENT = "financial_statement"
    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"
    OTHER = "other"


class OrderStatus(str, Enum):
    """Sales order statuses."""
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class InvoiceStatus(str, Enum):
    """Invoice payment statuses."""
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    VOID = "void"


class StockMovementType(str, Enum):
    """Types of inventory stock movements."""
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"
    WRITE_OFF = "write_off"


class LeadStatus(str, Enum):
    """CRM lead pipeline statuses."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class CustomerSegment(str, Enum):
    """Customer segmentation categories."""
    ENTERPRISE = "enterprise"
    MID_MARKET = "mid_market"
    SMALL_BUSINESS = "small_business"
    STARTUP = "startup"
    INDIVIDUAL = "individual"


class Currency(str, Enum):
    """Supported currencies."""
    BDT = "BDT"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class ReportType(str, Enum):
    """Report generation types."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    CUSTOM = "custom"


class ReportFormat(str, Enum):
    """Report export formats."""
    PDF = "pdf"
    CSV = "csv"
    EXCEL = "excel"


class AuditAction(str, Enum):
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
