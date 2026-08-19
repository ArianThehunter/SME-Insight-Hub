<!--
  OCR Processing — View and manage document processing status.
  Shows documents queued or in OCR extraction pipeline.
-->
<script lang="ts">
	import { ScanLine, Loader2, CheckCircle2, AlertCircle, Clock, FileText, RefreshCw, Play } from '@lucide/svelte';

	// Mock data while API is being connected
	const demoDocuments = [
		{ id: '1', name: 'INV-2026-0847.pdf', type: 'invoice', status: 'completed', confidence: 0.96, processed: '10 min ago', size: '1.2 MB' },
		{ id: '2', name: 'BRAC_Bank_Statement_Jul.pdf', type: 'bank_statement', status: 'processing', confidence: null, processed: 'In progress...', size: '3.4 MB' },
		{ id: '3', name: 'Purchase_Order_RMG.pdf', type: 'purchase_order', status: 'queued', confidence: null, processed: 'Queued', size: '0.8 MB' },
		{ id: '4', name: 'Utility_Bill_DESCO.jpg', type: 'utility_bill', status: 'review_needed', confidence: 0.61, processed: '1 hour ago', size: '0.5 MB' },
		{ id: '5', name: 'Receipt_Bashundhara.jpg', type: 'receipt', status: 'completed', confidence: 0.91, processed: '2 hours ago', size: '0.3 MB' },
		{ id: '6', name: 'Invoice_Chittagong_Port.pdf', type: 'invoice', status: 'failed', confidence: null, processed: '3 hours ago', size: '2.1 MB' },
	];

	const statusConfig: Record<string, { label: string; color: string; icon: any }> = {
		completed: { label: 'Completed', color: 'success', icon: CheckCircle2 },
		processing: { label: 'Processing', color: 'accent', icon: Loader2 },
		queued: { label: 'Queued', color: 'warning', icon: Clock },
		review_needed: { label: 'Review Needed', color: 'warning', icon: AlertCircle },
		failed: { label: 'Failed', color: 'danger', icon: AlertCircle },
		uploaded: { label: 'Uploaded', color: 'info', icon: FileText },
	};

	function getConfidenceClass(score: number | null) {
		if (!score) return '';
		if (score >= 0.85) return 'high';
		if (score >= 0.7) return 'medium';
		return 'low';
	}
</script>

<svelte:head>
	<title>OCR Processing — SME Insight Hub</title>
</svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">OCR Processing</h1>
			<p class="page-subtitle">AI-powered extraction from uploaded documents</p>
		</div>
		<div class="header-actions">
			<button class="btn-secondary">
				<RefreshCw size={15} />
				Refresh
			</button>
			<a href="/documents/upload" class="btn-primary">
				<ScanLine size={15} />
				Upload New
			</a>
		</div>
	</header>

	<!-- Stats row -->
	<div class="stats-row">
		{#each [
			{ label: 'Total Processed', value: '247', color: 'accent' },
			{ label: 'Completed', value: '231', color: 'success' },
			{ label: 'Queued', value: '8', color: 'warning' },
			{ label: 'Failed', value: '8', color: 'danger' },
		] as stat}
			<div class="stat-card">
				<span class="stat-value" style="color: var(--color-{stat.color})">{stat.value}</span>
				<span class="stat-label">{stat.label}</span>
			</div>
		{/each}
	</div>

	<!-- Document table -->
	<div class="card">
		<table class="doc-table">
			<thead>
				<tr>
					<th>Document</th>
					<th>Type</th>
					<th>Status</th>
					<th>Confidence</th>
					<th>Processed</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				{#each demoDocuments as doc}
					{@const cfg = statusConfig[doc.status] ?? statusConfig.uploaded}
					{@const StatusIcon = cfg.icon}
					<tr>
						<td>
							<div class="doc-name">
								<FileText size={15} />
								<div>
									<span class="name">{doc.name}</span>
									<span class="size">{doc.size}</span>
								</div>
							</div>
						</td>
						<td><span class="type-badge">{doc.type.replace(/_/g, ' ')}</span></td>
						<td>
							<span class="status-badge status-{cfg.color}">
								<StatusIcon size={12} class={doc.status === 'processing' ? 'spinning' : ''} />
								{cfg.label}
							</span>
						</td>
						<td>
							{#if doc.confidence}
								<div class="confidence">
									<div class="confidence-bar">
										<div class="confidence-fill {getConfidenceClass(doc.confidence)}" style="width:{doc.confidence * 100}%"></div>
									</div>
									<span class="confidence-val">{Math.round(doc.confidence * 100)}%</span>
								</div>
							{:else}
								<span class="text-muted">—</span>
							{/if}
						</td>
						<td class="text-muted">{doc.processed}</td>
						<td>
							<div class="row-actions">
								{#if doc.status === 'uploaded' || doc.status === 'failed'}
									<button class="action-btn accent" title="Start OCR">
										<Play size={13} />
									</button>
								{/if}
								<a href="/documents/parsed" class="action-btn" title="View results">
									<FileText size={13} />
								</a>
							</div>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.header-actions { display: flex; gap: 8px; }

	.btn-primary, .btn-secondary {
		display: inline-flex; align-items: center; gap: 6px;
		padding: 7px 14px; border-radius: var(--radius-md);
		font-size: 0.8125rem; font-weight: 600; cursor: pointer;
		border: none; text-decoration: none; transition: opacity 0.15s;
	}
	.btn-primary { background: var(--color-accent); color: white; }
	.btn-secondary { background: var(--color-bg-secondary); color: var(--color-text-primary); border: 1px solid var(--color-border); }
	.btn-primary:hover, .btn-secondary:hover { opacity: 0.85; }

	.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
	.stat-card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 16px;
		display: flex; flex-direction: column; gap: 2px;
	}
	.stat-value { font-size: 1.5rem; font-weight: 700; font-variant-numeric: tabular-nums; }
	.stat-label { font-size: 0.75rem; color: var(--color-text-secondary); }

	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden; }

	.doc-table { width: 100%; border-collapse: collapse; }
	.doc-table th {
		padding: 10px 14px;
		text-align: left;
		font-size: 0.6875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--color-text-tertiary);
		border-bottom: 1px solid var(--color-border);
		background: var(--color-bg-primary);
	}
	.doc-table td { padding: 12px 14px; border-bottom: 1px solid var(--color-border); }
	.doc-table tr:last-child td { border-bottom: none; }
	.doc-table tr:hover td { background: var(--color-bg-primary); }

	.doc-name { display: flex; align-items: center; gap: 8px; color: var(--color-text-secondary); }
	.doc-name .name { font-size: 0.8125rem; font-weight: 500; color: var(--color-text-primary); display: block; }
	.doc-name .size { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.type-badge { font-size: 0.6875rem; padding: 2px 8px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: 999px; color: var(--color-text-secondary); white-space: nowrap; text-transform: capitalize; }

	.status-badge {
		display: inline-flex; align-items: center; gap: 4px;
		font-size: 0.6875rem; font-weight: 600; padding: 3px 8px;
		border-radius: 999px; white-space: nowrap;
	}
	.status-success { background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.status-accent { background: color-mix(in srgb, var(--color-accent) 15%, transparent); color: var(--color-accent); }
	.status-warning { background: color-mix(in srgb, #f59e0b 15%, transparent); color: #d97706; }
	.status-danger { background: color-mix(in srgb, var(--color-danger) 15%, transparent); color: var(--color-danger); }
	.status-info { background: color-mix(in srgb, #38bdf8 15%, transparent); color: #0ea5e9; }

	:global(.spinning) { animation: spin 1s linear infinite; }

	.confidence { display: flex; align-items: center; gap: 8px; }
	.confidence-bar { width: 60px; height: 4px; background: var(--color-border); border-radius: 999px; overflow: hidden; }
	.confidence-fill { height: 100%; border-radius: 999px; }
	.confidence-fill.high { background: var(--color-success); }
	.confidence-fill.medium { background: #f59e0b; }
	.confidence-fill.low { background: var(--color-danger); }
	.confidence-val { font-size: 0.6875rem; font-weight: 600; color: var(--color-text-primary); }

	.text-muted { color: var(--color-text-tertiary); font-size: 0.8125rem; }

	.row-actions { display: flex; gap: 6px; }
	.action-btn {
		display: flex; align-items: center; justify-content: center;
		width: 28px; height: 28px;
		background: var(--color-bg-primary); border: 1px solid var(--color-border);
		border-radius: var(--radius-sm); cursor: pointer;
		color: var(--color-text-secondary); text-decoration: none;
		transition: all 0.15s;
	}
	.action-btn:hover { border-color: var(--color-accent); color: var(--color-accent); }
	.action-btn.accent { background: var(--color-accent); color: white; border-color: var(--color-accent); }
</style>
