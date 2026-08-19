<!--
  BI Custom Reports — Build and generate custom analytical reporting packs.
-->
<script lang="ts">
	import { BookOpen, FileText, Download, Play, Plus, Clock, CheckCircle } from '@lucide/svelte';

	const reports = [
		{
			id: '1',
			title: 'Monthly Executive Deck',
			desc: 'KPI scorecards, P&L statement, top customers, and stock risks',
			frequency: 'Monthly (1st)',
			format: 'PDF',
			lastRun: 'Aug 1, 2026',
			size: '2.4 MB'
		},
		{
			id: '2',
			title: 'VAT & Tax Compliance Pack (NBR 6.3)',
			desc: 'Input-output VAT calculation, Mushak 6.3 summary and NBR export',
			frequency: 'Monthly (15th)',
			format: 'Excel + PDF',
			lastRun: 'Jul 15, 2026',
			size: '4.1 MB'
		},
		{
			id: '3',
			title: 'Sales Performance by Division',
			desc: 'Regional breakdown of volume, value, margin across 8 BD divisions',
			frequency: 'Weekly (Mon)',
			format: 'Excel',
			lastRun: 'Aug 17, 2026',
			size: '1.1 MB'
		},
		{
			id: '4',
			title: 'Working Capital & Inventory Valuation',
			desc: 'Aging stock movement, warehouse holding value, supplier credit',
			frequency: 'Bi-Weekly',
			format: 'PDF',
			lastRun: 'Aug 10, 2026',
			size: '1.8 MB'
		}
	];

	let generating = $state<Record<string, boolean>>({});

	async function runReport(id: string) {
		generating = { ...generating, [id]: true };
		await new Promise((r) => setTimeout(r, 1500));
		generating = { ...generating, [id]: false };
	}
</script>

<svelte:head><title>Custom Reports — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Custom Analytical Reports</h1>
			<p class="page-subtitle">
				Configure automated reporting packs for board members, lenders, and NBR tax filings
			</p>
		</div>
		<div class="header-actions">
			<a href="/reports/monthly" class="btn-primary">
				<Plus size={16} />
				New Report Pack
			</a>
		</div>
	</header>

	<div class="report-grid">
		{#each reports as r}
			<div class="card report-card">
				<div class="report-top">
					<span class="report-format">{r.format}</span>
					<span class="report-freq">{r.frequency}</span>
				</div>
				<h3 class="report-title">{r.title}</h3>
				<p class="report-desc">{r.desc}</p>
				<div class="report-meta">
					<span>Last Run: <strong>{r.lastRun}</strong></span>
					<span>Size: {r.size}</span>
				</div>
				<div class="report-actions">
					<button class="btn-secondary" onclick={() => runReport(r.id)} disabled={generating[r.id]}>
						{#if generating[r.id]}
							Generating...
						{:else}
							<Play size={14} />
							Run Now
						{/if}
					</button>
					<a href="/documents/export" class="btn-icon-btn" title="Download latest pack">
						<Download size={15} />
					</a>
				</div>
			</div>
		{/each}
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
	.btn-primary {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 7px 14px;
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		font-weight: 600;
		cursor: pointer;
		background: var(--color-accent);
		color: white;
		border: none;
		text-decoration: none;
	}
	.btn-secondary {
		flex: 1;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 6px;
		padding: 7px 14px;
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		font-weight: 600;
		cursor: pointer;
		background: var(--color-bg-primary);
		color: var(--color-text-primary);
		border: 1px solid var(--color-border);
	}
	.btn-icon-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 34px;
		height: 34px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-secondary);
		text-decoration: none;
	}
	.btn-icon-btn:hover {
		color: var(--color-accent);
		border-color: var(--color-accent);
	}

	.report-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 16px;
		margin-top: 20px;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.report-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.report-top {
		display: flex;
		justify-content: space-between;
		font-size: 0.6875rem;
	}
	.report-format {
		font-weight: 700;
		color: var(--color-accent);
		background: color-mix(in srgb, var(--color-accent) 10%, transparent);
		padding: 2px 6px;
		border-radius: 4px;
	}
	.report-freq {
		color: var(--color-text-tertiary);
	}
	.report-title {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
	}
	.report-desc {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		margin: 0;
		line-height: 1.4;
	}
	.report-meta {
		display: flex;
		justify-content: space-between;
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		margin-top: auto;
		padding-top: 10px;
		border-top: 1px solid var(--color-border);
	}
	.report-meta strong {
		color: var(--color-text-secondary);
	}
	.report-actions {
		display: flex;
		gap: 8px;
	}
</style>
