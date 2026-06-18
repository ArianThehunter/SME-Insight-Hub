<!--
  Customers page — Customer list with lifetime value and segmentation.
-->
<script lang="ts">
	import { Search, Plus, Download, Star, Eye, ChevronLeft, ChevronRight, Users } from '@lucide/svelte';

	let searchQuery = $state('');
	let segmentFilter = $state('all');
	let currentPage = $state(1);
	const perPage = 8;

	const customers = [
		{ id: 1, name: 'Rahman Textiles Ltd.', contact: 'Mr. Abdur Rahman', email: 'rahman@textiles.com.bd', phone: '+880 1711-234567', segment: 'Enterprise', ltv: 4580000, orders: 87, lastOrder: '2026-06-18', status: 'active' },
		{ id: 2, name: 'Dhaka Electronics Hub', contact: 'Ms. Fatima Akter', email: 'fatima@deh.com.bd', phone: '+880 1812-345678', segment: 'Enterprise', ltv: 3250000, orders: 64, lastOrder: '2026-06-17', status: 'active' },
		{ id: 3, name: 'Chittagong Spice Co.', contact: 'Mr. Kamal Hossain', email: 'kamal@ctgspice.com', phone: '+880 1913-456789', segment: 'SME', ltv: 1820000, orders: 45, lastOrder: '2026-06-17', status: 'active' },
		{ id: 4, name: 'Sylhet Tea Gardens', contact: 'Mr. Rajan Das', email: 'rajan@sylhettea.com', phone: '+880 1614-567890', segment: 'Enterprise', ltv: 6750000, orders: 120, lastOrder: '2026-06-16', status: 'active' },
		{ id: 5, name: 'Rajshahi Mangoes Inc.', contact: 'Ms. Nusrat Jahan', email: 'nusrat@rajmango.com', phone: '+880 1515-678901', segment: 'SME', ltv: 980000, orders: 23, lastOrder: '2026-06-16', status: 'active' },
		{ id: 6, name: 'Khulna Fisheries', contact: 'Mr. Habib Sarker', email: 'habib@khulnafish.com', phone: '+880 1716-789012', segment: 'SME', ltv: 2340000, orders: 56, lastOrder: '2026-06-15', status: 'active' },
		{ id: 7, name: 'Narayanganj Jute Works', contact: 'Mr. Rafiq Islam', email: 'rafiq@juteworks.com', phone: '+880 1817-890123', segment: 'Enterprise', ltv: 8920000, orders: 145, lastOrder: '2026-06-15', status: 'active' },
		{ id: 8, name: 'Comilla Ceramics', contact: 'Ms. Ayesha Siddiqui', email: 'ayesha@ceramics.com', phone: '+880 1918-901234', segment: 'Startup', ltv: 420000, orders: 12, lastOrder: '2026-06-14', status: 'inactive' },
		{ id: 9, name: 'Bogura Steel Corp.', contact: 'Mr. Masud Khan', email: 'masud@bogurasteel.com', phone: '+880 1619-012345', segment: 'Enterprise', ltv: 12500000, orders: 198, lastOrder: '2026-06-14', status: 'active' },
		{ id: 10, name: 'Gazipur Garments Ltd.', contact: 'Ms. Shamima Begum', email: 'shamima@garments.com', phone: '+880 1520-123456', segment: 'Enterprise', ltv: 5680000, orders: 92, lastOrder: '2026-06-13', status: 'active' },
		{ id: 11, name: 'Jessore Food Products', contact: 'Mr. Alamgir Hasan', email: 'alamgir@jessorefood.com', phone: '+880 1721-234567', segment: 'SME', ltv: 1150000, orders: 34, lastOrder: '2026-06-13', status: 'active' },
		{ id: 12, name: 'Tangail Handicrafts', contact: 'Ms. Ruma Khatun', email: 'ruma@handicrafts.com', phone: '+880 1822-345678', segment: 'Startup', ltv: 380000, orders: 8, lastOrder: '2026-06-11', status: 'active' },
	];

	const segments = [
		{ name: 'Enterprise', count: 6, revenue: 41680000, color: 'accent' },
		{ name: 'SME', count: 4, revenue: 6290000, color: 'success' },
		{ name: 'Startup', count: 2, revenue: 800000, color: 'warning' },
	];

	const filtered = $derived(
		customers.filter(c => {
			const matchSearch = !searchQuery || c.name.toLowerCase().includes(searchQuery.toLowerCase()) || c.contact.toLowerCase().includes(searchQuery.toLowerCase());
			const matchSeg = segmentFilter === 'all' || c.segment === segmentFilter;
			return matchSearch && matchSeg;
		})
	);

	const totalPages = $derived(Math.ceil(filtered.length / perPage));
	const paginated = $derived(filtered.slice((currentPage - 1) * perPage, currentPage * perPage));

	function fmt(v: number): string {
		if (v >= 1000000) return `৳ ${(v / 1000000).toFixed(1)}M`;
		if (v >= 1000) return `৳ ${(v / 1000).toFixed(0)}K`;
		return `৳ ${v}`;
	}

	const segColors: Record<string, string> = { Enterprise: 'accent', SME: 'success', Startup: 'warning' };
</script>

<svelte:head><title>Customers — SME Insight Hub</title></svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Customers</h1>
			<p class="page-subtitle">Manage customer relationships and lifetime value</p>
		</div>
		<button class="btn-create"><Plus size={16} /> Add Customer</button>
	</header>

	<!-- Segment Cards -->
	<div class="seg-grid">
		{#each segments as seg, i}
			<div class="seg-card animate-fade-in-up stagger-{i + 1}">
				<div class="seg-head">
					<span class="seg-badge {seg.color}">{seg.name}</span>
					<span class="seg-count">{seg.count} customers</span>
				</div>
				<div class="seg-value">{fmt(seg.revenue)}</div>
				<div class="seg-label">Total Revenue</div>
			</div>
		{/each}
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search customers..." class="search-input" />
		</div>
		<div class="toolbar-right">
			<select bind:value={segmentFilter} class="filter-select">
				<option value="all">All Segments</option>
				<option value="Enterprise">Enterprise</option>
				<option value="SME">SME</option>
				<option value="Startup">Startup</option>
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
						<th>Customer</th>
						<th>Contact</th>
						<th>Segment</th>
						<th>Lifetime Value</th>
						<th>Orders</th>
						<th>Last Order</th>
						<th>Status</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each paginated as c}
						<tr>
							<td>
								<div class="customer-cell">
									<div class="avatar">{c.name.charAt(0)}</div>
									<div class="cust-info">
										<span class="cust-name">{c.name}</span>
										<span class="cust-email">{c.email}</span>
									</div>
								</div>
							</td>
							<td class="contact-cell">{c.contact}</td>
							<td><span class="badge {segColors[c.segment]}">{c.segment}</span></td>
							<td class="ltv-cell">{fmt(c.ltv)}</td>
							<td class="orders-cell">{c.orders}</td>
							<td class="date-cell">{new Date(c.lastOrder).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' })}</td>
							<td><span class="status-dot" class:active={c.status === 'active'}></span></td>
							<td><button class="btn-view"><Eye size={14} /></button></td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		<div class="pagination">
			<span class="pg-info">Showing {(currentPage-1)*perPage+1}–{Math.min(currentPage*perPage, filtered.length)} of {filtered.length}</span>
			<div class="pg-controls">
				<button class="pg-btn" disabled={currentPage<=1} onclick={()=>currentPage--}><ChevronLeft size={16}/></button>
				{#each Array(totalPages) as _, i}<button class="pg-btn" class:active={currentPage===i+1} onclick={()=>currentPage=i+1}>{i+1}</button>{/each}
				<button class="pg-btn" disabled={currentPage>=totalPages} onclick={()=>currentPage++}><ChevronRight size={16}/></button>
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

	.seg-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
	.seg-card { padding: 20px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); transition: all var(--transition-fast); }
	.seg-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
	.seg-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
	.seg-badge { padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.seg-badge.accent { background: var(--color-accent-muted); color: var(--color-accent); }
	.seg-badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.seg-badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }
	.seg-count { font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.seg-value { font-size: 1.25rem; font-weight: 700; color: var(--color-text-primary); }
	.seg-label { font-size: 0.6875rem; color: var(--color-text-tertiary); margin-top: 2px; }

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
	.data-table td { padding: 12px 16px; border-bottom: 1px solid var(--color-border-subtle); }
	.data-table tbody tr { transition: background var(--transition-fast); }
	.data-table tbody tr:hover { background: var(--color-bg-hover); }

	.customer-cell { display: flex; align-items: center; gap: 10px; }
	.avatar { width: 32px; height: 32px; border-radius: var(--radius-md); background: var(--color-accent-muted); color: var(--color-accent); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; }
	.cust-info { display: flex; flex-direction: column; }
	.cust-name { font-weight: 500; color: var(--color-text-primary); white-space: nowrap; }
	.cust-email { font-size: 0.6875rem; color: var(--color-text-tertiary); }
	.contact-cell { color: var(--color-text-secondary); white-space: nowrap; }
	.ltv-cell { font-weight: 600; color: var(--color-text-primary); white-space: nowrap; }
	.orders-cell { text-align: center; color: var(--color-text-secondary); }
	.date-cell { color: var(--color-text-secondary); white-space: nowrap; }

	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.badge.accent { background: var(--color-accent-muted); color: var(--color-accent); }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }

	.status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--color-text-muted); display: inline-block; }
	.status-dot.active { background: var(--color-success); box-shadow: 0 0 6px rgba(16,185,129,0.4); }

	.btn-view { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: transparent; color: var(--color-text-tertiary); cursor: pointer; transition: all var(--transition-fast); }
	.btn-view:hover { background: var(--color-accent-muted); color: var(--color-accent); border-color: var(--color-accent); }

	.pagination { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-top: 1px solid var(--color-border); flex-wrap: wrap; gap: 12px; }
	.pg-info { font-size: 0.75rem; color: var(--color-text-tertiary); }
	.pg-controls { display: flex; gap: 4px; }
	.pg-btn { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: transparent; color: var(--color-text-secondary); font-size: 0.75rem; font-weight: 500; cursor: pointer; transition: all var(--transition-fast); }
	.pg-btn:hover:not(:disabled) { background: var(--color-bg-hover); }
	.pg-btn.active { background: var(--color-accent); color: white; border-color: var(--color-accent); }
	.pg-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
