<!--
  Admin Audit — Compliance and security audit trail for user authentication, exports, and data modifications.
-->
<script lang="ts">
	import { ScrollText, Shield, Search, Filter, Download } from '@lucide/svelte';

	let searchQuery = $state('');

	const auditLogs = [
		{
			id: 'LOG-8842',
			actor: 'Rafiq Ahmed (admin@acmecorp.com)',
			action: 'USER_LOGIN',
			target: 'Auth / Session Token',
			ip: '103.114.152.12 (Dhaka)',
			time: '2026-08-19 23:42:15'
		},
		{
			id: 'LOG-8841',
			actor: 'Nadia Islam (nadia@acmecorp.com)',
			action: 'DOCUMENT_UPLOAD',
			target: 'INV-2026-0847.pdf',
			ip: '103.114.152.18 (Dhaka)',
			time: '2026-08-19 22:15:02'
		},
		{
			id: 'LOG-8840',
			actor: 'Zubair Hossain (zubair@acmecorp.com)',
			action: 'ORDER_CREATE',
			target: 'ORD-2026-031 (৳ 2,45,000)',
			ip: '103.205.180.45 (Chittagong)',
			time: '2026-08-19 20:30:11'
		},
		{
			id: 'LOG-8839',
			actor: 'Rafiq Ahmed (admin@acmecorp.com)',
			action: 'DATA_EXPORT',
			target: 'customers_full_export.csv',
			ip: '103.114.152.12 (Dhaka)',
			time: '2026-08-19 18:05:44'
		},
		{
			id: 'LOG-8838',
			actor: 'Sultana Begum (sultana@acmecorp.com)',
			action: 'STOCK_ADJUST',
			target: 'SKU: FAB-CTN-001 (+500 yards)',
			ip: '103.114.152.20 (Narayanganj)',
			time: '2026-08-19 16:22:30'
		}
	];

	const filtered = $derived(
		auditLogs.filter(
			(l) =>
				!searchQuery ||
				l.actor.toLowerCase().includes(searchQuery.toLowerCase()) ||
				l.action.toLowerCase().includes(searchQuery.toLowerCase()) ||
				l.target.toLowerCase().includes(searchQuery.toLowerCase())
		)
	);
</script>

<svelte:head><title>Audit Logs — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Security & Compliance Audit Trail</h1>
			<p class="page-subtitle">
				Immutable chronological log of administrative actions, user logins, and exports
			</p>
		</div>
		<div class="header-actions">
			<a href="/documents/export" class="btn-secondary">
				<Download size={15} />
				Export Audit Log
			</a>
		</div>
	</header>

	<div class="card filter-bar">
		<div class="search-box">
			<Search size={14} />
			<input
				type="text"
				placeholder="Search by actor, action, or target..."
				bind:value={searchQuery}
				aria-label="Search audit logs"
			/>
		</div>
	</div>

	<div class="card table-card">
		<table class="data-table">
			<thead>
				<tr>
					<th>Timestamp</th>
					<th>Event ID</th>
					<th>Actor</th>
					<th>Action</th>
					<th>Target Resource</th>
					<th>IP & Location</th>
				</tr>
			</thead>
			<tbody>
				{#each filtered as log}
					<tr>
						<td class="text-muted font-mono">{log.time}</td>
						<td><code class="code-tag">{log.id}</code></td>
						<td><strong>{log.actor}</strong></td>
						<td><span class="action-badge">{log.action}</span></td>
						<td>{log.target}</td>
						<td class="text-muted">{log.ip}</td>
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
		text-decoration: none;
	}

	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.filter-bar {
		padding: 12px 16px;
		margin: 20px 0 16px;
	}
	.search-box {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-tertiary);
		max-width: 400px;
	}
	.search-box input {
		flex: 1;
		background: none;
		border: none;
		outline: none;
		font-size: 0.8125rem;
		color: var(--color-text-primary);
	}

	.table-card {
		overflow: hidden;
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

	.font-mono {
		font-family: monospace;
		font-size: 0.75rem;
	}
	.code-tag {
		font-family: monospace;
		font-size: 0.75rem;
		background: var(--color-bg-primary);
		padding: 2px 6px;
		border-radius: 4px;
		border: 1px solid var(--color-border);
	}
	.action-badge {
		font-size: 0.6875rem;
		font-weight: 700;
		background: var(--color-bg-primary);
		padding: 2px 8px;
		border-radius: 4px;
		border: 1px solid var(--color-border);
		color: var(--color-accent);
	}
	.text-muted {
		color: var(--color-text-tertiary);
	}
</style>
