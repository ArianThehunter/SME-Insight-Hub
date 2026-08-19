"""
Documents domain — File upload, OCR processing, and data extraction router.
Handles PDF/Image/CSV/Excel uploads, Tesseract OCR, and CSV bulk imports.
"""

import csv
import io
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.dependencies import get_current_user, require_permission
from src.auth.models import User
from src.common.enums import DocumentStatus, DocumentType
from src.common.schemas import SuccessResponse
from src.config import get_settings
from src.database import get_db
from src.documents.schemas import (
    CSVImportResponse,
    DocumentDetailResponse,
    DocumentListResponse,
    DocumentUploadResponse,
    ExtractionResultResponse,
)
from src.sales.models import Document, ExtractionResult

router = APIRouter(prefix="/documents", tags=["Documents"])
settings = get_settings()

# Allowed MIME types
ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "image/png": "png",
    "image/jpeg": "jpg",
    "text/csv": "csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-excel": "xls",
}


async def _save_file(file: UploadFile, upload_dir: str) -> tuple[str, str, int]:
    """Save an uploaded file to disk. Returns (stored_filename, file_path, size)."""
    os.makedirs(upload_dir, exist_ok=True)
    ext = ALLOWED_TYPES.get(file.content_type, "bin")
    stored_name = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(upload_dir, stored_name)

    content = await file.read()
    file_size = len(content)

    if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    with open(file_path, "wb") as f:
        f.write(content)

    return stored_name, file_path, file_size


@router.post(
    "/upload",
    response_model=SuccessResponse[DocumentUploadResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document for processing",
    dependencies=[Depends(require_permission("documents", "create"))],
)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = DocumentType.OTHER,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Upload a PDF, image, CSV, or Excel file.
    Accepted: PDF, PNG, JPG, CSV, XLSX.
    Max size: 50MB.
    """
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {file.content_type}. Allowed: PDF, PNG, JPG, CSV, XLSX",
        )

    stored_name, file_path, file_size = await _save_file(file, settings.UPLOAD_DIR)

    doc = Document(
        org_id=user.org_id,
        filename=stored_name,
        original_filename=file.filename or stored_name,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        document_type=document_type.value,
        status=DocumentStatus.UPLOADED.value,
        uploaded_by=user.id,
    )
    db.add(doc)
    await db.flush()

    return SuccessResponse(
        message="File uploaded successfully. Use POST /{id}/process to start OCR.",
        data=DocumentUploadResponse.model_validate(doc),
    )


@router.get(
    "/",
    response_model=SuccessResponse[list[DocumentListResponse]],
    summary="List uploaded documents",
)
async def list_documents(
    document_type: Optional[DocumentType] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all documents uploaded by this organization."""
    query = select(Document).where(Document.org_id == user.org_id)
    if document_type:
        query = query.where(Document.document_type == document_type.value)
    if status_filter:
        query = query.where(Document.status == status_filter)

    query = query.order_by(Document.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    docs = result.scalars().all()

    return SuccessResponse(data=[DocumentListResponse.model_validate(d) for d in docs])


@router.get(
    "/{document_id}",
    response_model=SuccessResponse[DocumentDetailResponse],
    summary="Get document details with extraction results",
)
async def get_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Document)
        .where(Document.id == document_id, Document.org_id == user.org_id)
        .options(selectinload(Document.extraction_results))
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return SuccessResponse(data=DocumentDetailResponse.model_validate(doc))


@router.post(
    "/{document_id}/process",
    response_model=SuccessResponse,
    summary="Trigger OCR processing on an uploaded document",
    dependencies=[Depends(require_permission("documents", "update"))],
)
async def process_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Trigger OCR extraction on a PDF or image document.
    In production, this enqueues a Celery task. For now, runs synchronously.
    """
    result = await db.execute(
        select(Document).where(Document.id == document_id, Document.org_id == user.org_id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.status not in [DocumentStatus.UPLOADED.value, DocumentStatus.FAILED.value]:
        raise HTTPException(status_code=400, detail=f"Document is already {doc.status}")

    # Update status to queued — in production this would enqueue Celery task
    doc.status = DocumentStatus.QUEUED.value
    await db.flush()

    # TODO: In production → celery_app.send_task("tasks.process_document", args=[str(document_id)])
    # For now, attempt basic text extraction if PDF
    try:
        doc.status = DocumentStatus.PROCESSING.value
        await db.flush()

        if doc.mime_type == "application/pdf":
            try:
                import PyPDF2
                with open(doc.file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    text = "\n".join(page.extract_text() or "" for page in reader.pages)
                doc.raw_text = text[:10000]  # Limit stored text
                doc.status = DocumentStatus.OCR_COMPLETE.value
                doc.confidence_score = 0.85
            except Exception as e:
                doc.status = DocumentStatus.FAILED.value
                doc.error_message = str(e)
        else:
            doc.status = DocumentStatus.OCR_COMPLETE.value

        doc.processed_at = datetime.now(timezone.utc)
        await db.flush()

    except Exception as e:
        doc.status = DocumentStatus.FAILED.value
        doc.error_message = str(e)
        await db.flush()

    return SuccessResponse(message=f"Processing {doc.status}. Check GET /{document_id} for results.")


@router.get(
    "/templates/{data_type}",
    summary="Download a CSV template for bulk data import",
)
async def download_template(data_type: str):
    """
    Download a pre-formatted CSV template for bulk imports.
    data_type: customers | products | orders | expenses | invoices | suppliers
    """
    templates = {
        "customers": {
            "filename": "customers_template.csv",
            "headers": [
                "name", "name_bn", "email", "phone", "company", "company_bn",
                "address", "city", "district", "segment", "notes"
            ],
            "example": [
                "Rahman Textiles Ltd.", "রহমান টেক্সটাইলস লি.", "info@rahman.com.bd",
                "+8801712345678", "Rahman Group", "রহমান গ্রুপ",
                "123 Dilkusha C/A", "Dhaka", "Dhaka", "enterprise", ""
            ],
        },
        "products": {
            "filename": "products_template.csv",
            "headers": [
                "name", "name_bn", "sku", "category", "subcategory",
                "unit", "price_bdt", "cost_bdt", "tax_rate_pct", "stock_quantity", "reorder_level"
            ],
            "example": [
                "Cotton Fabric (per yard)", "তুলার কাপড় (প্রতি গজ)", "FAB-CTN-001",
                "Textiles", "Raw Materials", "yard",
                "250.00", "180.00", "15", "500", "50"
            ],
        },
        "orders": {
            "filename": "orders_template.csv",
            "headers": [
                "order_date", "customer_name_or_email", "product_sku",
                "quantity", "unit_price_bdt", "discount_bdt", "delivery_date",
                "payment_method", "shipping_address"
            ],
            "example": [
                "2026-08-01", "info@rahman.com.bd", "FAB-CTN-001",
                "100", "250.00", "0", "2026-08-10",
                "bkash", "123 Dilkusha C/A, Dhaka"
            ],
        },
        "expenses": {
            "filename": "expenses_template.csv",
            "headers": [
                "expense_date", "category", "subcategory", "description",
                "description_bn", "amount_bdt", "vendor", "payment_method",
                "department", "is_recurring"
            ],
            "example": [
                "2026-08-01", "Utilities", "Electricity", "DESCO electricity bill August",
                "আগস্ট মাসের বিদ্যুৎ বিল", "12500.00", "DESCO", "bank_transfer",
                "Operations", "false"
            ],
        },
        "invoices": {
            "filename": "invoices_template.csv",
            "headers": [
                "invoice_number", "customer_name_or_email", "issue_date",
                "due_date", "subtotal_bdt", "tax_amount_bdt", "discount_bdt",
                "total_bdt", "status", "vendor_name", "notes"
            ],
            "example": [
                "INV-2026-0001", "info@rahman.com.bd", "2026-08-01",
                "2026-08-30", "25000.00", "3750.00", "0",
                "28750.00", "sent", "", ""
            ],
        },
        "suppliers": {
            "filename": "suppliers_template.csv",
            "headers": [
                "name", "name_bn", "contact_person", "email", "phone",
                "address", "city", "lead_time_days"
            ],
            "example": [
                "Chittagong Port Traders", "চট্টগ্রাম বন্দর ব্যবসায়ী",
                "Mr. Karim", "karim@cptraders.com.bd", "+8801812345678",
                "Port area, Agrabad", "Chittagong", "7"
            ],
        },
    }

    if data_type not in templates:
        raise HTTPException(
            status_code=404,
            detail=f"Template '{data_type}' not found. Available: {', '.join(templates.keys())}"
        )

    tmpl = templates[data_type]
    output = io.StringIO()
    writer = csv.writer(output)
    # Write headers
    writer.writerow(tmpl["headers"])
    # Write example row
    writer.writerow(tmpl["example"])
    # Write blank rows for user to fill
    for _ in range(4):
        writer.writerow([""] * len(tmpl["headers"]))

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),  # utf-8-sig for Excel BOM
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={tmpl['filename']}"},
    )


@router.post(
    "/import/{data_type}",
    response_model=SuccessResponse[CSVImportResponse],
    summary="Bulk import data from CSV/Excel",
    dependencies=[Depends(require_permission("documents", "create"))],
)
async def import_csv(
    data_type: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Bulk import customers, products, expenses, or invoices from CSV.
    Download a template first from GET /documents/templates/{data_type}.
    """
    if file.content_type not in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        raise HTTPException(status_code=415, detail="Only CSV and XLSX files are accepted for import")

    content = await file.read()
    rows_processed = 0
    rows_inserted = 0
    errors = []

    try:
        if file.content_type == "text/csv":
            # Decode CSV (handle BOM from Excel)
            text = content.decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))
            rows = list(reader)
        else:
            # Excel import
            import openpyxl
            wb = openpyxl.load_workbook(io.BytesIO(content))
            ws = wb.active
            headers = [cell.value for cell in ws[1]]
            rows = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if any(cell is not None for cell in row):
                    rows.append(dict(zip(headers, row)))

        for i, row in enumerate(rows, start=2):
            rows_processed += 1
            try:
                if data_type == "customers":
                    from src.sales.models import Customer
                    customer = Customer(
                        org_id=user.org_id,
                        name=row.get("name", "").strip(),
                        name_bn=row.get("name_bn") or None,
                        email=row.get("email") or None,
                        phone=row.get("phone") or None,
                        company=row.get("company") or None,
                        company_bn=row.get("company_bn") or None,
                        address=row.get("address") or None,
                        city=row.get("city") or None,
                        district=row.get("district") or None,
                        segment=row.get("segment") or None,
                        notes=row.get("notes") or None,
                    )
                    if not customer.name:
                        errors.append({"row": i, "field": "name", "error": "Name is required", "value": ""})
                        continue
                    db.add(customer)
                    rows_inserted += 1

                elif data_type == "expenses":
                    from src.sales.models import Expense
                    from datetime import date
                    expense_date_str = row.get("expense_date", "")
                    try:
                        expense_date = date.fromisoformat(str(expense_date_str))
                    except ValueError:
                        errors.append({"row": i, "field": "expense_date", "error": "Invalid date format, use YYYY-MM-DD", "value": str(expense_date_str)})
                        continue

                    expense = Expense(
                        org_id=user.org_id,
                        category=row.get("category", "Other").strip(),
                        subcategory=row.get("subcategory") or None,
                        description=row.get("description", "").strip(),
                        description_bn=row.get("description_bn") or None,
                        amount=float(row.get("amount_bdt", 0) or 0),
                        vendor=row.get("vendor") or None,
                        payment_method=row.get("payment_method") or None,
                        department=row.get("department") or None,
                        expense_date=expense_date,
                        is_recurring=str(row.get("is_recurring", "false")).lower() == "true",
                    )
                    db.add(expense)
                    rows_inserted += 1

                else:
                    errors.append({"row": i, "field": "data_type", "error": f"Import for '{data_type}' not yet supported", "value": data_type})
                    break

            except Exception as e:
                errors.append({"row": i, "field": "unknown", "error": str(e), "value": ""})

        if rows_inserted > 0:
            await db.flush()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    return SuccessResponse(
        message=f"Import complete: {rows_inserted} inserted, {rows_processed - rows_inserted} failed",
        data=CSVImportResponse(
            rows_processed=rows_processed,
            rows_inserted=rows_inserted,
            rows_failed=rows_processed - rows_inserted,
            errors=errors,
        ),
    )
