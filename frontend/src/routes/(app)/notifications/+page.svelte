<!--
  Notifications Center — View all unread and historical notifications, invoice updates, and stock alerts.
-->
<script lang="ts">
	import {
		Bell,
		CheckCircle2,
		AlertTriangle,
		FileText,
		ShoppingCart,
		Shield,
		CheckCheck
	} from '@lucide/svelte';

	interface NotificationItem {
		id: string;
		title: string;
		desc: string;
		time: string;
		type: 'invoice' | 'stock' | 'order' | 'security';
		read: boolean;
	}

	let notifs = $state<NotificationItem[]>([
		{
			id: '1',
			title: 'Invoice INV-2026-0847 OCR Completed',
			desc: 'AI extracted 6 line items with 96% confidence from Chittagong Port Traders bill.',
			time: '12 minutes ago',
			type: 'invoice',
			read: false
		},
		{
			id: '2',
			title: 'Critical Low Stock Warning',
			desc: 'Wireless Mouse MX-200 is down to 4 units (reorder threshold is 10 units).',
			time: '1 hour ago',
			type: 'stock',
			read: false
		},
		{
			id: '3',
			title: 'New High-Value Sales Order',
			desc: 'Bogura Steel Corp. placed ORD-2026-009 for ৳ 12,50,000.',
			time: '3 hours ago',
			type: 'order',
			read: false
		},
		{
			id: '4',
			title: 'Quarterly Executive Summary Ready',
			desc: 'Q2 2026 Financial Deck has been automatically computed and saved to Reports.',
			time: '5 hours ago',
			type: 'invoice',
			read: true
		},
		{
			id: '5',
			title: 'New Customer Registered',
			desc: 'Sylhet Tea Gardens account opened by Mrs. Nusrat Jahan.',
			time: '1 day ago',
			type: 'order',
			read: true
		},
		{
			id: '6',
			title: 'Security Audit Sign-In Verified',
			desc: 'Successful login from Banani, Dhaka IP 103.114.152.12.',
			time: '2 days ago',
			type: 'security',
			read: true
		}
	]);

	function markAllRead() {
		notifs = notifs.map((n) => ({ ...n, read: true }));
	}

	function toggleRead(id: string) {
		notifs = notifs.map((n) => (n.id === id ? { ...n, read: !n.read } : n));
	}
</script>

<svelte:head><title>Notification Center — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Notifications & System Alerts</h1>
			<p class="page-subtitle">
				Real-time alerts for OCR documents, stock levels, sales orders, and audit updates
			</p>
		</div>
		<div class="header-actions">
			<button class="btn-secondary" onclick={markAllRead}>
				<CheckCheck size={16} />
				Mark All as Read
			</button>
		</div>
	</header>

	<div class="notif-list">
		{#each notifs as n}
			<div
				class="card notif-card"
				class:unread={!n.read}
				onclick={() => toggleRead(n.id)}
				role="button"
				tabindex="0"
				onkeydown={(e) => {
					if (e.key === 'Enter') toggleRead(n.id);
				}}
			>
				<div class="notif-icon-box type-{n.type}">
					{#if n.type === 'invoice'}<FileText size={18} />
					{:else if n.type === 'stock'}<AlertTriangle size={18} />
					{:else if n.type === 'order'}<ShoppingCart size={18} />
					{:else}<Shield size={18} />{/if}
				</div>
				<div class="notif-body">
					<div class="notif-header-row">
						<h3 class="notif-title">{n.title}</h3>
						<span class="notif-time">{n.time}</span>
					</div>
					<p class="notif-desc">{n.desc}</p>
				</div>
				{#if !n.read}
					<span class="unread-dot" title="Unread notification"></span>
				{/if}
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
	.btn-secondary {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 7px 14px;
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		font-weight: 600;
		cursor: pointer;
		background: var(--color-bg-secondary);
		color: var(--color-text-primary);
		border: 1px solid var(--color-border);
	}

	.notif-list {
		display: flex;
		flex-direction: column;
		gap: 10px;
		margin-top: 20px;
		max-width: 800px;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.notif-card {
		padding: 16px 20px;
		display: flex;
		align-items: flex-start;
		gap: 14px;
		cursor: pointer;
		transition: all 0.15s;
	}
	.notif-card.unread {
		background: color-mix(in srgb, var(--color-accent) 6%, var(--color-bg-secondary));
		border-color: color-mix(in srgb, var(--color-accent) 30%, var(--color-border));
	}
	.notif-card:hover {
		border-color: var(--color-accent);
	}

	.notif-icon-box {
		width: 38px;
		height: 38px;
		border-radius: var(--radius-md);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}
	.type-invoice {
		background: color-mix(in srgb, var(--color-accent) 15%, transparent);
		color: var(--color-accent);
	}
	.type-stock {
		background: color-mix(in srgb, #f59e0b 15%, transparent);
		color: #d97706;
	}
	.type-order {
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}
	.type-security {
		background: color-mix(in srgb, #8b5cf6 15%, transparent);
		color: #8b5cf6;
	}

	.notif-body {
		flex: 1;
	}
	.notif-header-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 4px;
	}
	.notif-title {
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
	}
	.notif-time {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.notif-desc {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		margin: 0;
		line-height: 1.4;
	}

	.unread-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--color-accent);
		flex-shrink: 0;
		margin-top: 6px;
	}
</style>
