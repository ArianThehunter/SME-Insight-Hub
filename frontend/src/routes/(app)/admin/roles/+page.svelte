<!--
  Admin Roles — Define organizational roles, access hierarchy, and assigned staff.
-->
<script lang="ts">
	import { Shield, Plus, Key, Users, CheckCircle2, Lock } from '@lucide/svelte';

	const systemRoles = [
		{ name: 'Organization Owner', slug: 'org_owner', members: 1, desc: 'Unrestricted administrative access to all organizational resources, billing, and API tokens.', isSystem: true },
		{ name: 'General Manager', slug: 'manager', members: 2, desc: 'Operational oversight across sales, inventory, finance approvals, and reporting.', isSystem: true },
		{ name: 'Accountant', slug: 'accountant', members: 3, desc: 'Full finance & tax management, expense logging, invoice creation, and bank statement reconciliations.', isSystem: true },
		{ name: 'Sales Officer', slug: 'sales_officer', members: 6, desc: 'Customer pipeline management, quotation generation, and order processing.', isSystem: true },
		{ name: 'Inventory Officer', slug: 'inventory_officer', members: 4, desc: 'Warehouse stock movement, purchase order receiving, and low stock threshold alerts.', isSystem: true },
		{ name: 'Auditor / Viewer', slug: 'viewer', members: 2, desc: 'Read-only visibility into financial and compliance reports.', isSystem: true },
	];
</script>

<svelte:head><title>Role Management — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Role-Based Access Control (RBAC)</h1>
			<p class="page-subtitle">Configure administrative hierarchy and granular privilege scopes</p>
		</div>
		<div class="header-actions">
			<a href="/admin/permissions" class="btn-primary">
				<Key size={15} />
				View Permission Matrix
			</a>
		</div>
	</header>

	<div class="roles-grid">
		{#each systemRoles as r}
			<div class="card role-card">
				<div class="role-top">
					<div class="role-icon-box">
						<Shield size={18} />
					</div>
					{#if r.isSystem}
						<span class="sys-badge"><Lock size={11} /> System Role</span>
					{/if}
				</div>
				<h3 class="role-name">{r.name}</h3>
				<span class="role-slug"><code>{r.slug}</code></span>
				<p class="role-desc">{r.desc}</p>
				<div class="role-footer">
					<span class="members-count"><Users size={13} /> {r.members} assigned members</span>
					<a href="/admin/permissions" class="edit-link">Configure →</a>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-accent); color: white; border: none; text-decoration: none; }

	.roles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; margin-top: 20px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.role-card { padding: 18px; display: flex; flex-direction: column; gap: 10px; }
	.role-top { display: flex; justify-content: space-between; align-items: center; }
	.role-icon-box { width: 34px; height: 34px; border-radius: var(--radius-sm); background: color-mix(in srgb, var(--color-accent) 12%, transparent); color: var(--color-accent); display: flex; align-items: center; justify-content: center; }
	.sys-badge { display: inline-flex; align-items: center; gap: 4px; font-size: 0.6875rem; font-weight: 600; background: var(--color-bg-primary); padding: 2px 8px; border-radius: 999px; border: 1px solid var(--color-border); color: var(--color-text-secondary); }

	.role-name { font-size: 0.9375rem; font-weight: 700; color: var(--color-text-primary); margin: 0; }
	.role-slug code { font-size: 0.6875rem; background: var(--color-bg-primary); padding: 2px 6px; border-radius: 4px; color: var(--color-text-tertiary); }
	.role-desc { font-size: 0.75rem; color: var(--color-text-secondary); line-height: 1.4; margin: 0; }
	.role-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 10px; border-top: 1px solid var(--color-border); font-size: 0.75rem; }
	.members-count { display: inline-flex; align-items: center; gap: 4px; color: var(--color-text-tertiary); }
	.edit-link { color: var(--color-accent); font-weight: 600; text-decoration: none; }
</style>
