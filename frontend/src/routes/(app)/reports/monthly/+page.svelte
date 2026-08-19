<!--
  Monthly Reports — Monthly executive summaries, sales and tax reporting.
-->
<script lang="ts">
	import {
		Calendar,
		Download,
		FileText,
		Printer,
		CheckCircle,
		ChevronLeft,
		ChevronRight
	} from '@lucide/svelte';

	let selectedMonth = $state('July 2026');

	const summaryCards = [
		{
			title: 'Total Revenue',
			value: '৳ 32,45,000',
			change: '+11.4% vs last month',
			positive: true
		},
		{
			title: 'Operating Expenses',
			value: '৳ 19,80,000',
			change: '+4.2% vs last month',
			positive: false
		},
		{ title: 'Net Profit', value: '৳ 12,65,000', change: '+24.1% vs last month', positive: true },
		{
			title: 'Tax / VAT Provision',
			value: '৳ 4,86,750',
			change: '15% standard rate',
			positive: true
		}
	];

	const previousReports = [
		{ month: 'June 2026', generated: 'Jul 2, 2026', revenue: '৳ 29,10,000', profit: '৳ 10,20,000' },
		{ month: 'May 2026', generated: 'Jun 2, 2026', revenue: '৳ 28,40,000', profit: '৳ 9,80,000' },
		{ month: 'April 2026', generated: 'May 2, 2026', revenue: '৳ 26,90,000', profit: '৳ 8,95,000' },
		{ month: 'March 2026', generated: 'Apr 2, 2026', revenue: '৳ 31,20,000', profit: '৳ 11,40,000' }
	];
</script>

<svelte:head><title>Monthly Reports — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Monthly Business Reports</h1>
			<p class="page-subtitle">
				Monthly financial statements, performance reviews, and compliance records
			</p>
		</div>
		<div class="header-actions">
			<a href="/documents/export" class="btn-primary">
				<Download size={15} />
				Download Full PDF Report
			</a>
		</div>
	</header>

	<div class="month-selector card">
		<div class="selector-content">
			<div class="selector-icon">
				<Calendar size={18} />
			</div>
			<div class="selector-info">
				<span class="active-month">{selectedMonth} Financial Statement</span>
				<span class="status-indicator"><CheckCircle size={13} /> Finalized & Reconciled</span>
			</div>
		</div>
		<select class="select-month" bind:value={selectedMonth} aria-label="Select report month">
			<option value="July 2026">July 2026</option>
			<option value="June 2026">June 2026</option>
			<option value="May 2026">May 2026</option>
			<option value="April 2026">April 2026</option>
		</select>
	</div>

	<!-- Summaries -->
	<div class="metrics-grid">
		{#each summaryCards as card}
			<div class="card metric-card">
				<span class="metric-title">{card.title}</span>
				<span class="metric-val">{card.value}</span>
				<span class="metric-change" class:positive={card.positive}>{card.change}</span>
			</div>
		{/each}
	</div>

	<!-- History table -->
	<div class="card">
		<div class="card-header">
			<h2 class="card-title">Past Monthly Reports</h2>
		</div>
		<table class="data-table">
			<thead>
				<tr>
					<th>Reporting Period</th>
					<th>Generated Date</th>
					<th>Gross Revenue</th>
					<th>Net Profit</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				{#each previousReports as rep}
					<tr>
						<td><strong>{rep.month}</strong></td>
						<td>{rep.generated}</td>
						<td class="num">{rep.revenue}</td>
						<td class="num font-bold">{rep.profit}</td>
						<td>
							<a href="/documents/export" class="table-link">Download PDF →</a>
						</td>
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

	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.month-selector {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 14px 18px;
		margin: 20px 0 16px;
	}
	.selector-content {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.selector-icon {
		color: var(--color-accent);
	}
	.active-month {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		display: block;
	}
	.status-indicator {
		font-size: 0.6875rem;
		color: var(--color-success);
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-weight: 500;
	}
	.select-month {
		padding: 6px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: 0.8125rem;
	}

	.metrics-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 14px;
		margin-bottom: 20px;
	}
	.metric-card {
		padding: 16px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.metric-title {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
	}
	.metric-val {
		font-size: 1.375rem;
		font-weight: 700;
		color: var(--color-text-primary);
	}
	.metric-change {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.metric-change.positive {
		color: var(--color-success);
		font-weight: 600;
	}

	.card-header {
		padding: 14px 18px;
		border-bottom: 1px solid var(--color-border);
	}
	.card-title {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
	}

	.data-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.8125rem;
	}
	.data-table th {
		text-align: left;
		padding: 10px 18px;
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		text-transform: uppercase;
		border-bottom: 1px solid var(--color-border);
	}
	.data-table td {
		padding: 12px 18px;
		border-bottom: 1px solid var(--color-border);
		color: var(--color-text-primary);
	}
	.data-table tr:last-child td {
		border-bottom: none;
	}
	.data-table .num {
		font-variant-numeric: tabular-nums;
	}
	.font-bold {
		font-weight: 700;
		color: var(--color-success);
	}
	.table-link {
		color: var(--color-accent);
		font-weight: 600;
		text-decoration: none;
		font-size: 0.75rem;
	}
</style>
