<!--
  Revenue page — Monthly comparisons, revenue by category, growth metrics.
-->
<script lang="ts">
	import { TrendingUp, TrendingDown, ArrowUpRight, CalendarDays } from '@lucide/svelte';

	const revenueMonths = [
		{ month: 'Jan 2026', revenue: 1820000, prevYear: 1540000 },
		{ month: 'Feb 2026', revenue: 2150000, prevYear: 1780000 },
		{ month: 'Mar 2026', revenue: 1980000, prevYear: 1920000 },
		{ month: 'Apr 2026', revenue: 2450000, prevYear: 2100000 },
		{ month: 'May 2026', revenue: 2680000, prevYear: 2250000 },
		{ month: 'Jun 2026', revenue: 2340000, prevYear: 2180000 },
	];

	const categories = [
		{ name: 'Food & Beverages', revenue: 8450000, share: 34.1, color: '#3b82f6' },
		{ name: 'Textiles & Apparel', revenue: 5820000, share: 23.5, color: '#8b5cf6' },
		{ name: 'Electronics', revenue: 4230000, share: 17.1, color: '#10b981' },
		{ name: 'Agriculture', revenue: 3150000, share: 12.7, color: '#f59e0b' },
		{ name: 'Handicrafts', revenue: 1850000, share: 7.5, color: '#06b6d4' },
		{ name: 'Others', revenue: 1300000, share: 5.1, color: '#64748b' },
	];

	const growthMetrics = [
		{ label: 'Revenue Growth (YoY)', value: '+18.5%', trend: 'up', context: 'vs ৳21.0M last year' },
		{ label: 'Average Monthly Revenue', value: '৳ 2.24M', trend: 'up', context: '+12.3% vs last 6 months' },
		{ label: 'Best Month', value: '৳ 2.68M', trend: 'up', context: 'May 2026' },
		{ label: 'Revenue per Customer', value: '৳ 51,028', trend: 'up', context: '+6.7% improvement' },
	];

	const maxRev = Math.max(...revenueMonths.map(m => Math.max(m.revenue, m.prevYear)));
	const maxCat = Math.max(...categories.map(c => c.revenue));

	function fmt(v: number): string {
		if (v >= 1000000) return `৳ ${(v / 1000000).toFixed(1)}M`;
		if (v >= 1000) return `৳ ${(v / 1000).toFixed(0)}K`;
		return `৳ ${v}`;
	}
</script>

<svelte:head><title>Revenue — SME Insight Hub</title></svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Revenue Analytics</h1>
			<p class="page-subtitle">Monthly comparisons, category breakdown, and growth metrics</p>
		</div>
	</header>

	<!-- Growth Cards -->
	<div class="growth-grid">
		{#each growthMetrics as m, i}
			<div class="growth-card animate-fade-in-up stagger-{i + 1}">
				<div class="growth-top">
					<span class="growth-label">{m.label}</span>
					{#if m.trend === 'up'}<TrendingUp size={14} class="trend-up" />{:else}<TrendingDown size={14} class="trend-down" />{/if}
				</div>
				<div class="growth-value">{m.value}</div>
				<div class="growth-context">{m.context}</div>
			</div>
		{/each}
	</div>

	<div class="charts-row">
		<!-- Monthly Comparison -->
		<div class="chart-card animate-fade-in-up">
			<div class="card-head">
				<h3 class="card-title">Monthly Revenue Comparison</h3>
				<div class="legend">
					<span class="legend-item"><span class="legend-dot current"></span> 2026</span>
					<span class="legend-item"><span class="legend-dot prev"></span> 2025</span>
				</div>
			</div>
			<div class="comparison-chart">
				{#each revenueMonths as m}
					<div class="comp-group">
						<div class="comp-bars">
							<div class="comp-bar prev" style="height: {(m.prevYear / maxRev) * 100}%" title="2025: {fmt(m.prevYear)}"></div>
							<div class="comp-bar current" style="height: {(m.revenue / maxRev) * 100}%" title="2026: {fmt(m.revenue)}"></div>
						</div>
						<span class="comp-label">{m.month.split(' ')[0]}</span>
						<span class="comp-growth" class:positive={m.revenue > m.prevYear} class:negative={m.revenue <= m.prevYear}>
							{m.revenue > m.prevYear ? '+' : ''}{(((m.revenue - m.prevYear) / m.prevYear) * 100).toFixed(0)}%
						</span>
					</div>
				{/each}
			</div>
		</div>

		<!-- Revenue by Category -->
		<div class="chart-card animate-fade-in-up stagger-2">
			<h3 class="card-title">Revenue by Category</h3>
			<div class="cat-list">
				{#each categories as cat}
					<div class="cat-item">
						<div class="cat-info">
							<div class="cat-dot" style="background: {cat.color}"></div>
							<span class="cat-name">{cat.name}</span>
						</div>
						<div class="cat-bar-area">
							<div class="cat-bar-bg">
								<div class="cat-bar-fill" style="width: {(cat.revenue / maxCat) * 100}%; background: {cat.color}"></div>
							</div>
						</div>
						<div class="cat-values">
							<span class="cat-rev">{fmt(cat.revenue)}</span>
							<span class="cat-share">{cat.share}%</span>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 24px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.growth-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
	.growth-card {
		padding: 20px; border-radius: var(--radius-lg); background: var(--color-bg-secondary);
		border: 1px solid var(--color-border); transition: all var(--transition-fast);
	}
	.growth-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
	.growth-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
	.growth-label { font-size: 0.75rem; color: var(--color-text-secondary); }
	:global(.trend-up) { color: var(--color-success); }
	:global(.trend-down) { color: var(--color-danger); }
	.growth-value { font-size: 1.375rem; font-weight: 700; color: var(--color-text-primary); letter-spacing: -0.02em; }
	.growth-context { font-size: 0.6875rem; color: var(--color-text-tertiary); margin-top: 4px; }

	.charts-row { display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px; }
	@media (max-width: 900px) { .charts-row { grid-template-columns: 1fr; } }

	.chart-card { padding: 24px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.card-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
	.card-title { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }

	.legend { display: flex; gap: 16px; }
	.legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.legend-dot { width: 8px; height: 8px; border-radius: 2px; }
	.legend-dot.current { background: var(--color-accent); }
	.legend-dot.prev { background: var(--color-border-hover); }

	.comparison-chart { display: flex; gap: 12px; height: 200px; }
	.comp-group { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px; }
	.comp-bars { flex: 1; display: flex; align-items: flex-end; gap: 4px; width: 100%; }
	.comp-bar { flex: 1; min-height: 4px; border-radius: 3px 3px 0 0; transition: height 0.6s ease; cursor: pointer; }
	.comp-bar.current { background: var(--color-accent); }
	.comp-bar.prev { background: var(--color-border-hover); }
	.comp-bar:hover { opacity: 0.8; }
	.comp-label { font-size: 0.625rem; color: var(--color-text-tertiary); }
	.comp-growth { font-size: 0.625rem; font-weight: 600; }
	.comp-growth.positive { color: var(--color-success); }
	.comp-growth.negative { color: var(--color-danger); }

	.cat-list { display: flex; flex-direction: column; gap: 14px; }
	.cat-item { display: flex; align-items: center; gap: 12px; }
	.cat-info { display: flex; align-items: center; gap: 8px; min-width: 140px; }
	.cat-dot { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }
	.cat-name { font-size: 0.8125rem; color: var(--color-text-primary); white-space: nowrap; }
	.cat-bar-area { flex: 1; }
	.cat-bar-bg { height: 8px; border-radius: var(--radius-full); background: var(--color-bg-tertiary); overflow: hidden; }
	.cat-bar-fill { height: 100%; border-radius: var(--radius-full); transition: width 0.6s ease; }
	.cat-values { display: flex; gap: 8px; min-width: 100px; justify-content: flex-end; }
	.cat-rev { font-size: 0.75rem; font-weight: 600; color: var(--color-text-primary); }
	.cat-share { font-size: 0.6875rem; color: var(--color-text-tertiary); }
</style>
