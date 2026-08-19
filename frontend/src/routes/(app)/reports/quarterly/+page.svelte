<!--
  Quarterly Reports — Multi-quarter comparative statements, EBITDA, and growth trends.
-->
<script lang="ts">
	import { CalendarDays, Download, TrendingUp, BarChart3, Layers } from '@lucide/svelte';

	const quarters = [
		{ q: 'Q2 2026 (Apr - Jun)', revenue: '৳ 84,40,000', expenses: '৳ 52,10,000', ebitda: '৳ 32,30,000', margin: '38.2%', status: 'Audited' },
		{ q: 'Q1 2026 (Jan - Mar)', revenue: '৳ 76,20,000', expenses: '৳ 48,90,000', ebitda: '৳ 27,30,000', margin: '35.8%', status: 'Audited' },
		{ q: 'Q4 2025 (Oct - Dec)', revenue: '৳ 92,00,000', expenses: '৳ 56,40,000', ebitda: '৳ 35,60,000', margin: '38.6%', status: 'Audited' },
		{ q: 'Q3 2025 (Jul - Sep)', revenue: '৳ 71,80,000', expenses: '৳ 46,20,000', ebitda: '৳ 25,60,000', margin: '35.6%', status: 'Audited' },
	];
</script>

<svelte:head><title>Quarterly Reports — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Quarterly Financial & Growth Reports</h1>
			<p class="page-subtitle">Quarter-over-quarter EBITDA, operating margin, and performance decks</p>
		</div>
		<div class="header-actions">
			<a href="/documents/export" class="btn-primary">
				<Download size={15} />
				Export Full Financials
			</a>
		</div>
	</header>

	<div class="card quarters-card">
		<div class="card-header">
			<h2 class="card-title">Fiscal Year 2025 - 2026 Quarterly Performance</h2>
		</div>
		<table class="data-table">
			<thead>
				<tr>
					<th>Quarter</th>
					<th>Gross Revenue</th>
					<th>Operating Expenses</th>
					<th>EBITDA (Net)</th>
					<th>Margin</th>
					<th>Status</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				{#each quarters as q}
					<tr>
						<td><strong>{q.q}</strong></td>
						<td class="num">{q.revenue}</td>
						<td class="num">{q.expenses}</td>
						<td class="num font-bold">{q.ebitda}</td>
						<td class="num">{q.margin}</td>
						<td><span class="status-badge">{q.status}</span></td>
						<td><a href="/documents/export" class="table-link">Download Deck →</a></td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-accent); color: white; border: none; text-decoration: none; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); margin-top: 20px; overflow: hidden; }
	.card-header { padding: 14px 18px; border-bottom: 1px solid var(--color-border); }
	.card-title { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }
	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table th { text-align: left; padding: 10px 18px; font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; border-bottom: 1px solid var(--color-border); background: var(--color-bg-primary); }
	.data-table td { padding: 12px 18px; border-bottom: 1px solid var(--color-border); color: var(--color-text-primary); }
	.data-table tr:last-child td { border-bottom: none; }
	.data-table .num { font-variant-numeric: tabular-nums; }
	.font-bold { font-weight: 700; color: var(--color-success); }
	.status-badge { font-size: 0.6875rem; padding: 2px 8px; border-radius: 999px; background: color-mix(in srgb, var(--color-success) 12%, transparent); color: var(--color-success); font-weight: 600; }
	.table-link { color: var(--color-accent); font-weight: 600; text-decoration: none; font-size: 0.75rem; }
</style>
