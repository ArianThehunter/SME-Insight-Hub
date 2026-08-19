"""
Documents domain — Pydantic schemas for file upload and OCR processing.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.common.enums import DocumentStatus, DocumentType
from src.common.schemas import BaseSchema, IDSchema


class DocumentUploadResponse(IDSchema):
    """Response after a file is uploaded."""
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    document_type: str
    status: str
    uploaded_by: uuid.UUID


class ExtractionResultResponse(BaseSchema):
    """Single extracted field from a document."""
    id: uuid.UUID
    field_name: str
    field_value: Optional[str] = None
    field_type: str
    confidence: float
    is_validated: bool
    validated_value: Optional[str] = None
    page_number: Optional[int] = None


class DocumentDetailResponse(IDSchema):
    """Detailed document with extraction results."""
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    document_type: str
    status: str
    confidence_score: Optional[float] = None
    uploaded_by: uuid.UUID
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    raw_text: Optional[str] = None
    extraction_results: List[ExtractionResultResponse] = []


class DocumentListResponse(BaseSchema):
    """Summary of a document for list views."""
    id: uuid.UUID
    original_filename: str
    document_type: str
    status: str
    file_size: int
    mime_type: str
    confidence_score: Optional[float] = None
    created_at: datetime
    processed_at: Optional[datetime] = None


class CSVImportResponse(BaseSchema):
    """Response after a CSV/Excel bulk import."""
    rows_processed: int
    rows_inserted: int
    rows_failed: int
    errors: List[Dict[str, Any]] = []


class CSVImportError(BaseSchema):
    """Details of a failed CSV import row."""
    row: int
    field: str
    error: str
    value: Optional[str] = None
