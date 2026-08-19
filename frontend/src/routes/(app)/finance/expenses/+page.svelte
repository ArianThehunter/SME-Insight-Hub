<!--
  Expenses page — Interactive operating expense tracker with Log Expense modal, Category breakdown, and CSV export.
-->
<script lang="ts">
	import {
		Search,
		Plus,
		Download,
		DollarSign,
		Wallet,
		FileText,
		ArrowRightLeft,
		TrendingUp,
		X,
		Eye,
		CheckCircle2
	} from '@lucide/svelte';

	interface ExpenseItem {
		id: string;
		desc: string;
		category: string;
		amount: number;
		date: string;
		method: string;
		status: 'Paid' | 'Pending' | 'Rejected';
		vendor?: string;
	}

	let searchQuery = $state('');
	let categoryFilter = $state('all');

	let expenseList = $state<ExpenseItem[]>([
		{
			id: 'EXP-001',
			desc: 'Banani Office Rent (August)',
			category: 'Rent & Utilities',
			amount: 85000,
			date: '2026-08-01',
			method: 'Bank Transfer',
			status: 'Paid',
			vendor: 'Building Management'
		},
		{
			id: 'EXP-002',
			desc: 'DESCO Electricity Utility Bill',
			category: 'Rent & Utilities',
			amount: 12500,
			date: '2026-08-05',
			method: 'MFS (bKash)',
			status: 'Paid',
			vendor: 'DESCO'
		},
		{
			id: 'EXP-003',
			desc: 'Cotton Yarn & Fabric Bulk Purchase',
			category: 'Cost of Goods Sold',
			amount: 120000,
			date: '2026-08-08',
			method: 'Bank Transfer',
			status: 'Paid',
			vendor: 'Narayanganj Textile Mills'
		},
		{
			id: 'EXP-004',
			desc: 'Office Supplies & A4 Paper',
			category: 'Operations',
			amount: 3200,
			date: '2026-08-10',
			method: 'Cash',
			status: 'Paid',
			vendor: 'Ananya Stationers'
		},
		{
			id: 'EXP-005',
			desc: 'Delivery Van Fuel & Maintenance',
			category: 'Logistics',
			amount: 8500,
			date: '2026-08-12',
			method: 'Card',
			status: 'Paid',
			vendor: 'Padma Oil'
		},
		{
			id: 'EXP-006',
			desc: 'Digital Ads & Meta Campaigns',
			category: 'Marketing',
			amount: 15000,
			date: '2026-08-15',
			method: 'Card',
			status: 'Pending',
			vendor: 'Meta Platforms'
		},
		{
			id: 'EXP-007',
			desc: 'Staff Training & Skill Workshop',
			category: 'Operations',
			amount: 22000,
			date: '2026-08-16',
			method: 'Bank Transfer',
			status: 'Paid',
			vendor: 'BRAC Training'
		},
		{
			id: 'EXP-008',
			desc: 'Eco Packaging Boxes (1000 pcs)',
			category: 'Logistics',
			amount: 22000,
			date: '2026-08-18',
			method: 'Bank Transfer',
			status: 'Pending',
			vendor: 'Packaging BD'
		}
	]);

	// Modals
	let showCreateModal = $state(false);
	let selectedExpense = $state<ExpenseItem | null>(null);

	// New Expense Form
	let newDesc = $state('');
	let newCategory = $state('Rent & Utilities');
	let newAmount = $state<number>(5000);
	let newVendor = $state('');
	let newMethod = $state('Bank Transfer');
	let newStatus = $state<'Paid' | 'Pending'>('Paid');

	const categories = $derived(['all', ...new Set(expenseList.map((e) => e.category))]);

	const filtered = $derived(
		expenseList.filter((e) => {
			const matchSearch =
				!searchQuery ||
				e.desc.toLowerCase().includes(searchQuery.toLowerCase()) ||
				e.id.toLowerCase().includes(searchQuery.toLowerCase());
			const matchCat = categoryFilter === 'all' || e.category === categoryFilter;
			return matchSearch && matchCat;
		})
	);

	const summary = $derived({
		totalPaid: expenseList.filter((e) => e.status === 'Paid').reduce((acc, e) => acc + e.amount, 0),
		totalPending: expenseList
			.filter((e) => e.status === 'Pending')
			.reduce((acc, e) => acc + e.amount, 0),
		total: expenseList.reduce((acc, e) => acc + e.amount, 0)
	});

	const categoryBreakdown = $derived(
		Array.from(new Set(expenseList.map((e) => e.category)))
			.map((cat) => {
				const total = expenseList
					.filter((e) => e.category === cat)
					.reduce((acc, e) => acc + e.amount, 0);
				return {
					name: cat,
					amount: total,
					percent: Math.round((total / (summary.total || 1)) * 100)
				};
			})
			.sort((a, b) => b.amount - a.amount)
	);

	function handleLogExpense(e: Event) {
		e.preventDefault();
		if (!newDesc || newAmount <= 0) return;

		const count = expenseList.length + 1;
		const newExp: ExpenseItem = {
			id: `EXP-${String(count).padStart(3, '0')}`,
			desc: newDesc,
			category: newCategory,
			amount: newAmount,
			date: new Date().toISOString().split('T')[0],
			method: newMethod,
			status: newStatus,
			vendor: newVendor || 'Vendor'
		};

		expenseList = [newExp, ...expenseList];
		showCreateModal = false;
		newDesc = '';
		newAmount = 0;
	}

	function exportExpensesCSV() {
		const headers =
			'Expense_ID,Description,Category,Amount_BDT,Date,Payment_Method,Status,Vendor\n';
		const rows = filtered
			.map(
				(e) =>
					`"${e.id}","${e.desc}","${e.category}",${e.amount},"${e.date}","${e.method}","${e.status}","${e.vendor || ''}"`
			)
			.join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_expenses_export_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Expenses — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Operating Expenses Tracker</h1>
			<p class="page-subtitle">
				Track overheads, operational vendor bills, procurement costs, and payment approvals
			</p>
		</div>
		<button class="btn-create" onclick={() => (showCreateModal = true)}>
			<Plus size={16} /> Log Expense
		</button>
	</header>

	<!-- Summary Metrics -->
	<div class="summary-grid">
		<div class="card summary-card">
			<span class="summary-val">৳ {summary.total.toLocaleString()}</span>
			<span class="summary-label">Total Outflows (This Month)</span>
		</div>
		<div class="card summary-card text-success">
			<span class="summary-val">৳ {summary.totalPaid.toLocaleString()}</span>
			<span class="summary-label">Disbursed & Paid</span>
		</div>
		<div class="card summary-card text-warning">
			<span class="summary-val">৳ {summary.totalPending.toLocaleString()}</span>
			<span class="summary-label">Pending Approval</span>
		</div>
	</div>

	<!-- Category Breakdown -->
	<div class="card breakdown-card">
		<h2 class="card-title">Expense Allocation by Category</h2>
		<div class="breakdown-grid">
			{#each categoryBreakdown as cat}
				<div class="breakdown-item">
					<div class="b-head">
						<span>{cat.name}</span>
						<strong>৳ {cat.amount.toLocaleString()} ({cat.percent}%)</strong>
					</div>
					<div class="progress-track">
						<div class="progress-fill" style="width: {cat.percent}%"></div>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input
				type="text"
				bind:value={searchQuery}
				placeholder="Search expense description or ID..."
				class="search-input"
				aria-label="Search expenses"
			/>
		</div>
		<div class="toolbar-right">
			<select bind:value={categoryFilter} class="filter-select" aria-label="Filter category">
				{#each categories as cat}
					<option value={cat}>{cat === 'all' ? 'All Categories' : cat}</option>
				{/each}
			</select>
			<button
				class="btn-icon"
				onclick={exportExpensesCSV}
				title="Export CSV"
				aria-label="Export expenses CSV"
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
						<th>Expense ID</th>
						<th>Description</th>
						<th>Category</th>
						<th>Amount (BDT)</th>
						<th>Date</th>
						<th>Payment Method</th>
						<th>Status</th>
						<th>Action</th>
					</tr>
				</thead>
				<tbody>
					{#each filtered as e}
						<tr>
							<td><code class="exp-tag">{e.id}</code></td>
							<td><strong>{e.desc}</strong></td>
							<td><span class="cat-pill">{e.category}</span></td>
							<td class="num-cell font-bold text-accent">৳ {e.amount.toLocaleString()}</td>
							<td class="text-muted">{e.date}</td>
							<td>{e.method}</td>
							<td>
								<span class="badge badge-{e.status === 'Paid' ? 'success' : 'warning'}"
									>{e.status}</span
								>
							</td>
							<td>
								<button
									class="btn-icon-row"
									onclick={() => (selectedExpense = e)}
									title="View expense details"
								>
									<Eye size={14} />
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>

	<!-- Expense Details Modal -->
	{#if selectedExpense}
		<div class="modal-backdrop" onclick={() => (selectedExpense = null)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="exp-details-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<div>
						<h2 id="exp-details-title" class="modal-title">{selectedExpense.desc}</h2>
						<span class="exp-tag">{selectedExpense.id}</span>
					</div>
					<button
						class="btn-close"
						onclick={() => (selectedExpense = null)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<div class="modal-body">
					<div class="detail-grid">
						<div class="detail-item">
							<span class="d-lbl">Category</span><span class="d-val"
								>{selectedExpense.category}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Disbursed Amount</span><span class="d-val text-accent font-bold"
								>৳ {selectedExpense.amount.toLocaleString()}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Payment Date</span><span class="d-val"
								>{selectedExpense.date}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Payment Method</span><span class="d-val"
								>{selectedExpense.method}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Vendor / Payee</span><span class="d-val"
								>{selectedExpense.vendor || 'Direct Payee'}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Payment Status</span><span
								class="badge badge-{selectedExpense.status === 'Paid' ? 'success' : 'warning'}"
								>{selectedExpense.status}</span
							>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button class="btn-primary" onclick={() => (selectedExpense = null)}> Done </button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Log Expense Modal -->
	{#if showCreateModal}
		<div class="modal-backdrop" onclick={() => (showCreateModal = false)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="add-exp-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<h2 id="add-exp-title" class="modal-title">Record Operating Expense</h2>
					<button
						class="btn-close"
						onclick={() => (showCreateModal = false)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleLogExpense} class="modal-form">
					<div class="form-group">
						<label for="ae-desc">Expense Description</label>
						<input
							id="ae-desc"
							type="text"
							placeholder="e.g. WASA Water Bill & Maintenance"
							bind:value={newDesc}
							required
						/>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ae-cat">Category</label>
							<select id="ae-cat" bind:value={newCategory}>
								<option value="Rent & Utilities">Rent & Utilities</option>
								<option value="Cost of Goods Sold">Cost of Goods Sold</option>
								<option value="Operations">Operations</option>
								<option value="Logistics">Logistics</option>
								<option value="Marketing">Marketing</option>
								<option value="Salaries & Staff">Salaries & Staff</option>
							</select>
						</div>
						<div class="form-group">
							<label for="ae-amt">Amount (BDT)</label>
							<input
								id="ae-amt"
								type="number"
								placeholder="5000"
								bind:value={newAmount}
								min="1"
								required
							/>
						</div>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ae-ven">Vendor / Payee Name</label>
							<input id="ae-ven" type="text" placeholder="e.g. Dhaka WASA" bind:value={newVendor} />
						</div>
						<div class="form-group">
							<label for="ae-meth">Payment Method</label>
							<select id="ae-meth" bind:value={newMethod}>
								<option value="Bank Transfer">Bank Transfer (BFTN)</option>
								<option value="MFS (bKash)">MFS (bKash)</option>
								<option value="MFS (Nagad)">MFS (Nagad)</option>
								<option value="Card">Corporate Card</option>
								<option value="Cash">Petty Cash</option>
							</select>
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => (showCreateModal = false)}
							>Cancel</button
						>
						<button type="submit" class="btn-primary">Save Expense</button>
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
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 14px;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.summary-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.summary-val {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text-primary);
		font-variant-numeric: tabular-nums;
	}
	.summary-label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
	}
	.text-success .summary-val {
		color: var(--color-success);
	}
	.text-warning .summary-val {
		color: #d97706;
	}

	.breakdown-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.card-title {
		font-size: 0.9375rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
	}
	.breakdown-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 14px;
	}
	.breakdown-item {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.b-head {
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
		background: var(--color-accent);
		border-radius: 999px;
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
	.exp-tag {
		font-family: monospace;
		font-size: 0.75rem;
		background: var(--color-bg-primary);
		padding: 2px 6px;
		border-radius: 4px;
		border: 1px solid var(--color-border);
		color: var(--color-accent);
	}
	.cat-pill {
		font-size: 0.6875rem;
		padding: 2px 8px;
		border-radius: 999px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		color: var(--color-text-secondary);
	}
	.num-cell {
		font-variant-numeric: tabular-nums;
	}
	.text-accent {
		color: var(--color-accent);
	}
	.text-muted {
		color: var(--color-text-tertiary);
	}
	.font-bold {
		font-weight: 700;
	}

	.badge {
		display: inline-flex;
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

	.btn-icon-row {
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		padding: 4px 8px;
		cursor: pointer;
		color: var(--color-text-secondary);
	}
	.btn-icon-row:hover {
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
