<!--
  Sidebar.svelte — Collapsible sidebar navigation with grouped sections.
  Enterprise-grade left navigation panel.
-->
<script lang="ts">
	import { page } from '$app/state';
	import { sidebarStore } from '$lib/stores/sidebar.svelte';
	import { localeStore } from '$lib/stores/locale.svelte';
	import {
		LayoutDashboard, BarChart3, TrendingUp, Target,
		ShoppingCart, LineChart, Receipt, Users,
		Package, Building2, Truck, AlertTriangle,
		Wallet, FileText, Banknote, PieChart,
		Brain, Search, Wrench, BookOpen, Telescope,
		Upload, ScanLine, ListTodo, Database, FileDown,
		Calendar, CalendarDays, CalendarRange, Clock,
		UserPlus, Filter, UserCheck,
		Shield, KeyRound, ScrollText, Activity,
		Building, Globe, Palette, Key, Plug,
		ChevronDown, ChevronRight, PanelLeftClose, PanelLeft, Zap
	} from '@lucide/svelte';

	interface NavItem {
		label: string;
		labelKey: string;
		href: string;
		icon: any;
	}

	interface NavGroup {
		title: string;
		titleKey: string;
		icon: any;
		items: NavItem[];
		defaultOpen?: boolean;
	}

	const navGroups: NavGroup[] = [
		{
			title: 'Dashboard', titleKey: 'nav.dashboard', icon: LayoutDashboard,
			defaultOpen: true,
			items: [
				{ label: 'Overview', labelKey: 'nav.overview', href: '/dashboard', icon: LayoutDashboard },
				{ label: 'Executive Summary', labelKey: 'nav.executive_summary', href: '/dashboard/executive', icon: BarChart3 },
				{ label: 'KPI Center', labelKey: 'nav.kpi_center', href: '/dashboard/kpis', icon: Target },
			]
		},
		{
			title: 'Sales', titleKey: 'nav.sales', icon: ShoppingCart,
			items: [
				{ label: 'Sales Analytics', labelKey: 'nav.sales_analytics', href: '/sales/analytics', icon: LineChart },
				{ label: 'Orders', labelKey: 'nav.orders', href: '/sales/orders', icon: ShoppingCart },
				{ label: 'Revenue', labelKey: 'nav.revenue', href: '/sales/revenue', icon: TrendingUp },
				{ label: 'Customers', labelKey: 'nav.customers', href: '/sales/customers', icon: Users },
			]
		},
		{
			title: 'Inventory', titleKey: 'nav.inventory', icon: Package,
			items: [
				{ label: 'Products', labelKey: 'nav.products', href: '/inventory/products', icon: Package },
				{ label: 'Warehouses', labelKey: 'nav.warehouses', href: '/inventory/warehouses', icon: Building2 },
				{ label: 'Suppliers', labelKey: 'nav.suppliers', href: '/inventory/suppliers', icon: Truck },
				{ label: 'Stock Alerts', labelKey: 'nav.stock_alerts', href: '/inventory/alerts', icon: AlertTriangle },
			]
		},
		{
			title: 'Finance', titleKey: 'nav.finance', icon: Wallet,
			items: [
				{ label: 'Expenses', labelKey: 'nav.expenses', href: '/finance/expenses', icon: Receipt },
				{ label: 'Invoices', labelKey: 'nav.invoices', href: '/finance/invoices', icon: FileText },
				{ label: 'Cash Flow', labelKey: 'nav.cash_flow', href: '/finance/cashflow', icon: Banknote },
				{ label: 'Profit & Loss', labelKey: 'nav.profit_loss', href: '/finance/pnl', icon: PieChart },
			]
		},
		{
			title: 'Business Intelligence', titleKey: 'nav.bi', icon: Brain,
			items: [
				{ label: 'Analytics', labelKey: 'nav.analytics', href: '/bi/analytics', icon: BarChart3 },
				{ label: 'Data Explorer', labelKey: 'nav.data_explorer', href: '/bi/explorer', icon: Search },
				{ label: 'KPI Builder', labelKey: 'nav.kpi_builder', href: '/bi/kpi-builder', icon: Wrench },
				{ label: 'Custom Reports', labelKey: 'nav.custom_reports', href: '/bi/reports', icon: BookOpen },
				{ label: 'Forecasting', labelKey: 'nav.forecasting', href: '/bi/forecasting', icon: Telescope },
			]
		},
		{
			title: 'Documents', titleKey: 'nav.documents', icon: FileText,
			items: [
				{ label: 'Upload PDF', labelKey: 'nav.upload_pdf', href: '/documents/upload', icon: Upload },
				{ label: 'OCR Processing', labelKey: 'nav.ocr_processing', href: '/documents/ocr', icon: ScanLine },
				{ label: 'Extraction Queue', labelKey: 'nav.extraction_queue', href: '/documents/queue', icon: ListTodo },
				{ label: 'Parsed Data', labelKey: 'nav.parsed_data', href: '/documents/parsed', icon: Database },
				{ label: 'CSV Export', labelKey: 'nav.csv_export', href: '/documents/export', icon: FileDown },
			]
		},
		{
			title: 'Reports', titleKey: 'nav.reports', icon: BookOpen,
			items: [
				{ label: 'Monthly Reports', labelKey: 'nav.monthly_reports', href: '/reports/monthly', icon: Calendar },
				{ label: 'Quarterly Reports', labelKey: 'nav.quarterly_reports', href: '/reports/quarterly', icon: CalendarDays },
				{ label: 'Annual Reports', labelKey: 'nav.annual_reports', href: '/reports/annual', icon: CalendarRange },
				{ label: 'Scheduled Reports', labelKey: 'nav.scheduled_reports', href: '/reports/scheduled', icon: Clock },
			]
		},
		{
			title: 'CRM', titleKey: 'nav.crm', icon: Users,
			items: [
				{ label: 'Customers', labelKey: 'nav.customers', href: '/crm/customers', icon: Users },
				{ label: 'Leads', labelKey: 'nav.leads', href: '/crm/leads', icon: UserPlus },
				{ label: 'Segmentation', labelKey: 'nav.segmentation', href: '/crm/segmentation', icon: Filter },
				{ label: 'Retention', labelKey: 'nav.retention', href: '/crm/retention', icon: UserCheck },
			]
		},
		{
			title: 'Administration', titleKey: 'nav.admin', icon: Shield,
			items: [
				{ label: 'Users', labelKey: 'nav.users', href: '/admin/users', icon: Users },
				{ label: 'Roles', labelKey: 'nav.roles', href: '/admin/roles', icon: Shield },
				{ label: 'Permissions', labelKey: 'nav.permissions', href: '/admin/permissions', icon: KeyRound },
				{ label: 'Audit Logs', labelKey: 'nav.audit_logs', href: '/admin/audit', icon: ScrollText },
				{ label: 'Activity Logs', labelKey: 'nav.activity_logs', href: '/admin/activity', icon: Activity },
			]
		},
		{
			title: 'Settings', titleKey: 'nav.settings', icon: Wrench,
			items: [
				{ label: 'Organization', labelKey: 'nav.organization', href: '/settings/organization', icon: Building },
				{ label: 'Localization', labelKey: 'nav.localization', href: '/settings/localization', icon: Globe },
				{ label: 'Branding', labelKey: 'nav.branding', href: '/settings/branding', icon: Palette },
				{ label: 'API Keys', labelKey: 'nav.api_keys', href: '/settings/api-keys', icon: Key },
				{ label: 'Integrations', labelKey: 'nav.integrations', href: '/settings/integrations', icon: Plug },
			]
		},
	];

	// Track which groups are open
	let openGroups = $state<Record<string, boolean>>(
		Object.fromEntries(navGroups.map(g => [g.titleKey, g.defaultOpen ?? false]))
	);

	function toggleGroup(key: string) {
		openGroups[key] = !openGroups[key];
	}

	function isActive(href: string): boolean {
		const currentPath = page.url?.pathname || '';
		if (href === '/dashboard') return currentPath === '/dashboard' || currentPath === '/';
		return currentPath.startsWith(href);
	}

	function isGroupActive(group: NavGroup): boolean {
		return group.items.some(item => isActive(item.href));
	}

	// Auto-expand group if it contains the active route
	$effect(() => {
		for (const group of navGroups) {
			if (isGroupActive(group)) {
				openGroups[group.titleKey] = true;
			}
		}
	});
</script>

<aside
	class="sidebar"
	class:collapsed={sidebarStore.collapsed}
	class:mobile-open={sidebarStore.mobileOpen}
	role="navigation"
	aria-label="Main navigation"
>
	<!-- Logo & Brand -->
	<div class="sidebar-header">
		<a href="/dashboard" class="logo-link">
			<div class="logo-icon">
				<Zap size={20} />
			</div>
			{#if !sidebarStore.collapsed}
				<div class="logo-text">
					<span class="logo-name">SME Insight</span>
					<span class="logo-tag">Hub</span>
				</div>
			{/if}
		</a>
		<button
			class="collapse-btn"
			onclick={() => sidebarStore.toggle()}
			aria-label={sidebarStore.collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
		>
			{#if sidebarStore.collapsed}
				<PanelLeft size={18} />
			{:else}
				<PanelLeftClose size={18} />
			{/if}
		</button>
	</div>

	<!-- Navigation Groups -->
	<nav class="sidebar-nav no-scrollbar">
		{#each navGroups as group}
			{@const GroupIcon = group.icon}
			<div class="nav-group" class:active={isGroupActive(group)}>
				<button
					class="nav-group-header"
					onclick={() => toggleGroup(group.titleKey)}
					aria-expanded={openGroups[group.titleKey]}
					title={sidebarStore.collapsed ? localeStore.t(group.titleKey) : ''}
				>
					<div class="nav-group-left">
						<GroupIcon size={18} />
						{#if !sidebarStore.collapsed}
							<span class="nav-group-title">{localeStore.t(group.titleKey)}</span>
						{/if}
					</div>
					{#if !sidebarStore.collapsed}
						<span class="nav-group-chevron" class:open={openGroups[group.titleKey]}>
							<ChevronRight size={14} />
						</span>
					{/if}
				</button>

				{#if (openGroups[group.titleKey] || sidebarStore.collapsed) && !sidebarStore.collapsed}
					<div class="nav-group-items">
						{#each group.items as item}
							{@const ItemIcon = item.icon}
							<a
								href={item.href}
								class="nav-item"
								class:active={isActive(item.href)}
								aria-current={isActive(item.href) ? 'page' : undefined}
								onclick={() => sidebarStore.closeMobile()}
							>
								<ItemIcon size={16} />
								<span>{localeStore.t(item.labelKey)}</span>
							</a>
						{/each}
					</div>
				{/if}
			</div>
		{/each}
	</nav>

	<!-- Sidebar Footer -->
	{#if !sidebarStore.collapsed}
		<div class="sidebar-footer">
			<div class="sidebar-version">
				<span>v1.0.0</span>
				<span class="dot">·</span>
				<span>Enterprise</span>
			</div>
		</div>
	{/if}
</aside>

<!-- Mobile overlay -->
{#if sidebarStore.mobileOpen}
	<button
		class="mobile-overlay"
		onclick={() => sidebarStore.closeMobile()}
		aria-label="Close navigation"
	></button>
{/if}

<style>
	.sidebar {
		position: fixed;
		top: 0;
		left: 0;
		bottom: 0;
		width: var(--sidebar-width);
		background: var(--color-bg-secondary);
		border-right: 1px solid var(--color-border);
		display: flex;
		flex-direction: column;
		z-index: 40;
		transition: width var(--transition-slow), transform var(--transition-slow);
		overflow: hidden;
	}

	.sidebar.collapsed {
		width: var(--sidebar-collapsed-width);
	}

	/* ── Header ──────────────────────────────────────── */
	.sidebar-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 16px;
		height: var(--topnav-height);
		border-bottom: 1px solid var(--color-border);
		flex-shrink: 0;
	}

	.logo-link {
		display: flex;
		align-items: center;
		gap: 10px;
		text-decoration: none;
		color: var(--color-text-primary);
	}

	.logo-icon {
		width: 36px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--gradient-accent);
		border-radius: var(--radius-md);
		color: white;
		flex-shrink: 0;
	}

	.logo-text {
		display: flex;
		align-items: baseline;
		gap: 4px;
		white-space: nowrap;
	}

	.logo-name {
		font-weight: 700;
		font-size: 1rem;
		letter-spacing: -0.02em;
	}

	.logo-tag {
		font-weight: 500;
		font-size: 0.875rem;
		color: var(--color-accent);
	}

	.collapse-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 32px;
		height: 32px;
		border: none;
		background: transparent;
		color: var(--color-text-tertiary);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--transition-fast);
		flex-shrink: 0;
	}

	.collapse-btn:hover {
		background: var(--color-bg-hover);
		color: var(--color-text-primary);
	}

	/* ── Navigation ──────────────────────────────────── */
	.sidebar-nav {
		flex: 1;
		overflow-y: auto;
		padding: 8px;
	}

	.nav-group {
		margin-bottom: 2px;
	}

	.nav-group-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		padding: 8px 10px;
		border: none;
		background: transparent;
		color: var(--color-text-secondary);
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: all var(--transition-fast);
		font-size: 0.8125rem;
		font-weight: 500;
		text-align: left;
	}

	.nav-group-header:hover {
		background: var(--color-bg-hover);
		color: var(--color-text-primary);
	}

	.nav-group.active > .nav-group-header {
		color: var(--color-text-primary);
	}

	.nav-group-left {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.nav-group-title {
		white-space: nowrap;
	}

	.nav-group-chevron {
		transition: transform var(--transition-fast);
		display: flex;
		align-items: center;
		opacity: 0.5;
	}

	.nav-group-chevron.open {
		transform: rotate(90deg);
	}

	.nav-group-items {
		padding: 2px 0 4px 18px;
		border-left: 1px solid var(--color-border);
		margin-left: 22px;
		margin-top: 2px;
	}

	.nav-item {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 7px 10px;
		margin: 1px 0;
		border-radius: var(--radius-sm);
		color: var(--color-text-tertiary);
		text-decoration: none;
		font-size: 0.8125rem;
		font-weight: 400;
		transition: all var(--transition-fast);
		white-space: nowrap;
	}

	.nav-item:hover {
		background: var(--color-bg-hover);
		color: var(--color-text-primary);
	}

	.nav-item.active {
		background: var(--color-accent-muted);
		color: var(--color-accent-light);
		font-weight: 500;
	}

	/* ── Footer ──────────────────────────────────────── */
	.sidebar-footer {
		padding: 12px 16px;
		border-top: 1px solid var(--color-border);
		flex-shrink: 0;
	}

	.sidebar-version {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.6875rem;
		color: var(--color-text-muted);
	}

	.dot {
		opacity: 0.4;
	}

	/* ── Mobile ──────────────────────────────────────── */
	.mobile-overlay {
		display: none;
		position: fixed;
		inset: 0;
		background: var(--color-bg-overlay);
		z-index: 39;
		border: none;
		cursor: pointer;
	}

	@media (max-width: 1024px) {
		.sidebar {
			transform: translateX(-100%);
		}

		.sidebar.mobile-open {
			transform: translateX(0);
		}

		.mobile-overlay {
			display: block;
		}

		.collapse-btn {
			display: none;
		}
	}
</style>
