<!--
  BI Data Explorer — Dynamic query and slice-and-dice explorer for orders, customers, and inventory.
-->
<script lang="ts">
	import { Search, Filter, Download, Table, Layers, ArrowUpDown, SlidersHorizontal } from '@lucide/svelte';

	let entity = $state('orders');
	let filterStatus = $state('all');
	let searchQuery = $state('');

	const rows = [
		{ id: 'ORD-101', date: '2026-08-18', customer: 'Rahman Textiles', amount: '৳ 2,45,000', margin: '41%', division: 'Dhaka', status: 'Completed' },
		{ id: 'ORD-102', date: '2026-08-17', customer: 'Dhaka Electronics', amount: '৳ 1,82,500', margin: '33%', division: 'Dhaka', status: 'Processing' },
		{ id: 'ORD-103', date: '2026-08-17', customer: 'Chittagong Spice Co.', amount: '৳ 67,800', margin: '29%', division: 'Chittagong', status: 'Completed' },
		{ id: 'ORD-104', date: '2026-08-16', customer: 'Sylhet Tea Gardens', amount: '৳ 4,25,000', margin: '46%', division: 'Sylhet', status: 'Shipped' },
		{ id: 'ORD-105', date: '2026-08-16', customer: 'Rajshahi Mangoes', amount: '৳ 38,200', margin: '35%', division: 'Rajshahi', status: 'Pending' },
		{ id: 'ORD-106', date: '2026-08-15', customer: 'Bogura Steel Corp.', amount: '৳ 12,50,000', margin: '22%', division: 'Rajshahi', status: 'Shipped' },
	];

	const filteredRows = $derived(
		rows.filter(r => {
			const matchesSearch = !searchQuery || r.customer.toLowerCase().includes(searchQuery.toLowerCase()) || r.id.toLowerCase().includes(searchQuery.toLowerCase());
			const matchesStatus = filterStatus === 'all' || r.status.toLowerCase() === filterStatus.toLowerCase();
			return matchesSearch && matchesStatus;
		})
	);
</script>

<svelte:head><title>Data Explorer — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Data Explorer</h1>
			<p class="page-subtitle">Interactive multidimensional drilldown across your enterprise data</p>
		</div>
		<div class="header-actions">
			<a href="/documents/export" class="btn-secondary">
				<Download size={15} />
				Export CSV
			</a>
		</div>
	</header>

	<div class="card explorer-controls">
		<div class="controls-row">
			<div class="entity-selector">
				<button class="tab-btn" class:active={entity === 'orders'} onclick={() => entity = 'orders'}>Orders</button>
				<button class="tab-btn" class:active={entity === 'customers'} onclick={() => entity = 'customers'}>Customers</button>
				<button class="tab-btn" class:active={entity === 'inventory'} onclick={() => entity = 'inventory'}>Inventory</button>
				<button class="tab-btn" class:active={entity === 'expenses'} onclick={() => entity = 'expenses'}>Expenses</button>
			</div>

			<div class="filter-group">
				<div class="search-box">
					<Search size={14} />
					<input type="text" placeholder="Search rows..." bind:value={searchQuery} aria-label="Search rows" />
				</div>
				<select class="select-input" bind:value={filterStatus} aria-label="Filter by status">
					<option value="all">All Statuses</option>
					<option value="completed">Completed</option>
					<option value="processing">Processing</option>
					<option value="shipped">Shipped</option>
					<option value="pending">Pending</option>
				</select>
			</div>
		</div>
	</div>

	<div class="card table-card">
		<table class="data-table">
			<thead>
				<tr>
					<th>Record ID</th>
					<th>Date</th>
					<th>Entity / Customer</th>
					<th>Amount (BDT)</th>
					<th>Est. Margin</th>
					<th>Division</th>
					<th>Status</th>
				</tr>
			</thead>
			<tbody>
				{#each filteredRows as row}
					<tr>
						<td><code class="code-tag">{row.id}</code></td>
						<td>{row.date}</td>
						<td><strong>{row.customer}</strong></td>
						<td class="num">{row.amount}</td>
						<td class="num">{row.margin}</td>
						<td><span class="division-badge">{row.division}</span></td>
						<td>
							<span class="status-pill status-{row.status.toLowerCase()}">{row.status}</span>
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
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.explorer-controls { padding: 14px 18px; margin: 20px 0 16px; }
	.controls-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
	.entity-selector { display: flex; background: var(--color-bg-primary); padding: 3px; border-radius: var(--radius-md); border: 1px solid var(--color-border); }
	.tab-btn { background: none; border: none; padding: 6px 14px; font-size: 0.8125rem; font-weight: 600; color: var(--color-text-secondary); cursor: pointer; border-radius: var(--radius-sm); transition: all 0.15s; }
	.tab-btn.active { background: var(--color-bg-secondary); color: var(--color-text-primary); box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
	.filter-group { display: flex; gap: 8px; align-items: center; }
	.search-box { display: flex; align-items: center; gap: 6px; padding: 6px 10px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-tertiary); }
	.search-box input { background: none; border: none; outline: none; font-size: 0.8125rem; color: var(--color-text-primary); }
	.select-input { padding: 6px 12px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; }
	.btn-secondary { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-bg-secondary); color: var(--color-text-primary); border: 1px solid var(--color-border); text-decoration: none; }
	.table-card { overflow: hidden; }
	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table th { text-align: left; padding: 10px 14px; font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; background: var(--color-bg-primary); border-bottom: 1px solid var(--color-border); }
	.data-table td { padding: 12px 14px; border-bottom: 1px solid var(--color-border); color: var(--color-text-primary); }
	.data-table tr:last-child td { border-bottom: none; }
	.data-table .num { font-variant-numeric: tabular-nums; }
	.code-tag { font-family: monospace; font-size: 0.75rem; background: var(--color-bg-primary); padding: 2px 6px; border-radius: 4px; border: 1px solid var(--color-border); }
	.division-badge { font-size: 0.6875rem; padding: 2px 8px; border-radius: 999px; background: var(--color-bg-primary); border: 1px solid var(--color-border); }
	.status-pill { font-size: 0.6875rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
	.status-completed { background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.status-processing { background: color-mix(in srgb, var(--color-accent) 15%, transparent); color: var(--color-accent); }
	.status-shipped { background: color-mix(in srgb, #38bdf8 15%, transparent); color: #0ea5e9; }
	.status-pending { background: color-mix(in srgb, #f59e0b 15%, transparent); color: #d97706; }
</style>
