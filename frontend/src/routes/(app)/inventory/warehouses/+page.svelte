<!--
  Warehouses page — Interactive warehouse management with Add Warehouse modal, Details dialog, and capacity tracking.
-->
<script lang="ts">
	import {
		Building2,
		Search,
		Plus,
		MapPin,
		Users,
		Package,
		Percent,
		ShieldAlert,
		Download,
		X,
		Eye,
		CheckCircle2
	} from '@lucide/svelte';

	interface WarehouseItem {
		id: string;
		name: string;
		location: string;
		manager: string;
		capacity: number;
		area: number;
		items: number;
		status: 'Active' | 'Near Capacity' | 'Maintenance';
	}

	let searchQuery = $state('');

	let warehouseList = $state<WarehouseItem[]>([
		{
			id: 'WH-001',
			name: 'Dhaka Central Warehouse',
			location: 'Tejgaon I/A, Dhaka',
			manager: 'Farhan Ahmed',
			capacity: 85,
			area: 15000,
			items: 12450,
			status: 'Active'
		},
		{
			id: 'WH-002',
			name: 'Chittagong Port Facility',
			location: 'Halishahar, Chittagong',
			manager: 'Yasmin Chowdhury',
			capacity: 60,
			area: 20000,
			items: 8900,
			status: 'Active'
		},
		{
			id: 'WH-003',
			name: 'Sylhet Regional Depot',
			location: 'Sobhanighat, Sylhet',
			manager: 'Tanvir Rahman',
			capacity: 35,
			area: 8000,
			items: 2100,
			status: 'Active'
		},
		{
			id: 'WH-004',
			name: 'Rajshahi Cold Storage',
			location: 'Sopura, Rajshahi',
			manager: 'Mahbubul Alam',
			capacity: 92,
			area: 10000,
			items: 5400,
			status: 'Near Capacity'
		}
	]);

	// Modals
	let showCreateModal = $state(false);
	let selectedWarehouse = $state<WarehouseItem | null>(null);

	// New warehouse form
	let newName = $state('');
	let newLocation = $state('');
	let newManager = $state('');
	let newArea = $state<number>(10000);

	const filtered = $derived(
		warehouseList.filter((w) => {
			return (
				!searchQuery ||
				w.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				w.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
				w.manager.toLowerCase().includes(searchQuery.toLowerCase())
			);
		})
	);

	const metrics = $derived({
		total: warehouseList.length,
		avgCapacity: Math.round(
			warehouseList.reduce((acc, w) => acc + w.capacity, 0) / (warehouseList.length || 1)
		),
		totalArea: warehouseList.reduce((acc, w) => acc + w.area, 0),
		totalItems: warehouseList.reduce((acc, w) => acc + w.items, 0)
	});

	function capacityColor(capacity: number): string {
		if (capacity >= 90) return 'danger';
		if (capacity >= 75) return 'warning';
		return 'success';
	}

	function handleAddWarehouse(e: Event) {
		e.preventDefault();
		if (!newName) return;

		const count = warehouseList.length + 1;
		const newWh: WarehouseItem = {
			id: `WH-${String(count).padStart(3, '0')}`,
			name: newName,
			location: newLocation || 'Dhaka, Bangladesh',
			manager: newManager || 'Branch Manager',
			capacity: 10,
			area: newArea || 10000,
			items: 0,
			status: 'Active'
		};

		warehouseList = [newWh, ...warehouseList];
		showCreateModal = false;
		newName = '';
		newLocation = '';
	}

	function exportWarehousesCSV() {
		const headers =
			'ID,Warehouse_Name,Location,Manager,Capacity_Pct,Area_SqFt,Total_Items,Status\n';
		const rows = filtered
			.map(
				(w) =>
					`"${w.id}","${w.name}","${w.location}","${w.manager}",${w.capacity},${w.area},${w.items},"${w.status}"`
			)
			.join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_warehouses_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Warehouses — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Warehouses & Storage Facilities</h1>
			<p class="page-subtitle">
				Track storage utilization, depot managers, and inventory distribution
			</p>
		</div>
		<button class="btn-create" onclick={() => (showCreateModal = true)}>
			<Plus size={16} /> Add Warehouse
		</button>
	</header>

	<!-- Summary Cards -->
	<div class="summary-grid">
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><Building2 size={20} /></div>
			<div class="summary-details">
				<span class="summary-val">{metrics.total}</span>
				<span class="summary-label">Total Facilities</span>
			</div>
		</div>
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><Percent size={20} /></div>
			<div class="summary-details">
				<span class="summary-val text-{capacityColor(metrics.avgCapacity)}"
					>{metrics.avgCapacity}%</span
				>
				<span class="summary-label">Average Utilization</span>
			</div>
		</div>
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><Package size={20} /></div>
			<div class="summary-details">
				<span class="summary-val">{metrics.totalItems.toLocaleString()}</span>
				<span class="summary-label">Stored Items</span>
			</div>
		</div>
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><MapPin size={20} /></div>
			<div class="summary-details">
				<span class="summary-val">{metrics.totalArea.toLocaleString()} sqft</span>
				<span class="summary-label">Total Floor Space</span>
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
				placeholder="Search facility name, manager, or district..."
				class="search-input"
				aria-label="Search warehouses"
			/>
		</div>
		<button
			class="btn-icon"
			onclick={exportWarehousesCSV}
			title="Export CSV"
			aria-label="Export warehouses CSV"
		>
			<Download size={16} />
		</button>
	</div>

	<!-- Warehouses Grid -->
	<div class="warehouse-grid">
		{#each filtered as w}
			<div class="card warehouse-card">
				<div class="warehouse-top">
					<div>
						<h3 class="warehouse-name">{w.name}</h3>
						<span class="warehouse-loc"><MapPin size={12} /> {w.location}</span>
					</div>
					<span class="badge badge-{w.status === 'Active' ? 'success' : 'warning'}">{w.status}</span
					>
				</div>

				<div class="capacity-section">
					<div class="capacity-labels">
						<span>Capacity Utilization</span>
						<strong class="text-{capacityColor(w.capacity)}">{w.capacity}%</strong>
					</div>
					<div class="progress-track">
						<div
							class="progress-fill bg-{capacityColor(w.capacity)}"
							style="width: {w.capacity}%"
						></div>
					</div>
				</div>

				<div class="warehouse-specs">
					<div class="spec-row">
						<span>Depot Manager</span>
						<strong>{w.manager}</strong>
					</div>
					<div class="spec-row">
						<span>Floor Space</span>
						<strong>{w.area.toLocaleString()} sqft</strong>
					</div>
					<div class="spec-row">
						<span>Items in Stock</span>
						<strong>{w.items.toLocaleString()} pcs</strong>
					</div>
				</div>

				<div class="warehouse-footer">
					<button class="btn-view" onclick={() => (selectedWarehouse = w)}>
						<Eye size={13} /> View Facility Details
					</button>
				</div>
			</div>
		{/each}
	</div>

	<!-- Warehouse Details Modal -->
	{#if selectedWarehouse}
		<div class="modal-backdrop" onclick={() => (selectedWarehouse = null)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="wh-details-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<div>
						<h2 id="wh-details-title" class="modal-title">{selectedWarehouse.name}</h2>
						<span class="warehouse-loc"><MapPin size={12} /> {selectedWarehouse.location}</span>
					</div>
					<button
						class="btn-close"
						onclick={() => (selectedWarehouse = null)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<div class="modal-body">
					<div class="detail-grid">
						<div class="detail-item">
							<span class="d-lbl">Facility Code</span><span class="d-val"
								>{selectedWarehouse.id}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Depot Manager</span><span class="d-val"
								>{selectedWarehouse.manager}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Utilization</span><span
								class="d-val text-{capacityColor(selectedWarehouse.capacity)} font-bold"
								>{selectedWarehouse.capacity}%</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Floor Area</span><span class="d-val"
								>{selectedWarehouse.area.toLocaleString()} sqft</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Items Stored</span><span class="d-val"
								>{selectedWarehouse.items.toLocaleString()} units</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Operational Status</span><span
								class="badge badge-{selectedWarehouse.status === 'Active' ? 'success' : 'warning'}"
								>{selectedWarehouse.status}</span
							>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button class="btn-primary" onclick={() => (selectedWarehouse = null)}> Done </button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Add Warehouse Modal -->
	{#if showCreateModal}
		<div class="modal-backdrop" onclick={() => (showCreateModal = false)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="add-wh-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<h2 id="add-wh-title" class="modal-title">Register Warehouse Facility</h2>
					<button
						class="btn-close"
						onclick={() => (showCreateModal = false)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleAddWarehouse} class="modal-form">
					<div class="form-group">
						<label for="aw-name">Facility Name</label>
						<input
							id="aw-name"
							type="text"
							placeholder="e.g. Bogura Regional Logistics Hub"
							bind:value={newName}
							required
						/>
					</div>
					<div class="form-group">
						<label for="aw-loc">Location / Address (Bangladesh)</label>
						<input
							id="aw-loc"
							type="text"
							placeholder="e.g. Santahar Road, Bogura"
							bind:value={newLocation}
							required
						/>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="aw-mgr">Depot Manager Name</label>
							<input
								id="aw-mgr"
								type="text"
								placeholder="e.g. Kamal Hossain"
								bind:value={newManager}
							/>
						</div>
						<div class="form-group">
							<label for="aw-area">Floor Space (Sq Ft)</label>
							<input
								id="aw-area"
								type="number"
								placeholder="12000"
								bind:value={newArea}
								min="100"
							/>
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => (showCreateModal = false)}
							>Cancel</button
						>
						<button type="submit" class="btn-primary">Save Facility</button>
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

	.summary-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
	.summary-icon-wrapper {
		width: 42px;
		height: 42px;
		border-radius: var(--radius-md);
		background: color-mix(in srgb, var(--color-accent) 12%, transparent);
		color: var(--color-accent);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
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
		font-size: 1.375rem;
		font-weight: 700;
		color: var(--color-text-primary);
		font-variant-numeric: tabular-nums;
	}
	.text-success {
		color: var(--color-success);
	}
	.text-warning {
		color: #d97706;
	}
	.text-danger {
		color: var(--color-danger);
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

	.warehouse-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: 16px;
	}
	.warehouse-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.warehouse-top {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 8px;
	}
	.warehouse-name {
		font-size: 0.9375rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
	}
	.warehouse-loc {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		display: inline-flex;
		align-items: center;
		gap: 4px;
		margin-top: 2px;
	}

	.badge {
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
	}
	.badge-success {
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}
	.badge-warning {
		background: color-mix(in srgb, #f59e0b 15%, transparent);
		color: #d97706;
	}

	.capacity-section {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.capacity-labels {
		display: flex;
		justify-content: space-between;
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}
	.progress-track {
		height: 6px;
		background: var(--color-border);
		border-radius: 999px;
		overflow: hidden;
	}
	.progress-fill {
		height: 100%;
		border-radius: 999px;
	}
	.bg-success {
		background: var(--color-success);
	}
	.bg-warning {
		background: #f59e0b;
	}
	.bg-danger {
		background: var(--color-danger);
	}

	.warehouse-specs {
		display: flex;
		flex-direction: column;
		gap: 6px;
		background: var(--color-bg-primary);
		padding: 10px 12px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
		font-size: 0.75rem;
	}
	.spec-row {
		display: flex;
		justify-content: space-between;
		color: var(--color-text-secondary);
	}
	.spec-row strong {
		color: var(--color-text-primary);
	}

	.warehouse-footer {
		margin-top: auto;
		padding-top: 10px;
		border-top: 1px solid var(--color-border);
	}
	.btn-view {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 6px;
		padding: 7px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-primary);
		cursor: pointer;
	}
	.btn-view:hover {
		border-color: var(--color-accent);
		color: var(--color-accent);
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

	.detail-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 12px;
		background: var(--color-bg-primary);
		padding: 14px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
	}
	.detail-item {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.d-lbl {
		font-size: 0.6875rem;
		text-transform: uppercase;
		color: var(--color-text-tertiary);
	}
	.d-val {
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}
	.font-bold {
		font-weight: 700;
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
	.form-group input {
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
