<!--
  Customers page — Interactive customer directory with Add Customer modal, Details viewer, and CSV export.
-->
<script lang="ts">
	import {
		Search, Plus, Download, Star, Eye, ChevronLeft, ChevronRight,
		Users, X, Phone, Mail, MapPin, Building, CheckCircle2
	} from '@lucide/svelte';

	interface Customer {
		id: number;
		name: string;
		contact: string;
		email: string;
		phone: string;
		segment: 'Enterprise' | 'SME' | 'Startup';
		ltv: number;
		orders: number;
		lastOrder: string;
		status: 'active' | 'inactive';
		city?: string;
	}

	let searchQuery = $state('');
	let segmentFilter = $state('all');
	let currentPage = $state(1);
	const perPage = 8;

	let customerList = $state<Customer[]>([
		{ id: 1, name: 'Rahman Textiles Ltd.', contact: 'Mr. Abdur Rahman', email: 'rahman@textiles.com.bd', phone: '+880 1711-234567', segment: 'Enterprise', ltv: 4580000, orders: 87, lastOrder: '2026-06-18', status: 'active', city: 'Narsingdi' },
		{ id: 2, name: 'Dhaka Electronics Hub', contact: 'Ms. Fatima Akter', email: 'fatima@deh.com.bd', phone: '+880 1812-345678', segment: 'Enterprise', ltv: 3250000, orders: 64, lastOrder: '2026-06-17', status: 'active', city: 'Dhaka' },
		{ id: 3, name: 'Chittagong Spice Co.', contact: 'Mr. Kamal Hossain', email: 'kamal@ctgspice.com', phone: '+880 1913-456789', segment: 'SME', ltv: 1820000, orders: 45, lastOrder: '2026-06-17', status: 'active', city: 'Chittagong' },
		{ id: 4, name: 'Sylhet Tea Gardens', contact: 'Mr. Rajan Das', email: 'rajan@sylhettea.com', phone: '+880 1614-567890', segment: 'Enterprise', ltv: 6750000, orders: 120, lastOrder: '2026-06-16', status: 'active', city: 'Sylhet' },
		{ id: 5, name: 'Rajshahi Mangoes Inc.', contact: 'Ms. Nusrat Jahan', email: 'nusrat@rajmango.com', phone: '+880 1515-678901', segment: 'SME', ltv: 980000, orders: 23, lastOrder: '2026-06-16', status: 'active', city: 'Rajshahi' },
		{ id: 6, name: 'Khulna Fisheries', contact: 'Mr. Habib Sarker', email: 'habib@khulnafish.com', phone: '+880 1716-789012', segment: 'SME', ltv: 2340000, orders: 56, lastOrder: '2026-06-15', status: 'active', city: 'Khulna' },
		{ id: 7, name: 'Narayanganj Jute Works', contact: 'Mr. Rafiq Islam', email: 'rafiq@juteworks.com', phone: '+880 1817-890123', segment: 'Enterprise', ltv: 8920000, orders: 145, lastOrder: '2026-06-15', status: 'active', city: 'Narayanganj' },
		{ id: 8, name: 'Comilla Ceramics', contact: 'Ms. Ayesha Siddiqui', email: 'ayesha@ceramics.com', phone: '+880 1918-901234', segment: 'Startup', ltv: 420000, orders: 12, lastOrder: '2026-06-14', status: 'inactive', city: 'Comilla' },
		{ id: 9, name: 'Bogura Steel Corp.', contact: 'Mr. Masud Khan', email: 'masud@bogurasteel.com', phone: '+880 1619-012345', segment: 'Enterprise', ltv: 12500000, orders: 198, lastOrder: '2026-06-14', status: 'active', city: 'Bogura' },
		{ id: 10, name: 'Gazipur Garments Ltd.', contact: 'Ms. Shamima Begum', email: 'shamima@garments.com', phone: '+880 1520-123456', segment: 'Enterprise', ltv: 5680000, orders: 92, lastOrder: '2026-06-13', status: 'active', city: 'Gazipur' },
		{ id: 11, name: 'Jessore Food Products', contact: 'Mr. Alamgir Hasan', email: 'alamgir@jessorefood.com', phone: '+880 1721-234567', segment: 'SME', ltv: 1150000, orders: 34, lastOrder: '2026-06-13', status: 'active', city: 'Jessore' },
		{ id: 12, name: 'Tangail Handicrafts', contact: 'Ms. Ruma Khatun', email: 'ruma@handicrafts.com', phone: '+880 1822-345678', segment: 'Startup', ltv: 380000, orders: 8, lastOrder: '2026-06-11', status: 'active', city: 'Tangail' },
	]);

	// Modals
	let showCreateModal = $state(false);
	let selectedCustomer = $state<Customer | null>(null);

	// New customer form
	let newName = $state('');
	let newContact = $state('');
	let newEmail = $state('');
	let newPhone = $state('');
	let newCity = $state('Dhaka');
	let newSegment = $state<'Enterprise' | 'SME' | 'Startup'>('SME');

	const segments = $derived([
		{ name: 'Enterprise', count: customerList.filter(c => c.segment === 'Enterprise').length, revenue: customerList.filter(c => c.segment === 'Enterprise').reduce((a, b) => a + b.ltv, 0), color: 'accent' },
		{ name: 'SME', count: customerList.filter(c => c.segment === 'SME').length, revenue: customerList.filter(c => c.segment === 'SME').reduce((a, b) => a + b.ltv, 0), color: 'success' },
		{ name: 'Startup', count: customerList.filter(c => c.segment === 'Startup').length, revenue: customerList.filter(c => c.segment === 'Startup').reduce((a, b) => a + b.ltv, 0), color: 'warning' },
	]);

	const filtered = $derived(
		customerList.filter(c => {
			const matchSearch = !searchQuery || c.name.toLowerCase().includes(searchQuery.toLowerCase()) || c.contact.toLowerCase().includes(searchQuery.toLowerCase());
			const matchSeg = segmentFilter === 'all' || c.segment === segmentFilter;
			return matchSearch && matchSeg;
		})
	);

	const totalPages = $derived(Math.ceil(filtered.length / perPage));
	const paginated = $derived(filtered.slice((currentPage - 1) * perPage, currentPage * perPage));

	function fmt(v: number): string {
		if (v >= 10000000) return `৳ ${(v / 10000000).toFixed(2)} Cr`;
		if (v >= 100000) return `৳ ${(v / 100000).toFixed(1)} Lakh`;
		if (v >= 1000) return `৳ ${(v / 1000).toFixed(0)}K`;
		return `৳ ${v}`;
	}

	const segColors: Record<string, string> = { Enterprise: 'accent', SME: 'success', Startup: 'warning' };

	function handleAddCustomer(e: Event) {
		e.preventDefault();
		if (!newName) return;

		const newCust: Customer = {
			id: customerList.length + 1,
			name: newName,
			contact: newContact || 'Direct Contact',
			email: newEmail || `${newName.toLowerCase().replace(/[^a-z0-9]/g, '')}@company.bd`,
			phone: newPhone || '+880 1712-000000',
			segment: newSegment,
			ltv: 0,
			orders: 0,
			lastOrder: 'New Customer',
			status: 'active',
			city: newCity,
		};

		customerList = [newCust, ...customerList];
		showCreateModal = false;
		newName = '';
		newContact = '';
	}

	function exportCustomersCSV() {
		const headers = 'ID,Name,Contact_Person,Email,Phone,Segment,LTV_BDT,Total_Orders,City,Status\n';
		const rows = filtered.map(c =>
			`"${c.id}","${c.name}","${c.contact}","${c.email}","${c.phone}","${c.segment}",${c.ltv},${c.orders},"${c.city || ''}","${c.status}"`
		).join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_customers_export_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Customers — SME Insight Hub</title></svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Customer Accounts</h1>
			<p class="page-subtitle">Track accounts, business contacts, and lifetime value across Bangladesh</p>
		</div>
		<button class="btn-create" onclick={() => showCreateModal = true}>
			<Plus size={16} /> Add Customer
		</button>
	</header>

	<!-- Segment Cards -->
	<div class="seg-grid">
		{#each segments as seg, i}
			<div class="seg-card animate-fade-in-up">
				<div class="seg-head">
					<span class="seg-badge {seg.color}">{seg.name}</span>
					<span class="seg-count">{seg.count} accounts</span>
				</div>
				<div class="seg-value">{fmt(seg.revenue)}</div>
				<div class="seg-label">Segment Lifetime Value</div>
			</div>
		{/each}
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search customers by company or contact..." class="search-input" aria-label="Search customers" />
		</div>
		<div class="toolbar-right">
			<select bind:value={segmentFilter} class="filter-select" aria-label="Filter segment">
				<option value="all">All Segments</option>
				<option value="Enterprise">Enterprise</option>
				<option value="SME">SME</option>
				<option value="Startup">Startup</option>
			</select>
			<button class="btn-icon" onclick={exportCustomersCSV} title="Export CSV" aria-label="Export customer list">
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
						<th>Customer Entity</th>
						<th>Primary Contact</th>
						<th>Segment</th>
						<th>Lifetime Value</th>
						<th>Orders</th>
						<th>Last Order</th>
						<th>Status</th>
						<th>Action</th>
					</tr>
				</thead>
				<tbody>
					{#each paginated as c}
						<tr>
							<td>
								<div class="customer-info">
									<span class="customer-name">{c.name}</span>
									<span class="customer-city">{c.city || 'Dhaka'}</span>
								</div>
							</td>
							<td>
								<div class="contact-info">
									<span class="contact-name">{c.contact}</span>
									<span class="contact-email">{c.email}</span>
								</div>
							</td>
							<td><span class="badge badge-{segColors[c.segment]}">{c.segment}</span></td>
							<td class="font-semibold num-cell">{fmt(c.ltv)}</td>
							<td>{c.orders} orders</td>
							<td class="text-muted">{c.lastOrder}</td>
							<td><span class="badge badge-{c.status === 'active' ? 'success' : 'neutral'}">{c.status}</span></td>
							<td>
								<button class="btn-icon-row" onclick={() => selectedCustomer = c} title="View account details">
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
			<span class="page-info">Showing {(currentPage - 1) * perPage + 1}–{Math.min(currentPage * perPage, filtered.length)} of {filtered.length} customers</span>
			<div class="page-controls">
				<button class="page-btn" disabled={currentPage <= 1} onclick={() => currentPage--} aria-label="Previous page">
					<ChevronLeft size={16} />
				</button>
				<span class="curr-page">{currentPage} / {Math.max(1, totalPages)}</span>
				<button class="page-btn" disabled={currentPage >= totalPages} onclick={() => currentPage++} aria-label="Next page">
					<ChevronRight size={16} />
				</button>
			</div>
		</div>
	</div>

	<!-- Customer Details Modal -->
	{#if selectedCustomer}
		<div class="modal-backdrop" onclick={() => selectedCustomer = null} role="presentation">
			<div class="modal-card" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" aria-labelledby="cust-details-title" tabindex="-1">
				<div class="modal-header">
					<div>
						<h2 id="cust-details-title" class="modal-title">{selectedCustomer.name}</h2>
						<span class="badge badge-{segColors[selectedCustomer.segment]}">{selectedCustomer.segment} Tier</span>
					</div>
					<button class="btn-close" onclick={() => selectedCustomer = null} aria-label="Close dialog">
						<X size={18} />
					</button>
				</div>
				<div class="modal-body">
					<div class="detail-grid">
						<div class="detail-item"><span class="d-lbl">Contact Person</span><span class="d-val">{selectedCustomer.contact}</span></div>
						<div class="detail-item"><span class="d-lbl">Email Address</span><span class="d-val">{selectedCustomer.email}</span></div>
						<div class="detail-item"><span class="d-lbl">Phone</span><span class="d-val">{selectedCustomer.phone}</span></div>
						<div class="detail-item"><span class="d-lbl">Region / City</span><span class="d-val">{selectedCustomer.city || 'Dhaka'}</span></div>
						<div class="detail-item"><span class="d-lbl">Lifetime Spend</span><span class="d-val text-accent font-bold">{fmt(selectedCustomer.ltv)}</span></div>
						<div class="detail-item"><span class="d-lbl">Completed Orders</span><span class="d-val">{selectedCustomer.orders} orders</span></div>
					</div>
				</div>
				<div class="modal-footer">
					<button class="btn-primary" onclick={() => selectedCustomer = null}>
						Done
					</button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Add Customer Modal -->
	{#if showCreateModal}
		<div class="modal-backdrop" onclick={() => showCreateModal = false} role="presentation">
			<div class="modal-card" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" aria-labelledby="add-cust-title" tabindex="-1">
				<div class="modal-header">
					<h2 id="add-cust-title" class="modal-title">Add Customer Entity</h2>
					<button class="btn-close" onclick={() => showCreateModal = false} aria-label="Close dialog">
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleAddCustomer} class="modal-form">
					<div class="form-group">
						<label for="ac-name">Company / Enterprise Name</label>
						<input id="ac-name" type="text" placeholder="e.g. Apex Enterprise Ltd." bind:value={newName} required />
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ac-contact">Contact Person</label>
							<input id="ac-contact" type="text" placeholder="e.g. Mr. Rafiqul Islam" bind:value={newContact} />
						</div>
						<div class="form-group">
							<label for="ac-city">City / District</label>
							<input id="ac-city" type="text" placeholder="e.g. Chittagong" bind:value={newCity} />
						</div>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ac-email">Email</label>
							<input id="ac-email" type="email" placeholder="contact@company.bd" bind:value={newEmail} />
						</div>
						<div class="form-group">
							<label for="ac-phone">Phone (+880)</label>
							<input id="ac-phone" type="text" placeholder="+880 1712-345678" bind:value={newPhone} />
						</div>
					</div>
					<div class="form-group">
						<label for="ac-seg">Customer Segment Tier</label>
						<select id="ac-seg" bind:value={newSegment}>
							<option value="Enterprise">Enterprise</option>
							<option value="SME">SME</option>
							<option value="Startup">Startup</option>
						</select>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => showCreateModal = false}>Cancel</button>
						<button type="submit" class="btn-primary">Save Account</button>
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

	.seg-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; }
	.seg-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px; display: flex; flex-direction: column; gap: 4px; }
	.seg-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
	.seg-badge { font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; padding: 2px 8px; border-radius: 999px; }
	.seg-badge.accent { background: color-mix(in srgb, var(--color-accent) 15%, transparent); color: var(--color-accent); }
	.seg-badge.success { background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.seg-badge.warning { background: color-mix(in srgb, #f59e0b 15%, transparent); color: #d97706; }
	.seg-count { font-size: 0.75rem; color: var(--color-text-tertiary); }
	.seg-value { font-size: 1.375rem; font-weight: 700; color: var(--color-text-primary); font-variant-numeric: tabular-nums; }
	.seg-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }

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

	.customer-info { display: flex; flex-direction: column; }
	.customer-name { font-weight: 600; color: var(--color-text-primary); }
	.customer-city { font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.contact-info { display: flex; flex-direction: column; }
	.contact-name { color: var(--color-text-secondary); }
	.contact-email { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.badge { display: inline-flex; font-size: 0.6875rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
	.badge-accent { background: color-mix(in srgb, var(--color-accent) 15%, transparent); color: var(--color-accent); }
	.badge-success { background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.badge-warning { background: color-mix(in srgb, #f59e0b 15%, transparent); color: #d97706; }
	.badge-neutral { background: var(--color-bg-primary); color: var(--color-text-tertiary); border: 1px solid var(--color-border); }

	.btn-icon-row { background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: 4px 8px; cursor: pointer; color: var(--color-text-secondary); }
	.btn-icon-row:hover { border-color: var(--color-accent); color: var(--color-accent); }

	.pagination { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-top: 1px solid var(--color-border); background: var(--color-bg-primary); font-size: 0.75rem; color: var(--color-text-secondary); }
	.page-controls { display: flex; align-items: center; gap: 8px; }
	.page-btn { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-sm); width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: var(--color-text-primary); }
	.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

	/* Modals */
	.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.65); display: flex; align-items: center; justify-content: center; z-index: 100; backdrop-filter: blur(4px); }
	.modal-card { width: 100%; max-width: 500px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; display: flex; flex-direction: column; gap: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
	.modal-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.modal-title { font-size: 1.125rem; font-weight: 700; color: var(--color-text-primary); margin: 0; }
	.btn-close { background: none; border: none; color: var(--color-text-tertiary); cursor: pointer; padding: 2px; }
	.btn-close:hover { color: var(--color-danger); }

	.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: var(--color-bg-primary); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); }
	.detail-item { display: flex; flex-direction: column; gap: 4px; }
	.d-lbl { font-size: 0.6875rem; text-transform: uppercase; color: var(--color-text-tertiary); }
	.d-val { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); }
	.text-accent { color: var(--color-accent); }
	.font-bold { font-weight: 700; }

	.modal-form { display: flex; flex-direction: column; gap: 14px; }
	.form-group { display: flex; flex-direction: column; gap: 6px; }
	.form-group label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; }
	.form-group input, .form-group select { padding: 8px 12px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; }
	.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
	.modal-footer { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }
</style>
