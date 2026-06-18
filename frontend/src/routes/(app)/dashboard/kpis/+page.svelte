<!--
  KPIs page — Targets, metrics trackers, progress bars, and status indicator dashboard.
-->
<script lang="ts">
	import { Target, TrendingUp, TrendingDown, Star, Activity, Plus } from '@lucide/svelte';

	let categoryFilter = $state('all');

	const kpis = [
		{ name: 'Gross Profit Margin', value: '76.1%', target: '70.0%', category: 'Finance', status: 'On Track', trend: '+1.2%', trendUp: true, pct: 100 },
		{ name: 'Net Profit Margin', value: '46.0%', target: '40.0%', category: 'Finance', status: 'On Track', trend: '+2.5%', trendUp: true, pct: 100 },
		{ name: 'Current Ratio (Liquidity)', value: '2.8x', target: '2.0x', category: 'Finance', status: 'On Track', trend: '+0.3x', trendUp: true, pct: 100 },
		
		{ name: 'Customer Acquisition Cost (CAC)', value: '৳ 450', target: '৳ 600', category: 'Sales', status: 'On Track', trend: '-৳ 50', trendUp: true, pct: 100 },
		{ name: 'Monthly Active Customers', value: '850', target: '1,000', category: 'Sales', status: 'At Risk', trend: '+5.0%', trendUp: true, pct: 85 },
		{ name: 'Customer Retention Rate', value: '82.5%', target: '85.0%', category: 'Sales', status: 'At Risk', trend: '-1.5%', trendUp: false, pct: 97 },
		
		{ name: 'Inventory Turnover Ratio', value: '6.2x', target: '6.0x', category: 'Inventory', status: 'On Track', trend: '+0.4x', trendUp: true, pct: 100 },
		{ name: 'Supplier On-Time Delivery', value: '92.2%', target: '95.0%', category: 'Inventory', status: 'At Risk', trend: '-0.8%', trendUp: false, pct: 97 },
		{ name: 'Stockout Incidence Rate', value: '1.5%', target: '< 2.0%', category: 'Inventory', status: 'On Track', trend: '-0.5%', trendUp: true, pct: 100 }
	];

	const categories = ['Finance', 'Sales', 'Inventory'];

	const filtered = $derived(
		kpis.filter(k => categoryFilter === 'all' || k.category === categoryFilter)
	);

	function statusClass(status: string): string {
		switch (status.toLowerCase()) {
			case 'on track': return 'success';
			case 'at risk': return 'warning';
			default: return 'danger';
		}
	}
</script>

<svelte:head><title>Key Performance Indicators — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Key Performance Indicators (KPIs)</h1>
			<p class="page-subtitle">Track targets, historical performance metrics, and departmental goals</p>
		</div>
		<button class="btn-create"><Plus size={16} /> Add KPI</button>
	</header>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="category-tabs">
			<button 
				class="tab-btn {categoryFilter === 'all' ? 'active' : ''}" 
				onclick={() => categoryFilter = 'all'}
			>
				All Departments
			</button>
			{#each categories as cat}
				<button 
					class="tab-btn {categoryFilter === cat ? 'active' : ''}" 
					onclick={() => categoryFilter = cat}
				>
					{cat}
				</button>
			{/each}
		</div>
	</div>

	<!-- KPIs Grid Layout -->
	<div class="kpis-grid animate-fade-in-up">
		{#each filtered as k}
			{@const stClass = statusClass(k.status)}
			<div class="kpi-card">
				<div class="card-header">
					<span class="category-tag">{k.category}</span>
					<span class="badge {stClass}">{k.status}</span>
				</div>

				<h3 class="kpi-name">{k.name}</h3>

				<div class="kpi-values">
					<div class="val-box">
						<span class="label">Current Value</span>
						<span class="value">{k.value}</span>
					</div>
					<div class="val-box">
						<span class="label">Target</span>
						<span class="value target">{k.target}</span>
					</div>
				</div>

				<div class="card-footer">
					<!-- Progress tracker -->
					<div class="progress-section">
						<div class="progress-bar-bg">
							<div class="progress-bar {stClass}" style="width: {k.pct}%"></div>
						</div>
						<span class="progress-pct">{k.pct}% of goal</span>
					</div>

					<!-- Trend -->
					<div class="trend-indicator {k.trendUp ? 'up' : 'down'}">
						{#if k.trendUp}
							<TrendingUp size={14} />
						{:else}
							<TrendingDown size={14} />
						{/if}
						<span>{k.trend}</span>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	
	.btn-create { display: flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: var(--radius-md); border: none; background: var(--gradient-accent); color: white; font-size: 0.8125rem; font-weight: 600; font-family: inherit; cursor: pointer; box-shadow: 0 2px 8px rgba(59,130,246,0.25); transition: all var(--transition-fast); }
	.btn-create:hover { opacity: 0.9; transform: translateY(-1px); }

	.toolbar { border-bottom: 1px solid var(--color-border); padding-bottom: 2px; }
	.category-tabs { display: flex; gap: 6px; }
	.tab-btn { padding: 8px 16px; border: none; background: transparent; color: var(--color-text-secondary); font-size: 0.8125rem; font-weight: 600; cursor: pointer; position: relative; font-family: inherit; transition: color var(--transition-fast); }
	.tab-btn:hover { color: var(--color-text-primary); }
	.tab-btn.active { color: var(--color-accent); }
	.tab-btn.active::after { content: ''; position: absolute; bottom: -3px; left: 0; right: 0; height: 2px; background: var(--color-accent); border-radius: var(--radius-full); }

	.kpis-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
	@media (max-width: 992px) { .kpis-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 640px) { .kpis-grid { grid-template-columns: 1fr; } }

	.kpi-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px; display: flex; flex-direction: column; gap: 14px; transition: all var(--transition-fast); }
	.kpi-card:hover { border-color: var(--color-border-hover); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
	
	.card-header { display: flex; justify-content: space-between; align-items: center; }
	.category-tag { font-size: 0.6875rem; font-weight: 600; color: var(--color-text-tertiary); text-transform: uppercase; background: var(--color-bg-tertiary); padding: 2px 8px; border-radius: var(--radius-sm); border: 1px solid var(--color-border-subtle); }
	
	.kpi-name { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }
	
	.kpi-values { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; background: var(--color-bg-tertiary); padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border-subtle); }
	.val-box { display: flex; flex-direction: column; gap: 2px; }
	.val-box .label { font-size: 0.625rem; color: var(--color-text-tertiary); text-transform: uppercase; font-weight: 600; }
	.val-box .value { font-size: 1.125rem; font-weight: 700; color: var(--color-text-primary); }
	.val-box .value.target { color: var(--color-text-secondary); font-weight: 500; }

	.card-footer { display: flex; justify-content: space-between; align-items: center; gap: 12px; border-top: 1px solid var(--color-border-subtle); padding-top: 12px; }
	.progress-section { display: flex; flex-direction: column; gap: 4px; flex: 1; }
	.progress-bar-bg { height: 4px; border-radius: var(--radius-full); background: var(--color-bg-tertiary); overflow: hidden; }
	.progress-bar { height: 100%; border-radius: var(--radius-full); }
	.progress-bar.success { background: var(--color-success); }
	.progress-bar.warning { background: var(--color-warning); }
	.progress-pct { font-size: 0.625rem; color: var(--color-text-tertiary); font-weight: 500; }

	.trend-indicator { display: flex; align-items: center; gap: 4px; font-size: 0.75rem; font-weight: 600; }
	.trend-indicator.up { color: var(--color-success); }
	.trend-indicator.down { color: var(--color-danger); }
	
	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }
</style>
