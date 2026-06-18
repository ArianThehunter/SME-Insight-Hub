<!--
  Invoices page — Client billing, payments, overdue tracking, and automated reminders.
-->
<script lang="ts">
	import { Search, Plus, Download, Mail, Eye, AlertCircle, FileCheck, Send, Clock } from '@lucide/svelte';

	let searchQuery = $state('');
	let statusFilter = $state('all');

	const invoices = [
		{ id: 'INV-2026-001', customer: 'Tejgaon Super Shops', amount: 45000, issuedDate: '2026-06-02', dueDate: '2026-06-17', status: 'Paid' },
		{ id: 'INV-2026-002', customer: 'Halishahar Grocery Hub', amount: 28000, issuedDate: '2026-06-05', dueDate: '2026-06-20', status: 'Sent' },
		{ id: 'INV-2026-003', customer: 'Sylhet Tea House Ltd', amount: 15400, issuedDate: '2026-06-08', dueDate: '2026-06-23', status: 'Paid' },
		{ id: 'INV-2026-004', customer: 'Dhaka Handicrafts Market', amount: 64000, issuedDate: '2026-05-15', dueDate: '2026-05-30', status: 'Overdue' },
		{ id: 'INV-2026-005', customer: 'Chittagong Fashion Depot', amount: 85000, issuedDate: '2026-06-12', dueDate: '2026-06-27', status: 'Sent' },
		{ id: 'INV-2026-006', customer: 'Rajshahi Retail Outlets', amount: 19200, issuedDate: '2026-06-15', dueDate: '2026-06-30', status: 'Draft' },
	];

	const filtered = $derived(
		invoices.filter(inv => {
			const matchSearch = !searchQuery || 
				inv.customer.toLowerCase().includes(searchQuery.toLowerCase()) || 
				inv.id.toLowerCase().includes(searchQuery.toLowerCase());
			const matchStatus = statusFilter === 'all' || inv.status.toLowerCase() === statusFilter;
			return matchSearch && matchStatus;
		})
	);

	const summary = $derived({
		totalInvoiced: invoices.reduce((acc, inv) => acc + inv.amount, 0),
		paid: invoices.filter(inv => inv.status === 'Paid').reduce((acc, inv) => acc + inv.amount, 0),
		pending: invoices.filter(inv => inv.status === 'Sent').reduce((acc, inv) => acc + inv.amount, 0),
		overdue: invoices.filter(inv => inv.status === 'Overdue').reduce((acc, inv) => acc + inv.amount, 0),
	});

	function statusClass(status: string): string {
		switch (status.toLowerCase()) {
			case 'paid': return 'success';
			case 'sent': return 'info';
			case 'overdue': return 'danger';
			default: return 'warning';
		}
	}
</script>

<svelte:head><title>Invoices — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Invoices</h1>
			<p class="page-subtitle">Generate client invoices, track receivables, and follow up on overdue bills</p>
		</div>
		<button class="btn-create"><Plus size={16} /> New Invoice</button>
	</header>

	<!-- Invoice KPI summary -->
	<div class="summary-grid">
		<div class="summary-card">
			<div class="summary-icon-wrapper"><FileCheck size={20} class="text-accent" /></div>
			<div class="summary-details">
				<span class="summary-val">৳ {summary.totalInvoiced.toLocaleString()}</span>
				<span class="summary-label">Total Invoiced</span>
			</div>
		</div>
		<div class="summary-card">
			<div class="summary-icon-wrapper"><Clock size={20} class="text-warning" /></div>
			<div class="summary-details">
				<span class="summary-val">৳ {summary.pending.toLocaleString()}</span>
				<span class="summary-label">Outstanding (Sent)</span>
			</div>
		</div>
		<div class="summary-card">
			<div class="summary-icon-wrapper"><AlertCircle size={20} class="text-danger" /></div>
			<div class="summary-details">
				<span class="summary-val text-danger">৳ {summary.overdue.toLocaleString()}</span>
				<span class="summary-label">Overdue Balance</span>
			</div>
		</div>
		<div class="summary-card">
			<div class="summary-icon-wrapper"><FileCheck size={20} class="text-success" /></div>
			<div class="summary-details">
				<span class="summary-val text-success">৳ {summary.paid.toLocaleString()}</span>
				<span class="summary-label">Payments Received</span>
			</div>
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search by customer or invoice #..." class="search-input" />
		</div>
		<div class="toolbar-right">
			<select bind:value={statusFilter} class="filter-select">
				<option value="all">All Statuses</option>
				<option value="paid">Paid</option>
				<option value="sent">Sent</option>
				<option value="overdue">Overdue</option>
				<option value="draft">Draft</option>
			</select>
			<button class="btn-icon" title="Export Invoices"><Download size={16} /></button>
		</div>
	</div>

	<!-- Invoices List Table -->
	<div class="table-card animate-fade-in-up">
		<div class="table-scroll">
			<table class="data-table">
				<thead>
					<tr>
						<th>Invoice #</th>
						<th>Customer</th>
						<th>Issue Date</th>
						<th>Due Date</th>
						<th>Amount</th>
						<th>Status</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each filtered as inv}
						{@const stClass = statusClass(inv.status)}
						<tr>
							<td class="id-cell">{inv.id}</td>
							<td class="cust-cell">{inv.customer}</td>
							<td class="date-cell">{inv.issuedDate}</td>
							<td class="date-cell">{inv.dueDate}</td>
							<td class="amount-cell">৳ {inv.amount.toLocaleString()}</td>
							<td>
								<span class="badge {stClass}">
									{inv.status}
								</span>
							</td>
							<td>
								<div class="actions-cell">
									<button class="btn-view" title="Preview PDF"><Eye size={13} /></button>
									{#if inv.status === 'Overdue'}
										<button class="btn-action danger" title="Send Overdue Notice"><Mail size={13} /> Remind</button>
									{:else if inv.status === 'Sent'}
										<button class="btn-action info" title="Resend Invoice"><Send size={13} /> Send</button>
									{:else}
										<button class="btn-action secondary" disabled>—</button>
									{/if}
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
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
	@media (max-width: 768px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 480px) { .summary-grid { grid-template-columns: 1fr; } }
	
	.summary-card { display: flex; align-items: center; gap: 14px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-icon-wrapper { width: 40px; height: 40px; border-radius: var(--radius-md); background: var(--color-bg-tertiary); display: flex; align-items: center; justify-content: center; }
	.summary-details { display: flex; flex-direction: column; gap: 2px; }
	.summary-val { font-size: 1.25rem; font-weight: 700; color: var(--color-text-primary); }
	.summary-val.text-success { color: var(--color-success); }
	.summary-val.text-danger { color: var(--color-danger); }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
	.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); min-width: 260px; color: var(--color-text-tertiary); }
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

	.id-cell { font-family: var(--font-mono); font-weight: 600; color: var(--color-accent); font-size: 0.75rem; }
	.cust-cell { font-weight: 500; }
	.date-cell { color: var(--color-text-secondary); white-space: nowrap; }
	.amount-cell { font-weight: 700; color: var(--color-text-primary); }

	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.info { background: var(--color-accent-muted); color: var(--color-accent); }
	.badge.danger { background: var(--color-danger-muted); color: var(--color-danger); }
	.badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }

	.actions-cell { display: flex; gap: 6px; align-items: center; }
	.btn-view { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: transparent; color: var(--color-text-tertiary); cursor: pointer; transition: all var(--transition-fast); }
	.btn-view:hover { background: var(--color-bg-hover); color: var(--color-text-primary); }
	
	.btn-action { display: inline-flex; align-items: center; gap: 4px; padding: 6px 10px; border-radius: var(--radius-sm); border: 1px solid var(--color-border); font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: all var(--transition-fast); }
	.btn-action.danger { background: var(--color-danger-muted); border-color: var(--color-danger-muted); color: var(--color-danger); }
	.btn-action.danger:hover { background: var(--color-danger); border-color: var(--color-danger); color: white; }
	.btn-action.info { background: var(--color-accent-muted); border-color: var(--color-accent-muted); color: var(--color-accent); }
	.btn-action.info:hover { background: var(--color-accent); border-color: var(--color-accent); color: white; }
	.btn-action.secondary { border-color: transparent; background: transparent; color: var(--color-text-muted); cursor: default; }
</style>
