<!--
  CRM Retention — Churn risk prediction, cohort retention curves, and winback tracking.
-->
<script lang="ts">
	import { UserCheck, AlertTriangle, ArrowDownRight, RefreshCcw, PhoneCall } from '@lucide/svelte';

	const retentionStats = [
		{ label: '90-Day Retention Rate', value: '86.4%', sub: '+3.2% vs previous quarter', good: true },
		{ label: 'Monthly Churn Rate', value: '2.1%', sub: 'Industry benchmark: 3.5%', good: true },
		{ label: 'Accounts At Risk (>60d inactive)', value: '18 accounts', sub: 'Est. ৳ 34 Lakh exposure', good: false },
		{ label: 'Winback Success Rate', value: '54.2%', sub: 'Re-activated in last 30d', good: true },
	];

	const atRiskAccounts = [
		{ id: '1', name: 'Comilla Ceramics Ltd.', lastOrder: '64 days ago', ltv: '৳ 7,24,000', contact: 'M. A. Matin (+8801912-222222)', risk: 'High' },
		{ id: '2', name: 'Tangail Handicrafts Export', lastOrder: '72 days ago', ltv: '৳ 4,35,000', contact: 'Begum Rokeya (+8801612-333333)', risk: 'High' },
		{ id: '3', name: 'Barishal Marine Supplies', lastOrder: '58 days ago', ltv: '৳ 26,70,000', contact: 'Capt. Enamul (+8801512-333333)', risk: 'Medium' },
		{ id: '4', name: 'Jessore Food Processing', lastOrder: '61 days ago', ltv: '৳ 9,56,000', contact: 'Tareq Aziz (+8801712-333333)', risk: 'High' },
	];
</script>

<svelte:head><title>Customer Retention & Churn — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Customer Retention & Churn Risk</h1>
			<p class="page-subtitle">Track account longevity, identify drop-off risk, and trigger proactive winback</p>
		</div>
	</header>

	<div class="metrics-grid">
		{#each retentionStats as s}
			<div class="card stat-card">
				<span class="stat-lbl">{s.label}</span>
				<span class="stat-val">{s.value}</span>
				<span class="stat-sub" class:good={s.good} class:bad={!s.good}>{s.sub}</span>
			</div>
		{/each}
	</div>

	<div class="card">
		<div class="card-header">
			<h2 class="card-title">High-Risk Inactive Accounts (Attention Required)</h2>
			<span class="alert-tag"><AlertTriangle size={13} /> 4 Immediate Actions</span>
		</div>
		<table class="data-table">
			<thead>
				<tr>
					<th>Account Name</th>
					<th>Days Inactive</th>
					<th>Historical LTV</th>
					<th>Primary Contact</th>
					<th>Risk Level</th>
					<th>Action</th>
				</tr>
			</thead>
			<tbody>
				{#each atRiskAccounts as acc}
					<tr>
						<td><strong>{acc.name}</strong></td>
						<td><span class="inactive-tag">{acc.lastOrder}</span></td>
						<td class="num font-bold">{acc.ltv}</td>
						<td>{acc.contact}</td>
						<td><span class="risk-badge risk-{acc.risk.toLowerCase()}">{acc.risk}</span></td>
						<td>
							<button class="btn-action">
								<PhoneCall size={13} />
								Call Rep
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 20px 0; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.stat-card { padding: 18px; display: flex; flex-direction: column; gap: 4px; }
	.stat-lbl { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; }
	.stat-val { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); }
	.stat-sub { font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.stat-sub.good { color: var(--color-success); font-weight: 600; }
	.stat-sub.bad { color: var(--color-danger); font-weight: 600; }

	.card-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; border-bottom: 1px solid var(--color-border); }
	.card-title { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }
	.alert-tag { display: inline-flex; align-items: center; gap: 4px; font-size: 0.6875rem; font-weight: 600; color: var(--color-danger); background: color-mix(in srgb, var(--color-danger) 12%, transparent); padding: 3px 8px; border-radius: 999px; }

	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table th { text-align: left; padding: 10px 18px; font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; border-bottom: 1px solid var(--color-border); background: var(--color-bg-primary); }
	.data-table td { padding: 12px 18px; border-bottom: 1px solid var(--color-border); color: var(--color-text-primary); }
	.data-table tr:last-child td { border-bottom: none; }
	.data-table .num { font-variant-numeric: tabular-nums; }
	.font-bold { font-weight: 600; }
	.inactive-tag { color: var(--color-danger); font-weight: 600; }
	.risk-badge { font-size: 0.6875rem; font-weight: 700; padding: 2px 8px; border-radius: 999px; text-transform: uppercase; }
	.risk-high { background: color-mix(in srgb, var(--color-danger) 15%, transparent); color: var(--color-danger); }
	.risk-medium { background: color-mix(in srgb, #f59e0b 15%, transparent); color: #d97706; }
	.btn-action { display: inline-flex; align-items: center; gap: 4px; padding: 5px 10px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.75rem; font-weight: 600; color: var(--color-text-primary); cursor: pointer; }
	.btn-action:hover { border-color: var(--color-accent); color: var(--color-accent); }
</style>
