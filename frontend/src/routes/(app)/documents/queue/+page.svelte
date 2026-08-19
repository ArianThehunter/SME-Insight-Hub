<!--
  Extraction Queue — Monitor document processing queue status.
-->
<script lang="ts">
	import { ListTodo, Clock, Loader2, CheckCircle2, AlertCircle, RefreshCw, Upload } from '@lucide/svelte';

	const queue = [
		{ id: 1, name: 'DBBL_Statement_Aug.pdf', type: 'Bank Statement', position: 1, eta: '~2 min', status: 'processing' },
		{ id: 2, name: 'Invoice_ABC_Trading.pdf', type: 'Invoice', position: 2, eta: '~5 min', status: 'queued' },
		{ id: 3, name: 'Receipt_Meena_Bazar.jpg', type: 'Receipt', position: 3, eta: '~7 min', status: 'queued' },
		{ id: 4, name: 'PO_Bashundhara.pdf', type: 'Purchase Order', position: 4, eta: '~10 min', status: 'queued' },
		{ id: 5, name: 'Utility_TITAS_Gas.pdf', type: 'Utility Bill', position: 5, eta: '~12 min', status: 'queued' },
	];
</script>

<svelte:head><title>Extraction Queue — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Extraction Queue</h1>
			<p class="page-subtitle">Documents awaiting AI data extraction</p>
		</div>
		<div class="header-actions">
			<button class="btn-secondary"><RefreshCw size={15} /> Refresh</button>
			<a href="/documents/upload" class="btn-primary"><Upload size={15} /> Upload</a>
		</div>
	</header>

	<div class="queue-layout">
		<div class="card queue-card">
			<div class="queue-header">
				<span class="queue-count">{queue.length} documents in queue</span>
				<span class="queue-time">Estimated total: ~12 min</span>
			</div>
			<div class="queue-list">
				{#each queue as item}
					<div class="queue-item" class:processing={item.status === 'processing'}>
						<div class="queue-pos">{item.status === 'processing' ? '▶' : item.position}</div>
						<div class="queue-info">
							<span class="queue-name">{item.name}</span>
							<span class="queue-type">{item.type}</span>
						</div>
						<div class="queue-eta">
							{#if item.status === 'processing'}
								<Loader2 size={14} class="spinning" />
								<span class="processing-label">Processing</span>
							{:else}
								<Clock size={13} />
								<span>{item.eta}</span>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>

		<div class="sidebar-cards">
			<div class="card info-card">
				<h3>How it works</h3>
				<ol class="steps">
					<li>Upload your PDF, image, or scanned document</li>
					<li>Our AI reads and extracts key fields (amounts, dates, vendor names)</li>
					<li>Review extracted data in <a href="/documents/parsed">Parsed Data</a></li>
					<li>Export as CSV or sync to your accounting records</li>
				</ol>
			</div>
			<div class="card info-card">
				<h3>Supported Documents</h3>
				<ul class="doc-types">
					<li>🧾 Invoices (Bengali + English)</li>
					<li>🏦 Bank statements (BRAC, DBBL, Islami, City)</li>
					<li>📋 Purchase orders</li>
					<li>⚡ Utility bills (DESCO, DPSCLCO, TITAS)</li>
					<li>🧾 VAT receipts (Mushak 6.3)</li>
				</ul>
			</div>
		</div>
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

	.queue-layout { display: grid; grid-template-columns: 1fr 320px; gap: 20px; align-items: start; }
	@media (max-width: 800px) { .queue-layout { grid-template-columns: 1fr; } }

	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden; }
	.queue-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-bottom: 1px solid var(--color-border); background: var(--color-bg-primary); }
	.queue-count { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); }
	.queue-time { font-size: 0.75rem; color: var(--color-text-secondary); }

	.queue-list { padding: 8px; display: flex; flex-direction: column; gap: 6px; }
	.queue-item {
		display: flex; align-items: center; gap: 12px;
		padding: 12px 14px;
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		background: var(--color-bg-primary);
		transition: border-color 0.2s;
	}
	.queue-item.processing { border-color: var(--color-accent); background: color-mix(in srgb, var(--color-accent) 5%, var(--color-bg-primary)); }
	.queue-pos { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; background: var(--color-border); border-radius: 50%; font-size: 0.6875rem; font-weight: 700; color: var(--color-text-secondary); flex-shrink: 0; }
	.queue-item.processing .queue-pos { background: var(--color-accent); color: white; }
	.queue-info { flex: 1; }
	.queue-name { font-size: 0.8125rem; font-weight: 500; color: var(--color-text-primary); display: block; }
	.queue-type { font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.queue-eta { display: flex; align-items: center; gap: 5px; font-size: 0.75rem; color: var(--color-text-secondary); flex-shrink: 0; }
	.processing-label { color: var(--color-accent); font-weight: 600; }

	:global(.spinning) { animation: spin 1s linear infinite; }

	.sidebar-cards { display: flex; flex-direction: column; gap: 16px; }
	.info-card { padding: 16px; }
	.info-card h3 { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); margin: 0 0 12px; }
	.steps { padding-left: 18px; margin: 0; display: flex; flex-direction: column; gap: 8px; font-size: 0.8125rem; color: var(--color-text-secondary); line-height: 1.5; }
	.steps a { color: var(--color-accent); }
	.doc-types { padding-left: 0; margin: 0; list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 0.8125rem; color: var(--color-text-secondary); }
</style>
