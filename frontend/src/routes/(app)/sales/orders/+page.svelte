<!--
  Orders page — Data table with mock order data.
-->
<script lang="ts">
	import { Search, Filter, Download, Plus, Eye, ChevronLeft, ChevronRight } from '@lucide/svelte';

	let searchQuery = $state('');
	let statusFilter = $state('all');
	let currentPage = $state(1);
	const perPage = 10;

	const orders = [
		{ id: 'ORD-2026-001', customer: 'Rahman Textiles Ltd.', date: '2026-06-18', amount: 245000, status: 'completed', payment: 'paid', items: 12 },
		{ id: 'ORD-2026-002', customer: 'Dhaka Electronics Hub', date: '2026-06-17', amount: 182500, status: 'processing', payment: 'partial', items: 8 },
		{ id: 'ORD-2026-003', customer: 'Chittagong Spice Co.', date: '2026-06-17', amount: 67800, status: 'completed', payment: 'paid', items: 5 },
		{ id: 'ORD-2026-004', customer: 'Sylhet Tea Gardens', date: '2026-06-16', amount: 425000, status: 'shipped', payment: 'paid', items: 20 },
		{ id: 'ORD-2026-005', customer: 'Rajshahi Mangoes Inc.', date: '2026-06-16', amount: 38200, status: 'pending', payment: 'unpaid', items: 3 },
		{ id: 'ORD-2026-006', customer: 'Khulna Fisheries', date: '2026-06-15', amount: 156000, status: 'completed', payment: 'paid', items: 14 },
		{ id: 'ORD-2026-007', customer: 'Narayanganj Jute Works', date: '2026-06-15', amount: 890000, status: 'processing', payment: 'partial', items: 35 },
		{ id: 'ORD-2026-008', customer: 'Comilla Ceramics', date: '2026-06-14', amount: 72400, status: 'cancelled', payment: 'refunded', items: 6 },
		{ id: 'ORD-2026-009', customer: 'Bogura Steel Corp.', date: '2026-06-14', amount: 1250000, status: 'shipped', payment: 'paid', items: 45 },
		{ id: 'ORD-2026-010', customer: 'Gazipur Garments Ltd.', date: '2026-06-13', amount: 324000, status: 'completed', payment: 'paid', items: 18 },
		{ id: 'ORD-2026-011', customer: 'Jessore Food Products', date: '2026-06-13', amount: 95600, status: 'pending', payment: 'unpaid', items: 7 },
		{ id: 'ORD-2026-012', customer: 'Mymensingh Dairy Farm', date: '2026-06-12', amount: 145200, status: 'completed', payment: 'paid', items: 10 },
		{ id: 'ORD-2026-013', customer: 'Rangpur Agro Solutions', date: '2026-06-12', amount: 518000, status: 'processing', payment: 'partial', items: 22 },
		{ id: 'ORD-2026-014', customer: 'Barishal Marine Co.', date: '2026-06-11', amount: 267000, status: 'shipped', payment: 'paid', items: 15 },
		{ id: 'ORD-2026-015', customer: 'Tangail Handicrafts', date: '2026-06-11', amount: 43500, status: 'completed', payment: 'paid', items: 4 },
	];

	const filteredOrders = $derived(
		orders.filter(o => {
			const matchSearch = !searchQuery ||
				o.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
				o.customer.toLowerCase().includes(searchQuery.toLowerCase());
			const matchStatus = statusFilter === 'all' || o.status === statusFilter;
			return matchSearch && matchStatus;
		})
	);

	const totalPages = $derived(Math.ceil(filteredOrders.length / perPage));
	const paginatedOrders = $derived(filteredOrders.slice((currentPage - 1) * perPage, currentPage * perPage));

	const statusColors: Record<string, string> = {
		completed: 'success', processing: 'accent', shipped: 'info',
		pending: 'warning', cancelled: 'danger',
	};
	const paymentColors: Record<string, string> = {
		paid: 'success', partial: 'warning', unpaid: 'danger', refunded: 'info',
	};

	function formatCurrency(v: number): string { return `৳ ${v.toLocaleString()}`; }
</script>

<svelte:head><title>Orders — SME Insight Hub</title></svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Orders</h1>
			<p class="page-subtitle">Manage and track all sales orders</p>
		</div>
		<button class="btn-create"><Plus size={16} /> New Order</button>
	</header>

	<!-- Toolbar -->
	<div class="toolbar animate-fade-in">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search orders..." class="search-input" />
		</div>
		<div class="toolbar-right">
			<select bind:value={statusFilter} class="filter-select">
				<option value="all">All Status</option>
				<option value="pending">Pending</option>
				<option value="processing">Processing</option>
				<option value="shipped">Shipped</option>
				<option value="completed">Completed</option>
				<option value="cancelled">Cancelled</option>
			</select>
			<button class="btn-icon" title="Export"><Download size={16} /></button>
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
						<th>Amount</th>
						<th>Status</th>
						<th>Payment</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each paginatedOrders as order}
						<tr>
							<td class="order-id">{order.id}</td>
							<td class="customer-name">{order.customer}</td>
							<td class="date-cell">{new Date(order.date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}</td>
							<td class="items-cell">{order.items}</td>
							<td class="amount-cell">{formatCurrency(order.amount)}</td>
							<td><span class="badge {statusColors[order.status]}">{order.status}</span></td>
							<td><span class="badge outline {paymentColors[order.payment]}">{order.payment}</span></td>
							<td><button class="btn-view"><Eye size={14} /></button></td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<!-- Pagination -->
		<div class="pagination">
			<span class="pagination-info">Showing {(currentPage - 1) * perPage + 1}–{Math.min(currentPage * perPage, filteredOrders.length)} of {filteredOrders.length}</span>
			<div class="pagination-controls">
				<button class="pg-btn" disabled={currentPage <= 1} onclick={() => currentPage--}><ChevronLeft size={16} /></button>
				{#each Array(totalPages) as _, i}
					<button class="pg-btn" class:active={currentPage === i + 1} onclick={() => currentPage = i + 1}>{i + 1}</button>
				{/each}
				<button class="pg-btn" disabled={currentPage >= totalPages} onclick={() => currentPage++}><ChevronRight size={16} /></button>
			</div>
		</div>
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.btn-create {
		display: flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: var(--radius-md);
		border: none; background: var(--gradient-accent); color: white; font-size: 0.8125rem;
		font-weight: 600; font-family: inherit; cursor: pointer; transition: all var(--transition-fast);
		box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
	}
	.btn-create:hover { opacity: 0.9; transform: translateY(-1px); }

	.toolbar {
		display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
	}
	.search-box {
		display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: var(--radius-md);
		border: 1px solid var(--color-border); background: var(--color-bg-secondary); min-width: 260px;
		color: var(--color-text-tertiary); transition: border-color var(--transition-fast);
	}
	.search-box:focus-within { border-color: var(--color-accent); }
	.search-input {
		border: none; background: transparent; outline: none; color: var(--color-text-primary);
		font-size: 0.8125rem; font-family: inherit; flex: 1;
	}
	.search-input::placeholder { color: var(--color-text-muted); }

	.toolbar-right { display: flex; gap: 8px; align-items: center; }
	.filter-select {
		padding: 8px 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border);
		background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.8125rem;
		font-family: inherit; cursor: pointer; outline: none;
	}
	.btn-icon {
		width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;
		border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary);
		color: var(--color-text-secondary); cursor: pointer; transition: all var(--transition-fast);
	}
	.btn-icon:hover { background: var(--color-bg-hover); color: var(--color-text-primary); }

	.table-card {
		border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); overflow: hidden;
	}
	.table-scroll { overflow-x: auto; }

	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table thead { background: var(--color-bg-tertiary); }
	.data-table th {
		padding: 12px 16px; text-align: left; font-weight: 600; font-size: 0.6875rem;
		text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border);
	}
	.data-table td { padding: 12px 16px; border-bottom: 1px solid var(--color-border-subtle); color: var(--color-text-primary); }
	.data-table tbody tr { transition: background var(--transition-fast); }
	.data-table tbody tr:hover { background: var(--color-bg-hover); }

	.order-id { font-weight: 600; color: var(--color-accent); font-size: 0.8125rem; white-space: nowrap; }
	.customer-name { font-weight: 500; max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.date-cell { color: var(--color-text-secondary); white-space: nowrap; }
	.items-cell { text-align: center; color: var(--color-text-secondary); }
	.amount-cell { font-weight: 600; white-space: nowrap; }

	.badge {
		display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full);
		font-size: 0.6875rem; font-weight: 600; text-transform: capitalize;
	}
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.accent { background: var(--color-accent-muted); color: var(--color-accent); }
	.badge.info { background: var(--color-info-muted); color: var(--color-info); }
	.badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }
	.badge.danger { background: var(--color-danger-muted); color: var(--color-danger); }
	.badge.outline { background: transparent; border: 1px solid; }
	.badge.outline.success { border-color: rgba(16, 185, 129, 0.3); }
	.badge.outline.warning { border-color: rgba(245, 158, 11, 0.3); }
	.badge.outline.danger { border-color: rgba(239, 68, 68, 0.3); }
	.badge.outline.info { border-color: rgba(6, 182, 212, 0.3); }

	.btn-view {
		width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
		border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: transparent;
		color: var(--color-text-tertiary); cursor: pointer; transition: all var(--transition-fast);
	}
	.btn-view:hover { background: var(--color-accent-muted); color: var(--color-accent); border-color: var(--color-accent); }

	.pagination {
		display: flex; justify-content: space-between; align-items: center; padding: 12px 16px;
		border-top: 1px solid var(--color-border); flex-wrap: wrap; gap: 12px;
	}
	.pagination-info { font-size: 0.75rem; color: var(--color-text-tertiary); }
	.pagination-controls { display: flex; gap: 4px; }
	.pg-btn {
		width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;
		border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: transparent;
		color: var(--color-text-secondary); font-size: 0.75rem; font-weight: 500; cursor: pointer;
		transition: all var(--transition-fast);
	}
	.pg-btn:hover:not(:disabled) { background: var(--color-bg-hover); }
	.pg-btn.active { background: var(--color-accent); color: white; border-color: var(--color-accent); }
	.pg-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
