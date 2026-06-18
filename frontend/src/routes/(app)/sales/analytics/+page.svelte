<!--
  Sales Analytics page — Revenue trends, top products, regional breakdown.
-->
<script lang="ts">
	import { TrendingUp, TrendingDown, DollarSign, ShoppingCart, Users, Target } from '@lucide/svelte';

	const kpis = [
		{ label: 'Total Revenue', value: '৳ 24.8M', change: '+12.5%', trend: 'up', icon: DollarSign, color: 'accent' },
		{ label: 'Orders', value: '1,847', change: '+8.2%', trend: 'up', icon: ShoppingCart, color: 'success' },
		{ label: 'Avg Order Value', value: '৳ 13,420', change: '+3.1%', trend: 'up', icon: Target, color: 'violet' },
		{ label: 'Active Customers', value: '486', change: '-2.4%', trend: 'down', icon: Users, color: 'warning' },
	];

	const monthlyRevenue = [
		{ month: 'Jan', revenue: 1820000, orders: 142 },
		{ month: 'Feb', revenue: 2150000, orders: 168 },
		{ month: 'Mar', revenue: 1980000, orders: 155 },
		{ month: 'Apr', revenue: 2450000, orders: 192 },
		{ month: 'May', revenue: 2680000, orders: 210 },
		{ month: 'Jun', revenue: 2340000, orders: 183 },
		{ month: 'Jul', revenue: 2890000, orders: 226 },
		{ month: 'Aug', revenue: 3120000, orders: 244 },
		{ month: 'Sep', revenue: 2750000, orders: 215 },
		{ month: 'Oct', revenue: 3350000, orders: 262 },
		{ month: 'Nov', revenue: 3580000, orders: 280 },
		{ month: 'Dec', revenue: 3850000, orders: 301 },
	];

	const topProducts = [
		{ name: 'Premium Basmati Rice 5kg', revenue: 3850000, units: 2420, growth: 18.5 },
		{ name: 'Organic Mustard Oil 1L', revenue: 2640000, units: 4800, growth: 12.3 },
		{ name: 'Bengal Spice Mix Set', revenue: 2180000, units: 3650, growth: 24.7 },
		{ name: 'Handloom Cotton Saree', revenue: 1950000, units: 650, growth: -3.2 },
		{ name: 'Artisan Leather Bag', revenue: 1720000, units: 430, growth: 8.9 },
	];

	const regionData = [
		{ region: 'Dhaka', revenue: 9800000, share: 39.5 },
		{ region: 'Chittagong', revenue: 5200000, share: 21.0 },
		{ region: 'Sylhet', revenue: 3100000, share: 12.5 },
		{ region: 'Rajshahi', revenue: 2400000, share: 9.7 },
		{ region: 'Khulna', revenue: 2100000, share: 8.5 },
		{ region: 'Others', revenue: 2200000, share: 8.8 },
	];

	const maxRevenue = Math.max(...monthlyRevenue.map(m => m.revenue));
	const maxRegion = Math.max(...regionData.map(r => r.revenue));

	function formatCurrency(v: number): string {
		if (v >= 1000000) return `৳ ${(v / 1000000).toFixed(1)}M`;
		if (v >= 1000) return `৳ ${(v / 1000).toFixed(0)}K`;
		return `৳ ${v}`;
	}
</script>

<svelte:head>
	<title>Sales Analytics — SME Insight Hub</title>
</svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Sales Analytics</h1>
			<p class="page-subtitle">Revenue trends, top products, and regional performance</p>
		</div>
		<div class="header-actions">
			<select class="period-select">
				<option>Last 12 Months</option>
				<option>Last 6 Months</option>
				<option>This Quarter</option>
				<option>This Year</option>
			</select>
		</div>
	</header>

	<!-- KPI Cards -->
	<div class="kpi-grid">
		{#each kpis as kpi, i}
			{@const Icon = kpi.icon}
			<div class="kpi-card animate-fade-in-up stagger-{i + 1}">
				<div class="kpi-header">
					<div class="kpi-icon {kpi.color}">
						<Icon size={18} />
					</div>
					<span class="kpi-change {kpi.trend}">
						{#if kpi.trend === 'up'}<TrendingUp size={14} />{:else}<TrendingDown size={14} />{/if}
						{kpi.change}
					</span>
				</div>
				<div class="kpi-value">{kpi.value}</div>
				<div class="kpi-label">{kpi.label}</div>
			</div>
		{/each}
	</div>

	<!-- Charts Row -->
	<div class="charts-row">
		<!-- Revenue Trend -->
		<div class="chart-card animate-fade-in-up">
			<h3 class="card-title">Revenue Trend</h3>
			<div class="bar-chart">
				{#each monthlyRevenue as item}
					<div class="bar-group">
						<div class="bar-wrapper">
							<div
								class="bar"
								style="height: {(item.revenue / maxRevenue) * 100}%"
								title="{item.month}: {formatCurrency(item.revenue)}"
							></div>
						</div>
						<span class="bar-label">{item.month}</span>
					</div>
				{/each}
			</div>
		</div>

		<!-- Top Products -->
		<div class="chart-card animate-fade-in-up stagger-2">
			<h3 class="card-title">Top Products</h3>
			<div class="product-list">
				{#each topProducts as product, i}
					<div class="product-item">
						<div class="product-rank">#{i + 1}</div>
						<div class="product-info">
							<div class="product-name">{product.name}</div>
							<div class="product-meta">
								<span>{formatCurrency(product.revenue)}</span>
								<span class="dot">·</span>
								<span>{product.units.toLocaleString()} units</span>
							</div>
						</div>
						<span class="product-growth" class:positive={product.growth > 0} class:negative={product.growth < 0}>
							{product.growth > 0 ? '+' : ''}{product.growth}%
						</span>
					</div>
				{/each}
			</div>
		</div>
	</div>

	<!-- Regional Breakdown -->
	<div class="chart-card animate-fade-in-up stagger-3">
		<h3 class="card-title">Revenue by Region</h3>
		<div class="region-grid">
			{#each regionData as region}
				<div class="region-item">
					<div class="region-header">
						<span class="region-name">{region.region}</span>
						<span class="region-value">{formatCurrency(region.revenue)}</span>
					</div>
					<div class="region-bar-bg">
						<div class="region-bar-fill" style="width: {(region.revenue / maxRegion) * 100}%"></div>
					</div>
					<span class="region-share">{region.share}% of total</span>
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 24px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.period-select {
		padding: 8px 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border);
		background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.8125rem;
		font-family: inherit; cursor: pointer; outline: none;
	}
	.period-select:focus { border-color: var(--color-accent); }

	.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }

	.kpi-card {
		padding: 20px; border-radius: var(--radius-lg); background: var(--color-bg-secondary);
		border: 1px solid var(--color-border); transition: all var(--transition-fast);
	}
	.kpi-card:hover { border-color: var(--color-border-hover); box-shadow: var(--shadow-md); transform: translateY(-2px); }

	.kpi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
	.kpi-icon {
		width: 36px; height: 36px; border-radius: var(--radius-md);
		display: flex; align-items: center; justify-content: center;
	}
	.kpi-icon.accent { background: var(--color-accent-muted); color: var(--color-accent); }
	.kpi-icon.success { background: var(--color-success-muted); color: var(--color-success); }
	.kpi-icon.violet { background: var(--color-violet-muted); color: var(--color-violet); }
	.kpi-icon.warning { background: var(--color-warning-muted); color: var(--color-warning); }

	.kpi-change { display: flex; align-items: center; gap: 4px; font-size: 0.75rem; font-weight: 600; }
	.kpi-change.up { color: var(--color-success); }
	.kpi-change.down { color: var(--color-danger); }

	.kpi-value { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); letter-spacing: -0.02em; }
	.kpi-label { font-size: 0.75rem; color: var(--color-text-secondary); margin-top: 4px; }

	.charts-row { display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px; }
	@media (max-width: 900px) { .charts-row { grid-template-columns: 1fr; } }

	.chart-card {
		padding: 24px; border-radius: var(--radius-lg); background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
	}
	.card-title { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0 0 20px; }

	/* Bar Chart */
	.bar-chart { display: flex; align-items: flex-end; gap: 6px; height: 200px; }
	.bar-group { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; height: 100%; }
	.bar-wrapper { flex: 1; width: 100%; display: flex; align-items: flex-end; }
	.bar {
		width: 100%; min-height: 4px; border-radius: 4px 4px 0 0;
		background: var(--gradient-accent); transition: height 0.6s cubic-bezier(0.4, 0, 0.2, 1);
		cursor: pointer; position: relative;
	}
	.bar:hover { opacity: 0.85; }
	.bar-label { font-size: 0.625rem; color: var(--color-text-tertiary); }

	/* Product List */
	.product-list { display: flex; flex-direction: column; gap: 12px; }
	.product-item {
		display: flex; align-items: center; gap: 12px; padding: 10px 12px;
		border-radius: var(--radius-md); background: var(--color-bg-primary);
		border: 1px solid var(--color-border-subtle); transition: all var(--transition-fast);
	}
	.product-item:hover { background: var(--color-bg-hover); }
	.product-rank { font-size: 0.75rem; font-weight: 700; color: var(--color-text-tertiary); min-width: 24px; }
	.product-info { flex: 1; min-width: 0; }
	.product-name { font-size: 0.8125rem; font-weight: 500; color: var(--color-text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.product-meta { font-size: 0.6875rem; color: var(--color-text-tertiary); margin-top: 2px; display: flex; gap: 4px; }
	.dot { color: var(--color-text-muted); }
	.product-growth { font-size: 0.75rem; font-weight: 600; white-space: nowrap; }
	.product-growth.positive { color: var(--color-success); }
	.product-growth.negative { color: var(--color-danger); }

	/* Regional */
	.region-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
	.region-item { display: flex; flex-direction: column; gap: 6px; }
	.region-header { display: flex; justify-content: space-between; align-items: center; }
	.region-name { font-size: 0.8125rem; font-weight: 500; color: var(--color-text-primary); }
	.region-value { font-size: 0.8125rem; font-weight: 600; color: var(--color-accent); }
	.region-bar-bg { height: 6px; border-radius: var(--radius-full); background: var(--color-bg-tertiary); overflow: hidden; }
	.region-bar-fill { height: 100%; border-radius: var(--radius-full); background: var(--gradient-accent); transition: width 0.8s ease; }
	.region-share { font-size: 0.6875rem; color: var(--color-text-tertiary); }
</style>
