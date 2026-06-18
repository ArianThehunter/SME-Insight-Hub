<!--
  Expenses page — Operating expenses tracking, categorization, and approval status.
-->
<script lang="ts">
	import { Search, Plus, Download, DollarSign, Wallet, FileText, ArrowRightLeft, TrendingUp } from '@lucide/svelte';

	let searchQuery = $state('');
	let categoryFilter = $state('all');

	const expenses = [
		{ id: 'EXP-001', desc: 'Tejgaon Warehouse Rent (June)', category: 'Rent & Utilities', amount: 45000, date: '2026-06-01', method: 'Bank Transfer', status: 'Paid' },
		{ id: 'EXP-002', desc: 'Tejgaon Facility Electricity Bill', category: 'Rent & Utilities', amount: 12500, date: '2026-06-05', method: 'MFS (bKash)', status: 'Paid' },
		{ id: 'EXP-003', desc: 'Cotton Yarn & Fabric Purchase', category: 'Cost of Goods Sold', amount: 120000, date: '2026-06-08', method: 'Bank Transfer', status: 'Paid' },
		{ id: 'EXP-004', desc: 'Office Supplies & Stationery', category: 'Operations', amount: 3200, date: '2026-06-10', method: 'Cash', status: 'Paid' },
		{ id: 'EXP-005', desc: 'Delivery Truck Fuel & Maintenance', category: 'Logistics', amount: 8500, date: '2026-06-12', method: 'Card', status: 'Paid' },
		{ id: 'EXP-006', desc: 'Facebook/Instagram Ads Campaign', category: 'Marketing', amount: 15000, date: '2026-06-15', method: 'Card', status: 'Pending' },
		{ id: 'EXP-007', desc: 'Office Tea & Catering', category: 'Operations', amount: 1800, date: '2026-06-16', method: 'Cash', status: 'Paid' },
		{ id: 'EXP-008', desc: 'Eco Packaging Boxes (1000 units)', category: 'Logistics', amount: 22000, date: '2026-06-18', method: 'Bank Transfer', status: 'Pending' },
	];

	const categories = [...new Set(expenses.map(e => e.category))];

	const filtered = $derived(
		expenses.filter(e => {
			const matchSearch = !searchQuery || e.desc.toLowerCase().includes(searchQuery.toLowerCase()) || e.id.toLowerCase().includes(searchQuery.toLowerCase());
			const matchCat = categoryFilter === 'all' || e.category === categoryFilter;
			return matchSearch && matchCat;
		})
	);

	const summary = $derived({
		totalPaid: expenses.filter(e => e.status === 'Paid').reduce((acc, e) => acc + e.amount, 0),
		totalPending: expenses.filter(e => e.status === 'Pending').reduce((acc, e) => acc + e.amount, 0),
		total: expenses.reduce((acc, e) => acc + e.amount, 0),
	});

	// Compute category totals for visual breakdown
	const categoryBreakdown = $derived(
		categories.map(cat => {
			const total = expenses.filter(e => e.category === cat).reduce((acc, e) => acc + e.amount, 0);
			return { name: cat, amount: total, percent: Math.round(total / summary.total * 100) };
		}).sort((a, b) => b.amount - a.amount)
	);
</script>

<svelte:head><title>Expenses — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Expense Tracker</h1>
			<p class="page-subtitle">Track overheads, operational costs, procurement, and approval pipelines</p>
		</div>
		<button class="btn-create"><Plus size={16} /> Log Expense</button>
	</header>

	<!-- Summary Metrics -->
	<div class="summary-grid">
		<div class="summary-card">
			<span class="summary-val">৳ {summary.total.toLocaleString()}</span>
			<span class="summary-label">Total Outflow (Month)</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-success">৳ {summary.totalPaid.toLocaleString()}</span>
			<span class="summary-label">Paid Expenses</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-warning">৳ {summary.totalPending.toLocaleString()}</span>
			<span class="summary-label">Pending Approval</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-accent">{categoryBreakdown[0]?.name || 'N/A'}</span>
			<span class="summary-label">Largest Cost Center</span>
		</div>
	</div>

	<!-- Content Layout: Left = Table, Right = Category Breakdown -->
	<div class="content-layout">
		<div class="main-content">
			<!-- Toolbar -->
			<div class="toolbar">
				<div class="search-box">
					<Search size={16} />
					<input type="text" bind:value={searchQuery} placeholder="Search expense description..." class="search-input" />
				</div>
				<div class="toolbar-right">
					<select bind:value={categoryFilter} class="filter-select">
						<option value="all">All Categories</option>
						{#each categories as cat}<option value={cat}>{cat}</option>{/each}
					</select>
					<button class="btn-icon" title="Download Statement"><Download size={16} /></button>
				</div>
			</div>

			<!-- Table -->
			<div class="table-card animate-fade-in-up">
				<div class="table-scroll">
					<table class="data-table">
						<thead>
							<tr>
								<th>Expense ID</th>
								<th>Description</th>
								<th>Category</th>
								<th>Amount</th>
								<th>Date</th>
								<th>Payment Method</th>
								<th>Status</th>
							</tr>
						</thead>
						<tbody>
							{#each filtered as e}
								<tr>
									<td class="id-cell">{e.id}</td>
									<td class="desc-cell">{e.desc}</td>
									<td><span class="cat-badge">{e.category}</span></td>
									<td class="amount-cell">৳ {e.amount.toLocaleString()}</td>
									<td class="date-cell">{e.date}</td>
									<td class="method-cell">{e.method}</td>
									<td>
										<span class="badge {e.status === 'Paid' ? 'success' : 'warning'}">
											{e.status}
										</span>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		</div>

		<!-- Right Panel: Category Breakdown progress list -->
		<div class="side-panel">
			<div class="breakdown-card">
				<h3 class="panel-title"><TrendingUp size={16} /> Costs by Category</h3>
				<div class="breakdown-list">
					{#each categoryBreakdown as cat}
						<div class="breakdown-item">
							<div class="breakdown-info">
								<span class="category-name">{cat.name}</span>
								<span class="category-val">৳ {cat.amount.toLocaleString()}</span>
							</div>
							<div class="progress-bar-bg">
								<div class="progress-bar" style="width: {cat.percent}%"></div>
							</div>
							<span class="percentage-label">{cat.percent}% of total</span>
						</div>
					{/each}
				</div>
			</div>
		</div>
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
	@media (max-width: 640px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
	.summary-card { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-val { font-size: 1.375rem; font-weight: 700; color: var(--color-text-primary); text-align: center; }
	.summary-val.text-success { color: var(--color-success); }
	.summary-val.text-warning { color: var(--color-warning); }
	.summary-val.text-accent { color: var(--color-accent); font-size: 1.125rem; word-break: break-all; }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); text-align: center; }

	.content-layout { display: grid; grid-template-columns: 1fr 280px; gap: 20px; }
	@media (max-width: 992px) { .content-layout { grid-template-columns: 1fr; } }

	.main-content { display: flex; flex-direction: column; gap: 16px; }

	.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
	.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); min-width: 260px; color: var(--color-text-tertiary); flex: 1; }
	.search-box:focus-within { border-color: var(--color-accent); }
	.search-input { border: none; background: transparent; outline: none; color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; flex: 1; }
	.search-input::placeholder { color: var(--color-text-muted); }
	.toolbar-right { display: flex; gap: 8px; }
	.filter-select { padding: 8px 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; cursor: pointer; outline: none; }
	.btn-icon { width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); color: var(--color-text-secondary); cursor: pointer; transition: all var(--transition-fast); }
	.btn-icon:hover { background: var(--color-bg-hover); color: var(--color-text-primary); }

	.table-card { border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); overflow: hidden; }
	.table-scroll { overflow-x: auto; }
	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table thead { background: var(--color-bg-tertiary); }
	.data-table th { padding: 12px 16px; text-align: left; font-weight: 600; font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border); }
	.data-table td { padding: 12px 16px; border-bottom: 1px solid var(--color-border-subtle); color: var(--color-text-primary); }
	.data-table tbody tr { transition: background var(--transition-fast); }
	.data-table tbody tr:hover { background: var(--color-bg-hover); }

	.id-cell { font-family: var(--font-mono); font-weight: 600; color: var(--color-text-secondary); font-size: 0.75rem; }
	.desc-cell { font-weight: 500; }
	.cat-badge { font-size: 0.75rem; color: var(--color-text-secondary); background: var(--color-bg-tertiary); padding: 4px 8px; border-radius: var(--radius-sm); border: 1px solid var(--color-border); }
	.amount-cell { font-weight: 700; color: var(--color-text-primary); }
	.date-cell { color: var(--color-text-secondary); white-space: nowrap; }
	.method-cell { color: var(--color-text-secondary); font-size: 0.75rem; }

	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }

	.side-panel { display: flex; flex-direction: column; }
	.breakdown-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px; }
	.panel-title { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); margin: 0 0 16px; display: flex; align-items: center; gap: 6px; }
	
	.breakdown-list { display: flex; flex-direction: column; gap: 14px; }
	.breakdown-item { display: flex; flex-direction: column; gap: 6px; }
	.breakdown-info { display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 500; }
	.category-name { color: var(--color-text-secondary); }
	.category-val { color: var(--color-text-primary); font-weight: 600; }
	
	.progress-bar-bg { height: 6px; border-radius: var(--radius-full); background: var(--color-bg-tertiary); overflow: hidden; }
	.progress-bar { height: 100%; border-radius: var(--radius-full); background: var(--color-accent); }
	
	.percentage-label { font-size: 0.625rem; color: var(--color-text-tertiary); text-align: right; }
</style>
