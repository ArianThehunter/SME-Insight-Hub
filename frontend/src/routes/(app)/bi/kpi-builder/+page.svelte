<!--
  KPI Builder — Configure custom SME performance metrics, targets, and formula rules.
-->
<script lang="ts">
	import { Target, Plus, Sliders, CheckCircle2, Save, Trash2, Gauge, Zap } from '@lucide/svelte';

	interface CustomKPI {
		id: string;
		name: string;
		formula: string;
		target: string;
		current: string;
		status: 'on_track' | 'at_risk' | 'exceeded';
		cadence: string;
	}

	let kpis = $state<CustomKPI[]>([
		{
			id: '1',
			name: 'Order Fulfilment Velocity',
			formula: 'Shipped Orders / Total Orders (7d)',
			target: '95%',
			current: '92.4%',
			status: 'on_track',
			cadence: 'Weekly'
		},
		{
			id: '2',
			name: 'Cash Flow Buffer',
			formula: 'Liquid Balance / Avg Daily Outflow',
			target: '45 days',
			current: '52 days',
			status: 'exceeded',
			cadence: 'Daily'
		},
		{
			id: '3',
			name: 'Inventory Turnover Days',
			formula: 'Avg Inventory / (COGS / 365)',
			target: '30 days',
			current: '38 days',
			status: 'at_risk',
			cadence: 'Monthly'
		},
		{
			id: '4',
			name: 'Customer Repeat Ratio',
			formula: 'Returning Customers / Total Active Customers',
			target: '40%',
			current: '44.8%',
			status: 'exceeded',
			cadence: 'Monthly'
		}
	]);

	let showModal = $state(false);
	let newName = $state('');
	let newFormula = $state('');
	let newTarget = $state('');
	let newCadence = $state('Monthly');

	function addKPI(e: Event) {
		e.preventDefault();
		if (!newName || !newTarget) return;
		kpis = [
			...kpis,
			{
				id: crypto.randomUUID(),
				name: newName,
				formula: newFormula || 'Custom Formula',
				target: newTarget,
				current: '0%',
				status: 'on_track',
				cadence: newCadence
			}
		];
		newName = '';
		newFormula = '';
		newTarget = '';
		showModal = false;
	}

	function removeKPI(id: string) {
		kpis = kpis.filter((k) => k.id !== id);
	}
</script>

<svelte:head><title>KPI Builder — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Custom KPI Builder</h1>
			<p class="page-subtitle">
				Formulate, track, and automate custom operational and financial targets
			</p>
		</div>
		<div class="header-actions">
			<button class="btn-primary" onclick={() => (showModal = true)}>
				<Plus size={16} />
				Create Custom KPI
			</button>
		</div>
	</header>

	<div class="kpi-grid">
		{#each kpis as kpi}
			<div class="card kpi-card">
				<div class="kpi-top">
					<div class="kpi-icon-wrap">
						<Gauge size={18} />
					</div>
					<span class="status-tag status-{kpi.status}">{kpi.status.replace('_', ' ')}</span>
				</div>
				<h3 class="kpi-title">{kpi.name}</h3>
				<p class="kpi-formula"><code>{kpi.formula}</code></p>
				<div class="kpi-values">
					<div class="val-box">
						<span class="val-lbl">Current</span>
						<span class="val-num current">{kpi.current}</span>
					</div>
					<div class="val-divider">/</div>
					<div class="val-box">
						<span class="val-lbl">Target</span>
						<span class="val-num target">{kpi.target}</span>
					</div>
				</div>
				<div class="kpi-footer">
					<span class="cadence-tag">Cadence: {kpi.cadence}</span>
					<button class="btn-icon danger" onclick={() => removeKPI(kpi.id)} aria-label="Delete KPI">
						<Trash2 size={14} />
					</button>
				</div>
			</div>
		{/each}
	</div>

	{#if showModal}
		<div class="modal-backdrop" onclick={() => (showModal = false)} role="presentation">
			<div
				class="modal-card card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="modal-title"
				tabindex="-1"
			>
				<h2 id="modal-title" class="modal-title">Define New Target Metric</h2>
				<form onsubmit={addKPI} class="modal-form">
					<div class="form-group">
						<label for="kpi-name">KPI Name</label>
						<input
							id="kpi-name"
							type="text"
							placeholder="e.g. On-Time Delivery %"
							bind:value={newName}
							required
						/>
					</div>
					<div class="form-group">
						<label for="kpi-formula">Formula / Calculation</label>
						<input
							id="kpi-formula"
							type="text"
							placeholder="e.g. Delivered On Time / Total Orders"
							bind:value={newFormula}
						/>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="kpi-target">Target Threshold</label>
							<input
								id="kpi-target"
								type="text"
								placeholder="e.g. 98%"
								bind:value={newTarget}
								required
							/>
						</div>
						<div class="form-group">
							<label for="kpi-cadence">Evaluation Cadence</label>
							<select id="kpi-cadence" bind:value={newCadence}>
								<option value="Daily">Daily</option>
								<option value="Weekly">Weekly</option>
								<option value="Monthly">Monthly</option>
								<option value="Quarterly">Quarterly</option>
							</select>
						</div>
					</div>
					<div class="modal-actions">
						<button type="button" class="btn-secondary" onclick={() => (showModal = false)}
							>Cancel</button
						>
						<button type="submit" class="btn-primary">Save Metric</button>
					</div>
				</form>
			</div>
		</div>
	{/if}
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
		background: var(--color-bg-primary);
		color: var(--color-text-primary);
		border: 1px solid var(--color-border);
	}

	.kpi-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 16px;
		margin-top: 20px;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.kpi-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.kpi-top {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.kpi-icon-wrap {
		color: var(--color-accent);
		background: color-mix(in srgb, var(--color-accent) 10%, transparent);
		width: 32px;
		height: 32px;
		border-radius: var(--radius-sm);
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.status-tag {
		font-size: 0.6875rem;
		font-weight: 600;
		text-transform: uppercase;
		padding: 2px 8px;
		border-radius: 999px;
	}
	.status-on_track {
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}
	.status-exceeded {
		background: color-mix(in srgb, var(--color-accent) 15%, transparent);
		color: var(--color-accent);
	}
	.status-at_risk {
		background: color-mix(in srgb, #f59e0b 15%, transparent);
		color: #d97706;
	}

	.kpi-title {
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
	}
	.kpi-formula code {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		background: var(--color-bg-primary);
		padding: 2px 6px;
		border-radius: 4px;
		display: block;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.kpi-values {
		display: flex;
		align-items: center;
		justify-content: space-around;
		background: var(--color-bg-primary);
		padding: 10px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
	}
	.val-box {
		text-align: center;
	}
	.val-lbl {
		font-size: 0.625rem;
		text-transform: uppercase;
		color: var(--color-text-tertiary);
		display: block;
	}
	.val-num {
		font-size: 1.125rem;
		font-weight: 700;
	}
	.val-num.current {
		color: var(--color-text-primary);
	}
	.val-num.target {
		color: var(--color-accent);
	}
	.val-divider {
		color: var(--color-text-tertiary);
		font-weight: 300;
	}
	.kpi-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: auto;
	}
	.cadence-tag {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.btn-icon {
		background: none;
		border: none;
		cursor: pointer;
		color: var(--color-text-tertiary);
		padding: 4px;
		border-radius: 4px;
		transition: color 0.15s;
	}
	.btn-icon.danger:hover {
		color: var(--color-danger);
	}

	/* Modal */
	.modal-backdrop {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.6);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 100;
	}
	.modal-card {
		width: 100%;
		max-width: 480px;
		padding: 24px;
	}
	.modal-title {
		font-size: 1.125rem;
		font-weight: 700;
		margin: 0 0 16px;
		color: var(--color-text-primary);
	}
	.modal-form {
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.form-group {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.form-group label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
	}
	.form-group input,
	.form-group select {
		padding: 8px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: 0.8125rem;
	}
	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 12px;
	}
	.modal-actions {
		display: flex;
		justify-content: flex-end;
		gap: 8px;
		margin-top: 8px;
	}
</style>
