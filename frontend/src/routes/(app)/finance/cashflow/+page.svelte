<!--
  Cash Flow page — Visualizations and summaries of inflows, outflows, and net cash balances.
-->
<script lang="ts">
	import { TrendingUp, ArrowUpRight, ArrowDownRight, DollarSign, Wallet, Calendar, ShieldCheck } from '@lucide/svelte';

	const cashFlowData = [
		{ month: 'Jan 2026', inflow: 450000, outflow: 380000, balance: 800000 },
		{ month: 'Feb 2026', inflow: 520000, outflow: 410000, balance: 910000 },
		{ month: 'Mar 2026', inflow: 490000, outflow: 430000, balance: 970000 },
		{ month: 'Apr 2026', inflow: 610000, outflow: 480000, balance: 1100000 },
		{ month: 'May 2026', inflow: 680000, outflow: 520000, balance: 1260000 },
		{ month: 'Jun 2026', inflow: 720000, outflow: 550000, balance: 1430000 },
	];

	// Extract current metrics
	const currentMonth = cashFlowData[cashFlowData.length - 1];
	const prevMonth = cashFlowData[cashFlowData.length - 2];

	const metrics = {
		balance: currentMonth.balance,
		netFlow: currentMonth.inflow - currentMonth.outflow,
		inflow: currentMonth.inflow,
		outflow: currentMonth.outflow,
		growthRate: Math.round(((currentMonth.inflow - currentMonth.outflow) - (prevMonth.inflow - prevMonth.outflow)) / (prevMonth.inflow - prevMonth.outflow) * 100),
		runway: 24, // months
	};

	// SVG chart properties
	const chartWidth = 500;
	const chartHeight = 200;
	const padding = 30;

	// Scale helpers
	const maxAmount = Math.max(...cashFlowData.map(d => Math.max(d.inflow, d.outflow))) * 1.1;

	function getX(index: number) {
		return padding + (index * (chartWidth - padding * 2) / (cashFlowData.length - 1));
	}

	function getY(amount: number) {
		return chartHeight - padding - (amount * (chartHeight - padding * 2) / maxAmount);
	}

	// Balance Line Chart Path
	const balancePath = cashFlowData.map((d, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(d.balance / 2)}`).join(' ');
</script>

<svelte:head><title>Cash Flow — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Cash Flow Analytics</h1>
			<p class="page-subtitle">Track liquid assets, cash runway, inflows, and operational cash burns</p>
		</div>
	</header>

	<!-- KPI Grid -->
	<div class="summary-grid">
		<div class="summary-card">
			<span class="summary-val">৳ {metrics.balance.toLocaleString()}</span>
			<span class="summary-label">Liquid Cash Balance</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-success">৳ +{metrics.netFlow.toLocaleString()}</span>
			<span class="summary-label">Net Flow (June)</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-success">+{metrics.growthRate}% <TrendingUp size={16} class="inline-icon" /></span>
			<span class="summary-label">Net Growth MoM</span>
		</div>
		<div class="summary-card">
			<span class="summary-val">{metrics.runway} Months</span>
			<span class="summary-label">Calculated Cash Runway</span>
		</div>
	</div>

	<!-- Chart Grid -->
	<div class="charts-grid animate-fade-in-up">
		<!-- Inflow vs Outflow Bar Chart -->
		<div class="chart-card">
			<h3 class="chart-title">Cash Inflow vs Outflow (Last 6 Months)</h3>
			<div class="chart-container">
				<svg viewBox="0 0 {chartWidth} {chartHeight}" class="svg-chart">
					<!-- Grid lines -->
					{#each [0, 0.25, 0.5, 0.75, 1] as pct}
						{@const y = getY(maxAmount * pct)}
						<line x1={padding} y1={y} x2={chartWidth - padding} y2={y} class="grid-line" />
					{/each}

					<!-- Bar Chart Content -->
					{#each cashFlowData as d, i}
						{@const x = getX(i)}
						{@const barWidth = 18}
						<!-- Inflow Bar (Green) -->
						<rect 
							x={x - barWidth - 2} 
							y={getY(d.inflow)} 
							width={barWidth} 
							height={chartHeight - padding - getY(d.inflow)} 
							class="bar inflow" 
							rx="2"
						/>
						<!-- Outflow Bar (Red) -->
						<rect 
							x={x + 2} 
							y={getY(d.outflow)} 
							width={barWidth} 
							height={chartHeight - padding - getY(d.outflow)} 
							class="bar outflow" 
							rx="2"
						/>
						<!-- Month Labels -->
						<text x={x} y={chartHeight - 8} class="chart-axis-label text-center">{d.month.split(' ')[0]}</text>
					{/each}
				</svg>
			</div>
			<div class="chart-legend">
				<span class="legend-item"><span class="legend-color inflow"></span> Inflow</span>
				<span class="legend-item"><span class="legend-color outflow"></span> Outflow</span>
			</div>
		</div>

		<!-- Cumulative Cash Balance Line Chart -->
		<div class="chart-card">
			<h3 class="chart-title">Liquid Cash Trend</h3>
			<div class="chart-container">
				<svg viewBox="0 0 {chartWidth} {chartHeight}" class="svg-chart">
					<!-- Grid lines -->
					{#each [0, 0.25, 0.5, 0.75, 1] as pct}
						{@const y = getY(maxAmount * pct)}
						<line x1={padding} y1={y} x2={chartWidth - padding} y2={y} class="grid-line" />
					{/each}

					<!-- Trend Line -->
					<path d={balancePath} class="trend-path" fill="none" />

					<!-- Data Points -->
					{#each cashFlowData as d, i}
						{@const x = getX(i)}
						{@const y = getY(d.balance / 2)}
						<circle cx={x} cy={y} r="4" class="trend-node" />
						<text x={x} y={chartHeight - 8} class="chart-axis-label text-center">{d.month.split(' ')[0]}</text>
					{/each}
				</svg>
			</div>
			<div class="chart-legend">
				<span class="legend-item"><span class="legend-color trend"></span> Cumulative Balance</span>
			</div>
		</div>
	</div>

	<!-- Inflow/Outflow Breakdown Details -->
	<div class="details-grid animate-fade-in-up">
		<div class="details-card">
			<h3 class="details-title text-success"><ArrowUpRight size={16} /> Cash Inflow Channels</h3>
			<ul class="breakdown-list">
				<li><span class="label">Product Sales (B2C + Retail)</span> <span class="val">৳ 480,000</span></li>
				<li><span class="label">B2B Wholesale Accounts</span> <span class="val">৳ 190,000</span></li>
				<li><span class="label">Direct Customer Pre-orders</span> <span class="val">৳ 50,000</span></li>
			</ul>
		</div>

		<div class="details-card">
			<h3 class="details-title text-danger"><ArrowDownRight size={16} /> Cash Outflow Channels</h3>
			<ul class="breakdown-list">
				<li><span class="label">Inventory & Material Procurement</span> <span class="val">৳ 380,000</span></li>
				<li><span class="label">Rent, Power & Overheads</span> <span class="val">৳ 85,000</span></li>
				<li><span class="label">Salaries & Contractor Fees</span> <span class="val">৳ 62,000</span></li>
				<li><span class="label">Marketing & Logistics</span> <span class="val">৳ 23,000</span></li>
			</ul>
		</div>
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
	@media (max-width: 768px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 480px) { .summary-grid { grid-template-columns: 1fr; } }
	
	.summary-card { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-val { font-size: 1.375rem; font-weight: 700; color: var(--color-text-primary); display: flex; align-items: center; gap: 4px; }
	.summary-val.text-success { color: var(--color-success); }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.inline-icon { color: var(--color-success); }

	.charts-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
	@media (max-width: 992px) { .charts-grid { grid-template-columns: 1fr; } }
	
	.chart-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px; display: flex; flex-direction: column; }
	.chart-title { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); margin: 0 0 16px; }
	.chart-container { flex: 1; min-height: 200px; display: flex; align-items: center; }
	
	.svg-chart { width: 100%; height: 200px; overflow: visible; }
	.grid-line { stroke: var(--color-border-subtle); stroke-width: 1; stroke-dasharray: 2 2; }
	
	.bar { transition: height 0.6s ease, y 0.6s ease; }
	.bar.inflow { fill: var(--color-success); opacity: 0.85; }
	.bar.outflow { fill: var(--color-danger); opacity: 0.85; }
	
	.trend-path { stroke: var(--color-accent); stroke-width: 2.5; stroke-linecap: round; }
	.trend-node { fill: var(--color-bg-secondary); stroke: var(--color-accent); stroke-width: 2; }
	
	.chart-axis-label { font-size: 0.625rem; fill: var(--color-text-tertiary); text-anchor: middle; font-weight: 500; }
	
	.chart-legend { display: flex; justify-content: center; gap: 16px; margin-top: 12px; font-size: 0.75rem; color: var(--color-text-secondary); }
	.legend-item { display: flex; align-items: center; gap: 6px; }
	.legend-color { width: 12px; height: 12px; border-radius: 3px; }
	.legend-color.inflow { background: var(--color-success); }
	.legend-color.outflow { background: var(--color-danger); }
	.legend-color.trend { background: var(--color-accent); height: 4px; border-radius: var(--radius-full); width: 16px; }

	.details-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
	@media (max-width: 768px) { .details-grid { grid-template-columns: 1fr; } }
	
	.details-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px; }
	.details-title { font-size: 0.875rem; font-weight: 600; margin: 0 0 16px; display: flex; align-items: center; gap: 6px; }
	.details-title.text-success { color: var(--color-success); }
	.details-title.text-danger { color: var(--color-danger); }
	
	.breakdown-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }
	.breakdown-list li { display: flex; justify-content: space-between; font-size: 0.8125rem; padding-bottom: 8px; border-bottom: 1px solid var(--color-border-subtle); }
	.breakdown-list li:last-child { border-bottom: none; padding-bottom: 0; }
	.breakdown-list .label { color: var(--color-text-secondary); }
	.breakdown-list .val { font-weight: 600; color: var(--color-text-primary); }
</style>
