<!--
  Suppliers page — Interactive supplier directory with Add Supplier modal, Details dialog, and CSV export.
-->
<script lang="ts">
	import {
		Search, Plus, Star, Phone, Mail, Award, TrendingUp, Calendar,
		ChevronRight, Download, X, Eye, CheckCircle2, Building2
	} from '@lucide/svelte';

	interface SupplierItem {
		id: string;
		name: string;
		category: string;
		contactName: string;
		email: string;
		phone: string;
		rating: number;
		onTime: number;
		activeOrders: number;
		status: 'Preferred' | 'Active' | 'Under Review';
		city?: string;
	}

	let searchQuery = $state('');
	let categoryFilter = $state('all');

	let supplierList = $state<SupplierItem[]>([
		{ id: 'SPL-001', name: 'Bengal Agro Ltd', category: 'Food & Beverages', contactName: 'Mizanur Rahman', email: 'mizan@bengalagro.com', phone: '+880-1711-223344', rating: 4.8, onTime: 97, activeOrders: 3, status: 'Preferred', city: 'Rajshahi' },
		{ id: 'SPL-002', name: 'Chittagong Textiles Co.', category: 'Textiles', contactName: 'Farhana Kabir', email: 'fkabir@ctgtextiles.com', phone: '+880-1811-556677', rating: 4.5, onTime: 92, activeOrders: 1, status: 'Active', city: 'Chittagong' },
		{ id: 'SPL-003', name: 'Dhaka Leather Craft', category: 'Handicrafts', contactName: 'Sajidul Islam', email: 'sajid@dhakaleather.com', phone: '+880-1911-889900', rating: 4.2, onTime: 88, activeOrders: 2, status: 'Active', city: 'Hazaribagh, Dhaka' },
		{ id: 'SPL-004', name: 'Sylhet Tea Estates', category: 'Food & Beverages', contactName: 'Tanzeem Ahmed', email: 't.ahmed@sylhettea.com', phone: '+880-1311-112233', rating: 4.9, onTime: 99, activeOrders: 0, status: 'Preferred', city: 'Sreemangal' },
		{ id: 'SPL-005', name: 'Rajshahi Fruit Growers', category: 'Food & Beverages', contactName: 'Asaduzzaman', email: 'asad@rajshahifruit.com', phone: '+880-1511-445566', rating: 4.0, onTime: 85, activeOrders: 4, status: 'Under Review', city: 'Rajshahi' },
	]);

	// Modals
	let showCreateModal = $state(false);
	let selectedSupplier = $state<SupplierItem | null>(null);

	// New supplier form
	let newName = $state('');
	let newCategory = $state('Food & Beverages');
	let newContact = $state('');
	let newEmail = $state('');
	let newPhone = $state('');
	let newCity = $state('Dhaka');

	const categories = $derived(['all', ...new Set(supplierList.map(s => s.category))]);

	const filtered = $derived(
		supplierList.filter(s => {
			const matchSearch = !searchQuery || 
				s.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
				s.contactName.toLowerCase().includes(searchQuery.toLowerCase());
			const matchCat = categoryFilter === 'all' || s.category === categoryFilter;
			return matchSearch && matchCat;
		})
	);

	const metrics = $derived({
		total: supplierList.length,
		avgRating: (supplierList.reduce((acc, s) => acc + s.rating, 0) / (supplierList.length || 1)).toFixed(1),
		avgOnTime: Math.round(supplierList.reduce((acc, s) => acc + s.onTime, 0) / (supplierList.length || 1)),
		activeOrders: supplierList.reduce((acc, s) => acc + s.activeOrders, 0),
	});

	function performanceClass(rate: number): string {
		if (rate >= 95) return 'success';
		if (rate >= 88) return 'warning';
		return 'danger';
	}

	function handleAddSupplier(e: Event) {
		e.preventDefault();
		if (!newName) return;

		const count = supplierList.length + 1;
		const newSpl: SupplierItem = {
			id: `SPL-${String(count).padStart(3, '0')}`,
			name: newName,
			category: newCategory,
			contactName: newContact || 'Procurement Rep',
			email: newEmail || `vendor@${newName.toLowerCase().replace(/[^a-z0-9]/g, '')}.com`,
			phone: newPhone || '+880 1712-000000',
			rating: 4.5,
			onTime: 95,
			activeOrders: 0,
			status: 'Active',
			city: newCity,
		};

		supplierList = [newSpl, ...supplierList];
		showCreateModal = false;
		newName = '';
		newContact = '';
	}

	function exportSuppliersCSV() {
		const headers = 'Supplier_ID,Company_Name,Category,Contact_Person,Email,Phone,Rating,On_Time_Pct,City,Status\n';
		const rows = filtered.map(s =>
			`"${s.id}","${s.name}","${s.category}","${s.contactName}","${s.email}","${s.phone}",${s.rating},${s.onTime},"${s.city || ''}","${s.status}"`
		).join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_suppliers_export_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Suppliers — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Suppliers & Vendors</h1>
			<p class="page-subtitle">Manage supplier directory, reliability ratings, and procurement statistics</p>
		</div>
		<button class="btn-create" onclick={() => showCreateModal = true}>
			<Plus size={16} /> Add Supplier
		</button>
	</header>

	<!-- Metrics Grid -->
	<div class="summary-grid">
		<div class="card summary-card">
			<span class="summary-val">{metrics.total}</span>
			<span class="summary-label">Total Suppliers</span>
		</div>
		<div class="card summary-card">
			<span class="summary-val text-accent">★ {metrics.avgRating}</span>
			<span class="summary-label">Average Vendor Rating</span>
		</div>
		<div class="card summary-card">
			<span class="summary-val text-success">{metrics.avgOnTime}%</span>
			<span class="summary-label">On-Time Delivery Rate</span>
		</div>
		<div class="card summary-card">
			<span class="summary-val">{metrics.activeOrders}</span>
			<span class="summary-label">Active Purchase Orders</span>
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input type="text" bind:value={searchQuery} placeholder="Search supplier or contact person..." class="search-input" aria-label="Search suppliers" />
		</div>
		<div class="toolbar-right">
			<select bind:value={categoryFilter} class="filter-select" aria-label="Filter category">
				{#each categories as cat}
					<option value={cat}>{cat === 'all' ? 'All Categories' : cat}</option>
				{/each}
			</select>
			<button class="btn-icon" onclick={exportSuppliersCSV} title="Export CSV" aria-label="Export suppliers CSV">
				<Download size={16} />
			</button>
		</div>
	</div>

	<!-- Suppliers Grid -->
	<div class="supplier-grid">
		{#each filtered as s}
			<div class="card supplier-card">
				<div class="supplier-top">
					<div>
						<h3 class="supplier-name">{s.name}</h3>
						<span class="supplier-cat">{s.category}</span>
					</div>
					<span class="badge badge-{s.status === 'Preferred' ? 'success' : s.status === 'Active' ? 'accent' : 'warning'}">{s.status}</span>
				</div>

				<div class="supplier-stats">
					<div class="stat-pill">
						<span class="stat-num">★ {s.rating}</span>
						<span class="stat-sub">Score</span>
					</div>
					<div class="stat-pill">
						<span class="stat-num text-{performanceClass(s.onTime)}">{s.onTime}%</span>
						<span class="stat-sub">On-Time</span>
					</div>
					<div class="stat-pill">
						<span class="stat-num">{s.activeOrders}</span>
						<span class="stat-sub">Active POs</span>
					</div>
				</div>

				<div class="supplier-contact">
					<div class="contact-row"><Phone size={13} /> {s.phone}</div>
					<div class="contact-row"><Mail size={13} /> {s.email}</div>
				</div>

				<div class="supplier-footer">
					<button class="btn-view" onclick={() => selectedSupplier = s}>
						<Eye size={13} /> View Vendor Profile
					</button>
				</div>
			</div>
		{/each}
	</div>

	<!-- Supplier Details Modal -->
	{#if selectedSupplier}
		<div class="modal-backdrop" onclick={() => selectedSupplier = null} role="presentation">
			<div class="modal-card" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" aria-labelledby="spl-details-title" tabindex="-1">
				<div class="modal-header">
					<div>
						<h2 id="spl-details-title" class="modal-title">{selectedSupplier.name}</h2>
						<span class="supplier-cat">{selectedSupplier.category} ({selectedSupplier.id})</span>
					</div>
					<button class="btn-close" onclick={() => selectedSupplier = null} aria-label="Close dialog">
						<X size={18} />
					</button>
				</div>
				<div class="modal-body">
					<div class="detail-grid">
						<div class="detail-item"><span class="d-lbl">Contact Person</span><span class="d-val">{selectedSupplier.contactName}</span></div>
						<div class="detail-item"><span class="d-lbl">Phone</span><span class="d-val">{selectedSupplier.phone}</span></div>
						<div class="detail-item"><span class="d-lbl">Email</span><span class="d-val">{selectedSupplier.email}</span></div>
						<div class="detail-item"><span class="d-lbl">Location / City</span><span class="d-val">{selectedSupplier.city || 'Dhaka'}</span></div>
						<div class="detail-item"><span class="d-lbl">Vendor Rating</span><span class="d-val text-accent font-bold">★ {selectedSupplier.rating} / 5.0</span></div>
						<div class="detail-item"><span class="d-lbl">On-Time Reliability</span><span class="d-val text-success font-bold">{selectedSupplier.onTime}%</span></div>
					</div>
				</div>
				<div class="modal-footer">
					<button class="btn-primary" onclick={() => selectedSupplier = null}>
						Done
					</button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Add Supplier Modal -->
	{#if showCreateModal}
		<div class="modal-backdrop" onclick={() => showCreateModal = false} role="presentation">
			<div class="modal-card" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" aria-labelledby="add-spl-title" tabindex="-1">
				<div class="modal-header">
					<h2 id="add-spl-title" class="modal-title">Add Supplier / Vendor</h2>
					<button class="btn-close" onclick={() => showCreateModal = false} aria-label="Close dialog">
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleAddSupplier} class="modal-form">
					<div class="form-group">
						<label for="as-name">Vendor Company Name</label>
						<input id="as-name" type="text" placeholder="e.g. Chittagong Steel Suppliers" bind:value={newName} required />
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="as-cat">Category</label>
							<input id="as-cat" type="text" placeholder="Construction" bind:value={newCategory} required />
						</div>
						<div class="form-group">
							<label for="as-city">City / Hub</label>
							<input id="as-city" type="text" placeholder="Chittagong" bind:value={newCity} />
						</div>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="as-contact">Contact Person</label>
							<input id="as-contact" type="text" placeholder="e.g. Mr. Rafiqul Bari" bind:value={newContact} />
						</div>
						<div class="form-group">
							<label for="as-phone">Phone (+880)</label>
							<input id="as-phone" type="text" placeholder="+880 1812-345678" bind:value={newPhone} />
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => showCreateModal = false}>Cancel</button>
						<button type="submit" class="btn-primary">Save Vendor</button>
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

	.summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.summary-card { padding: 16px; display: flex; flex-direction: column; gap: 4px; }
	.summary-label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; }
	.summary-val { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); font-variant-numeric: tabular-nums; }
	.text-accent { color: var(--color-accent); }
	.text-success { color: var(--color-success); }

	.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
	.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-md); flex: 1; max-width: 380px; color: var(--color-text-tertiary); }
	.search-input { background: none; border: none; outline: none; font-size: 0.8125rem; color: var(--color-text-primary); width: 100%; }
	.toolbar-right { display: flex; gap: 8px; }
	.filter-select { padding: 8px 12px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; }
	.btn-icon { display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-secondary); cursor: pointer; }
	.btn-icon:hover { border-color: var(--color-accent); color: var(--color-accent); }

	.supplier-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
	.supplier-card { padding: 18px; display: flex; flex-direction: column; gap: 12px; }
	.supplier-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
	.supplier-name { font-size: 0.9375rem; font-weight: 700; color: var(--color-text-primary); margin: 0; }
	.supplier-cat { font-size: 0.6875rem; color: var(--color-text-tertiary); text-transform: uppercase; letter-spacing: 0.04em; }

	.badge { font-size: 0.6875rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
	.badge-success { background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.badge-accent { background: color-mix(in srgb, var(--color-accent) 15%, transparent); color: var(--color-accent); }
	.badge-warning { background: color-mix(in srgb, #f59e0b 15%, transparent); color: #d97706; }

	.supplier-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; background: var(--color-bg-primary); padding: 10px; border-radius: var(--radius-md); border: 1px solid var(--color-border); }
	.stat-pill { display: flex; flex-direction: column; align-items: center; gap: 2px; }
	.stat-num { font-size: 0.9375rem; font-weight: 700; color: var(--color-text-primary); }
	.stat-sub { font-size: 0.625rem; color: var(--color-text-tertiary); text-transform: uppercase; }

	.supplier-contact { display: flex; flex-direction: column; gap: 4px; font-size: 0.75rem; color: var(--color-text-secondary); }
	.contact-row { display: flex; align-items: center; gap: 6px; }

	.supplier-footer { margin-top: auto; padding-top: 10px; border-top: 1px solid var(--color-border); }
	.btn-view { width: 100%; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 7px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: 0.75rem; font-weight: 600; color: var(--color-text-primary); cursor: pointer; }
	.btn-view:hover { border-color: var(--color-accent); color: var(--color-accent); }

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
	.font-bold { font-weight: 700; }

	.modal-form { display: flex; flex-direction: column; gap: 14px; }
	.form-group { display: flex; flex-direction: column; gap: 6px; }
	.form-group label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; }
	.form-group input { padding: 8px 12px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; }
	.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
	.modal-footer { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }
</style>
