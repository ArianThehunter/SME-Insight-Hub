<!--
  Stock Alerts page — Monitored low-stock levels and automated reorder rules.
-->
<script lang="ts">
	import { AlertOctagon, AlertTriangle, CheckCircle, Search, Settings, ArrowUpRight, Plus, ShieldCheck } from '@lucide/svelte';

	let searchQuery = $state('');
	let severityFilter = $state('all');

	const alerts = [
		{ sku: 'PRD-005', name: 'Artisan Leather Bag', stock: 0, reorder: 15, severity: 'critical', supplier: 'Dhaka Leather Craft', date: '2026-06-17 08:32 AM' },
		{ sku: 'PRD-010', name: 'Jute Tote Bag (Eco)', stock: 0, reorder: 50, severity: 'critical', supplier: 'Dhaka Leather Craft', date: '2026-06-16 02:15 PM' },
		{ sku: 'PRD-007', name: 'Pabna Yogurt 500g', stock: 8, reorder: 100, severity: 'warning', supplier: 'Bengal Agro Ltd', date: '2026-06-18 11:04 AM' },
		{ sku: 'PRD-003', name: 'Bengal Spice Mix Set', stock: 15, reorder: 50, severity: 'warning', supplier: 'Bengal Agro Ltd', date: '2026-06-18 09:45 AM' },
		{ sku: 'PRD-011', name: 'Nakshi Kantha Bedcover', stock: 22, reorder: 10, severity: 'resolved', supplier: 'Chittagong Textiles Co.', date: '2026-06-15 05:30 PM' },
	];

	const filtered = $derived(
		alerts.filter(a => {
			const matchSearch = !searchQuery || a.name.toLowerCase().includes(searchQuery.toLowerCase()) || a.sku.toLowerCase().includes(searchQuery.toLowerCase());
			const matchSeverity = severityFilter === 'all' || a.severity === severityFilter;
			return matchSearch && matchSeverity;
		})
	);

	const counts = $derived({
		critical: alerts.filter(a => a.severity === 'critical').length,
		warning: alerts.filter(a => a.severity === 'warning').length,
		resolved: alerts.filter(a => a.severity === 'resolved').length,
		total: alerts.filter(a => a.severity !== 'resolved').length,
	});
</script>

<svelte:head><title>Stock Alerts — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Stock Alerts</h1>
			<p class="page-subtitle">Monitor out-of-stock items, critical thresholds, and automation policies</p>
		</div>
		<div class="header-actions">
			<button class="btn-secondary"><Settings size={15} /> Configure Rules</button>
			<button class="btn-create"><Plus size={16} /> Create Rule</button>
		</div>
	</header>

	<!-- Metrics -->
	<div class="summary-grid">
		<div class="summary-card danger">
			<AlertOctagon size={20} class="text-danger" />
			<div class="summary-details">
				<span class="summary-val text-danger">{counts.critical}</span>
				<span class="summary-label">Critical (Out of Stock)</span>
			</div>
		</div>
		<div class="summary-card warning">
			<AlertTriangle size={20} class="text-warning" />
			<div class="summary-details">
				<span class="summary-val text-warning">{counts.warning}</span>
				<span class="summary-label">Warnings (Low Stock)</span>
			</div>
		</div>
		<div class="summary-card success">
			<CheckCircle size={20} class="text-success" />
			<div class="summary-details">
				<span class="summary-val text-success">{counts.resolved}</span>
				<span class="summary-label">Resolved Recently</span>
			</div>
		</div>
		<div class="summary-card info">
			<ShieldCheck size={20} class="text-accent" />
			<div class="summary-details">
				<span class="summary-val">Auto</span>
				<span class="summary-label">Reorder Automation</span>
			</div>
		</div>
	</div>

	<!-- Content Layout -->
	<div class="content-layout">
		<!-- Left: Alerts List -->
		<div class="alerts-container">
			<div class="toolbar">
				<div class="search-box">
					<Search size={16} />
					<input type="text" bind:value={searchQuery} placeholder="Search alerts..." class="search-input" />
				</div>
				<div class="toolbar-right">
					<select bind:value={severityFilter} class="filter-select">
						<option value="all">All Severities</option>
						<option value="critical">Critical</option>
						<option value="warning">Warning</option>
						<option value="resolved">Resolved</option>
					</select>
				</div>
			</div>

			<div class="alerts-list animate-fade-in-up">
				{#if filtered.length === 0}
					<div class="empty-state">No alerts found matching the criteria.</div>
				{:else}
					{#each filtered as a}
						<div class="alert-item-card {a.severity}">
							<div class="alert-status-indicator">
								{#if a.severity === 'critical'}
									<AlertOctagon size={20} class="text-danger" />
								{:else if a.severity === 'warning'}
									<AlertTriangle size={20} class="text-warning" />
								{:else}
									<CheckCircle size={20} class="text-success" />
								{/if}
							</div>
							
							<div class="alert-details">
								<div class="alert-header-row">
									<div>
										<h3 class="product-name">{a.name}</h3>
										<span class="product-sku">{a.sku}</span>
									</div>
									<span class="alert-date">{a.date}</span>
								</div>

								<div class="alert-stats">
									<div class="stat-bubble">
										<span class="stat-label">Current Stock</span>
										<span class="stat-val {a.stock <= a.reorder ? 'text-danger' : 'text-success'}">{a.stock} units</span>
									</div>
									<div class="stat-bubble">
										<span class="stat-label">Reorder Level</span>
										<span class="stat-val">{a.reorder} units</span>
									</div>
									<div class="stat-bubble">
										<span class="stat-label">Preferred Supplier</span>
										<span class="stat-val">{a.supplier}</span>
									</div>
								</div>

								<div class="alert-actions">
									{#if a.severity !== 'resolved'}
										<button class="btn-alert-action primary">
											Order Now <ArrowUpRight size={13} />
										</button>
										<button class="btn-alert-action secondary">Acknowledge</button>
									{:else}
										<span class="replenish-msg text-success"><CheckCircle size={12} class="inline-icon" /> Replenished and verified.</span>
									{/if}
								</div>
							</div>
						</div>
					{/each}
				{/if}
			</div>
		</div>

		<!-- Right: Auto-Reorder Policies -->
		<div class="policy-sidebar">
			<div class="policy-card">
				<h3 class="policy-title"><ShieldCheck size={16} /> Automated Policies</h3>
				<p class="policy-description">Rules that auto-generate Purchase Orders (POs) when stock thresholds are breached.</p>
				
				<div class="rule-list">
					<div class="rule-item">
						<div class="rule-header">
							<span class="rule-name">Fast-Moving Foods Rule</span>
							<span class="rule-toggle active">ON</span>
						</div>
						<p class="rule-summary">If Category is <strong>Food & Beverages</strong> and Stock &lt; <strong>50%</strong> of Reorder Level, auto-draft PO for 3x safety margin.</p>
					</div>

					<div class="rule-item">
						<div class="rule-header">
							<span class="rule-name">Critical Out of Stock Alert</span>
							<span class="rule-toggle active">ON</span>
						</div>
						<p class="rule-summary">If Stock reaches <strong>0</strong> units, send urgent Email/SMS notifications to Purchase Manager immediately.</p>
					</div>
				</div>

				<button class="btn-policy-create">Manage Reorder Schedules</button>
			</div>
		</div>
	</div>
</div>

<style>
	.page { display: flex; flex-direction: column; gap: 20px; }
	.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; }
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.header-actions { display: flex; gap: 8px; }
	
	.btn-create { display: flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: var(--radius-md); border: none; background: var(--gradient-accent); color: white; font-size: 0.8125rem; font-weight: 600; font-family: inherit; cursor: pointer; box-shadow: 0 2px 8px rgba(59,130,246,0.25); transition: all var(--transition-fast); }
	.btn-create:hover { opacity: 0.9; transform: translateY(-1px); }
	
	.btn-secondary { display: flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.8125rem; font-weight: 600; font-family: inherit; cursor: pointer; transition: all var(--transition-fast); }
	.btn-secondary:hover { background: var(--color-bg-hover); border-color: var(--color-border-hover); }

	.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
	@media (max-width: 768px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 480px) { .summary-grid { grid-template-columns: 1fr; } }
	
	.summary-card { display: flex; align-items: center; gap: 14px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); }
	.summary-card.danger { border-left: 4px solid var(--color-danger); }
	.summary-card.warning { border-left: 4px solid var(--color-warning); }
	.summary-card.success { border-left: 4px solid var(--color-success); }
	.summary-card.info { border-left: 4px solid var(--color-accent); }
	.summary-details { display: flex; flex-direction: column; gap: 2px; }
	.summary-val { font-size: 1.25rem; font-weight: 700; color: var(--color-text-primary); }
	.summary-val.text-danger { color: var(--color-danger); }
	.summary-val.text-warning { color: var(--color-warning); }
	.summary-val.text-success { color: var(--color-success); }
	.summary-label { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.content-layout { display: grid; grid-template-columns: 1fr 300px; gap: 20px; }
	@media (max-width: 992px) { .content-layout { grid-template-columns: 1fr; } }

	.alerts-container { display: flex; flex-direction: column; gap: 16px; }

	.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
	.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); min-width: 260px; color: var(--color-text-tertiary); flex: 1; }
	.search-box:focus-within { border-color: var(--color-accent); }
	.search-input { border: none; background: transparent; outline: none; color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; flex: 1; }
	.search-input::placeholder { color: var(--color-text-muted); }
	.toolbar-right { display: flex; gap: 8px; }
	.filter-select { padding: 8px 12px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: var(--color-bg-secondary); color: var(--color-text-primary); font-size: 0.8125rem; font-family: inherit; cursor: pointer; outline: none; }

	.alerts-list { display: flex; flex-direction: column; gap: 12px; }
	.empty-state { padding: 32px; text-align: center; color: var(--color-text-secondary); background: var(--color-bg-secondary); border-radius: var(--radius-lg); border: 1px dashed var(--color-border); }

	.alert-item-card { display: flex; gap: 16px; padding: 16px; border-radius: var(--radius-lg); background: var(--color-bg-secondary); border: 1px solid var(--color-border); transition: all var(--transition-fast); }
	.alert-item-card:hover { border-color: var(--color-border-hover); box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
	.alert-item-card.critical { border-left: 4px solid var(--color-danger); }
	.alert-item-card.warning { border-left: 4px solid var(--color-warning); }
	.alert-item-card.resolved { border-left: 4px solid var(--color-success); opacity: 0.8; }
	
	.alert-status-indicator { display: flex; align-items: flex-start; padding-top: 2px; }
	.alert-details { flex: 1; display: flex; flex-direction: column; gap: 12px; }
	
	.alert-header-row { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px; }
	.product-name { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }
	.product-sku { font-family: var(--font-mono); font-size: 0.6875rem; color: var(--color-text-tertiary); display: block; margin-top: 2px; }
	.alert-date { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.alert-stats { display: flex; gap: 8px; flex-wrap: wrap; }
	.stat-bubble { background: var(--color-bg-tertiary); padding: 8px 12px; border-radius: var(--radius-md); display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 110px; border: 1px solid var(--color-border-subtle); }
	.stat-label { font-size: 0.625rem; color: var(--color-text-tertiary); text-transform: uppercase; font-weight: 600; }
	.stat-val { font-size: 0.75rem; font-weight: 600; color: var(--color-text-primary); }
	.stat-val.text-danger { color: var(--color-danger); }
	.stat-val.text-success { color: var(--color-success); }

	.alert-actions { display: flex; gap: 8px; align-items: center; }
	.btn-alert-action { padding: 6px 12px; border-radius: var(--radius-md); border: none; font-size: 0.75rem; font-weight: 600; font-family: inherit; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all var(--transition-fast); }
	.btn-alert-action.primary { background: var(--gradient-accent); color: white; }
	.btn-alert-action.primary:hover { opacity: 0.9; }
	.btn-alert-action.secondary { background: var(--color-bg-tertiary); border: 1px solid var(--color-border); color: var(--color-text-primary); }
	.btn-alert-action.secondary:hover { background: var(--color-bg-hover); border-color: var(--color-border-hover); }
	.replenish-msg { font-size: 0.75rem; font-weight: 500; display: inline-flex; align-items: center; gap: 4px; }
	.inline-icon { display: inline-block; }

	.policy-sidebar { display: flex; flex-direction: column; }
	.policy-card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px; display: flex; flex-direction: column; gap: 14px; }
	.policy-title { font-size: 0.875rem; font-weight: 600; color: var(--color-text-primary); margin: 0; display: flex; align-items: center; gap: 6px; }
	.policy-description { font-size: 0.75rem; color: var(--color-text-secondary); margin: 0; line-height: 1.4; }
	
	.rule-list { display: flex; flex-direction: column; gap: 12px; }
	.rule-item { border: 1px solid var(--color-border-subtle); padding: 12px; border-radius: var(--radius-md); background: var(--color-bg-tertiary); }
	.rule-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
	.rule-name { font-size: 0.75rem; font-weight: 600; color: var(--color-text-primary); }
	.rule-toggle.active { font-size: 0.625rem; font-weight: 700; background: var(--color-success-muted); color: var(--color-success); padding: 2px 6px; border-radius: var(--radius-full); }
	.rule-summary { font-size: 0.6875rem; color: var(--color-text-secondary); margin: 0; line-height: 1.4; }

	.btn-policy-create { width: 100%; padding: 8px; border-radius: var(--radius-md); border: 1px solid var(--color-border); background: transparent; color: var(--color-text-primary); font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: all var(--transition-fast); }
	.btn-policy-create:hover { background: var(--color-bg-hover); color: var(--color-accent); border-color: var(--color-accent); }
</style>
