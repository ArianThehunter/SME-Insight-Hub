<!--
  Suppliers page — Supplier/Vendor database with ratings, delivery performance, and contacts.
-->
<script lang="ts">
	import { Search, Plus, Star, Phone, Mail, Award, TrendingUp, Calendar, ChevronRight } from '@lucide/svelte';

	let searchQuery = $state('');
	let categoryFilter = $state('all');

	const suppliers = [
		{ id: 'SPL-001', name: 'Bengal Agro Ltd', category: 'Food & Beverages', contactName: 'Mizanur Rahman', email: 'mizan@bengalagro.com', phone: '+880-1711-223344', rating: 4.8, onTime: 97, activeOrders: 3, status: 'Preferred' },
		{ id: 'SPL-002', name: 'Chittagong Textiles Co.', category: 'Textiles', contactName: 'Farhana Kabir', email: 'fkabir@ctgtextiles.com', phone: '+880-1811-556677', rating: 4.5, onTime: 92, activeOrders: 1, status: 'Active' },
		{ id: 'SPL-003', name: 'Dhaka Leather Craft', category: 'Handicrafts', contactName: 'Sajidul Islam', email: 'sajid@dhakaleather.com', phone: '+880-1911-889900', rating: 4.2, onTime: 88, activeOrders: 2, status: 'Active' },
		{ id: 'SPL-004', name: 'Sylhet Tea Estates', category: 'Food & Beverages', contactName: 'Tanzeem Ahmed', email: 't.ahmed@sylhettea.com', phone: '+880-1311-112233', rating: 4.9, onTime: 99, activeOrders: 0, status: 'Preferred' },
		{ id: 'SPL-005', name: 'Rajshahi Fruit Growers', category: 'Food & Beverages', contactName: 'Asaduzzaman', email: 'asad@rajshahifruit.com', phone: '+880-1511-445566', rating: 4.0, onTime: 85, activeOrders: 4, status: 'Under Review' },
	];

	const categories = [...new Set(suppliers.map(s => s.category))];

	const filtered = $derived(
		suppliers.filter(s => {
			const matchSearch = !searchQuery || 
				s.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
				s.contactName.toLowerCase().includes(searchQuery.toLowerCase());
			const matchCat = categoryFilter === 'all' || s.category === categoryFilter;
			return matchSearch && matchCat;
		})
	);

	const metrics = $derived({
		total: suppliers.length,
		avgRating: (suppliers.reduce((acc, s) => acc + s.rating, 0) / suppliers.length).toFixed(1),
		avgOnTime: Math.round(suppliers.reduce((acc, s) => acc + s.onTime, 0) / suppliers.length),
		activeOrders: suppliers.reduce((acc, s) => acc + s.activeOrders, 0),
	});

	function performanceClass(rate: number): string {
		if (rate >= 95) return 'success';
		if (rate >= 88) return 'warning';
		return 'danger';
	}
</script>

<svelte:head><title>Suppliers — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Suppliers & Vendors</h1>
			<p class="page-subtitle">Manage supplier directory, reliability ratings, and procurement statistics</p>
		</div>
		<button class="btn-create"><Plus size={16} /> Add Supplier</button>
	</header>

	<!-- Metrics Grid -->
	<div class="summary-grid">
		<div class="summary-card">
			<span class="summary-val">{metrics.total}</span>
			<span class="summary-label">Total Suppliers</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-accent">{metrics.avgRating} <Star size={16} class="inline-icon text-accent fill-accent" /></span>
			<span class="summary-label">Average Rating</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-success">{metrics.avgOnTime}%</span>
			<span class="summary-label">On-Time Delivery</span>
		</div>
		<div class="summary-card">
			<span class="summary-val">{metrics.activeOrders}</span>
			<span class="summary-label">Active Purchase Orders</span>
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search by name or contact..." class="search-input" />
		</div>
		<div class="toolbar-right">
			<select bind:value={categoryFilter} class="filter-select">
				<option value="all">All Categories</option>
				{#each categories as cat}<option value={cat}>{cat}</option>{/each}
			</select>
		</div>
	</div>

	<!-- Suppliers Table -->
	<div class="table-card animate-fade-in-up">
		<div class="table-scroll">
			<table class="data-table">
				<thead>
					<tr>
						<th>Supplier</th>
						<th>Category</th>
						<th>Contact Details</th>
						<th>Rating</th>
						<th>On-Time Delivery</th>
						<th>Active POs</th>
						<th>Status</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each filtered as s}
						{@const level = performanceClass(s.onTime)}
						<tr>
							<td>
								<div class="supplier-cell">
									<span class="supplier-name">{s.name}</span>
									<span class="supplier-id">{s.id}</span>
								</div>
							</td>
							<td><span class="cat-badge">{s.category}</span></td>
							<td>
								<div class="contact-cell">
									<span class="contact-name">{s.contactName}</span>
									<div class="contact-details">
										<span><Phone size={11} /> {s.phone}</span>
										<span><Mail size={11} /> {s.email}</span>
									</div>
								</div>
							</td>
							<td>
								<div class="rating-cell">
									<Star size={13} class="text-warning fill-warning" />
									<span class="rating-num">{s.rating}</span>
								</div>
							</td>
							<td>
								<div class="perf-cell">
									<div class="progress-bar-bg">
										<div class="progress-bar {level}" style="width: {s.onTime}%"></div>
									</div>
									<span class="perf-num {level}">{s.onTime}%</span>
								</div>
							</td>
							<td class="po-cell">{s.activeOrders}</td>
							<td>
								<span class="badge {s.status === 'Preferred' ? 'success' : s.status === 'Active' ? 'info' : 'warning'}">
									{s.status}
								</span>
							</td>
							<td>
								<button class="btn-action">Place Order</button>
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
	@media (max-width: 640px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
	.summary-card { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-val { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); display: flex; align-items: center; gap: 6px; }
	.summary-val.text-accent { color: var(--color-accent); }
	.summary-val.text-success { color: var(--color-success); }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.inline-icon { display: inline-block; vertical-align: middle; }

	.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
	.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); min-width: 260px; color: var(--color-text-tertiary); }
	.search-box:focus-within { border-color: var(--color-accent); }
	.search-input { border: none; background: transparent; outline: none; color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; flex: 1; }
	.search-input::placeholder { color: var(--color-text-muted); }
	.toolbar-right { display: flex; gap: 8px; }
	.filter-select { padding: 8px 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; cursor: pointer; outline: none; }

	.table-card { border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); overflow: hidden; }
	.table-scroll { overflow-x: auto; }
	.data-table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
	.data-table thead { background: var(--color-bg-tertiary); }
	.data-table th { padding: 12px 16px; text-align: left; font-weight: 600; font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border); }
	.data-table td { padding: 12px 16px; border-bottom: 1px solid var(--color-border-subtle); color: var(--color-text-primary); }
	.data-table tbody tr { transition: background var(--transition-fast); }
	.data-table tbody tr:hover { background: var(--color-bg-hover); }

	.supplier-cell { display: flex; flex-direction: column; gap: 2px; }
	.supplier-name { font-weight: 600; color: var(--color-text-primary); }
	.supplier-id { font-family: var(--font-mono); font-size: 0.6875rem; color: var(--color-text-tertiary); }
	
	.cat-badge { font-size: 0.75rem; color: var(--color-text-secondary); background: var(--color-bg-tertiary); padding: 4px 8px; border-radius: var(--radius-sm); border: 1px solid var(--color-border); }
	
	.contact-cell { display: flex; flex-direction: column; gap: 4px; }
	.contact-name { font-weight: 500; color: var(--color-text-primary); }
	.contact-details { display: flex; flex-direction: column; gap: 2px; font-size: 0.6875rem; color: var(--color-text-secondary); }
	.contact-details span { display: flex; align-items: center; gap: 4px; }

	.rating-cell { display: flex; align-items: center; gap: 4px; }
	.rating-num { font-weight: 600; font-size: 0.75rem; }

	.perf-cell { display: flex; align-items: center; gap: 8px; min-width: 110px; }
	.progress-bar-bg { flex: 1; height: 6px; border-radius: var(--radius-full); background: var(--color-bg-tertiary); overflow: hidden; }
	.progress-bar { height: 100%; border-radius: var(--radius-full); }
	.progress-bar.success { background: var(--color-success); }
	.progress-bar.warning { background: var(--color-warning); }
	.progress-bar.danger { background: var(--color-danger); }
	.perf-num { font-size: 0.75rem; font-weight: 600; }
	.perf-num.success { color: var(--color-success); }
	.perf-num.warning { color: var(--color-warning); }
	.perf-num.danger { color: var(--color-danger); }

	.po-cell { font-weight: 600; text-align: center; }

	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.info { background: var(--color-accent-muted); color: var(--color-accent); }
	.badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }

	.btn-action { padding: 6px 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: all var(--transition-fast); }
	.btn-action:hover { background: var(--color-accent); border-color: var(--color-accent); color: white; }
</style>
