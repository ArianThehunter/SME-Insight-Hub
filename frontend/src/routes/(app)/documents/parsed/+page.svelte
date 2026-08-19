<!--
  Parsed Data — Review and validate extracted fields from processed documents.
-->
<script lang="ts">
	import { Database, CheckCircle2, AlertCircle, Edit3, Eye, Search, Filter } from '@lucide/svelte';

	let searchQuery = $state('');
	let selectedStatus = $state('all');

	const parsedDocs = [
		{
			id: '1',
			filename: 'INV-2026-0847.pdf',
			type: 'invoice',
			confidence: 0.96,
			fields: [
				{ name: 'Invoice Number', value: 'INV-2026-0847', confidence: 0.99, validated: true },
				{
					name: 'Vendor Name',
					value: 'Chittagong Port Traders',
					confidence: 0.95,
					validated: true
				},
				{ name: 'Issue Date', value: '2026-08-01', confidence: 0.98, validated: true },
				{ name: 'Due Date', value: '2026-08-30', confidence: 0.97, validated: true },
				{ name: 'Total Amount (BDT)', value: '৳ 2,85,000', confidence: 0.94, validated: true },
				{ name: 'VAT Amount', value: '৳ 37,174', confidence: 0.91, validated: false }
			]
		},
		{
			id: '2',
			filename: 'BRAC_Bank_Jul_2026.pdf',
			type: 'bank_statement',
			confidence: 0.89,
			fields: [
				{ name: 'Account Number', value: '1234567890', confidence: 0.99, validated: true },
				{ name: 'Statement Period', value: 'July 2026', confidence: 0.98, validated: true },
				{ name: 'Opening Balance', value: '৳ 8,45,230', confidence: 0.88, validated: true },
				{ name: 'Closing Balance', value: '৳ 12,37,850', confidence: 0.88, validated: false },
				{ name: 'Total Credits', value: '৳ 18,50,000', confidence: 0.85, validated: false },
				{ name: 'Total Debits', value: '৳ 14,57,380', confidence: 0.84, validated: false }
			]
		}
	];

	const filtered = $derived(
		parsedDocs.filter((d) => {
			const q = searchQuery.toLowerCase();
			return !q || d.filename.toLowerCase().includes(q) || d.type.includes(q);
		})
	);

	let selectedDoc = $state(parsedDocs[0]);
</script>

<svelte:head><title>Parsed Data — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Parsed Data</h1>
			<p class="page-subtitle">Review and validate AI-extracted fields from your documents</p>
		</div>
	</header>

	<div class="parsed-layout">
		<!-- Document list -->
		<div class="doc-list-panel card">
			<div class="search-box">
				<Search size={14} />
				<input
					type="text"
					placeholder="Search documents..."
					bind:value={searchQuery}
					class="search-input"
					aria-label="Search parsed documents"
				/>
			</div>
			<div class="doc-list">
				{#each filtered as doc}
					<button
						class="doc-list-item"
						class:active={selectedDoc.id === doc.id}
						onclick={() => (selectedDoc = doc)}
					>
						<div class="doc-thumb">📄</div>
						<div class="doc-list-info">
							<span class="doc-list-name">{doc.filename}</span>
							<div class="doc-list-meta">
								<span class="type-tag">{doc.type.replace(/_/g, ' ')}</span>
								<span class="conf-tag" class:high={doc.confidence >= 0.85}
									>{Math.round(doc.confidence * 100)}% conf.</span
								>
							</div>
						</div>
					</button>
				{/each}
			</div>
		</div>

		<!-- Field viewer -->
		<div class="field-panel card">
			{#if selectedDoc}
				<div class="field-header">
					<div>
						<h2 class="field-doc-name">{selectedDoc.filename}</h2>
						<span class="field-type">{selectedDoc.type.replace(/_/g, ' ')}</span>
					</div>
					<div class="field-actions">
						<button class="action-btn">
							<Edit3 size={13} />
							Edit All
						</button>
						<a href="/documents/export" class="action-btn accent"> Export CSV </a>
					</div>
				</div>

				<div class="fields-table">
					<div class="fields-row header">
						<span>Field</span>
						<span>Extracted Value</span>
						<span>Confidence</span>
						<span>Status</span>
					</div>
					{#each selectedDoc.fields as field}
						<div class="fields-row">
							<span class="field-name">{field.name}</span>
							<span class="field-value">{field.value}</span>
							<div class="conf-bar-wrap">
								<div class="mini-bar">
									<div
										class="mini-fill"
										class:high={field.confidence >= 0.85}
										class:medium={field.confidence >= 0.7 && field.confidence < 0.85}
										style="width:{field.confidence * 100}%"
									></div>
								</div>
								<span class="conf-pct">{Math.round(field.confidence * 100)}%</span>
							</div>
							<span
								class="validated-badge"
								class:ok={field.validated}
								class:pending={!field.validated}
							>
								{#if field.validated}
									<CheckCircle2 size={13} />
									Validated
								{:else}
									<AlertCircle size={13} />
									Review
								{/if}
							</span>
						</div>
					{/each}
				</div>
			{/if}
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

	.parsed-layout {
		display: grid;
		grid-template-columns: 300px 1fr;
		gap: 20px;
		align-items: start;
	}
	@media (max-width: 800px) {
		.parsed-layout {
			grid-template-columns: 1fr;
		}
	}

	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		overflow: hidden;
	}

	/* Doc list */
	.doc-list-panel {
		padding: 12px;
	}
	.search-box {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 10px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		margin-bottom: 8px;
	}
	.search-input {
		flex: 1;
		background: none;
		border: none;
		outline: none;
		color: var(--color-text-primary);
		font-size: 0.8125rem;
	}
	.doc-list {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.doc-list-item {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 10px 8px;
		border-radius: var(--radius-md);
		cursor: pointer;
		border: 1px solid transparent;
		background: none;
		text-align: left;
		width: 100%;
		transition: all 0.15s;
	}
	.doc-list-item:hover {
		background: var(--color-bg-primary);
	}
	.doc-list-item.active {
		background: color-mix(in srgb, var(--color-accent) 10%, transparent);
		border-color: var(--color-accent);
	}
	.doc-thumb {
		font-size: 1.25rem;
		flex-shrink: 0;
	}
	.doc-list-info {
		flex: 1;
		min-width: 0;
	}
	.doc-list-name {
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-text-primary);
		display: block;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.doc-list-meta {
		display: flex;
		gap: 6px;
		margin-top: 2px;
	}
	.type-tag {
		font-size: 0.625rem;
		padding: 1px 6px;
		background: var(--color-border);
		border-radius: 999px;
		color: var(--color-text-secondary);
		text-transform: capitalize;
	}
	.conf-tag {
		font-size: 0.625rem;
		padding: 1px 6px;
		background: var(--color-border);
		border-radius: 999px;
		color: var(--color-text-secondary);
	}
	.conf-tag.high {
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}

	/* Field panel */
	.field-panel {
		padding: 0;
	}
	.field-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		padding: 16px 20px;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-bg-primary);
	}
	.field-doc-name {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0 0 2px;
	}
	.field-type {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		text-transform: capitalize;
	}
	.field-actions {
		display: flex;
		gap: 8px;
	}
	.action-btn {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		padding: 6px 12px;
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		border: 1px solid var(--color-border);
		background: var(--color-bg-secondary);
		color: var(--color-text-primary);
		text-decoration: none;
		transition: opacity 0.15s;
	}
	.action-btn.accent {
		background: var(--color-accent);
		color: white;
		border-color: transparent;
	}
	.action-btn:hover {
		opacity: 0.8;
	}

	.fields-table {
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 2px;
	}
	.fields-row {
		display: grid;
		grid-template-columns: 1.5fr 1.5fr 1fr auto;
		gap: 12px;
		align-items: center;
		padding: 10px 10px;
		border-radius: var(--radius-sm);
	}
	.fields-row.header {
		font-size: 0.6875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--color-text-tertiary);
		padding-bottom: 4px;
	}
	.fields-row:not(.header):hover {
		background: var(--color-bg-primary);
	}
	.field-name {
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
	}
	.field-value {
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--color-text-primary);
		font-variant-numeric: tabular-nums;
	}
	.conf-bar-wrap {
		display: flex;
		align-items: center;
		gap: 6px;
	}
	.mini-bar {
		width: 50px;
		height: 4px;
		background: var(--color-border);
		border-radius: 999px;
		overflow: hidden;
	}
	.mini-fill {
		height: 100%;
		border-radius: 999px;
		background: var(--color-danger);
	}
	.mini-fill.medium {
		background: #f59e0b;
	}
	.mini-fill.high {
		background: var(--color-success);
	}
	.conf-pct {
		font-size: 0.6875rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}
	.validated-badge {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
	}
	.validated-badge.ok {
		background: color-mix(in srgb, var(--color-success) 12%, transparent);
		color: var(--color-success);
	}
	.validated-badge.pending {
		background: color-mix(in srgb, #f59e0b 12%, transparent);
		color: #d97706;
	}
</style>
