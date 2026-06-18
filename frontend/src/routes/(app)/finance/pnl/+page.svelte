<!--
  Profit & Loss (P&L) Statement page — Structured income statement with margins, expenses, and net profit.
-->
<script lang="ts">
	import { Search, Calendar, FileText, ArrowRightLeft, Percent, Calculator, ArrowUpRight, ArrowDownRight } from '@lucide/svelte';

	let period = $state('june-2026');

	const pnlData = {
		'june-2026': {
			revenue: {
				retail: 480000,
				wholesale: 190000,
				total: 670000
			},
			cogs: {
				materials: 120000,
				labor: 40000,
				total: 160000
			},
			opex: {
				rent: 57500,
				marketing: 15000,
				logistics: 30500,
				salaries: 62000,
				total: 165000
			},
			tax: 25000,
			depreciation: 12000
		},
		'q2-2026': {
			revenue: {
				retail: 1350000,
				wholesale: 540000,
				total: 1890000
			},
			cogs: {
				materials: 350000,
				labor: 110000,
				total: 460000
			},
			opex: {
				rent: 172500,
				marketing: 55000,
				logistics: 85000,
				salaries: 186000,
				total: 498500
			},
			tax: 72000,
			depreciation: 36000
		}
	};

	const currentData = $derived(period === 'june-2026' ? pnlData['june-2026'] : pnlData['q2-2026']);

	const calculations = $derived({
		grossProfit: currentData.revenue.total - currentData.cogs.total,
		grossMargin: ((currentData.revenue.total - currentData.cogs.total) / currentData.revenue.total * 100).toFixed(1),
		ebitda: (currentData.revenue.total - currentData.cogs.total) - currentData.opex.total,
		ebitdaMargin: (((currentData.revenue.total - currentData.cogs.total) - currentData.opex.total) / currentData.revenue.total * 100).toFixed(1),
		ebit: ((currentData.revenue.total - currentData.cogs.total) - currentData.opex.total) - currentData.depreciation,
		netIncome: (((currentData.revenue.total - currentData.cogs.total) - currentData.opex.total) - currentData.depreciation) - currentData.tax,
		netMargin: (((((currentData.revenue.total - currentData.cogs.total) - currentData.opex.total) - currentData.depreciation) - currentData.tax) / currentData.revenue.total * 100).toFixed(1),
	});
</script>

<svelte:head><title>P&L Statement — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Profit & Loss (P&L)</h1>
			<p class="page-subtitle">Standardized income statement showing revenues, expenses, margins, and bottom line</p>
		</div>
		<div class="toolbar-right">
			<select bind:value={period} class="filter-select">
				<option value="june-2026">June 2026 (MTD)</option>
				<option value="q2-2026">Q2 2026 (Quarterly)</option>
			</select>
		</div>
	</header>

	<!-- High level calculations -->
	<div class="summary-grid">
		<div class="summary-card">
			<span class="summary-val">৳ {currentData.revenue.total.toLocaleString()}</span>
			<span class="summary-label">Gross Revenue</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-success">৳ {calculations.grossProfit.toLocaleString()}</span>
			<span class="summary-label">Gross Profit ({calculations.grossMargin}%)</span>
		</div>
		<div class="summary-card text-warning">
			<span class="summary-val text-warning">৳ {currentData.opex.total.toLocaleString()}</span>
			<span class="summary-label">Operating Costs (OPEX)</span>
		</div>
		<div class="summary-card">
			<span class="summary-val text-accent">৳ {calculations.netIncome.toLocaleString()}</span>
			<span class="summary-label">Net Profit ({calculations.netMargin}%)</span>
		</div>
	</div>

	<!-- Income Statement Card -->
	<div class="table-card animate-fade-in-up">
		<div class="statement-header">
			<div class="brand">Income Statement</div>
			<div class="currency">Values in BDT (৳)</div>
		</div>

		<div class="statement-table">
			<!-- REVENUE SECTION -->
			<div class="section-row header">
				<span class="row-label">1. Revenues & Sales</span>
				<span class="row-val">৳ {currentData.revenue.total.toLocaleString()}</span>
			</div>
			<div class="section-row sub">
				<span class="row-label">Retail Sales (B2C)</span>
				<span class="row-val">৳ {currentData.revenue.retail.toLocaleString()}</span>
			</div>
			<div class="section-row sub border-bottom-heavy">
				<span class="row-label">Wholesale Accounts (B2B)</span>
				<span class="row-val">৳ {currentData.revenue.wholesale.toLocaleString()}</span>
			</div>

			<!-- COGS SECTION -->
			<div class="section-row header">
				<span class="row-label">2. Cost of Goods Sold (COGS)</span>
				<span class="row-val text-danger">৳ ({currentData.cogs.total.toLocaleString()})</span>
			</div>
			<div class="section-row sub">
				<span class="row-label">Raw Materials & Sourcing</span>
				<span class="row-val">৳ {currentData.cogs.materials.toLocaleString()}</span>
			</div>
			<div class="section-row sub border-bottom-heavy">
				<span class="row-label">Direct Factory Labor</span>
				<span class="row-val">৳ {currentData.cogs.labor.toLocaleString()}</span>
			</div>

			<!-- GROSS PROFIT TOTAL -->
			<div class="section-row total-row">
				<span class="row-label">Gross Profit</span>
				<span class="row-val">৳ {calculations.grossProfit.toLocaleString()}</span>
			</div>
			<div class="section-row margin-row border-bottom-heavy">
				<span class="row-label">Gross Profit Margin %</span>
				<span class="row-val">{calculations.grossMargin}%</span>
			</div>

			<!-- OPEX SECTION -->
			<div class="section-row header">
				<span class="row-label">3. Operating Expenses (OPEX)</span>
				<span class="row-val text-danger">৳ ({currentData.opex.total.toLocaleString()})</span>
			</div>
			<div class="section-row sub">
				<span class="row-label">Facility Rent & Utility Overheads</span>
				<span class="row-val">৳ {currentData.opex.rent.toLocaleString()}</span>
			</div>
			<div class="section-row sub">
				<span class="row-label">Marketing, Ads & Campaigns</span>
				<span class="row-val">৳ {currentData.opex.marketing.toLocaleString()}</span>
			</div>
			<div class="section-row sub">
				<span class="row-label">Logistics, Delivery & Freight</span>
				<span class="row-val">৳ {currentData.opex.logistics.toLocaleString()}</span>
			</div>
			<div class="section-row sub border-bottom-heavy">
				<span class="row-label">Salaries, Perks & Contractors</span>
				<span class="row-val">৳ {currentData.opex.salaries.toLocaleString()}</span>
			</div>

			<!-- EBITDA TOTAL -->
			<div class="section-row total-row">
				<span class="row-label">Operating Income (EBITDA)</span>
				<span class="row-val">৳ {calculations.ebitda.toLocaleString()}</span>
			</div>
			<div class="section-row sub">
				<span class="row-label">Depreciation & Amortization (D&A)</span>
				<span class="row-val">৳ ({currentData.depreciation.toLocaleString()})</span>
			</div>
			<div class="section-row total-row">
				<span class="row-label">Earnings Before Interest & Taxes (EBIT)</span>
				<span class="row-val">৳ {calculations.ebit.toLocaleString()}</span>
			</div>
			<div class="section-row sub border-bottom-heavy">
				<span class="row-label">Corporate Income Taxes</span>
				<span class="row-val">৳ ({currentData.tax.toLocaleString()})</span>
			</div>

			<!-- NET INCOME -->
			<div class="section-row net-income-row">
				<span class="row-label">Net Income (Bottom Line Profit)</span>
				<span class="row-val">৳ {calculations.netIncome.toLocaleString()}</span>
			</div>
			<div class="section-row margin-row bottom-margin">
				<span class="row-label">Net Profit Margin %</span>
				<span class="row-val">{calculations.netMargin}%</span>
			</div>
		</div>
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.filter-select { padding: 8px 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; cursor: pointer; outline: none; }

	.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
	@media (max-width: 768px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 480px) { .summary-grid { grid-template-columns: 1fr; } }
	
	.summary-card { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-val { font-size: 1.375rem; font-weight: 700; color: var(--color-text-primary); }
	.summary-val.text-success { color: var(--color-success); }
	.summary-val.text-warning { color: var(--color-warning); }
	.summary-val.text-accent { color: var(--color-accent); }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.table-card { border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); display: flex; flex-direction: column; overflow: hidden; }
	
	.statement-header { padding: 16px; border-bottom: 1px solid var(--color-border); display: flex; justify-content: space-between; align-items: center; background: var(--color-bg-tertiary); }
	.brand { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); }
	.currency { font-size: 0.75rem; color: var(--color-text-tertiary); font-weight: 500; }

	.statement-table { display: flex; flex-direction: column; }
	
	.section-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; font-size: 0.8125rem; border-bottom: 1px solid var(--color-border-subtle); }
	
	.section-row.header { font-weight: 600; color: var(--color-text-primary); background: var(--color-bg-secondary); font-size: 0.875rem; }
	.section-row.sub { padding-left: 36px; color: var(--color-text-secondary); }
	
	.border-bottom-heavy { border-bottom: 1px solid var(--color-border); }
	
	.section-row.total-row { font-weight: 700; color: var(--color-text-primary); background: var(--color-bg-tertiary); font-size: 0.875rem; border-top: 1px solid var(--color-border); }
	.section-row.margin-row { font-weight: 500; color: var(--color-text-tertiary); font-size: 0.75rem; font-style: italic; }
	.section-row.margin-row .row-val { color: var(--color-text-secondary); font-weight: 600; }

	.section-row.net-income-row { font-weight: 800; color: var(--color-accent); background: var(--color-accent-muted); font-size: 1rem; border-top: 2px solid var(--color-accent); border-bottom: 1px solid var(--color-accent-muted); }
	
	.bottom-margin { border-bottom: none; }
	.bottom-margin .row-val { color: var(--color-accent); font-weight: 700; font-size: 0.8125rem; }
	
	.row-label { display: flex; align-items: center; gap: 6px; }
	.row-val { font-weight: 600; font-family: var(--font-mono); }
	
	.text-danger { color: var(--color-danger) !important; }
</style>
