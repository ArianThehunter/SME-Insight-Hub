<!--
  Warehouses page — Warehouse locations with capacity tracking and details.
-->
<script lang="ts">
	import { Building2, Search, Plus, MapPin, Users, Package, Percent, ShieldAlert } from '@lucide/svelte';

	let searchQuery = $state('');

	const warehouses = [
		{ id: 'WH-001', name: 'Dhaka Central Warehouse', location: 'Tejgaon I/A, Dhaka', manager: 'Farhan Ahmed', capacity: 85, area: 15000, items: 12450, status: 'Active' },
		{ id: 'WH-002', name: 'Chittagong Port Facility', location: 'Halishahar, Chittagong', manager: 'Yasmin Chowdhury', capacity: 60, area: 20000, items: 8900, status: 'Active' },
		{ id: 'WH-003', name: 'Sylhet Regional Depot', location: 'Sobhanighat, Sylhet', manager: 'Tanvir Rahman', capacity: 35, area: 8000, items: 2100, status: 'Active' },
		{ id: 'WH-004', name: 'Rajshahi Cold Storage', location: 'Sopura, Rajshahi', manager: 'Mahbubul Alam', capacity: 92, area: 10000, items: 5400, status: 'Near Capacity' },
	];

	const filtered = $derived(
		warehouses.filter(w => {
			return !searchQuery || 
				w.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
				w.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
				w.manager.toLowerCase().includes(searchQuery.toLowerCase());
		})
	);

	const metrics = $derived({
		total: warehouses.length,
		avgCapacity: Math.round(warehouses.reduce((acc, w) => acc + w.capacity, 0) / warehouses.length),
		totalArea: warehouses.reduce((acc, w) => acc + w.area, 0),
		totalItems: warehouses.reduce((acc, w) => acc + w.items, 0),
	});

	function capacityColor(capacity: number): string {
		if (capacity >= 90) return 'danger';
		if (capacity >= 75) return 'warning';
		return 'success';
	}
</script>

<svelte:head><title>Warehouses — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Warehouses</h1>
			<p class="page-subtitle">Track storage capacity, distribution, and warehouse management</p>
		</div>
		<button class="btn-create"><Plus size={16} /> Add Warehouse</button>
	</header>

	<!-- Summary Cards -->
	<div class="summary-grid">
		<div class="summary-card">
			<div class="summary-icon-wrapper"><Building2 size={20} /></div>
			<div class="summary-details">
				<span class="summary-val">{metrics.total}</span>
				<span class="summary-label">Total Warehouses</span>
			</div>
		</div>
		<div class="summary-card">
			<div class="summary-icon-wrapper"><Percent size={20} /></div>
			<div class="summary-details">
				<span class="summary-val">{metrics.avgCapacity}%</span>
				<span class="summary-label">Average Capacity</span>
			</div>
		</div>
		<div class="summary-card">
			<div class="summary-icon-wrapper"><Package size={20} /></div>
			<div class="summary-details">
				<span class="summary-val">{metrics.totalItems.toLocaleString()}</span>
				<span class="summary-label">Total Items Stored</span>
			</div>
		</div>
		<div class="summary-card">
			<div class="summary-icon-wrapper"><MapPin size={20} /></div>
			<div class="summary-details">
				<span class="summary-val">{metrics.totalArea.toLocaleString()} sq ft</span>
				<span class="summary-label">Total Storage Area</span>
			</div>
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search warehouses..." class="search-input" />
		</div>
	</div>

	<!-- Warehouse Grid -->
	<div class="warehouse-grid animate-fade-in-up">
		{#each filtered as w}
			{@const capClass = capacityColor(w.capacity)}
			<div class="warehouse-card">
				<div class="card-header">
					<div>
						<h2 class="card-title">{w.name}</h2>
						<p class="card-subtitle"><MapPin size={12} class="inline-icon" /> {w.location}</p>
					</div>
					<span class="badge {capClass === 'danger' ? 'danger' : 'success'}">{w.status}</span>
				</div>

				<div class="card-body">
					<!-- Capacity Progress Bar -->
					<div class="capacity-section">
						<div class="capacity-labels">
							<span class="capacity-title">Capacity Utilized</span>
							<span class="capacity-num {capClass}">{w.capacity}%</span>
						</div>
						<div class="progress-bar-bg">
							<div class="progress-bar {capClass}" style="width: {w.capacity}%"></div>
						</div>
					</div>

					<div class="info-grid">
						<div class="info-item">
							<Users size={14} class="info-icon" />
							<div>
								<span class="info-label">Manager</span>
								<span class="info-val">{w.manager}</span>
							</div>
						</div>
						<div class="info-item">
							<Package size={14} class="info-icon" />
							<div>
								<span class="info-label">Stock Stored</span>
								<span class="info-val">{w.items.toLocaleString()} units</span>
							</div>
						</div>
						<div class="info-item">
							<Building2 size={14} class="info-icon" />
							<div>
								<span class="info-label">Dimensions</span>
								<span class="info-val">{w.area.toLocaleString()} sq ft</span>
							</div>
						</div>
					</div>
				</div>

				<div class="card-footer">
					<button class="btn-action">Manage Stock</button>
					<button class="btn-action secondary">View Layout</button>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	
	.btn-create { display: flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: var(--radius-md); border: none; background: var(--gradient-accent); color: white; font-size: 0.8125rem; font-weight: 600; font-family: inherit; cursor: pointer; box-shadow: 0 2px 8px rgba(59,130,246,0.25); transition: all var(--transition-fast); }
	.btn-create:hover { opacity: 0.9; transform: translateY(-1px); }

	.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
	@media (max-width: 768px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 480px) { .summary-grid { grid-template-columns: 1fr; } }
	
	.summary-card { display: flex; align-items: center; gap: 14px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-icon-wrapper { width: 40px; height: 40px; border-radius: var(--radius-md); background: var(--color-bg-tertiary); display: flex; align-items: center; justify-content: center; color: var(--color-accent); }
	.summary-details { display: flex; flex-direction: column; gap: 2px; }
	.summary-val { font-size: 1.25rem; font-weight: 700; color: var(--color-text-primary); }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
	.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); min-width: 280px; color: var(--color-text-tertiary); }
	.search-box:focus-within { border-color: var(--color-accent); }
	.search-input { border: none; background: transparent; outline: none; color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; flex: 1; }
	.search-input::placeholder { color: var(--color-text-muted); }

	.warehouse-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
	@media (max-width: 768px) { .warehouse-grid { grid-template-columns: 1fr; } }
	
	.warehouse-card { border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); display: flex; flex-direction: column; overflow: hidden; transition: all var(--transition-fast); }
	.warehouse-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: var(--color-border-hover); }
	
	.card-header { padding: 16px; border-bottom: 1px solid var(--color-border-subtle); display: flex; justify-content: space-between; align-items: flex-start; }
	.card-title { font-size: 1rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }
	.card-subtitle { font-size: 0.75rem; color: var(--color-text-secondary); margin: 4px 0 0; display: flex; align-items: center; gap: 4px; }
	.inline-icon { color: var(--color-text-tertiary); }

	.card-body { padding: 16px; display: flex; flex-direction: column; gap: 16px; flex: 1; }
	
	.capacity-section { display: flex; flex-direction: column; gap: 6px; }
	.capacity-labels { display: flex; justify-content: space-between; align-items: center; }
	.capacity-title { font-size: 0.75rem; font-weight: 500; color: var(--color-text-secondary); }
	.capacity-num { font-size: 0.8125rem; font-weight: 600; }
	.capacity-num.success { color: var(--color-success); }
	.capacity-num.warning { color: var(--color-warning); }
	.capacity-num.danger { color: var(--color-danger); }
	
	.progress-bar-bg { height: 6px; border-radius: var(--radius-full); background: var(--color-bg-tertiary); overflow: hidden; }
	.progress-bar { height: 100%; border-radius: var(--radius-full); }
	.progress-bar.success { background: var(--color-success); }
	.progress-bar.warning { background: var(--color-warning); }
	.progress-bar.danger { background: var(--color-danger); }

	.info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; background: var(--color-bg-tertiary); padding: 12px; border-radius: var(--radius-md); }
	.info-item { display: flex; gap: 8px; }
	.info-icon { color: var(--color-text-tertiary); margin-top: 2px; }
	.info-label { display: block; font-size: 0.625rem; color: var(--color-text-tertiary); text-transform: uppercase; font-weight: 600; }
	.info-val { display: block; font-size: 0.75rem; font-weight: 500; color: var(--color-text-primary); margin-top: 1px; }

	.card-footer { padding: 12px 16px; border-top: 1px solid var(--color-border-subtle); display: flex; gap: 8px; background: var(--color-bg-tertiary); }
	.btn-action { flex: 1; padding: 8px; border-radius: var(--radius-md); border: none; background: var(--color-bg-secondary); border: 1px solid var(--color-border); color: var(--color-text-primary); font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: all var(--transition-fast); text-align: center; }
	.btn-action:hover { background: var(--color-accent-muted); color: var(--color-accent); border-color: var(--color-accent); }
	.btn-action.secondary { background: transparent; border-color: transparent; color: var(--color-text-secondary); }
	.btn-action.secondary:hover { background: var(--color-bg-hover); color: var(--color-text-primary); border-color: transparent; }

	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.danger { background: var(--color-danger-muted); color: var(--color-danger); }
</style>
