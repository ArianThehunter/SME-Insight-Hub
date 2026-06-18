<!--
  Products page — Product catalog with stock level indicators.
-->
<script lang="ts">
	import { Search, Plus, Download, Package, AlertTriangle, Eye } from '@lucide/svelte';

	let searchQuery = $state('');
	let categoryFilter = $state('all');

	const products = [
		{ sku: 'PRD-001', name: 'Premium Basmati Rice 5kg', category: 'Food & Beverages', price: 850, cost: 620, stock: 342, reorder: 100, status: 'In Stock' },
		{ sku: 'PRD-002', name: 'Organic Mustard Oil 1L', category: 'Food & Beverages', price: 320, cost: 210, stock: 580, reorder: 200, status: 'In Stock' },
		{ sku: 'PRD-003', name: 'Bengal Spice Mix Set', category: 'Food & Beverages', price: 450, cost: 280, stock: 15, reorder: 50, status: 'Low Stock' },
		{ sku: 'PRD-004', name: 'Handloom Cotton Saree', category: 'Textiles', price: 3200, cost: 1800, stock: 78, reorder: 30, status: 'In Stock' },
		{ sku: 'PRD-005', name: 'Artisan Leather Bag', category: 'Handicrafts', price: 4500, cost: 2800, stock: 0, reorder: 15, status: 'Out of Stock' },
		{ sku: 'PRD-006', name: 'Jamdani Silk Fabric (1m)', category: 'Textiles', price: 2800, cost: 1650, stock: 120, reorder: 40, status: 'In Stock' },
		{ sku: 'PRD-007', name: 'Pabna Yogurt 500g', category: 'Food & Beverages', price: 180, cost: 110, stock: 8, reorder: 100, status: 'Low Stock' },
		{ sku: 'PRD-008', name: 'Brass Decorative Plate', category: 'Handicrafts', price: 1500, cost: 850, stock: 45, reorder: 20, status: 'In Stock' },
		{ sku: 'PRD-009', name: 'Sylhet Orange Tea 250g', category: 'Food & Beverages', price: 650, cost: 380, stock: 234, reorder: 80, status: 'In Stock' },
		{ sku: 'PRD-010', name: 'Jute Tote Bag (Eco)', category: 'Handicrafts', price: 550, cost: 280, stock: 0, reorder: 50, status: 'Out of Stock' },
		{ sku: 'PRD-011', name: 'Nakshi Kantha Bedcover', category: 'Textiles', price: 5200, cost: 3100, stock: 22, reorder: 10, status: 'In Stock' },
		{ sku: 'PRD-012', name: 'Mango Pickle Jar 500g', category: 'Food & Beverages', price: 220, cost: 120, stock: 456, reorder: 150, status: 'In Stock' },
	];

	const categories = [...new Set(products.map(p => p.category))];

	const filtered = $derived(
		products.filter(p => {
			const matchSearch = !searchQuery || p.name.toLowerCase().includes(searchQuery.toLowerCase()) || p.sku.toLowerCase().includes(searchQuery.toLowerCase());
			const matchCat = categoryFilter === 'all' || p.category === categoryFilter;
			return matchSearch && matchCat;
		})
	);

	const stockSummary = $derived({
		total: products.length,
		inStock: products.filter(p => p.status === 'In Stock').length,
		low: products.filter(p => p.status === 'Low Stock').length,
		out: products.filter(p => p.status === 'Out of Stock').length,
	});

	function stockLevel(stock: number, reorder: number): string {
		if (stock === 0) return 'out';
		if (stock <= reorder) return 'low';
		return 'good';
	}
</script>

<svelte:head><title>Products — SME Insight Hub</title></svelte:head>

<div class="page">
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">Product Catalog</h1>
			<p class="page-subtitle">Manage products, pricing, and stock levels</p>
		</div>
		<button class="btn-create"><Plus size={16} /> Add Product</button>
	</header>

	<!-- Summary -->
	<div class="summary-grid">
		<div class="summary-card"><span class="summary-val">{stockSummary.total}</span><span class="summary-label">Total Products</span></div>
		<div class="summary-card"><span class="summary-val text-success">{stockSummary.inStock}</span><span class="summary-label">In Stock</span></div>
		<div class="summary-card"><span class="summary-val text-warning">{stockSummary.low}</span><span class="summary-label">Low Stock</span></div>
		<div class="summary-card"><span class="summary-val text-danger">{stockSummary.out}</span><span class="summary-label">Out of Stock</span></div>
	</div>

	<!-- Toolbar -->
	<div class="toolbar">
		<div class="search-box"><Search size={16}/><input type="text" bind:value={searchQuery} placeholder="Search by name or SKU..." class="search-input"/></div>
		<div class="toolbar-right">
			<select bind:value={categoryFilter} class="filter-select">
				<option value="all">All Categories</option>
				{#each categories as cat}<option value={cat}>{cat}</option>{/each}
			</select>
			<button class="btn-icon" title="Export CSV"><Download size={16}/></button>
		</div>
	</div>

	<!-- Table -->
	<div class="table-card animate-fade-in-up">
		<div class="table-scroll">
			<table class="data-table">
				<thead><tr><th>SKU</th><th>Product</th><th>Category</th><th>Price</th><th>Cost</th><th>Margin</th><th>Stock</th><th>Status</th><th></th></tr></thead>
				<tbody>
					{#each filtered as p}
						{@const margin = ((p.price - p.cost) / p.price * 100).toFixed(1)}
						{@const level = stockLevel(p.stock, p.reorder)}
						<tr>
							<td class="sku-cell">{p.sku}</td>
							<td class="name-cell">{p.name}</td>
							<td class="cat-cell">{p.category}</td>
							<td class="price-cell">৳ {p.price.toLocaleString()}</td>
							<td class="cost-cell">৳ {p.cost.toLocaleString()}</td>
							<td class="margin-cell">{margin}%</td>
							<td>
								<div class="stock-cell">
									<div class="stock-bar-bg">
										<div class="stock-bar {level}" style="width: {Math.min(p.stock / (p.reorder * 3) * 100, 100)}%"></div>
									</div>
									<span class="stock-num">{p.stock}</span>
								</div>
							</td>
							<td><span class="badge {level === 'good' ? 'success' : level === 'low' ? 'warning' : 'danger'}">{p.status}</span></td>
							<td><button class="btn-view"><Eye size={14}/></button></td>
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
	.summary-val { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); }
	.summary-val.text-success { color: var(--color-success); }
	.summary-val.text-warning { color: var(--color-warning); }
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

	.sku-cell { font-weight: 600; color: var(--color-accent); font-family: var(--font-mono); font-size: 0.75rem; white-space: nowrap; }
	.name-cell { font-weight: 500; max-width: 220px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.cat-cell { color: var(--color-text-secondary); white-space: nowrap; }
	.price-cell { font-weight: 600; white-space: nowrap; }
	.cost-cell { color: var(--color-text-secondary); white-space: nowrap; }
	.margin-cell { color: var(--color-success); font-weight: 500; }

	.stock-cell { display: flex; align-items: center; gap: 8px; min-width: 100px; }
	.stock-bar-bg { flex: 1; height: 6px; border-radius: var(--radius-full); background: var(--color-bg-tertiary); overflow: hidden; }
	.stock-bar { height: 100%; border-radius: var(--radius-full); transition: width 0.6s ease; }
	.stock-bar.good { background: var(--color-success); }
	.stock-bar.low { background: var(--color-warning); }
	.stock-bar.out { background: var(--color-danger); width: 0 !important; }
	.stock-num { font-size: 0.75rem; font-weight: 500; color: var(--color-text-secondary); min-width: 28px; }

	.badge { display: inline-flex; padding: 3px 10px; border-radius: var(--radius-full); font-size: 0.6875rem; font-weight: 600; }
	.badge.success { background: var(--color-success-muted); color: var(--color-success); }
	.badge.warning { background: var(--color-warning-muted); color: var(--color-warning); }
	.badge.danger { background: var(--color-danger-muted); color: var(--color-danger); }

	.btn-view { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: transparent; color: var(--color-text-tertiary); cursor: pointer; transition: all var(--transition-fast); }
	.btn-view:hover { background: var(--color-accent-muted); color: var(--color-accent); border-color: var(--color-accent); }
</style>
