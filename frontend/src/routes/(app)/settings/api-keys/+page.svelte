<!--
  Settings API Keys — Developer access tokens and programmatic webhooks.
-->
<script lang="ts">
	import { Key, Plus, Copy, Trash2, CheckCircle2, ShieldAlert } from '@lucide/svelte';

	interface ApiKey {
		id: string;
		name: string;
		tokenMasked: string;
		created: string;
		lastUsed: string;
	}

	let keys = $state<ApiKey[]>([
		{ id: '1', name: 'Production Backend Ingestion', tokenMasked: 'sme_live_9f81a7...4b28', created: 'Aug 1, 2026', lastUsed: '5 minutes ago' },
		{ id: '2', name: 'E-commerce POS Webhook (WooCommerce)', tokenMasked: 'sme_live_3c92e1...8f14', created: 'Jul 15, 2026', lastUsed: '1 hour ago' },
	]);

	let copied = $state(false);

	function copyKey() {
		copied = true;
		setTimeout(() => copied = false, 2000);
	}
</script>

<svelte:head><title>API Keys — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Developer API Keys & Webhooks</h1>
			<p class="page-subtitle">Manage REST API credentials for syncing with external ERPs, POS systems, and ecommerce</p>
		</div>
		<div class="header-actions">
			<button class="btn-primary">
				<Plus size={16} />
				Generate New API Key
			</button>
		</div>
	</header>

	<div class="card warning-card">
		<div class="warn-icon">
			<ShieldAlert size={18} />
		</div>
		<div>
			<strong>Secret Key Security</strong>
			<p>API keys carry full read/write privileges on your organization's records. Keep them confidential and rotate them periodically.</p>
		</div>
	</div>

	<div class="card table-card">
		<table class="data-table">
			<thead>
				<tr>
					<th>Key Label / Name</th>
					<th>Token Prefix</th>
					<th>Created On</th>
					<th>Last Ingestion</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				{#each keys as k}
					<tr>
						<td><strong>{k.name}</strong></td>
						<td><code class="token-code">{k.tokenMasked}</code></td>
						<td>{k.created}</td>
						<td class="text-muted">{k.lastUsed}</td>
						<td>
							<div class="btn-group">
								<button class="btn-icon" onclick={copyKey} title="Copy Key">
									<Copy size={14} />
								</button>
								<button class="btn-icon danger" title="Revoke Key">
									<Trash2 size={14} />
								</button>
							</div>
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
	.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-accent); color: white; border: none; }

	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.warning-card { display: flex; align-items: flex-start; gap: 12px; padding: 14px 18px; margin: 20px 0 16px; background: color-mix(in srgb, #f59e0b 8%, transparent); border-color: color-mix(in srgb, #f59e0b 25%, transparent); }
	.warn-icon { color: #d97706; flex-shrink: 0; margin-top: 2px; }
	.warning-card strong { font-size: 0.8125rem; color: var(--color-text-primary); display: block; margin-bottom: 2px; }
	.warning-card p { font-size: 0.75rem; color: var(--color-text-secondary); margin: 0; line-height: 1.4; }

	.table-card { overflow: hidden; }
	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table th { text-align: left; padding: 10px 18px; font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; border-bottom: 1px solid var(--color-border); background: var(--color-bg-primary); }
	.data-table td { padding: 12px 18px; border-bottom: 1px solid var(--color-border); color: var(--color-text-primary); }
	.data-table tr:last-child td { border-bottom: none; }

	.token-code { font-family: monospace; font-size: 0.75rem; background: var(--color-bg-primary); padding: 2px 8px; border-radius: 4px; border: 1px solid var(--color-border); color: var(--color-accent); }
	.text-muted { color: var(--color-text-tertiary); }
	.btn-group { display: flex; gap: 6px; }
	.btn-icon { background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: 5px; cursor: pointer; color: var(--color-text-secondary); }
	.btn-icon:hover { border-color: var(--color-accent); color: var(--color-accent); }
	.btn-icon.danger:hover { border-color: var(--color-danger); color: var(--color-danger); }
</style>
