<!--
  Stock Alerts page — Interactive alert management with Reorder trigger, rule creator modal, and resolution.
-->
<script lang="ts">
	import {
		AlertOctagon,
		AlertTriangle,
		CheckCircle,
		Search,
		Settings,
		ArrowUpRight,
		Plus,
		ShieldCheck,
		Download,
		X,
		ShoppingCart,
		CheckCheck
	} from '@lucide/svelte';

	interface AlertItem {
		sku: string;
		name: string;
		stock: number;
		reorder: number;
		severity: 'critical' | 'warning' | 'resolved';
		supplier: string;
		date: string;
	}

	let searchQuery = $state('');
	let severityFilter = $state('all');

	let alertList = $state<AlertItem[]>([
		{
			sku: 'PRD-005',
			name: 'Artisan Leather Bag',
			stock: 0,
			reorder: 15,
			severity: 'critical',
			supplier: 'Dhaka Leather Craft',
			date: '2026-06-17 08:32 AM'
		},
		{
			sku: 'PRD-010',
			name: 'Jute Tote Bag (Eco)',
			stock: 0,
			reorder: 50,
			severity: 'critical',
			supplier: 'Dhaka Leather Craft',
			date: '2026-06-16 02:15 PM'
		},
		{
			sku: 'PRD-007',
			name: 'Pabna Yogurt 500g',
			stock: 8,
			reorder: 100,
			severity: 'warning',
			supplier: 'Bengal Agro Ltd',
			date: '2026-06-18 11:04 AM'
		},
		{
			sku: 'PRD-003',
			name: 'Bengal Spice Mix Set',
			stock: 15,
			reorder: 50,
			severity: 'warning',
			supplier: 'Bengal Agro Ltd',
			date: '2026-06-18 09:45 AM'
		},
		{
			sku: 'PRD-011',
			name: 'Nakshi Kantha Bedcover',
			stock: 22,
			reorder: 10,
			severity: 'resolved',
			supplier: 'Chittagong Textiles Co.',
			date: '2026-06-15 05:30 PM'
		}
	]);

	// Modals
	let showRuleModal = $state(false);
	let reorderSuccessMsg = $state('');

	// Rule form
	let newRuleName = $state('');
	let newRuleSKU = $state('');
	let newThreshold = $state<number>(20);
	let newSupplier = $state('Bengal Agro Ltd');

	const filtered = $derived(
		alertList.filter((a) => {
			const matchSearch =
				!searchQuery ||
				a.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.sku.toLowerCase().includes(searchQuery.toLowerCase());
			const matchSeverity = severityFilter === 'all' || a.severity === severityFilter;
			return matchSearch && matchSeverity;
		})
	);

	const counts = $derived({
		critical: alertList.filter((a) => a.severity === 'critical').length,
		warning: alertList.filter((a) => a.severity === 'warning').length,
		resolved: alertList.filter((a) => a.severity === 'resolved').length,
		total: alertList.filter((a) => a.severity !== 'resolved').length
	});

	function resolveAlert(sku: string) {
		alertList = alertList.map((a) => (a.sku === sku ? { ...a, severity: 'resolved' } : a));
	}

	function triggerReorder(sku: string, supplier: string) {
		reorderSuccessMsg = `Purchase Order drafted with ${supplier} for SKU ${sku}!`;
		setTimeout(() => (reorderSuccessMsg = ''), 3500);
	}

	function handleCreateRule(e: Event) {
		e.preventDefault();
		if (!newRuleName || !newRuleSKU) return;

		alertList = [
			{
				sku: newRuleSKU,
				name: newRuleName,
				stock: 5,
				reorder: newThreshold,
				severity: 'warning',
				supplier: newSupplier,
				date: 'Just now'
			},
			...alertList
		];

		showRuleModal = false;
		newRuleName = '';
		newRuleSKU = '';
	}

	function exportAlertsCSV() {
		const headers =
			'SKU,Product_Name,Current_Stock,Reorder_Threshold,Severity,Supplier,Timestamp\n';
		const rows = filtered
			.map(
				(a) =>
					`"${a.sku}","${a.name}",${a.stock},${a.reorder},"${a.severity}","${a.supplier}","${a.date}"`
			)
			.join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_stock_alerts_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Stock Alerts — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Inventory Stock Alerts</h1>
			<p class="page-subtitle">
				Monitor out-of-stock items, critical safety thresholds, and automated vendor PO triggers
			</p>
		</div>
		<div class="header-actions">
			<button class="btn-create" onclick={() => (showRuleModal = true)}>
				<Plus size={16} /> Create Alert Rule
			</button>
		</div>
	</header>

	{#if reorderSuccessMsg}
		<div class="card toast-banner animate-fade-in">
			<CheckCheck size={18} />
			<span>{reorderSuccessMsg}</span>
		</div>
	{/if}

	<!-- Metrics -->
	<div class="summary-grid">
		<div class="card summary-card danger">
			<AlertOctagon size={20} class="text-danger" />
			<div class="summary-details">
				<span class="summary-val text-danger">{counts.critical}</span>
				<span class="summary-label">Critical (Out of Stock)</span>
			</div>
		</div>
		<div class="card summary-card warning">
			<AlertTriangle size={20} class="text-warning" />
			<div class="summary-details">
				<span class="summary-val text-warning">{counts.warning}</span>
				<span class="summary-label">Low Stock Warning</span>
			</div>
		</div>
		<div class="card summary-card success">
			<CheckCircle size={20} class="text-success" />
			<div class="summary-details">
				<span class="summary-val text-success">{counts.resolved}</span>
				<span class="summary-label">Resolved / Restocked</span>
			</div>
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input
				type="text"
				bind:value={searchQuery}
				placeholder="Search alerts by SKU or title..."
				class="search-input"
				aria-label="Search alerts"
			/>
		</div>
		<div class="toolbar-right">
			<select bind:value={severityFilter} class="filter-select" aria-label="Filter severity">
				<option value="all">All Severities</option>
				<option value="critical">Critical</option>
				<option value="warning">Warning</option>
				<option value="resolved">Resolved</option>
			</select>
			<button
				class="btn-icon"
				onclick={exportAlertsCSV}
				title="Export CSV"
				aria-label="Export stock alerts CSV"
			>
				<Download size={16} />
			</button>
		</div>
	</div>

	<!-- Table -->
	<div class="table-card animate-fade-in-up">
		<div class="table-scroll">
			<table class="data-table">
				<thead>
					<tr>
						<th>SKU</th>
						<th>Product Item</th>
						<th>Current Stock</th>
						<th>Reorder Point</th>
						<th>Severity</th>
						<th>Supplier / Vendor</th>
						<th>Triggered On</th>
						<th>Quick Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each filtered as a}
						<tr>
							<td><code class="sku-tag">{a.sku}</code></td>
							<td><strong>{a.name}</strong></td>
							<td class="num-cell"
								><span class="stock-val text-{a.stock === 0 ? 'danger' : 'warning'} font-bold"
									>{a.stock} units</span
								></td
							>
							<td class="num-cell">{a.reorder} units</td>
							<td>
								<span class="badge badge-{a.severity}">{a.severity}</span>
							</td>
							<td>{a.supplier}</td>
							<td class="text-muted">{a.date}</td>
							<td>
								<div class="btn-row">
									{#if a.severity !== 'resolved'}
										<button
											class="btn-action-accent"
											onclick={() => triggerReorder(a.sku, a.supplier)}
											title="Draft PO"
										>
											<ShoppingCart size={13} /> Reorder
										</button>
										<button
											class="btn-action"
											onclick={() => resolveAlert(a.sku)}
											title="Mark as resolved"
										>
											<CheckCircle size={13} />
										</button>
									{:else}
										<span class="text-success font-semibold">Restocked</span>
									{/if}
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>

	<!-- Create Alert Rule Modal -->
	{#if showRuleModal}
		<div class="modal-backdrop" onclick={() => (showRuleModal = false)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="add-rule-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<h2 id="add-rule-title" class="modal-title">Define Stock Alert Rule</h2>
					<button
						class="btn-close"
						onclick={() => (showRuleModal = false)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleCreateRule} class="modal-form">
					<div class="form-group">
						<label for="ar-name">Product Name</label>
						<input
							id="ar-name"
							type="text"
							placeholder="e.g. Basmati Rice 5kg"
							bind:value={newRuleName}
							required
						/>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ar-sku">SKU Code</label>
							<input
								id="ar-sku"
								type="text"
								placeholder="PRD-019"
								bind:value={newRuleSKU}
								required
							/>
						</div>
						<div class="form-group">
							<label for="ar-thresh">Threshold Level</label>
							<input
								id="ar-thresh"
								type="number"
								placeholder="25"
								bind:value={newThreshold}
								min="1"
								required
							/>
						</div>
					</div>
					<div class="form-group">
						<label for="ar-supp">Preferred Supplier</label>
						<select id="ar-supp" bind:value={newSupplier}>
							<option value="Bengal Agro Ltd">Bengal Agro Ltd</option>
							<option value="Chittagong Textiles Co.">Chittagong Textiles Co.</option>
							<option value="Dhaka Leather Craft">Dhaka Leather Craft</option>
							<option value="Sylhet Tea Estates">Sylhet Tea Estates</option>
						</select>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => (showRuleModal = false)}
							>Cancel</button
						>
						<button type="submit" class="btn-primary">Save Rule</button>
					</div>
				</form>
			</div>
		</div>
	{/if}
</div>

<style>
	.page {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
	.page-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
	}
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

	.btn-create,
	.btn-primary {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 8px 16px;
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
		padding: 8px 16px;
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		font-weight: 600;
		cursor: pointer;
		background: var(--color-bg-primary);
		color: var(--color-text-primary);
		border: 1px solid var(--color-border);
	}

	.toast-banner {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 12px 18px;
		background: color-mix(in srgb, var(--color-success) 12%, transparent);
		border-color: var(--color-success);
		color: var(--color-success);
		font-weight: 600;
		font-size: 0.8125rem;
	}

	.summary-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 14px;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.summary-card {
		padding: 16px;
		display: flex;
		align-items: center;
		gap: 14px;
	}
	.summary-details {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}
	.summary-label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
	}
	.summary-val {
		font-size: 1.5rem;
		font-weight: 700;
		font-variant-numeric: tabular-nums;
	}
	.text-danger {
		color: var(--color-danger);
	}
	.text-warning {
		color: #d97706;
	}
	.text-success {
		color: var(--color-success);
	}
	.font-bold {
		font-weight: 700;
	}
	.font-semibold {
		font-weight: 600;
	}

	.toolbar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 12px;
	}
	.search-box {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 12px;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		flex: 1;
		max-width: 380px;
		color: var(--color-text-tertiary);
	}
	.search-input {
		background: none;
		border: none;
		outline: none;
		font-size: 0.8125rem;
		color: var(--color-text-primary);
		width: 100%;
	}
	.toolbar-right {
		display: flex;
		gap: 8px;
	}
	.filter-select {
		padding: 8px 12px;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: 0.8125rem;
	}
	.btn-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-secondary);
		cursor: pointer;
	}
	.btn-icon:hover {
		border-color: var(--color-accent);
		color: var(--color-accent);
	}

	.table-card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		overflow: hidden;
	}
	.table-scroll {
		overflow-x: auto;
	}
	.data-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.8125rem;
	}
	.data-table th {
		text-align: left;
		padding: 10px 16px;
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		text-transform: uppercase;
		background: var(--color-bg-primary);
		border-bottom: 1px solid var(--color-border);
	}
	.data-table td {
		padding: 12px 16px;
		border-bottom: 1px solid var(--color-border);
		color: var(--color-text-primary);
	}
	.data-table tr:last-child td {
		border-bottom: none;
	}
	.sku-tag {
		font-family: monospace;
		font-size: 0.75rem;
		background: var(--color-bg-primary);
		padding: 2px 6px;
		border-radius: 4px;
		border: 1px solid var(--color-border);
		color: var(--color-accent);
	}
	.num-cell {
		font-variant-numeric: tabular-nums;
	}
	.text-muted {
		color: var(--color-text-tertiary);
	}

	.badge {
		display: inline-flex;
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
		text-transform: capitalize;
	}
	.badge-critical {
		background: color-mix(in srgb, var(--color-danger) 15%, transparent);
		color: var(--color-danger);
	}
	.badge-warning {
		background: color-mix(in srgb, #f59e0b 15%, transparent);
		color: #d97706;
	}
	.badge-resolved {
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}

	.btn-row {
		display: flex;
		align-items: center;
		gap: 6px;
	}
	.btn-action-accent {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		padding: 4px 10px;
		background: var(--color-accent);
		color: white;
		border: none;
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
	}
	.btn-action {
		display: inline-flex;
		align-items: center;
		padding: 4px 8px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		cursor: pointer;
	}
	.btn-action:hover {
		border-color: var(--color-success);
		color: var(--color-success);
	}

	/* Modals */
	.modal-backdrop {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.65);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 100;
		backdrop-filter: blur(4px);
	}
	.modal-card {
		width: 100%;
		max-width: 500px;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 24px;
		display: flex;
		flex-direction: column;
		gap: 16px;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
	}
	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
	}
	.modal-title {
		font-size: 1.125rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
	}
	.btn-close {
		background: none;
		border: none;
		color: var(--color-text-tertiary);
		cursor: pointer;
		padding: 2px;
	}
	.btn-close:hover {
		color: var(--color-danger);
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
	.modal-footer {
		display: flex;
		justify-content: flex-end;
		gap: 8px;
		margin-top: 8px;
	}
</style>
