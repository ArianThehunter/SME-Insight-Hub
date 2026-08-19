<!--
  Admin Permissions — Granular RBAC permission matrix (Read, Write, Delete, Export).
-->
<script lang="ts">
	import { KeyRound, Check, X, Shield, Save } from '@lucide/svelte';

	const modules = [
		{ name: 'Sales & Orders', owner: [true, true, true, true], manager: [true, true, false, true], accountant: [true, false, false, true], sales: [true, true, false, false], viewer: [true, false, false, false] },
		{ name: 'Inventory & Warehouses', owner: [true, true, true, true], manager: [true, true, false, true], accountant: [true, false, false, true], sales: [true, false, false, false], viewer: [true, false, false, false] },
		{ name: 'Finance & Invoices', owner: [true, true, true, true], manager: [true, true, false, true], accountant: [true, true, true, true], sales: [false, false, false, false], viewer: [true, false, false, false] },
		{ name: 'Document OCR & Upload', owner: [true, true, true, true], manager: [true, true, false, true], accountant: [true, true, false, true], sales: [true, true, false, false], viewer: [true, false, false, false] },
		{ name: 'User & Team Management', owner: [true, true, true, true], manager: [true, false, false, false], accountant: [false, false, false, false], sales: [false, false, false, false], viewer: [false, false, false, false] },
		{ name: 'Tax / NBR Filings', owner: [true, true, true, true], manager: [true, false, false, true], accountant: [true, true, false, true], sales: [false, false, false, false], viewer: [true, false, false, false] },
	];
</script>

<svelte:head><title>Permission Matrix — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Granular Permissions Matrix</h1>
			<p class="page-subtitle">Inspect privilege scopes (Read / Write / Delete / Export) across organizational roles</p>
		</div>
	</header>

	<div class="card matrix-card">
		<table class="matrix-table">
			<thead>
				<tr>
					<th>Module / Resource</th>
					<th>Owner</th>
					<th>Manager</th>
					<th>Accountant</th>
					<th>Sales Officer</th>
					<th>Viewer</th>
				</tr>
			</thead>
			<tbody>
				{#each modules as m}
					<tr>
						<td><strong>{m.name}</strong></td>
						{#each [m.owner, m.manager, m.accountant, m.sales, m.viewer] as perms}
							<td class="perm-cell">
								<div class="perm-badges">
									<span class="p-tag" class:active={perms[0]} title="Read">R</span>
									<span class="p-tag" class:active={perms[1]} title="Write">W</span>
									<span class="p-tag" class:active={perms[2]} title="Delete">D</span>
									<span class="p-tag" class:active={perms[3]} title="Export">X</span>
								</div>
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); margin-top: 20px; overflow: hidden; }

	.matrix-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.matrix-table th { text-align: left; padding: 12px 18px; font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; border-bottom: 1px solid var(--color-border); background: var(--color-bg-primary); }
	.matrix-table td { padding: 14px 18px; border-bottom: 1px solid var(--color-border); color: var(--color-text-primary); }
	.matrix-table tr:last-child td { border-bottom: none; }

	.perm-badges { display: flex; gap: 4px; }
	.p-tag { width: 22px; height: 22px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 0.625rem; font-weight: 700; background: var(--color-bg-primary); color: var(--color-text-tertiary); border: 1px solid var(--color-border); }
	.p-tag.active { background: color-mix(in srgb, var(--color-success) 18%, transparent); color: var(--color-success); border-color: var(--color-success); }
</style>
