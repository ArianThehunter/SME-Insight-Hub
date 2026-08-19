<!--
  BI Analytics — Advanced Business Intelligence with multi-dimensional performance metrics, category breakdown, and cohort analysis.
-->
<script lang="ts">
	import {
		BarChart3, TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight,
		PieChart, LineChart, Calendar, Download, RefreshCw, Layers, Sparkles
	} from '@lucide/svelte';

	let timeRange = $state('last_30_days');
	let selectedCategory = $state('all');

	const metrics = [
		{ label: 'Customer Lifetime Value (LTV)', value: '৳ 2,45,000', change: '+14.2%', up: true, subtitle: 'Average per enterprise account' },
		{ label: 'Customer Acquisition Cost (CAC)', value: '৳ 18,500', change: '-6.8%', up: false, subtitle: 'Down across digital channels' },
		{ label: 'LTV / CAC Ratio', value: '13.2x', change: '+2.1x', up: true, subtitle: 'Healthy benchmark (>3x)' },
		{ label: 'Gross Profit Margin', value: '38.4%', change: '+3.1%', up: true, subtitle: 'Textiles & Electronics lead' },
	];

	const categoryPerformance = [
		{ name: 'Textiles & Garments', revenue: 11400000, margin: 42, growth: 18.5, share: 40 },
		{ name: 'Consumer Electronics', revenue: 7980000, margin: 34, growth: 12.1, share: 28 },
		{ name: 'Construction Materials', revenue: 5130000, margin: 26, growth: 8.4, share: 18 },
		{ name: 'Agro & Food Processing', revenue: 3990000, margin: 31, growth: 15.2, share: 14 },
	];

	const regionalBreakdown = [
		{ division: 'Dhaka', sales: '৳ 1,42,00,000', orders: 1420, activeSMEs: 412, growth: '+16%' },
		{ division: 'Chittagong', sales: '৳ 78,50,000', orders: 810, activeSMEs: 235, growth: '+12%' },
		{ division: 'Rajshahi', sales: '৳ 24,00,000', orders: 280, activeSMEs: 84, growth: '+19%' },
		{ division: 'Sylhet', sales: '৳ 21,50,000', orders: 240, activeSMEs: 72, growth: '+9%' },
		{ division: 'Khulna', sales: '৳ 18,50,000', orders: 195, activeSMEs: 61, growth: '+14%' },
	];
</script>

<svelte:head>
	<title>BI Analytics — SME Insight Hub</title>
	<meta name="description" content="Advanced business intelligence, unit economics, and regional sales distribution for Bangladesh SMEs." />
</svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Business Intelligence & Analytics</h1>
			<p class="page-subtitle">Unit economics, cross-category performance, and geographic revenue distribution</p>
		</div>
		<div class="header-actions">
			<select class="select-input" bind:value={timeRange} aria-label="Select timeframe">
				<option value="last_7_days">Last 7 Days</option>
				<option value="last_30_days">Last 30 Days</option>
				<option value="last_quarter">This Quarter</option>
				<option value="ytd">Year to Date (2026)</option>
			</select>
			<a href="/documents/export" class="btn-secondary">
				<Download size={15} />
				Export BI Dataset
			</a>
		</div>
	</header>

	<!-- Metric Cards -->
	<div class="metrics-grid">
		{#each metrics as m}
			<div class="metric-card card">
				<span class="metric-label">{m.label}</span>
				<div class="metric-val-row">
					<span class="metric-value">{m.value}</span>
					<span class="badge {m.up ? 'badge-success' : 'badge-info'}">
						{#if m.up}<ArrowUpRight size={14} />{:else}<ArrowDownRight size={14} />{/if}
						{m.change}
					</span>
				</div>
				<span class="metric-sub">{m.subtitle}</span>
			</div>
		{/each}
	</div>

	<!-- Two Column Section -->
	<div class="grid-2">
		<!-- Category Breakdown -->
		<div class="card">
			<div class="card-header">
				<h2 class="card-title">Category Performance & Margin</h2>
				<span class="card-tag">FY 2026</span>
			</div>
			<div class="category-list">
				{#each categoryPerformance as cat}
					<div class="category-item">
						<div class="category-info">
							<div class="cat-name-row">
								<span class="cat-name">{cat.name}</span>
								<span class="cat-revenue">৳ {(cat.revenue / 100000).toFixed(1)} Lakh ({cat.share}%)</span>
							</div>
							<div class="progress-track">
								<div class="progress-fill" style="width: {cat.share}%;"></div>
							</div>
						</div>
						<div class="cat-stats">
							<span class="cat-stat">Margin: <strong>{cat.margin}%</strong></span>
							<span class="cat-stat growth">+{cat.growth}% YoY</span>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<!-- Regional Breakdown -->
		<div class="card">
			<div class="card-header">
				<h2 class="card-title">Regional Distribution (Bangladesh)</h2>
				<span class="card-tag">5 Divisions</span>
			</div>
			<table class="data-table">
				<thead>
					<tr>
						<th>Division</th>
						<th>Revenue</th>
						<th>Orders</th>
						<th>Active SMEs</th>
						<th>Growth</th>
					</tr>
				</thead>
				<tbody>
					{#each regionalBreakdown as r}
						<tr>
							<td><strong>{r.division}</strong></td>
							<td class="num">{r.sales}</td>
							<td class="num">{r.orders}</td>
							<td class="num">{r.activeSMEs}</td>
							<td class="growth-cell">{r.growth}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.header-actions { display: flex; gap: 8px; align-items: center; }

	.select-input {
		padding: 7px 12px; background: var(--color-bg-secondary);
		border: 1px solid var(--color-border); border-radius: var(--radius-md);
		color: var(--color-text-primary); font-size: 0.8125rem;
	}
	.btn-secondary {
		display: inline-flex; align-items: center; gap: 6px;
		padding: 7px 14px; border-radius: var(--radius-md);
		font-size: 0.8125rem; font-weight: 600; cursor: pointer;
		background: var(--color-bg-secondary); color: var(--color-text-primary);
		border: 1px solid var(--color-border); text-decoration: none;
	}

	.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 20px 0; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 18px; }
	.metric-card { display: flex; flex-direction: column; gap: 6px; }
	.metric-label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }
	.metric-val-row { display: flex; justify-content: space-between; align-items: baseline; }
	.metric-value { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); }
	.metric-sub { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.badge { display: inline-flex; align-items: center; gap: 2px; font-size: 0.75rem; font-weight: 600; padding: 2px 6px; border-radius: 999px; }
	.badge-success { background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.badge-info { background: color-mix(in srgb, #38bdf8 15%, transparent); color: #0ea5e9; }

	.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
	@media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }

	.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
	.card-title { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }
	.card-tag { font-size: 0.6875rem; font-weight: 600; padding: 2px 8px; background: var(--color-bg-primary); border-radius: 999px; color: var(--color-text-tertiary); border: 1px solid var(--color-border); }

	.category-list { display: flex; flex-direction: column; gap: 14px; }
	.category-item { display: flex; flex-direction: column; gap: 6px; }
	.cat-name-row { display: flex; justify-content: space-between; font-size: 0.8125rem; font-weight: 500; color: var(--color-text-primary); }
	.cat-revenue { color: var(--color-text-secondary); font-size: 0.75rem; }
	.progress-track { height: 6px; background: var(--color-border); border-radius: 999px; overflow: hidden; }
	.progress-fill { height: 100%; background: var(--color-accent); border-radius: 999px; }
	.cat-stats { display: flex; justify-content: space-between; font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.cat-stats .growth { color: var(--color-success); font-weight: 600; }

	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table th { text-align: left; padding: 8px 10px; font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; border-bottom: 1px solid var(--color-border); }
	.data-table td { padding: 10px; border-bottom: 1px solid var(--color-border); color: var(--color-text-primary); }
	.data-table tr:last-child td { border-bottom: none; }
	.data-table .num { font-variant-numeric: tabular-nums; }
	.growth-cell { color: var(--color-success); font-weight: 600; }
</style>
