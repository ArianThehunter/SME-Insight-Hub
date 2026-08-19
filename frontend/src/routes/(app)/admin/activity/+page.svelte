<!--
  Admin Activity — Real-time team activity feed, system events, and transactions.
-->
<script lang="ts">
	import { Activity, ShoppingCart, Upload, DollarSign, Package, UserCheck, Clock } from '@lucide/svelte';

	const activities = [
		{ id: '1', user: 'Zubair Hossain', action: 'Created new order', detail: 'ORD-2026-031 for Rahman Textiles (৳ 2,45,000)', icon: ShoppingCart, color: 'blue', time: '12 minutes ago' },
		{ id: '2', user: 'Nadia Islam', action: 'Uploaded OCR document', detail: 'INV-2026-0847.pdf processed with 96% confidence', icon: Upload, color: 'accent', time: '45 minutes ago' },
		{ id: '3', user: 'Nadia Islam', action: 'Recorded business expense', detail: 'DESCO electricity bill for August (৳ 12,500)', icon: DollarSign, color: 'rose', time: '1 hour ago' },
		{ id: '4', user: 'Sultana Begum', action: 'Received stock shipment', detail: 'Chittagong Port Traders (+500 pcs Cotton Fabric)', icon: Package, color: 'amber', time: '3 hours ago' },
		{ id: '5', user: 'Rafiq Ahmed', action: 'Approved quarterly statement', detail: 'Q2 2026 Financial Pack published for directors', icon: UserCheck, color: 'emerald', time: '5 hours ago' },
	];
</script>

<svelte:head><title>Activity Stream — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Live Organizational Activity</h1>
			<p class="page-subtitle">Real-time pulse of team operations, order creations, and financial updates</p>
		</div>
	</header>

	<div class="activity-feed">
		{#each activities as act}
			{@const ActIcon = act.icon}
			<div class="card activity-item">
				<div class="act-icon-box bg-{act.color}">
					<ActIcon size={18} />
				</div>
				<div class="act-content">
					<div class="act-header">
						<strong class="act-user">{act.user}</strong>
						<span class="act-action">{act.action}</span>
					</div>
					<p class="act-detail">{act.detail}</p>
					<span class="act-time"><Clock size={12} /> {act.time}</span>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.activity-feed { display: flex; flex-direction: column; gap: 12px; margin-top: 20px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.activity-item { padding: 16px; display: flex; align-items: flex-start; gap: 14px; }
	.act-icon-box { width: 38px; height: 38px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0; }
	.bg-blue { background: #3b82f6; }
	.bg-accent { background: var(--color-accent); }
	.bg-rose { background: #f43f5e; }
	.bg-amber { background: #f59e0b; }
	.bg-emerald { background: #10b981; }

	.act-content { flex: 1; }
	.act-header { display: flex; align-items: center; gap: 6px; font-size: 0.875rem; margin-bottom: 2px; }
	.act-user { color: var(--color-text-primary); }
	.act-action { color: var(--color-text-secondary); font-weight: 500; }
	.act-detail { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 0 0 6px; }
	.act-time { font-size: 0.6875rem; color: var(--color-text-tertiary); display: inline-flex; align-items: center; gap: 4px; }
</style>
