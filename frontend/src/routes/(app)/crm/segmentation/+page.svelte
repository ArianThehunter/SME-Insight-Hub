<!--
  CRM Segmentation — RFM (Recency, Frequency, Monetary) customer segmentation for targeting.
-->
<script lang="ts">
	import { Filter, Users, ArrowUpRight, Target, Sparkles, Send } from '@lucide/svelte';

	const segments = [
		{
			name: 'Champions (High LTV, High Recency)',
			count: 48,
			revenue: '৳ 1,42,00,000',
			avgOrder: '৳ 3,20,000',
			color: 'emerald',
			strategy: 'VIP perks & early product access'
		},
		{
			name: 'Loyal Customers',
			count: 142,
			revenue: '৳ 88,50,000',
			avgOrder: '৳ 1,45,000',
			color: 'blue',
			strategy: 'Volume discounts & upsell higher tier bundles'
		},
		{
			name: 'Potential Loyalists (Recent, Mid Spend)',
			count: 96,
			revenue: '৳ 34,20,000',
			avgOrder: '৳ 85,000',
			color: 'cyan',
			strategy: 'Cross-sell complementary categories'
		},
		{
			name: 'At Risk (High Value, Lapsed >60d)',
			count: 24,
			revenue: '৳ 28,00,000',
			avgOrder: '৳ 2,10,000',
			color: 'amber',
			strategy: 'Dedicated account manager outreach'
		},
		{
			name: 'Hibernating (Low Spend, Lapsed >120d)',
			count: 85,
			revenue: '৳ 11,80,000',
			avgOrder: '৳ 32,000',
			color: 'rose',
			strategy: 'Re-engagement promotional campaign'
		}
	];
</script>

<svelte:head><title>Customer Segmentation — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">RFM Customer Segmentation</h1>
			<p class="page-subtitle">
				Behavioral clusters based on purchase recency, order frequency, and monetary spend
			</p>
		</div>
		<div class="header-actions">
			<a href="/sales/customers" class="btn-primary">
				<Send size={15} />
				Launch Targeted Campaign
			</a>
		</div>
	</header>

	<div class="segment-grid">
		{#each segments as seg}
			<div class="card seg-card border-{seg.color}">
				<div class="seg-top">
					<h3 class="seg-name">{seg.name}</h3>
					<span class="count-badge">{seg.count} SMEs</span>
				</div>
				<div class="seg-metrics">
					<div class="metric-item">
						<span class="m-lbl">Total Segment Revenue</span>
						<span class="m-val">{seg.revenue}</span>
					</div>
					<div class="metric-item">
						<span class="m-lbl">Avg Order Value</span>
						<span class="m-val">{seg.avgOrder}</span>
					</div>
				</div>
				<div class="seg-strategy">
					<span class="strat-lbl"><Sparkles size={13} /> Recommended Strategy:</span>
					<p class="strat-text">{seg.strategy}</p>
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

	.segment-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: 16px;
		margin-top: 20px;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.seg-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.seg-top {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 10px;
	}
	.seg-name {
		font-size: 0.875rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
	}
	.count-badge {
		font-size: 0.6875rem;
		font-weight: 700;
		background: var(--color-bg-primary);
		padding: 2px 8px;
		border-radius: 999px;
		border: 1px solid var(--color-border);
		color: var(--color-text-secondary);
		white-space: nowrap;
	}

	.seg-metrics {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 10px;
		background: var(--color-bg-primary);
		padding: 10px 12px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
	}
	.metric-item {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}
	.m-lbl {
		font-size: 0.625rem;
		text-transform: uppercase;
		color: var(--color-text-tertiary);
	}
	.m-val {
		font-size: 0.875rem;
		font-weight: 700;
		color: var(--color-text-primary);
		font-variant-numeric: tabular-nums;
	}

	.seg-strategy {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}
	.strat-lbl {
		font-weight: 600;
		color: var(--color-accent);
		display: flex;
		align-items: center;
		gap: 4px;
		margin-bottom: 2px;
	}
	.strat-text {
		margin: 0;
		line-height: 1.4;
		color: var(--color-text-secondary);
	}
</style>
