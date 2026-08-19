<!--
  Invoices page — Interactive invoices management with New Invoice modal, Details/Print preview, and CSV export.
-->
<script lang="ts">
	import {
		Search, Plus, Download, Mail, Eye, AlertCircle, FileCheck,
		Send, Clock, X, Printer, CheckCircle2
	} from '@lucide/svelte';

	interface InvoiceItem {
		id: string;
		customer: string;
		amount: number;
		subtotal: number;
		tax: number;
		issuedDate: string;
		dueDate: string;
		status: 'Paid' | 'Sent' | 'Overdue' | 'Draft';
	}

	let searchQuery = $state('');
	let statusFilter = $state('all');

	let invoiceList = $state<InvoiceItem[]>([
		{ id: 'INV-2026-001', customer: 'Rahman Textiles Ltd.', amount: 281750, subtotal: 245000, tax: 36750, issuedDate: '2026-08-01', dueDate: '2026-08-16', status: 'Paid' },
		{ id: 'INV-2026-002', customer: 'Dhaka Electronics Hub', amount: 209875, subtotal: 182500, tax: 27375, issuedDate: '2026-08-05', dueDate: '2026-08-20', status: 'Sent' },
		{ id: 'INV-2026-003', customer: 'Sylhet Tea Gardens', amount: 488750, subtotal: 425000, tax: 63750, issuedDate: '2026-08-08', dueDate: '2026-08-23', status: 'Paid' },
		{ id: 'INV-2026-004', customer: 'Bogura Steel Corp.', amount: 1437500, subtotal: 1250000, tax: 187500, issuedDate: '2026-07-15', dueDate: '2026-07-30', status: 'Overdue' },
		{ id: 'INV-2026-005', customer: 'Chittagong Spice Co.', amount: 77970, subtotal: 67800, tax: 10170, issuedDate: '2026-08-12', dueDate: '2026-08-27', status: 'Sent' },
		{ id: 'INV-2026-006', customer: 'Rajshahi Mangoes Inc.', amount: 43930, subtotal: 38200, tax: 5730, issuedDate: '2026-08-15', dueDate: '2026-08-30', status: 'Draft' },
	]);

	// Modals
	let showCreateModal = $state(false);
	let selectedInvoice = $state<InvoiceItem | null>(null);

	// New Invoice Form
	let newCustomer = $state('');
	let newSubtotal = $state<number>(50000);
	let newDueDate = $state('2026-09-01');

	const filtered = $derived(
		invoiceList.filter(inv => {
			const matchSearch = !searchQuery || 
				inv.customer.toLowerCase().includes(searchQuery.toLowerCase()) || 
				inv.id.toLowerCase().includes(searchQuery.toLowerCase());
			const matchStatus = statusFilter === 'all' || inv.status.toLowerCase() === statusFilter.toLowerCase();
			return matchSearch && matchStatus;
		})
	);

	const summary = $derived({
		totalInvoiced: invoiceList.reduce((acc, inv) => acc + inv.amount, 0),
		paid: invoiceList.filter(inv => inv.status === 'Paid').reduce((acc, inv) => acc + inv.amount, 0),
		pending: invoiceList.filter(inv => inv.status === 'Sent').reduce((acc, inv) => acc + inv.amount, 0),
		overdue: invoiceList.filter(inv => inv.status === 'Overdue').reduce((acc, inv) => acc + inv.amount, 0),
	});

	function statusClass(status: string): string {
		switch (status.toLowerCase()) {
			case 'paid': return 'success';
			case 'sent': return 'info';
			case 'overdue': return 'danger';
			default: return 'warning';
		}
	}

	function handleCreateInvoice(e: Event) {
		e.preventDefault();
		if (!newCustomer || newSubtotal <= 0) return;

		const count = invoiceList.length + 1;
		const tax = Math.round(newSubtotal * 0.15); // 15% NBR VAT
		const total = newSubtotal + tax;

		const newInv: InvoiceItem = {
			id: `INV-2026-${String(count).padStart(3, '0')}`,
			customer: newCustomer,
			amount: total,
			subtotal: newSubtotal,
			tax: tax,
			issuedDate: new Date().toISOString().split('T')[0],
			dueDate: newDueDate || '2026-09-01',
			status: 'Sent',
		};

		invoiceList = [newInv, ...invoiceList];
		showCreateModal = false;
		newCustomer = '';
		newSubtotal = 0;
	}

	function markAsPaid(id: string) {
		invoiceList = invoiceList.map(inv => inv.id === id ? { ...inv, status: 'Paid' } : inv);
		if (selectedInvoice && selectedInvoice.id === id) {
			selectedInvoice = { ...selectedInvoice, status: 'Paid' };
		}
	}

	function exportInvoicesCSV() {
		const headers = 'Invoice_ID,Customer_Name,Subtotal_BDT,VAT_15pct_BDT,Total_Amount_BDT,Issue_Date,Due_Date,Status\n';
		const rows = filtered.map(inv =>
			`"${inv.id}","${inv.customer}",${inv.subtotal},${inv.tax},${inv.amount},"${inv.issuedDate}","${inv.dueDate}","${inv.status}"`
		).join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_invoices_export_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Invoices — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Client Invoices & Receivables</h1>
			<p class="page-subtitle">Generate client invoices, track collections, calculate 15% VAT, and follow up on overdue bills</p>
		</div>
		<button class="btn-create" onclick={() => showCreateModal = true}>
			<Plus size={16} /> New Invoice
		</button>
	</header>

	<!-- Invoice KPI summary -->
	<div class="summary-grid">
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><FileCheck size={20} class="text-accent" /></div>
			<div class="summary-details">
				<span class="summary-val">৳ {summary.totalInvoiced.toLocaleString()}</span>
				<span class="summary-label">Total Invoiced</span>
			</div>
		</div>
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><CheckCircle2 size={20} class="text-success" /></div>
			<div class="summary-details">
				<span class="summary-val text-success">৳ {summary.paid.toLocaleString()}</span>
				<span class="summary-label">Collected & Paid</span>
			</div>
		</div>
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><Clock size={20} class="text-info" /></div>
			<div class="summary-details">
				<span class="summary-val text-info">৳ {summary.pending.toLocaleString()}</span>
				<span class="summary-label">Sent & Outstanding</span>
			</div>
		</div>
		<div class="card summary-card">
			<div class="summary-icon-wrapper"><AlertCircle size={20} class="text-danger" /></div>
			<div class="summary-details">
				<span class="summary-val text-danger">৳ {summary.overdue.toLocaleString()}</span>
				<span class="summary-label">Overdue Exposure</span>
			</div>
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search invoice # or customer..." class="search-input" aria-label="Search invoices" />
		</div>
		<div class="toolbar-right">
			<select bind:value={statusFilter} class="filter-select" aria-label="Filter status">
				<option value="all">All Invoices</option>
				<option value="Paid">Paid</option>
				<option value="Sent">Sent</option>
				<option value="Overdue">Overdue</option>
				<option value="Draft">Draft</option>
			</select>
			<button class="btn-icon" onclick={exportInvoicesCSV} title="Export CSV" aria-label="Export invoices CSV">
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
						<th>Invoice #</th>
						<th>Customer</th>
						<th>Pre-Tax Subtotal</th>
						<th>VAT (15%)</th>
						<th>Total Amount</th>
						<th>Issue Date</th>
						<th>Due Date</th>
						<th>Status</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each filtered as inv}
						<tr>
							<td><code class="inv-tag">{inv.id}</code></td>
							<td><strong>{inv.customer}</strong></td>
							<td class="num-cell">৳ {inv.subtotal.toLocaleString()}</td>
							<td class="num-cell text-muted">৳ {inv.tax.toLocaleString()}</td>
							<td class="num-cell font-bold text-accent">৳ {inv.amount.toLocaleString()}</td>
							<td class="text-muted">{inv.issuedDate}</td>
							<td class="text-muted">{inv.dueDate}</td>
							<td>
								<span class="badge badge-{statusClass(inv.status)}">{inv.status}</span>
							</td>
							<td>
								<div class="btn-row">
									<button class="btn-icon-row" onclick={() => selectedInvoice = inv} title="View invoice">
										<Eye size={14} />
									</button>
									{#if inv.status !== 'Paid'}
										<button class="btn-action-paid" onclick={() => markAsPaid(inv.id)} title="Mark Paid">
											<CheckCircle2 size={13} /> Paid
										</button>
									{/if}
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>

	<!-- Invoice Preview Modal -->
	{#if selectedInvoice}
		<div class="modal-backdrop" onclick={() => selectedInvoice = null} role="presentation">
			<div class="modal-card" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" aria-labelledby="inv-details-title" tabindex="-1">
				<div class="modal-header">
					<div>
						<h2 id="inv-details-title" class="modal-title">{selectedInvoice.id}</h2>
						<span class="inv-sub">{selectedInvoice.customer}</span>
					</div>
					<button class="btn-close" onclick={() => selectedInvoice = null} aria-label="Close dialog">
						<X size={18} />
					</button>
				</div>
				<div class="modal-body">
					<div class="detail-grid">
						<div class="detail-item"><span class="d-lbl">Issue Date</span><span class="d-val">{selectedInvoice.issuedDate}</span></div>
						<div class="detail-item"><span class="d-lbl">Payment Due</span><span class="d-val">{selectedInvoice.dueDate}</span></div>
						<div class="detail-item"><span class="d-lbl">Subtotal (Pre-tax)</span><span class="d-val">৳ {selectedInvoice.subtotal.toLocaleString()}</span></div>
						<div class="detail-item"><span class="d-lbl">VAT Mushak 6.3 (15%)</span><span class="d-val">৳ {selectedInvoice.tax.toLocaleString()}</span></div>
						<div class="detail-item"><span class="d-lbl">Total Payable</span><span class="d-val text-accent font-bold">৳ {selectedInvoice.amount.toLocaleString()}</span></div>
						<div class="detail-item"><span class="d-lbl">Current Status</span><span class="badge badge-{statusClass(selectedInvoice.status)}">{selectedInvoice.status}</span></div>
					</div>
				</div>
				<div class="modal-footer">
					{#if selectedInvoice && selectedInvoice.status !== 'Paid'}
						<button class="btn-success-btn" onclick={() => selectedInvoice && markAsPaid(selectedInvoice.id)}>
							<CheckCircle2 size={14} /> Mark as Paid
						</button>
					{/if}
					<button class="btn-secondary" onclick={() => window.print()}>
						<Printer size={14} /> Print Invoice
					</button>
					<button class="btn-primary" onclick={() => selectedInvoice = null}>
						Done
					</button>
				</div>
			</div>
		</div>
	{/if}

	<!-- New Invoice Modal -->
	{#if showCreateModal}
		<div class="modal-backdrop" onclick={() => showCreateModal = false} role="presentation">
			<div class="modal-card" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" aria-labelledby="add-inv-title" tabindex="-1">
				<div class="modal-header">
					<h2 id="add-inv-title" class="modal-title">Generate Client Invoice</h2>
					<button class="btn-close" onclick={() => showCreateModal = false} aria-label="Close dialog">
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleCreateInvoice} class="modal-form">
					<div class="form-group">
						<label for="ai-cust">Client / Enterprise Account</label>
						<input id="ai-cust" type="text" placeholder="e.g. Sylhet Tea Gardens" bind:value={newCustomer} required />
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ai-sub">Pre-Tax Amount (BDT)</label>
							<input id="ai-sub" type="number" placeholder="50000" bind:value={newSubtotal} min="1" required />
						</div>
						<div class="form-group">
							<label for="ai-due">Payment Due Date</label>
							<input id="ai-due" type="date" bind:value={newDueDate} required />
						</div>
					</div>
					<div class="vat-notice">
						<span class="vat-label">NBR Standard VAT (15%):</span>
						<strong>৳ {Math.round(newSubtotal * 0.15).toLocaleString()}</strong>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => showCreateModal = false}>Cancel</button>
						<button type="submit" class="btn-primary">Issue Invoice</button>
					</div>
				</form>
			</div>
		</div>
	{/if}
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.btn-create, .btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-accent); color: white; border: none; }
	.btn-secondary { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-bg-primary); color: var(--color-text-primary); border: 1px solid var(--color-border); }
	.btn-success-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-success); color: white; border: none; }

	.summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.summary-card { padding: 16px; display: flex; align-items: center; gap: 14px; }
	.summary-icon-wrapper { width: 42px; height: 42px; border-radius: var(--radius-md); background: var(--color-bg-primary); display: flex; align-items: center; justify-content: center; flex-shrink: 0; border: 1px solid var(--color-border); }
	.summary-details { display: flex; flex-direction: column; gap: 2px; }
	.summary-label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; }
	.summary-val { font-size: 1.375rem; font-weight: 700; color: var(--color-text-primary); font-variant-numeric: tabular-nums; }
	.text-accent { color: var(--color-accent); }
	.text-success { color: var(--color-success); }
	.text-info { color: #0ea5e9; }
	.text-danger { color: var(--color-danger); }
	.font-bold { font-weight: 700; }

	.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
	.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-md); flex: 1; max-width: 380px; color: var(--color-text-tertiary); }
	.search-input { background: none; border: none; outline: none; font-size: 0.8125rem; color: var(--color-text-primary); width: 100%; }
	.toolbar-right { display: flex; gap: 8px; }
	.filter-select { padding: 8px 12px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; }
	.btn-icon { display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-secondary); cursor: pointer; }
	.btn-icon:hover { border-color: var(--color-accent); color: var(--color-accent); }

	.table-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden; }
	.table-scroll { overflow-x: auto; }
	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table th { text-align: left; padding: 10px 16px; font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; background: var(--color-bg-primary); border-bottom: 1px solid var(--color-border); }
	.data-table td { padding: 12px 16px; border-bottom: 1px solid var(--color-border); color: var(--color-text-primary); }
	.data-table tr:last-child td { border-bottom: none; }
	.inv-tag { font-family: monospace; font-size: 0.75rem; background: var(--color-bg-primary); padding: 2px 6px; border-radius: 4px; border: 1px solid var(--color-border); color: var(--color-accent); }
	.num-cell { font-variant-numeric: tabular-nums; }
	.text-muted { color: var(--color-text-tertiary); }

	.badge { display: inline-flex; font-size: 0.6875rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
	.badge-success { background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.badge-info { background: color-mix(in srgb, #38bdf8 15%, transparent); color: #0ea5e9; }
	.badge-danger { background: color-mix(in srgb, var(--color-danger) 15%, transparent); color: var(--color-danger); }
	.badge-warning { background: color-mix(in srgb, #f59e0b 15%, transparent); color: #d97706; }

	.btn-row { display: flex; align-items: center; gap: 6px; }
	.btn-icon-row { background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: 4px 8px; cursor: pointer; color: var(--color-text-secondary); }
	.btn-icon-row:hover { border-color: var(--color-accent); color: var(--color-accent); }
	.btn-action-paid { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; background: color-mix(in srgb, var(--color-success) 12%, transparent); border: 1px solid var(--color-success); color: var(--color-success); border-radius: var(--radius-sm); font-size: 0.6875rem; font-weight: 600; cursor: pointer; }

	/* Modals */
	.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.65); display: flex; align-items: center; justify-content: center; z-index: 100; backdrop-filter: blur(4px); }
	.modal-card { width: 100%; max-width: 520px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; display: flex; flex-direction: column; gap: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
	.modal-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.modal-title { font-size: 1.125rem; font-weight: 700; color: var(--color-text-primary); margin: 0; }
	.inv-sub { font-size: 0.75rem; color: var(--color-text-secondary); }
	.btn-close { background: none; border: none; color: var(--color-text-tertiary); cursor: pointer; padding: 2px; }
	.btn-close:hover { color: var(--color-danger); }

	.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: var(--color-bg-primary); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); }
	.detail-item { display: flex; flex-direction: column; gap: 4px; }
	.d-lbl { font-size: 0.6875rem; text-transform: uppercase; color: var(--color-text-tertiary); }
	.d-val { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); }

	.modal-form { display: flex; flex-direction: column; gap: 14px; }
	.form-group { display: flex; flex-direction: column; gap: 6px; }
	.form-group label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; }
	.form-group input { padding: 8px 12px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; }
	.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
	.vat-notice { display: flex; justify-content: space-between; background: var(--color-bg-primary); padding: 10px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); font-size: 0.8125rem; color: var(--color-text-secondary); }
	.modal-footer { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }
</style>
