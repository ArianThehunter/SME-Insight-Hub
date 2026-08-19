<!--
  Documents Upload — Drag-and-drop file uploader for PDFs, images, CSV, and Excel.
  Users can upload business documents for OCR extraction or bulk data import via CSV templates.
-->
<script lang="ts">
	import {
		Upload,
		FileText,
		File as FileIcon,
		Image,
		Table2,
		Download,
		CheckCircle2,
		AlertCircle,
		Loader2,
		X,
		Plus
	} from '@lucide/svelte';
	import { api } from '$lib/services/api';
	import { authStore } from '$lib/stores/auth.svelte';

	type UploadStatus = 'idle' | 'uploading' | 'success' | 'error';

	interface UploadedFile {
		id: string;
		name: string;
		size: number;
		type: string;
		status: UploadStatus;
		error?: string;
		docId?: string;
	}

	let dragOver = $state(false);
	let files = $state<UploadedFile[]>([]);
	let selectedDocType = $state('other');
	let fileInput: HTMLInputElement;

	const docTypes = [
		{ value: 'invoice', label: 'Invoice' },
		{ value: 'receipt', label: 'Receipt' },
		{ value: 'bank_statement', label: 'Bank Statement' },
		{ value: 'purchase_order', label: 'Purchase Order' },
		{ value: 'financial_statement', label: 'Financial Statement' },
		{ value: 'utility_bill', label: 'Utility Bill' },
		{ value: 'other', label: 'Other Document' }
	];

	const templates = [
		{ type: 'customers', label: 'Customers', icon: '👥', desc: 'Customer list with contact info' },
		{
			type: 'products',
			label: 'Products',
			icon: '📦',
			desc: 'Product catalog with SKU, price, stock'
		},
		{ type: 'orders', label: 'Orders', icon: '🛒', desc: 'Sales orders with line items' },
		{ type: 'expenses', label: 'Expenses', icon: '💸', desc: 'Business expenses by category' },
		{
			type: 'invoices',
			label: 'Invoices',
			icon: '🧾',
			desc: 'Customer invoices and payment status'
		},
		{ type: 'suppliers', label: 'Suppliers', icon: '🏭', desc: 'Supplier contact and rating info' }
	];

	function formatSize(bytes: number): string {
		if (bytes < 1024) return `${bytes} B`;
		if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
		return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
	}

	function getFileIcon(type: string) {
		if (type.includes('pdf')) return FileText;
		if (type.includes('image')) return Image;
		if (type.includes('csv') || type.includes('sheet')) return Table2;
		return FileIcon;
	}

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		dragOver = false;
		if (e.dataTransfer?.files) processFiles(e.dataTransfer.files);
	}

	function handleFileInput(e: Event) {
		const input = e.target as HTMLInputElement;
		if (input.files) processFiles(input.files);
	}

	function processFiles(fileList: FileList) {
		Array.from(fileList).forEach((file) => {
			const uploadFile: UploadedFile = {
				id: crypto.randomUUID(),
				name: file.name,
				size: file.size,
				type: file.type,
				status: 'uploading'
			};
			files = [...files, uploadFile];
			uploadFile_(uploadFile.id, file);
		});
	}

	async function uploadFile_(id: string, file: File) {
		const formData = new FormData();
		formData.append('file', file);
		formData.append('document_type', selectedDocType);

		try {
			const res = await fetch(
				`${import.meta.env.PUBLIC_API_URL || '/api/v1'}/documents/upload?document_type=${selectedDocType}`,
				{
					method: 'POST',
					headers: {
						Authorization: `Bearer ${localStorage.getItem('sme-access-token') || ''}`
					},
					body: formData
				}
			);

			if (!res.ok) {
				const err = await res.json();
				throw new Error(err.detail || 'Upload failed');
			}

			const json = await res.json();
			files = files.map((f) =>
				f.id === id ? { ...f, status: 'success', docId: json.data?.id } : f
			);
		} catch (err: any) {
			files = files.map((f) => (f.id === id ? { ...f, status: 'error', error: err.message } : f));
		}
	}

	function removeFile(id: string) {
		files = files.filter((f) => f.id !== id);
	}

	async function downloadTemplate(type: string) {
		const token = localStorage.getItem('sme-access-token') || '';
		const base = import.meta.env.PUBLIC_API_URL || '/api/v1';
		window.open(`${base}/documents/templates/${type}?token=${token}`, '_blank');
	}
</script>

<svelte:head>
	<title>Upload Documents — SME Insight Hub</title>
	<meta
		name="description"
		content="Upload PDF invoices, receipts, and bank statements for AI extraction. Or import your data in bulk via CSV templates."
	/>
</svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Document Upload</h1>
			<p class="page-subtitle">
				Upload invoices, receipts, or bank statements for AI extraction — or import bulk data via
				CSV
			</p>
		</div>
	</header>

	<div class="upload-grid">
		<!-- ── Left: File Upload ──────────────────────────── -->
		<div class="upload-panel card">
			<h2 class="section-title">Upload Documents</h2>
			<p class="section-desc">PDFs, images, CSV and Excel files accepted. Max 50MB per file.</p>

			<!-- Document type selector -->
			<div class="doc-type-row">
				<label class="field-label" for="doc-type">Document Type</label>
				<select id="doc-type" class="type-select" bind:value={selectedDocType}>
					{#each docTypes as dt}
						<option value={dt.value}>{dt.label}</option>
					{/each}
				</select>
			</div>

			<!-- Drop zone -->
			<button
				class="drop-zone"
				class:drag-over={dragOver}
				ondragover={(e) => {
					e.preventDefault();
					dragOver = true;
				}}
				ondragleave={() => (dragOver = false)}
				ondrop={handleDrop}
				onclick={() => fileInput.click()}
				type="button"
				aria-label="Click or drag files to upload"
			>
				<div class="drop-icon">
					<Upload size={32} />
				</div>
				<p class="drop-title">Drop files here or <span class="drop-link">browse</span></p>
				<p class="drop-hint">PDF, PNG, JPG, CSV, XLSX — max 50MB</p>
				<input
					bind:this={fileInput}
					type="file"
					multiple
					accept=".pdf,.png,.jpg,.jpeg,.csv,.xlsx,.xls"
					onchange={handleFileInput}
					style="display:none"
					aria-hidden="true"
				/>
			</button>

			<!-- File list -->
			{#if files.length > 0}
				<div class="file-list">
					{#each files as file (file.id)}
						{@const DocIcon = getFileIcon(file.type)}
						<div
							class="file-item"
							class:success={file.status === 'success'}
							class:error={file.status === 'error'}
						>
							<div class="file-icon">
								<DocIcon size={18} />
							</div>
							<div class="file-info">
								<span class="file-name">{file.name}</span>
								<span class="file-meta">{formatSize(file.size)}</span>
							</div>
							<div class="file-status">
								{#if file.status === 'uploading'}
									<Loader2 size={16} class="spinning" />
								{:else if file.status === 'success'}
									<CheckCircle2 size={16} class="text-success" />
									{#if file.docId}
										<a href="/documents/ocr" class="process-link">Process OCR →</a>
									{/if}
								{:else if file.status === 'error'}
									<AlertCircle size={16} class="text-danger" />
									<span class="error-msg">{file.error}</span>
								{/if}
							</div>
							<button
								class="remove-btn"
								onclick={() => removeFile(file.id)}
								aria-label="Remove file"
							>
								<X size={14} />
							</button>
						</div>
					{/each}
				</div>
			{/if}
		</div>

		<!-- ── Right: CSV Templates ───────────────────────── -->
		<div class="templates-panel">
			<div class="card">
				<h2 class="section-title">Bulk Import via CSV</h2>
				<p class="section-desc">
					Download a template, fill it with your data, then upload it as a CSV or Excel file.
				</p>

				<div class="template-list">
					{#each templates as tmpl}
						<div class="template-item">
							<div class="tmpl-icon">{tmpl.icon}</div>
							<div class="tmpl-info">
								<span class="tmpl-name">{tmpl.label}</span>
								<span class="tmpl-desc">{tmpl.desc}</span>
							</div>
							<button
								class="tmpl-btn"
								onclick={() => downloadTemplate(tmpl.type)}
								title="Download {tmpl.label} template"
							>
								<Download size={14} />
								<span>Template</span>
							</button>
						</div>
					{/each}
				</div>

				<div class="import-note">
					<AlertCircle size={14} />
					<p>
						After downloading the template, fill it with your data and upload it using the uploader
						on the left. Select the matching document type.
					</p>
				</div>
			</div>

			<div class="card guidelines-card">
				<h2 class="section-title">Data Guidelines</h2>
				<ul class="guidelines-list">
					<li>Use <strong>UTF-8 encoding</strong> for Bangla text support</li>
					<li>Dates in <strong>YYYY-MM-DD</strong> format (e.g. 2026-08-01)</li>
					<li>All monetary amounts in <strong>BDT (Taka)</strong>, no currency symbols</li>
					<li>Phone numbers: <strong>+8801XXXXXXXXX</strong> or <strong>01XXXXXXXXX</strong></li>
					<li>Max <strong>50MB</strong> per file, max <strong>10,000 rows</strong> per CSV</li>
					<li>First row must be the <strong>header row</strong> (exactly as in template)</li>
				</ul>
			</div>
		</div>
	</div>
</div>

<style>
	.page-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
		letter-spacing: -0.02em;
	}
	.page-subtitle {
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
		margin: 4px 0 0;
	}

	.upload-grid {
		display: grid;
		grid-template-columns: 1fr 380px;
		gap: 20px;
		align-items: start;
	}

	@media (max-width: 900px) {
		.upload-grid {
			grid-template-columns: 1fr;
		}
	}

	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 20px;
	}

	.section-title {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0 0 4px;
	}
	.section-desc {
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
		margin: 0 0 16px;
	}

	/* ── Doc type selector ────────── */
	.doc-type-row {
		margin-bottom: 16px;
	}
	.field-label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		display: block;
		margin-bottom: 6px;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}
	.type-select {
		width: 100%;
		padding: 8px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: 0.875rem;
	}

	/* ── Drop zone ────────────────── */
	.drop-zone {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 8px;
		padding: 48px 24px;
		border: 2px dashed var(--color-border);
		border-radius: var(--radius-lg);
		cursor: pointer;
		transition: all 0.2s;
		background: var(--color-bg-primary);
		width: 100%;
		text-align: center;
	}

	.drop-zone:hover,
	.drop-zone.drag-over {
		border-color: var(--color-accent);
		background: color-mix(in srgb, var(--color-accent) 5%, transparent);
	}

	.drop-icon {
		color: var(--color-accent);
		opacity: 0.7;
		margin-bottom: 4px;
	}
	.drop-title {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
	}
	.drop-link {
		color: var(--color-accent);
	}
	.drop-hint {
		font-size: 0.75rem;
		color: var(--color-text-tertiary);
		margin: 0;
	}

	/* ── File list ─────────────────── */
	.file-list {
		margin-top: 16px;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.file-item {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 10px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		transition: border-color 0.2s;
	}
	.file-item.success {
		border-color: var(--color-success);
	}
	.file-item.error {
		border-color: var(--color-danger);
	}

	.file-icon {
		color: var(--color-text-secondary);
		flex-shrink: 0;
	}
	.file-info {
		flex: 1;
		min-width: 0;
	}
	.file-name {
		font-size: 0.8125rem;
		font-weight: 500;
		color: var(--color-text-primary);
		display: block;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.file-meta {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.file-status {
		display: flex;
		align-items: center;
		gap: 6px;
		flex-shrink: 0;
	}

	:global(.text-success) {
		color: var(--color-success);
	}
	:global(.text-danger) {
		color: var(--color-danger);
	}
	:global(.spinning) {
		animation: spin 1s linear infinite;
	}

	.process-link {
		font-size: 0.75rem;
		color: var(--color-accent);
		text-decoration: none;
		font-weight: 600;
	}
	.error-msg {
		font-size: 0.6875rem;
		color: var(--color-danger);
		max-width: 120px;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.remove-btn {
		background: none;
		border: none;
		cursor: pointer;
		padding: 2px;
		color: var(--color-text-tertiary);
		transition: color 0.15s;
		display: flex;
		align-items: center;
		flex-shrink: 0;
	}
	.remove-btn:hover {
		color: var(--color-danger);
	}

	/* ── Templates ────────────────── */
	.templates-panel {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.template-list {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.template-item {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 10px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
	}
	.tmpl-icon {
		font-size: 1.25rem;
		flex-shrink: 0;
	}
	.tmpl-info {
		flex: 1;
	}
	.tmpl-name {
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--color-text-primary);
		display: block;
	}
	.tmpl-desc {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.tmpl-btn {
		display: flex;
		align-items: center;
		gap: 4px;
		padding: 5px 10px;
		background: var(--color-accent);
		color: white;
		border: none;
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		white-space: nowrap;
		transition: opacity 0.2s;
		flex-shrink: 0;
	}
	.tmpl-btn:hover {
		opacity: 0.85;
	}

	.import-note {
		display: flex;
		align-items: flex-start;
		gap: 8px;
		margin-top: 16px;
		padding: 10px 12px;
		background: color-mix(in srgb, var(--color-accent) 8%, transparent);
		border: 1px solid color-mix(in srgb, var(--color-accent) 25%, transparent);
		border-radius: var(--radius-md);
		color: var(--color-text-secondary);
		font-size: 0.75rem;
		line-height: 1.5;
	}
	.import-note p {
		margin: 0;
	}

	.guidelines-card .guidelines-list {
		margin: 0;
		padding-left: 16px;
		display: flex;
		flex-direction: column;
		gap: 8px;
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
		line-height: 1.5;
	}
	.guidelines-list li strong {
		color: var(--color-text-primary);
	}
</style>
