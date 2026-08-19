<!--
  Annual Reports — Comprehensive fiscal year financials, balance sheet summary, and NBR tax filing returns.
-->
<script lang="ts">
	import { CalendarRange, Download, ShieldCheck, FileCheck, CheckCircle2 } from '@lucide/svelte';

	const annualYears = [
		{
			year: 'FY 2025 - 2026 (Jul 25 - Jun 26)',
			revenue: '৳ 3,24,40,000',
			profit: '৳ 1,22,60,000',
			taxPaid: '৳ 18,39,000',
			auditStatus: 'Ready for Filing'
		},
		{
			year: 'FY 2024 - 2025 (Jul 24 - Jun 25)',
			revenue: '৳ 2,68,20,000',
			profit: '৳ 94,50,000',
			taxPaid: '৳ 14,17,500',
			auditStatus: 'Filed & Certified'
		},
		{
			year: 'FY 2023 - 2024 (Jul 23 - Jun 24)',
			revenue: '৳ 2,12,00,000',
			profit: '৳ 72,10,000',
			taxPaid: '৳ 10,81,500',
			auditStatus: 'Filed & Certified'
		}
	];
</script>

<svelte:head><title>Annual Reports — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Annual Audited Reports</h1>
			<p class="page-subtitle">
				Fiscal year financial statements and statutory tax filing documents (July - June)
			</p>
		</div>
		<div class="header-actions">
			<a href="/documents/export" class="btn-primary">
				<Download size={15} />
				Export FY 2025-26 Tax Audit Pack
			</a>
		</div>
	</header>

	<div class="card annual-card">
		<div class="card-header">
			<h2 class="card-title">Fiscal Year Historical Returns</h2>
		</div>
		<table class="data-table">
			<thead>
				<tr>
					<th>Fiscal Year (Bangladesh)</th>
					<th>Gross Turnover</th>
					<th>Net Pre-tax Profit</th>
					<th>VAT & Corporate Tax</th>
					<th>NBR Filing Status</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				{#each annualYears as yr}
					<tr>
						<td><strong>{yr.year}</strong></td>
						<td class="num">{yr.revenue}</td>
						<td class="num font-bold">{yr.profit}</td>
						<td class="num">{yr.taxPaid}</td>
						<td><span class="status-badge"><ShieldCheck size={13} /> {yr.auditStatus}</span></td>
						<td><a href="/documents/export" class="table-link">Download Audit Pack →</a></td>
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
		margin-top: 20px;
		overflow: hidden;
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
		background: var(--color-bg-primary);
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
	.status-badge {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-size: 0.6875rem;
		padding: 2px 8px;
		border-radius: 999px;
		background: color-mix(in srgb, var(--color-success) 12%, transparent);
		color: var(--color-success);
		font-weight: 600;
	}
	.table-link {
		color: var(--color-accent);
		font-weight: 600;
		text-decoration: none;
		font-size: 0.75rem;
	}
</style>
