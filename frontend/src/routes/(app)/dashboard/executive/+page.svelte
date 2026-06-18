<!--
  Executive Summary page — Executive overview of SME business health, AI suggestions, CAC/LTV, and metrics.
-->
<script lang="ts">
	import { BarChart3, Brain, ArrowUpRight, TrendingUp, Target, HeartPulse, Sparkles } from '@lucide/svelte';

	const qDetails = [
		{ label: 'Revenue', q1: 1450000, q2: 1890000, growth: 30.3 },
		{ label: 'Gross Profit', q1: 1080000, q2: 1430000, growth: 32.4 },
		{ label: 'Net Income', q1: 210000, q2: 308000, growth: 46.6 },
	];

	const aiInsights = [
		{ type: 'opportunity', text: 'Gross Profit margins are strong at 76.1% due to fabric cost optimization. Reinvest 10% in marketing.' },
		{ type: 'warning', text: 'Logistics costs rose 12% this month due to emergency shipments. Centralizing inventory in Rajshahi can save ৳18,000/mo.' },
		{ type: 'success', text: 'LTV to CAC ratio is at 10.7x (excellent). Ideal range for scaling ad-spend on digital channels.' }
	];
</script>

<svelte:head><title>Executive Summary — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Executive Summary</h1>
			<p class="page-subtitle">Cross-module operational and financial performance summary for company executives</p>
		</div>
	</header>

	<!-- Business Health Metrics -->
	<div class="summary-grid">
		<div class="summary-card health-good">
			<div class="card-top">
				<HeartPulse size={20} class="text-success" />
				<span class="badge success">EXCELLENT</span>
			</div>
			<span class="summary-val">Health Score: 94%</span>
			<span class="summary-label">Based on margin, liquidity, and growth metrics</span>
		</div>

		<div class="summary-card">
			<div class="card-top">
				<Target size={20} class="text-accent" />
				<span class="badge info">10.7x Ratio</span>
			</div>
			<span class="summary-val">LTV : CAC Ratio</span>
			<span class="summary-label">LTV: ৳4,800 / CAC: ৳450</span>
		</div>

		<div class="summary-card">
			<div class="card-top">
				<TrendingUp size={20} class="text-success" />
				<span class="badge success">+18.2%</span>
			</div>
			<span class="summary-val">MoM Growth Rate</span>
			<span class="summary-label">Average revenue growth over last 3 months</span>
		</div>
	</div>

	<!-- Main Executive Grid -->
	<div class="content-grid animate-fade-in-up">
		<!-- Left: Performance Comparison -->
		<div class="details-card">
			<h3 class="card-title"><BarChart3 size={16} /> QoQ Financial Comparison (Q1 vs Q2)</h3>
			<div class="comparison-table-wrapper">
				<table class="comparison-table">
					<thead>
						<tr>
							<th>Metric</th>
							<th>Q1 2026</th>
							<th>Q2 2026</th>
							<th>Growth MoM/QoQ</th>
						</tr>
					</thead>
					<tbody>
						{#each qDetails as row}
							<tr>
								<td class="metric-label">{row.label}</td>
								<td class="value-cell">৳ {row.q1.toLocaleString()}</td>
								<td class="value-cell">৳ {row.q2.toLocaleString()}</td>
								<td class="growth-cell text-success">
									<ArrowUpRight size={14} class="inline-icon" /> +{row.growth}%
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

		<!-- Right: AI-Generated Strategic Insights -->
		<div class="insights-card">
			<div class="card-header-with-icon">
				<Brain size={18} class="text-accent" />
				<h3 class="card-title">AI Copilot Business Insights</h3>
			</div>
			<p class="insights-desc">Automated analysis highlighting optimizations, risks, and recommendations.</p>

			<div class="insight-list">
				{#each aiInsights as insight}
					<div class="insight-item {insight.type}">
						<div class="insight-status">
							{#if insight.type === 'opportunity'}
								<Sparkles size={14} class="text-accent" />
							{:else if insight.type === 'warning'}
								<span class="dot warning"></span>
							{:else}
								<span class="dot success"></span>
							{/if}
						</div>
						<p class="insight-text">{insight.text}</p>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
	@media (max-width: 768px) { .summary-grid { grid-template-columns: 1fr; } }
	
	.summary-card { display: flex; flex-direction: column; align-items: flex-start; gap: 8px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-card.health-good { border-left: 4px solid var(--color-success); }
	
	.card-top { width: 100%; display: flex; justify-content: space-between; align-items: center; }
	.summary-val { font-size: 1.375rem; font-weight: 700; color: var(--color-text-primary); margin-top: 6px; }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.625rem; font-weight: 700; text-transform: uppercase; }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.info { background: var(--color-accent-muted); color: var(--color-accent); }

	.content-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px; }
	@media (max-width: 992px) { .content-grid { grid-template-columns: 1fr; } }

	.details-card, .insights-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px; }
	
	.card-title { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); margin: 0; display: flex; align-items: center; gap: 6px; }
	
	.card-header-with-icon { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
	.insights-desc { font-size: 0.75rem; color: var(--color-text-secondary); margin: 0 0 16px; }

	.comparison-table-wrapper { overflow-x: auto; margin-top: 16px; }
	.comparison-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.comparison-table th { padding: 10px 14px; text-align: left; font-weight: 600; color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border); background: var(--color-bg-tertiary); }
	.comparison-table td { padding: 12px 14px; border-bottom: 1px solid var(--color-border-subtle); }
	.metric-label { font-weight: 600; color: var(--color-text-primary); }
	.value-cell { font-family: var(--font-mono); }
	.growth-cell { font-weight: 600; display: flex; align-items: center; gap: 4px; }
	.inline-icon { display: inline-block; }

	.insight-list { display: flex; flex-direction: column; gap: 12px; }
	.insight-item { display: flex; gap: 10px; padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border-subtle); background: var(--color-bg-tertiary); }
	.insight-item.opportunity { border-left: 3px solid var(--color-accent); }
	.insight-item.warning { border-left: 3px solid var(--color-warning); }
	.insight-item.success { border-left: 3px solid var(--color-success); }
	
	.insight-status { display: flex; align-items: flex-start; padding-top: 2px; }
	.dot { width: 8px; height: 8px; border-radius: var(--radius-full); }
	.dot.warning { background: var(--color-warning); }
	.dot.success { background: var(--color-success); }
	
	.insight-text { font-size: 0.75rem; color: var(--color-text-secondary); margin: 0; line-height: 1.45; }
</style>
