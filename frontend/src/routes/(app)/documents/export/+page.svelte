<!--
  CSV Export — Export your business data as CSV or Excel files.
-->
<script lang="ts">
	import { FileDown, Download, CheckCircle2, Loader2, Calendar } from '@lucide/svelte';

	interface ExportItem {
		id: string;
		name: string;
		description: string;
		endpoint: string;
		icon: string;
		rowCount: number;
		lastExported: string;
	}

	const exports: ExportItem[] = [
		{ id: 'customers', name: 'Customers', description: 'All customer records with contact info and lifetime value', endpoint: '/sales/customers', icon: '👥', rowCount: 1247, lastExported: '2 days ago' },
		{ id: 'orders', name: 'Sales Orders', description: 'Orders with line items, status, and payment details', endpoint: '/sales/orders', icon: '🛒', rowCount: 8432, lastExported: '1 day ago' },
		{ id: 'products', name: 'Product Catalog', description: 'All products with SKU, price, cost, and stock levels', endpoint: '/sales/products', icon: '📦', rowCount: 342, lastExported: '3 days ago' },
		{ id: 'expenses', name: 'Expenses', description: 'All expense records by category, vendor, and date', endpoint: '/finance/expenses', icon: '💸', rowCount: 2156, lastExported: 'Today' },
		{ id: 'invoices', name: 'Invoices', description: 'All invoices with payment status and amounts', endpoint: '/finance/invoices', icon: '🧾', rowCount: 1893, lastExported: 'Today' },
		{ id: 'suppliers', name: 'Suppliers', description: 'Supplier list with contact info and rating', endpoint: '/sales/suppliers', icon: '🏭', rowCount: 87, lastExported: '1 week ago' },
		{ id: 'documents', name: 'Document Extractions', description: 'All OCR-extracted fields from uploaded documents', endpoint: '/documents', icon: '📄', rowCount: 247, lastExported: '5 hours ago' },
	];

	let exporting = $state<Record<string, boolean>>({});
	let exported = $state<Record<string, boolean>>({});

	async function exportData(item: ExportItem) {
		exporting = { ...exporting, [item.id]: true };

		// For demo mode, generate a fake CSV
		await new Promise(r => setTimeout(r, 1200));

		// Demo: generate CSV with headers
		const demoHeaders: Record<string, string> = {
			customers: 'id,name,email,phone,company,city,segment,lifetime_value_bdt,total_orders,is_active',
			orders: 'id,order_number,customer,order_date,total_bdt,status,payment_status',
			products: 'id,name,sku,category,price_bdt,cost_bdt,stock_quantity,reorder_level',
			expenses: 'id,date,category,description,amount_bdt,vendor,payment_method,department',
			invoices: 'id,invoice_number,customer,issue_date,due_date,total_bdt,status,amount_paid_bdt',
			suppliers: 'id,name,contact_person,email,phone,city,rating',
			documents: 'id,filename,document_type,status,confidence,processed_date',
		};

		const csv = demoHeaders[item.id] + '\n(Connect backend to export real data)';
		const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sme_${item.id}_export_${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
		URL.revokeObjectURL(url);

		exporting = { ...exporting, [item.id]: false };
		exported = { ...exported, [item.id]: true };
		setTimeout(() => { exported = { ...exported, [item.id]: false }; }, 3000);
	}
</script>

<svelte:head><title>CSV Export — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Data Export</h1>
			<p class="page-subtitle">Export your business data as CSV or Excel. All amounts in BDT (Taka).</p>
		</div>
	</header>

	<div class="export-grid">
		{#each exports as item}
			<div class="export-card card">
				<div class="export-header">
					<span class="export-icon">{item.icon}</span>
					<div class="export-title-wrap">
						<h3 class="export-name">{item.name}</h3>
						<p class="export-desc">{item.description}</p>
					</div>
				</div>
				<div class="export-meta">
					<span class="row-count">{item.rowCount.toLocaleString()} records</span>
					<span class="last-export">Last: {item.lastExported}</span>
				</div>
				<div class="export-actions">
					<button
						class="export-btn csv"
						onclick={() => exportData(item)}
						disabled={exporting[item.id]}
					>
						{#if exporting[item.id]}
							<Loader2 size={14} class="spinning" />
							Exporting...
						{:else if exported[item.id]}
							<CheckCircle2 size={14} />
							Downloaded!
						{:else}
							<FileDown size={14} />
							Export CSV
						{/if}
					</button>
				</div>
			</div>
		{/each}
	</div>

	<div class="export-note card">
		<Calendar size={16} />
		<div>
			<strong>Date Range Filtering</strong>
			<p>Exports currently include all records. Date-range filtering will be available once the backend is connected.</p>
		</div>
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }

	.export-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-bottom: 20px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.export-card { padding: 18px; display: flex; flex-direction: column; gap: 12px; transition: border-color 0.2s; }
	.export-card:hover { border-color: var(--color-accent); }

	.export-header { display: flex; gap: 12px; }
	.export-icon { font-size: 1.75rem; flex-shrink: 0; }
	.export-name { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0 0 4px; }
	.export-desc { font-size: 0.75rem; color: var(--color-text-secondary); margin: 0; line-height: 1.4; }

	.export-meta { display: flex; justify-content: space-between; align-items: center; }
	.row-count { font-size: 0.8125rem; font-weight: 600; color: var(--color-text-primary); }
	.last-export { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.export-actions { display: flex; gap: 8px; }
	.export-btn {
		flex: 1;
		display: flex; align-items: center; justify-content: center; gap: 6px;
		padding: 8px 14px; border-radius: var(--radius-md);
		font-size: 0.8125rem; font-weight: 600; cursor: pointer;
		border: none; transition: opacity 0.2s;
	}
	.export-btn.csv { background: var(--color-accent); color: white; }
	.export-btn:disabled { opacity: 0.6; cursor: not-allowed; }
	.export-btn:not(:disabled):hover { opacity: 0.85; }

	:global(.spinning) { animation: spin 1s linear infinite; }

	.export-note {
		display: flex; align-items: flex-start; gap: 12px;
		padding: 14px 18px;
		color: var(--color-text-secondary);
		font-size: 0.8125rem;
	}
	.export-note strong { color: var(--color-text-primary); display: block; margin-bottom: 2px; }
	.export-note p { margin: 0; }
</style>
