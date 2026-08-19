"""
Unit tests for Document processing domain and supported MIME types.
"""

from src.common.enums import DocumentStatus, DocumentType
from src.documents.router import ALLOWED_TYPES


def test_allowed_document_types():
    """Verify supported document upload formats."""
    assert "application/pdf" in ALLOWED_TYPES
    assert "image/png" in ALLOWED_TYPES
    assert "image/jpeg" in ALLOWED_TYPES
    assert "text/csv" in ALLOWED_TYPES
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in ALLOWED_TYPES


def test_document_enums():
    """Verify document lifecycle status enums."""
    assert DocumentStatus.UPLOADED.value == "uploaded"
    assert DocumentStatus.PROCESSING.value == "processing"
    assert DocumentStatus.OCR_COMPLETE.value == "ocr_complete"
    assert DocumentType.INVOICE.value == "invoice"
    assert DocumentType.RECEIPT.value == "receipt"
