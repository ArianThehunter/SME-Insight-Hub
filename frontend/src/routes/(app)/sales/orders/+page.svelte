<!--
  Orders page — Fully interactive orders management with New Order modal, Details viewer, CSV export, and live filtering.
-->
<script lang="ts">
	import {
		Search,
		Filter,
		Download,
		Plus,
		Eye,
		ChevronLeft,
		ChevronRight,
		X,
		CheckCircle2,
		ShoppingCart,
		Clock,
		Truck,
		Ban,
		Printer
	} from '@lucide/svelte';
	import { api } from '$lib/services/api';

	interface Order {
		id: string;
		customer: string;
		date: string;
		amount: number;
		status: 'pending' | 'processing' | 'shipped' | 'completed' | 'cancelled';
		payment: 'paid' | 'partial' | 'unpaid' | 'refunded';
		items: number;
		deliveryAddress?: string;
		notes?: string;
	}

	let searchQuery = $state('');
	let statusFilter = $state('all');
	let currentPage = $state(1);
	const perPage = 10;

	let ordersList = $state<Order[]>([
		{
			id: 'ORD-2026-001',
			customer: 'Rahman Textiles Ltd.',
			date: '2026-06-18',
			amount: 245000,
			status: 'completed',
			payment: 'paid',
			items: 12,
			deliveryAddress: 'Dilkusha C/A, Dhaka'
		},
		{
			id: 'ORD-2026-002',
			customer: 'Dhaka Electronics Hub',
			date: '2026-06-17',
			amount: 182500,
			status: 'processing',
			payment: 'partial',
			items: 8,
			deliveryAddress: 'Elephant Road, Dhaka'
		},
		{
			id: 'ORD-2026-003',
			customer: 'Chittagong Spice Co.',
			date: '2026-06-17',
			amount: 67800,
			status: 'completed',
			payment: 'paid',
			items: 5,
			deliveryAddress: 'Khatunganj, Chittagong'
		},
		{
			id: 'ORD-2026-004',
			customer: 'Sylhet Tea Gardens',
			date: '2026-06-16',
			amount: 425000,
			status: 'shipped',
			payment: 'paid',
			items: 20,
			deliveryAddress: 'Sreemangal, Sylhet'
		},
		{
			id: 'ORD-2026-005',
			customer: 'Rajshahi Mangoes Inc.',
			date: '2026-06-16',
			amount: 38200,
			status: 'pending',
			payment: 'unpaid',
			items: 3,
			deliveryAddress: 'Shaheb Bazar, Rajshahi'
		},
		{
			id: 'ORD-2026-006',
			customer: 'Khulna Fisheries',
			date: '2026-06-15',
			amount: 156000,
			status: 'completed',
			payment: 'paid',
			items: 14,
			deliveryAddress: 'Rupsha, Khulna'
		},
		{
			id: 'ORD-2026-007',
			customer: 'Narayanganj Jute Works',
			date: '2026-06-15',
			amount: 890000,
			status: 'processing',
			payment: 'partial',
			items: 35,
			deliveryAddress: 'Tanbazar, Narayanganj'
		},
		{
			id: 'ORD-2026-008',
			customer: 'Comilla Ceramics',
			date: '2026-06-14',
			amount: 72400,
			status: 'cancelled',
			payment: 'refunded',
			items: 6,
			deliveryAddress: 'EPZ Road, Comilla'
		},
		{
			id: 'ORD-2026-009',
			customer: 'Bogura Steel Corp.',
			date: '2026-06-14',
			amount: 1250000,
			status: 'shipped',
			payment: 'paid',
			items: 45,
			deliveryAddress: 'Santahar Road, Bogura'
		},
		{
			id: 'ORD-2026-010',
			customer: 'Gazipur Garments Ltd.',
			date: '2026-06-13',
			amount: 324000,
			status: 'completed',
			payment: 'paid',
			items: 18,
			deliveryAddress: 'Konabari, Gazipur'
		},
		{
			id: 'ORD-2026-011',
			customer: 'Jessore Food Products',
			date: '2026-06-13',
			amount: 95600,
			status: 'pending',
			payment: 'unpaid',
			items: 7,
			deliveryAddress: 'Chowrasta, Jessore'
		},
		{
			id: 'ORD-2026-012',
			customer: 'Mymensingh Dairy Farm',
			date: '2026-06-12',
			amount: 145200,
			status: 'completed',
			payment: 'paid',
			items: 10,
			deliveryAddress: 'Valuka, Mymensingh'
		},
		{
			id: 'ORD-2026-013',
			customer: 'Rangpur Agro Solutions',
			date: '2026-06-12',
			amount: 518000,
			status: 'processing',
			payment: 'partial',
			items: 22,
			deliveryAddress: 'Station Road, Rangpur'
		},
		{
			id: 'ORD-2026-014',
			customer: 'Barishal Marine Co.',
			date: '2026-06-11',
			amount: 267000,
			status: 'shipped',
			payment: 'paid',
			items: 15,
			deliveryAddress: 'Launch Ghat, Barishal'
		},
		{
			id: 'ORD-2026-015',
			customer: 'Tangail Handicrafts',
			date: '2026-06-11',
			amount: 43500,
			status: 'completed',
			payment: 'paid',
			items: 4,
			deliveryAddress: 'Porabari, Tangail'
		}
	]);

	// Modals state
	let showCreateModal = $state(false);
	let selectedOrder = $state<Order | null>(null);

	// Create Form state
	let newCustomer = $state('');
	let newAmount = $state<number>(0);
	let newItems = $state<number>(1);
	let newPayment = $state<'paid' | 'partial' | 'unpaid'>('paid');
	let newStatus = $state<'pending' | 'processing' | 'shipped' | 'completed'>('processing');
	let newAddress = $state('Dhaka, Bangladesh');

	const filteredOrders = $derived(
		ordersList.filter((o) => {
			const matchSearch =
				!searchQuery ||
				o.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
				o.customer.toLowerCase().includes(searchQuery.toLowerCase());
			const matchStatus = statusFilter === 'all' || o.status === statusFilter;
			return matchSearch && matchStatus;
		})
	);

	const totalPages = $derived(Math.ceil(filteredOrders.length / perPage));
	const paginatedOrders = $derived(
		filteredOrders.slice((currentPage - 1) * perPage, currentPage * perPage)
	);

	const statusColors: Record<string, string> = {
		completed: 'success',
		processing: 'accent',
		shipped: 'info',
		pending: 'warning',
		cancelled: 'danger'
	};
	const paymentColors: Record<string, string> = {
		paid: 'success',
		partial: 'warning',
		unpaid: 'danger',
		refunded: 'info'
	};

	function formatCurrency(v: number): string {
		return `৳ ${v.toLocaleString()}`;
	}

	function handleCreateOrder(e: Event) {
		e.preventDefault();
		if (!newCustomer || newAmount <= 0) return;

		const count = ordersList.length + 1;
		const newOrd: Order = {
			id: `ORD-2026-${String(count).padStart(3, '0')}`,
			customer: newCustomer,
			date: new Date().toISOString().split('T')[0],
			amount: newAmount,
			status: newStatus,
			payment: newPayment,
			items: newItems,
			deliveryAddress: newAddress
		};

		ordersList = [newOrd, ...ordersList];
		showCreateModal = false;
		newCustomer = '';
		newAmount = 0;
	}

	function exportOrdersCSV() {
		const headers =
			'Order_ID,Customer,Order_Date,Amount_BDT,Items_Count,Status,Payment_Status,Address\n';
		const rows = filteredOrders
			.map(
				(o) =>
					`"${o.id}","${o.customer}","${o.date}",${o.amount},${o.items},"${o.status}","${o.payment}","${o.deliveryAddress || ''}"`
			)
			.join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_orders_export_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Orders — SME Insight Hub</title></svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Sales Orders</h1>
			<p class="page-subtitle">Track, filter, create, and dispatch orders across all channels</p>
		</div>
		<button class="btn-create" onclick={() => (showCreateModal = true)}>
			<Plus size={16} /> New Order
		</button>
	</header>

	<!-- Toolbar -->
	<div class="toolbar animate-fade-in">
		<div class="search-box">
			<Search size={16} />
			<input
				type="text"
				bind:value={searchQuery}
				placeholder="Search orders by ID or customer..."
				class="search-input"
				aria-label="Search orders"
			/>
		</div>
		<div class="toolbar-right">
			<select bind:value={statusFilter} class="filter-select" aria-label="Filter status">
				<option value="all">All Status</option>
				<option value="pending">Pending</option>
				<option value="processing">Processing</option>
				<option value="shipped">Shipped</option>
				<option value="completed">Completed</option>
				<option value="cancelled">Cancelled</option>
			</select>
			<button
				class="btn-icon"
				onclick={exportOrdersCSV}
				title="Export CSV"
				aria-label="Export orders CSV"
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
						<th>Order #</th>
						<th>Customer</th>
						<th>Date</th>
						<th>Items</th>
						<th>Amount (BDT)</th>
						<th>Status</th>
						<th>Payment</th>
						<th>Action</th>
					</tr>
				</thead>
				<tbody>
					{#each paginatedOrders as o}
						<tr>
							<td class="font-mono font-bold text-accent">{o.id}</td>
							<td><strong>{o.customer}</strong></td>
							<td class="text-muted">{o.date}</td>
							<td>{o.items} pcs</td>
							<td class="font-semibold num-cell">{formatCurrency(o.amount)}</td>
							<td>
								<span class="badge badge-{statusColors[o.status]}">{o.status}</span>
							</td>
							<td>
								<span class="badge badge-{paymentColors[o.payment]}">{o.payment}</span>
							</td>
							<td>
								<button
									class="btn-icon-row"
									onclick={() => (selectedOrder = o)}
									title="View order details"
								>
									<Eye size={14} />
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<!-- Pagination -->
		<div class="pagination">
			<span class="page-info"
				>Showing {(currentPage - 1) * perPage + 1}–{Math.min(
					currentPage * perPage,
					filteredOrders.length
				)} of {filteredOrders.length} orders</span
			>
			<div class="page-controls">
				<button
					class="page-btn"
					disabled={currentPage <= 1}
					onclick={() => currentPage--}
					aria-label="Previous page"
				>
					<ChevronLeft size={16} />
				</button>
				<span class="curr-page">{currentPage} / {Math.max(1, totalPages)}</span>
				<button
					class="page-btn"
					disabled={currentPage >= totalPages}
					onclick={() => currentPage++}
					aria-label="Next page"
				>
					<ChevronRight size={16} />
				</button>
			</div>
		</div>
	</div>

	<!-- Order Details Modal / Drawer -->
	{#if selectedOrder}
		<div class="modal-backdrop" onclick={() => (selectedOrder = null)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="order-details-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<div>
						<h2 id="order-details-title" class="modal-title">{selectedOrder.id}</h2>
						<span class="modal-sub">{selectedOrder.customer}</span>
					</div>
					<button
						class="btn-close"
						onclick={() => (selectedOrder = null)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<div class="modal-body">
					<div class="detail-grid">
						<div class="detail-item">
							<span class="d-lbl">Order Date</span><span class="d-val">{selectedOrder.date}</span>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Total Amount</span><span class="d-val text-accent font-bold"
								>{formatCurrency(selectedOrder.amount)}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Status</span><span
								class="badge badge-{statusColors[selectedOrder.status]}"
								>{selectedOrder.status}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Payment</span><span
								class="badge badge-{paymentColors[selectedOrder.payment]}"
								>{selectedOrder.payment}</span
							>
						</div>
					</div>
					<div class="detail-box">
						<span class="d-lbl">Delivery Destination</span>
						<p class="d-address">{selectedOrder.deliveryAddress || 'Dhaka, Bangladesh'}</p>
					</div>
				</div>
				<div class="modal-footer">
					<button class="btn-secondary" onclick={() => window.print()}>
						<Printer size={14} /> Print Invoice
					</button>
					<button class="btn-primary" onclick={() => (selectedOrder = null)}> Done </button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Create Order Modal -->
	{#if showCreateModal}
		<div class="modal-backdrop" onclick={() => (showCreateModal = false)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="create-order-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<h2 id="create-order-title" class="modal-title">Create Sales Order</h2>
					<button
						class="btn-close"
						onclick={() => (showCreateModal = false)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleCreateOrder} class="modal-form">
					<div class="form-group">
						<label for="c-customer">Customer / Enterprise Name</label>
						<input
							id="c-customer"
							type="text"
							placeholder="e.g. Rahman Textiles Ltd."
							bind:value={newCustomer}
							required
						/>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="c-amount">Total Amount (BDT)</label>
							<input
								id="c-amount"
								type="number"
								placeholder="25000"
								bind:value={newAmount}
								required
								min="1"
							/>
						</div>
						<div class="form-group">
							<label for="c-items">Items Count</label>
							<input
								id="c-items"
								type="number"
								placeholder="5"
								bind:value={newItems}
								required
								min="1"
							/>
						</div>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="c-payment">Payment Status</label>
							<select id="c-payment" bind:value={newPayment}>
								<option value="paid">Paid</option>
								<option value="partial">Partial</option>
								<option value="unpaid">Unpaid</option>
							</select>
						</div>
						<div class="form-group">
							<label for="c-status">Order Status</label>
							<select id="c-status" bind:value={newStatus}>
								<option value="processing">Processing</option>
								<option value="pending">Pending</option>
								<option value="shipped">Shipped</option>
								<option value="completed">Completed</option>
							</select>
						</div>
					</div>
					<div class="form-group">
						<label for="c-address">Delivery Address (Bangladesh)</label>
						<input
							id="c-address"
							type="text"
							placeholder="e.g. Banani, Dhaka"
							bind:value={newAddress}
						/>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => (showCreateModal = false)}
							>Cancel</button
						>
						<button type="submit" class="btn-primary">Save Order</button>
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

	.btn-create {
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
	.num-cell {
		font-variant-numeric: tabular-nums;
	}
	.text-accent {
		color: var(--color-accent);
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
	.badge-success {
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}
	.badge-accent {
		background: color-mix(in srgb, var(--color-accent) 15%, transparent);
		color: var(--color-accent);
	}
	.badge-info {
		background: color-mix(in srgb, #38bdf8 15%, transparent);
		color: #0ea5e9;
	}
	.badge-warning {
		background: color-mix(in srgb, #f59e0b 15%, transparent);
		color: #d97706;
	}
	.badge-danger {
		background: color-mix(in srgb, var(--color-danger) 15%, transparent);
		color: var(--color-danger);
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

	.pagination {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		border-top: 1px solid var(--color-border);
		background: var(--color-bg-primary);
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}
	.page-controls {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.page-btn {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		color: var(--color-text-primary);
	}
	.page-btn:disabled {
		opacity: 0.4;
		cursor: not-allowed;
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
	.modal-sub {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
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
	.detail-box {
		background: var(--color-bg-primary);
		padding: 12px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
	}
	.d-address {
		font-size: 0.8125rem;
		color: var(--color-text-primary);
		margin: 4px 0 0;
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
