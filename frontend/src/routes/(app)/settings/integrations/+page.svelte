<!--
  Settings Integrations — Third-party connectors (bKash, Nagad, Supabase, Tally, QuickBooks).
-->
<script lang="ts">
	import { Plug, CheckCircle2, ArrowUpRight, Zap } from '@lucide/svelte';

	interface Integration {
		id: string;
		name: string;
		category: string;
		desc: string;
		icon: string;
		connected: boolean;
	}

	let integrations = $state<Integration[]>([
		{
			id: '1',
			name: 'bKash Merchant Gateway',
			category: 'Payment & MFS',
			desc: 'Sync customer payments, refunds, and daily mobile balance transfers in real-time.',
			icon: '📱',
			connected: true
		},
		{
			id: '2',
			name: 'Nagad Business Portal',
			category: 'Payment & MFS',
			desc: 'Automate post-office digital banking collections and merchant fee reconciliation.',
			icon: '💳',
			connected: true
		},
		{
			id: '3',
			name: 'Supabase Cloud Database',
			category: 'Cloud Storage & DB',
			desc: 'Encrypted PostgreSQL document backup, cold storage, and real-time CDC subscriptions.',
			icon: '⚡',
			connected: false
		},
		{
			id: '4',
			name: 'BRAC Bank Corporate Net Banking',
			category: 'Commercial Bank',
			desc: 'Automated bank statement CSV import and BFTN vendor disbursement feed.',
			icon: '🏦',
			connected: true
		},
		{
			id: '5',
			name: 'Tally Prime / ERP Bridge',
			category: 'Accounting Software',
			desc: 'Two-way sync of ledger accounts, voucher entries, and VAT Mushak journals.',
			icon: '📑',
			connected: false
		},
		{
			id: '6',
			name: 'Upstash Redis Caching',
			category: 'Performance',
			desc: 'Serverless in-memory cache for ultra-low latency dashboard analytics and rate limiting.',
			icon: '🚀',
			connected: false
		}
	]);

	function toggleConnect(id: string) {
		integrations = integrations.map((i) => (i.id === id ? { ...i, connected: !i.connected } : i));
	}
</script>

<svelte:head><title>Integrations — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Third-Party Connectors & Ecosystem</h1>
			<p class="page-subtitle">
				Connect Bangladeshi MFS gateways (bKash, Nagad), commercial banks, and cloud infrastructure
			</p>
		</div>
	</header>

	<div class="integrations-grid">
		{#each integrations as item}
			<div class="card integ-card" class:connected={item.connected}>
				<div class="integ-top">
					<span class="integ-icon">{item.icon}</span>
					{#if item.connected}
						<span class="conn-pill"><CheckCircle2 size={12} /> Connected</span>
					{:else}
						<span class="disc-pill">Not Connected</span>
					{/if}
				</div>
				<h3 class="integ-name">{item.name}</h3>
				<span class="integ-cat">{item.category}</span>
				<p class="integ-desc">{item.desc}</p>
				<div class="integ-footer">
					<button
						class="conn-btn"
						class:active={item.connected}
						onclick={() => toggleConnect(item.id)}
					>
						{item.connected ? 'Disconnect' : 'Connect Gateway'}
					</button>
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

	.integrations-grid {
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
	.integ-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 10px;
		transition: border-color 0.2s;
	}
	.integ-card.connected {
		border-color: color-mix(in srgb, var(--color-success) 40%, var(--color-border));
	}

	.integ-top {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.integ-icon {
		font-size: 1.75rem;
	}
	.conn-pill {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}
	.disc-pill {
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
		background: var(--color-bg-primary);
		color: var(--color-text-tertiary);
		border: 1px solid var(--color-border);
	}

	.integ-name {
		font-size: 0.9375rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
	}
	.integ-cat {
		font-size: 0.6875rem;
		font-weight: 600;
		color: var(--color-accent);
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}
	.integ-desc {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		line-height: 1.4;
		margin: 0;
	}

	.integ-footer {
		margin-top: auto;
		padding-top: 10px;
		border-top: 1px solid var(--color-border);
	}
	.conn-btn {
		width: 100%;
		padding: 7px;
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		border: 1px solid var(--color-border);
		background: var(--color-bg-primary);
		color: var(--color-text-primary);
		transition: all 0.15s;
	}
	.conn-btn:hover {
		border-color: var(--color-accent);
		color: var(--color-accent);
	}
	.conn-btn.active {
		color: var(--color-danger);
		border-color: color-mix(in srgb, var(--color-danger) 40%, transparent);
	}
	.conn-btn.active:hover {
		background: color-mix(in srgb, var(--color-danger) 10%, transparent);
	}
</style>
