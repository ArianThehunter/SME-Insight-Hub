<!--
  BI Forecasting — Predictive revenue, expense, and cash runway projections with scenario planning.
-->
<script lang="ts">
	import {
		Telescope,
		TrendingUp,
		Sparkles,
		Sliders,
		AlertCircle,
		ArrowUpRight,
		DollarSign
	} from '@lucide/svelte';

	let growthScenario = $state('moderate'); // conservative, moderate, aggressive

	const projections = $derived(
		{
			conservative: {
				rev: '৳ 3,10,00,000',
				profit: '৳ 98,00,000',
				runway: '8.5 months',
				growthPct: '+9%'
			},
			moderate: {
				rev: '৳ 3,55,00,000',
				profit: '৳ 1,22,00,000',
				runway: '11.2 months',
				growthPct: '+25%'
			},
			aggressive: {
				rev: '৳ 4,10,00,000',
				profit: '৳ 1,55,00,000',
				runway: '14.0 months',
				growthPct: '+44%'
			}
		}[growthScenario]
	);

	const monthlyProjections = [
		{
			month: 'Sep 2026',
			projected: '৳ 31,50,000',
			expectedExpenses: '৳ 19,20,000',
			confidence: '94%'
		},
		{
			month: 'Oct 2026',
			projected: '৳ 34,20,000',
			expectedExpenses: '৳ 20,10,000',
			confidence: '90%'
		},
		{
			month: 'Nov 2026',
			projected: '৳ 36,80,000',
			expectedExpenses: '৳ 21,50,000',
			confidence: '86%'
		},
		{
			month: 'Dec 2026',
			projected: '৳ 42,00,000',
			expectedExpenses: '৳ 24,00,000',
			confidence: '82%'
		},
		{
			month: 'Jan 2027',
			projected: '৳ 38,50,000',
			expectedExpenses: '৳ 22,00,000',
			confidence: '78%'
		},
		{
			month: 'Feb 2027',
			projected: '৳ 39,20,000',
			expectedExpenses: '৳ 22,80,000',
			confidence: '75%'
		}
	];
</script>

<svelte:head><title>AI Forecasting — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">AI Predictive Forecasting</h1>
			<p class="page-subtitle">
				Machine-learning forecast modeling for revenue, expenses, and cash liquidity
			</p>
		</div>
		<div class="header-actions">
			<div class="scenario-toggle">
				<button
					class="scenario-btn"
					class:active={growthScenario === 'conservative'}
					onclick={() => (growthScenario = 'conservative')}>Conservative</button
				>
				<button
					class="scenario-btn"
					class:active={growthScenario === 'moderate'}
					onclick={() => (growthScenario = 'moderate')}>Moderate</button
				>
				<button
					class="scenario-btn"
					class:active={growthScenario === 'aggressive'}
					onclick={() => (growthScenario = 'aggressive')}>Aggressive</button
				>
			</div>
		</div>
	</header>

	<!-- Projections summary -->
	<div class="metrics-grid">
		<div class="metric-card card">
			<span class="metric-label">Projected Annual Revenue</span>
			<span class="metric-value">{projections?.rev}</span>
			<span class="badge badge-success"
				><ArrowUpRight size={14} /> {projections?.growthPct} YoY</span
			>
		</div>
		<div class="metric-card card">
			<span class="metric-label">Estimated Net Profit</span>
			<span class="metric-value">{projections?.profit}</span>
			<span class="metric-sub">Based on 34.5% avg margin</span>
		</div>
		<div class="metric-card card">
			<span class="metric-label">Estimated Cash Runway</span>
			<span class="metric-value">{projections?.runway}</span>
			<span class="metric-sub">Under selected scenario</span>
		</div>
	</div>

	<!-- Monthly Table -->
	<div class="card">
		<div class="card-header">
			<h2 class="card-title">Next 6 Months Projections (BDT)</h2>
			<span class="ai-badge"><Sparkles size={13} /> ML Model v1.4</span>
		</div>
		<table class="data-table">
			<thead>
				<tr>
					<th>Forecast Period</th>
					<th>Projected Inflow</th>
					<th>Expected Outflow</th>
					<th>Estimated Net Cash</th>
					<th>Confidence Interval</th>
				</tr>
			</thead>
			<tbody>
				{#each monthlyProjections as m}
					<tr>
						<td><strong>{m.month}</strong></td>
						<td class="num success-text">{m.projected}</td>
						<td class="num danger-text">{m.expectedExpenses}</td>
						<td class="num">৳ 12,30,000</td>
						<td><span class="conf-pill">{m.confidence}</span></td>
					</tr>
				{/each}
			</tbody>
		</table>
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

	.scenario-toggle {
		display: flex;
		background: var(--color-bg-secondary);
		padding: 3px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
	}
	.scenario-btn {
		background: none;
		border: none;
		padding: 6px 14px;
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		cursor: pointer;
		border-radius: var(--radius-sm);
		transition: all 0.15s;
	}
	.scenario-btn.active {
		background: var(--color-accent);
		color: white;
	}

	.metrics-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 14px;
		margin: 20px 0;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 18px;
	}
	.metric-card {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.metric-label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
	}
	.metric-value {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text-primary);
	}
	.metric-sub {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.badge-success {
		display: inline-flex;
		align-items: center;
		gap: 2px;
		font-size: 0.75rem;
		font-weight: 600;
		padding: 2px 6px;
		border-radius: 999px;
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
		width: fit-content;
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 14px;
	}
	.card-title {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
	}
	.ai-badge {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-size: 0.6875rem;
		font-weight: 600;
		color: var(--color-accent);
		background: color-mix(in srgb, var(--color-accent) 12%, transparent);
		padding: 3px 8px;
		border-radius: 999px;
	}

	.data-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.8125rem;
	}
	.data-table th {
		text-align: left;
		padding: 8px 10px;
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		text-transform: uppercase;
		border-bottom: 1px solid var(--color-border);
	}
	.data-table td {
		padding: 12px 10px;
		border-bottom: 1px solid var(--color-border);
		color: var(--color-text-primary);
	}
	.data-table tr:last-child td {
		border-bottom: none;
	}
	.data-table .num {
		font-variant-numeric: tabular-nums;
	}
	.success-text {
		color: var(--color-success);
		font-weight: 600;
	}
	.danger-text {
		color: var(--color-danger);
	}
	.conf-pill {
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		color: var(--color-text-secondary);
	}
</style>
