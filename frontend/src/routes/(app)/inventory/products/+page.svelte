<!--
  Products page — Interactive product catalog with Add Product modal, stock badges, and CSV export.
-->
<script lang="ts">
	import {
		Search,
		Plus,
		Download,
		Package,
		AlertTriangle,
		Eye,
		X,
		CheckCircle2,
		DollarSign,
		Layers
	} from '@lucide/svelte';

	interface ProductItem {
		sku: string;
		name: string;
		category: string;
		price: number;
		cost: number;
		stock: number;
		reorder: number;
		status: 'In Stock' | 'Low Stock' | 'Out of Stock';
		unit?: string;
	}

	let searchQuery = $state('');
	let categoryFilter = $state('all');

	let productList = $state<ProductItem[]>([
		{
			sku: 'PRD-001',
			name: 'Premium Basmati Rice 5kg',
			category: 'Food & Beverages',
			price: 850,
			cost: 620,
			stock: 342,
			reorder: 100,
			status: 'In Stock',
			unit: 'bag'
		},
		{
			sku: 'PRD-002',
			name: 'Organic Mustard Oil 1L',
			category: 'Food & Beverages',
			price: 320,
			cost: 210,
			stock: 580,
			reorder: 200,
			status: 'In Stock',
			unit: 'bottle'
		},
		{
			sku: 'PRD-003',
			name: 'Bengal Spice Mix Set',
			category: 'Food & Beverages',
			price: 450,
			cost: 280,
			stock: 15,
			reorder: 50,
			status: 'Low Stock',
			unit: 'pack'
		},
		{
			sku: 'PRD-004',
			name: 'Handloom Cotton Saree',
			category: 'Textiles',
			price: 3200,
			cost: 1800,
			stock: 78,
			reorder: 30,
			status: 'In Stock',
			unit: 'pcs'
		},
		{
			sku: 'PRD-005',
			name: 'Artisan Leather Bag',
			category: 'Handicrafts',
			price: 4500,
			cost: 2800,
			stock: 0,
			reorder: 15,
			status: 'Out of Stock',
			unit: 'pcs'
		},
		{
			sku: 'PRD-006',
			name: 'Jamdani Silk Fabric (1m)',
			category: 'Textiles',
			price: 2800,
			cost: 1650,
			stock: 120,
			reorder: 40,
			status: 'In Stock',
			unit: 'meter'
		},
		{
			sku: 'PRD-007',
			name: 'Pabna Yogurt 500g',
			category: 'Food & Beverages',
			price: 180,
			cost: 110,
			stock: 8,
			reorder: 100,
			status: 'Low Stock',
			unit: 'pot'
		},
		{
			sku: 'PRD-008',
			name: 'Brass Decorative Plate',
			category: 'Handicrafts',
			price: 1500,
			cost: 850,
			stock: 45,
			reorder: 20,
			status: 'In Stock',
			unit: 'pcs'
		},
		{
			sku: 'PRD-009',
			name: 'Sylhet Orange Tea 250g',
			category: 'Food & Beverages',
			price: 650,
			cost: 380,
			stock: 234,
			reorder: 80,
			status: 'In Stock',
			unit: 'box'
		},
		{
			sku: 'PRD-010',
			name: 'Jute Tote Bag (Eco)',
			category: 'Handicrafts',
			price: 550,
			cost: 280,
			stock: 0,
			reorder: 50,
			status: 'Out of Stock',
			unit: 'pcs'
		},
		{
			sku: 'PRD-011',
			name: 'Nakshi Kantha Bedcover',
			category: 'Textiles',
			price: 5200,
			cost: 3100,
			stock: 22,
			reorder: 10,
			status: 'In Stock',
			unit: 'pcs'
		},
		{
			sku: 'PRD-012',
			name: 'Mango Pickle Jar 500g',
			category: 'Food & Beverages',
			price: 220,
			cost: 120,
			stock: 456,
			reorder: 150,
			status: 'In Stock',
			unit: 'jar'
		}
	]);

	// Modals
	let showCreateModal = $state(false);
	let selectedProduct = $state<ProductItem | null>(null);

	// New Product form
	let newName = $state('');
	let newCategory = $state('Textiles');
	let newPrice = $state<number>(500);
	let newCost = $state<number>(300);
	let newStock = $state<number>(50);
	let newReorder = $state<number>(10);
	let newUnit = $state('pcs');

	const categories = $derived(['all', ...new Set(productList.map((p) => p.category))]);

	const filtered = $derived(
		productList.filter((p) => {
			const matchSearch =
				!searchQuery ||
				p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				p.sku.toLowerCase().includes(searchQuery.toLowerCase());
			const matchCat = categoryFilter === 'all' || p.category === categoryFilter;
			return matchSearch && matchCat;
		})
	);

	const stockSummary = $derived({
		total: productList.length,
		inStock: productList.filter((p) => p.status === 'In Stock').length,
		low: productList.filter((p) => p.status === 'Low Stock').length,
		out: productList.filter((p) => p.status === 'Out of Stock').length
	});

	function handleAddProduct(e: Event) {
		e.preventDefault();
		if (!newName) return;

		const count = productList.length + 1;
		let status: 'In Stock' | 'Low Stock' | 'Out of Stock' = 'In Stock';
		if (newStock === 0) status = 'Out of Stock';
		else if (newStock <= newReorder) status = 'Low Stock';

		const newProd: ProductItem = {
			sku: `PRD-${String(count).padStart(3, '0')}`,
			name: newName,
			category: newCategory,
			price: newPrice,
			cost: newCost,
			stock: newStock,
			reorder: newReorder,
			status,
			unit: newUnit
		};

		productList = [newProd, ...productList];
		showCreateModal = false;
		newName = '';
	}

	function exportProductsCSV() {
		const headers = 'SKU,Name,Category,Price_BDT,Cost_BDT,Stock_Qty,Reorder_Level,Status,Unit\n';
		const rows = filtered
			.map(
				(p) =>
					`"${p.sku}","${p.name}","${p.category}",${p.price},${p.cost},${p.stock},${p.reorder},"${p.status}","${p.unit || 'pcs'}"`
			)
			.join('\n');

		const blob = new Blob(['\uFEFF' + headers + rows], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_products_catalog_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head><title>Products — SME Insight Hub</title></svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Product Catalog & Inventory</h1>
			<p class="page-subtitle">
				Track SKUs, retail pricing, gross margins, and safety stock levels
			</p>
		</div>
		<button class="btn-create" onclick={() => (showCreateModal = true)}>
			<Plus size={16} /> Add Product
		</button>
	</header>

	<!-- Summary Cards -->
	<div class="sum-grid">
		<div class="card sum-card">
			<span class="sum-label">Total SKUs</span>
			<span class="sum-val">{stockSummary.total}</span>
		</div>
		<div class="card sum-card text-success">
			<span class="sum-label">In Stock</span>
			<span class="sum-val">{stockSummary.inStock}</span>
		</div>
		<div class="card sum-card text-warning">
			<span class="sum-label">Low Stock</span>
			<span class="sum-val">{stockSummary.low}</span>
		</div>
		<div class="card sum-card text-danger">
			<span class="sum-label">Out of Stock</span>
			<span class="sum-val">{stockSummary.out}</span>
		</div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box">
			<Search size={16} />
			<input
				type="text"
				bind:value={searchQuery}
				placeholder="Search product name or SKU..."
				class="search-input"
				aria-label="Search products"
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
				onclick={exportProductsCSV}
				title="Export CSV"
				aria-label="Export products catalog"
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
						<th>SKU</th>
						<th>Product Name</th>
						<th>Category</th>
						<th>Selling Price</th>
						<th>Unit Cost</th>
						<th>Est. Margin</th>
						<th>Current Stock</th>
						<th>Status</th>
						<th>Action</th>
					</tr>
				</thead>
				<tbody>
					{#each filtered as p}
						{@const margin = Math.round(((p.price - p.cost) / p.price) * 100)}
						<tr>
							<td><code class="sku-tag">{p.sku}</code></td>
							<td><strong>{p.name}</strong></td>
							<td><span class="cat-pill">{p.category}</span></td>
							<td class="num-cell">৳ {p.price.toLocaleString()}</td>
							<td class="num-cell text-muted">৳ {p.cost.toLocaleString()}</td>
							<td class="num-cell text-success font-semibold">{margin}%</td>
							<td class="num-cell"
								><strong>{p.stock}</strong> <span class="unit-text">{p.unit || 'pcs'}</span></td
							>
							<td>
								<span
									class="badge badge-{p.status === 'In Stock'
										? 'success'
										: p.status === 'Low Stock'
											? 'warning'
											: 'danger'}"
								>
									{p.status}
								</span>
							</td>
							<td>
								<button
									class="btn-icon-row"
									onclick={() => (selectedProduct = p)}
									title="View product details"
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

	<!-- Product Details Modal -->
	{#if selectedProduct}
		{@const marginPct = Math.round(
			((selectedProduct.price - selectedProduct.cost) / selectedProduct.price) * 100
		)}
		<div class="modal-backdrop" onclick={() => (selectedProduct = null)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="prod-details-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<div>
						<h2 id="prod-details-title" class="modal-title">{selectedProduct.name}</h2>
						<span class="sku-tag">{selectedProduct.sku}</span>
					</div>
					<button
						class="btn-close"
						onclick={() => (selectedProduct = null)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<div class="modal-body">
					<div class="detail-grid">
						<div class="detail-item">
							<span class="d-lbl">Category</span><span class="d-val"
								>{selectedProduct.category}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Stock Quantity</span><span class="d-val"
								>{selectedProduct.stock} {selectedProduct.unit || 'pcs'}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Selling Price</span><span class="d-val text-accent font-bold"
								>৳ {selectedProduct.price.toLocaleString()}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Unit Cost</span><span class="d-val"
								>৳ {selectedProduct.cost.toLocaleString()}</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Gross Margin</span><span class="d-val text-success font-bold"
								>{marginPct}%</span
							>
						</div>
						<div class="detail-item">
							<span class="d-lbl">Reorder Safety Level</span><span class="d-val"
								>{selectedProduct.reorder} units</span
							>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button class="btn-primary" onclick={() => (selectedProduct = null)}> Done </button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Add Product Modal -->
	{#if showCreateModal}
		<div class="modal-backdrop" onclick={() => (showCreateModal = false)} role="presentation">
			<div
				class="modal-card"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-labelledby="add-prod-title"
				tabindex="-1"
			>
				<div class="modal-header">
					<h2 id="add-prod-title" class="modal-title">Add New Product</h2>
					<button
						class="btn-close"
						onclick={() => (showCreateModal = false)}
						aria-label="Close dialog"
					>
						<X size={18} />
					</button>
				</div>
				<form onsubmit={handleAddProduct} class="modal-form">
					<div class="form-group">
						<label for="ap-name">Product Title</label>
						<input
							id="ap-name"
							type="text"
							placeholder="e.g. Silk Dupatta Handwoven"
							bind:value={newName}
							required
						/>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ap-cat">Category</label>
							<input
								id="ap-cat"
								type="text"
								placeholder="Textiles"
								bind:value={newCategory}
								required
							/>
						</div>
						<div class="form-group">
							<label for="ap-unit">Unit of Measure</label>
							<input id="ap-unit" type="text" placeholder="pcs / kg / meter" bind:value={newUnit} />
						</div>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ap-price">Selling Price (BDT)</label>
							<input
								id="ap-price"
								type="number"
								placeholder="1200"
								bind:value={newPrice}
								required
								min="1"
							/>
						</div>
						<div class="form-group">
							<label for="ap-cost">Unit Cost (BDT)</label>
							<input
								id="ap-cost"
								type="number"
								placeholder="800"
								bind:value={newCost}
								required
								min="1"
							/>
						</div>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="ap-stock">Initial Stock</label>
							<input
								id="ap-stock"
								type="number"
								placeholder="100"
								bind:value={newStock}
								required
								min="0"
							/>
						</div>
						<div class="form-group">
							<label for="ap-reorder">Reorder Threshold</label>
							<input
								id="ap-reorder"
								type="number"
								placeholder="20"
								bind:value={newReorder}
								required
								min="1"
							/>
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn-secondary" onclick={() => (showCreateModal = false)}
							>Cancel</button
						>
						<button type="submit" class="btn-primary">Save Product</button>
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

	.sum-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
		gap: 14px;
	}
	.sum-card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 16px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.sum-label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
	}
	.sum-val {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text-primary);
		font-variant-numeric: tabular-nums;
	}
	.text-success .sum-val {
		color: var(--color-success);
	}
	.text-warning .sum-val {
		color: #d97706;
	}
	.text-danger .sum-val {
		color: var(--color-danger);
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
	.sku-tag {
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
	.unit-text {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.text-muted {
		color: var(--color-text-tertiary);
	}
	.text-success {
		color: var(--color-success);
	}
	.font-semibold {
		font-weight: 600;
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
	.text-accent {
		color: var(--color-accent);
	}
	.font-bold {
		font-weight: 700;
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
	.form-group input {
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
