<!--
  Dashboard — Executive overview with KPIs, charts, AI insights, and activity feed.
  The centerpiece of the SME Insight Hub platform.
-->
<script lang="ts">
	import { localeStore } from '$lib/stores/locale.svelte';
	import {
		TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight,
		Receipt, Wallet, Banknote, Users, Package, FileText,
		AlertTriangle, Sparkles, Activity, Clock,
		UserPlus, Upload, CheckCircle, ScanLine, Truck,
		BarChart3, Megaphone, UserMinus,
		ChevronRight, MoreHorizontal, ExternalLink
	} from '@lucide/svelte';

	// ── Demo KPI Data ──────────────────────────────────
	const kpis = [
		{
			id: 'revenue', title: 'Revenue', titleBn: 'রাজস্ব',
			value: 28450000, formatted: '৳2,84,50,000',
			change: 12.5, direction: 'up',
			sparkline: [20, 22, 19, 24, 21, 25, 23, 27, 24, 28, 26, 29],
			icon: TrendingUp, color: 'emerald',
		},
		{
			id: 'expenses', title: 'Expenses', titleBn: 'ব্যয়',
			value: 18200000, formatted: '৳1,82,00,000',
			change: 8.3, direction: 'up',
			sparkline: [14, 15, 13, 16, 15, 17, 16, 18, 15, 17, 18, 19],
			icon: Receipt, color: 'rose',
		},
		{
			id: 'profit', title: 'Profit', titleBn: 'মুনাফা',
			value: 10250000, formatted: '৳1,02,50,000',
			change: 18.2, direction: 'up',
			sparkline: [6, 7, 6, 8, 7, 9, 8, 10, 9, 11, 10, 12],
			icon: Wallet, color: 'blue',
		},
		{
			id: 'cashflow', title: 'Cash Flow', titleBn: 'নগদ প্রবাহ',
			value: 5800000, formatted: '৳58,00,000',
			change: 5.1, direction: 'up',
			sparkline: [4, 5, 4, 6, 5, 6, 5, 7, 6, 6, 5, 7],
			icon: Banknote, color: 'violet',
		},
		{
			id: 'customers', title: 'Customers', titleBn: 'গ্রাহক',
			value: 1247, formatted: '1,247',
			change: 15.3, direction: 'up',
			sparkline: [90, 95, 98, 100, 105, 108, 110, 115, 118, 120, 122, 125],
			icon: Users, color: 'cyan',
		},
		{
			id: 'inventory', title: 'Inventory Value', titleBn: 'মজুদ মূল্য',
			value: 12500000, formatted: '৳1,25,00,000',
			change: -3.2, direction: 'down',
			sparkline: [110, 108, 112, 107, 105, 108, 103, 106, 104, 105, 102, 100],
			icon: Package, color: 'amber',
		},
		{
			id: 'invoices', title: 'Outstanding Invoices', titleBn: 'বকেয়া চালান',
			value: 3200000, formatted: '৳32,00,000',
			change: -6.8, direction: 'down',
			sparkline: [35, 33, 30, 32, 28, 30, 27, 25, 28, 26, 24, 22],
			icon: FileText, color: 'orange',
		},
		{
			id: 'growth', title: 'Growth', titleBn: 'প্রবৃদ্ধি',
			value: 12.5, formatted: '12.5%',
			change: 2.1, direction: 'up',
			sparkline: [8, 9, 8, 10, 9, 11, 10, 11, 11, 12, 12, 13],
			icon: TrendingUp, color: 'teal',
		},
	];

	// ── AI Insights ────────────────────────────────────
	const insights = [
		{
			title: 'Revenue Growth Acceleration', titleBn: 'রাজস্ব বৃদ্ধি ত্বরান্বিত',
			desc: 'Revenue increased by 12.5% compared to last quarter, driven primarily by electronics and healthcare categories.',
			descBn: 'গত প্রান্তিকের তুলনায় রাজস্ব ১২.৫% বৃদ্ধি পেয়েছে।',
			severity: 'success', icon: TrendingUp, metric: '+12.5%',
		},
		{
			title: 'Customer Retention Alert', titleBn: 'গ্রাহক ধারণ সতর্কতা',
			desc: 'Customer retention rate declined by 6.2% this month. 23 enterprise customers haven\'t placed orders in 60 days.',
			descBn: 'এই মাসে গ্রাহক ধরে রাখার হার ৬.২% কমেছে।',
			severity: 'warning', icon: UserMinus, metric: '-6.2%',
		},
		{
			title: 'Critical Stock Level', titleBn: 'মজুদের সংকটপূর্ণ স্তর',
			desc: 'Samsung Galaxy A54 stock critically low — 12 units remaining, avg daily sale: 8 units. Reorder immediately.',
			descBn: 'Samsung Galaxy A54-এর মজুদ সংকটপূর্ণ — মাত্র ১২ ইউনিট অবশিষ্ট।',
			severity: 'critical', icon: AlertTriangle, metric: '12 units',
		},
		{
			title: 'Supplier Delivery Delays', titleBn: 'সরবরাহকারী বিলম্ব',
			desc: 'Global Trade BD delayed deliveries 3 months in a row. Average delay: 5.2 days. Consider diversifying.',
			descBn: 'Global Trade BD পরপর ৩ মাস ডেলিভারি বিলম্ব করেছে।',
			severity: 'warning', icon: Truck, metric: '5.2 days',
		},
		{
			title: 'Sales Peak Pattern', titleBn: 'বিক্রয় শীর্ষ প্যাটার্ন',
			desc: 'Sales peak on Friday afternoons (2-6 PM) and Saturday mornings. Increase staffing during these periods.',
			descBn: 'শুক্রবার বিকেলে এবং শনিবার সকালে বিক্রয় সর্বোচ্চ হয়।',
			severity: 'info', icon: BarChart3, metric: 'Fri-Sat',
		},
		{
			title: 'Marketing ROI Improved', titleBn: 'বিপণন ROI উন্নতি',
			desc: 'Marketing ROI improved by 18.3% this quarter. Social media campaigns generated 340 new leads.',
			descBn: 'এই প্রান্তিকে বিপণন ROI ১৮.৩% উন্নতি হয়েছে।',
			severity: 'success', icon: Megaphone, metric: '+18.3%',
		},
	];

	// ── Activity Feed ──────────────────────────────────
	const activities = [
		{ title: 'New Invoice Uploaded', desc: 'INV-2024-0847 from Rahman Enterprise — ৳125,000', icon: FileText, time: '12m ago', type: 'invoice' },
		{ title: 'Monthly Report Generated', desc: 'May 2024 Executive Summary report ready', icon: BarChart3, time: '45m ago', type: 'report' },
		{ title: 'New Customer Registered', desc: 'ABC Trading Co. (মোঃ করিম ট্রেডিং) — Enterprise', icon: UserPlus, time: '1h ago', type: 'customer' },
		{ title: 'Low Stock Alert', desc: 'Wireless Mouse MX-200 below reorder level (8 remaining)', icon: AlertTriangle, time: '2h ago', type: 'alert' },
		{ title: 'Bulk Import Completed', desc: '156 product records imported from CSV', icon: Upload, time: '3h ago', type: 'import' },
		{ title: 'Order Delivered', desc: 'ORD-2024-1234 delivered to Dhaka — ৳85,500', icon: CheckCircle, time: '4h ago', type: 'order' },
		{ title: 'Payment Received', desc: 'INV-2024-0839 — ৳250,000 via bank transfer', icon: Banknote, time: '5h ago', type: 'payment' },
		{ title: 'OCR Processing Complete', desc: '3 invoices processed — 94.2% avg confidence', icon: ScanLine, time: '6h ago', type: 'processing' },
	];

	// ── Sparkline SVG helper ───────────────────────────
	function sparklinePath(data: number[], width = 80, height = 28): string {
		if (data.length < 2) return '';
		const min = Math.min(...data);
		const max = Math.max(...data);
		const range = max - min || 1;
		const step = width / (data.length - 1);

		return data
			.map((val, i) => {
				const x = i * step;
				const y = height - ((val - min) / range) * height * 0.8 - height * 0.1;
				return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
			})
			.join(' ');
	}

	function getColorVar(color: string): string {
		const map: Record<string, string> = {
			emerald: 'var(--color-success)',
			rose: 'var(--color-danger)',
			blue: 'var(--color-accent)',
			violet: 'var(--color-violet)',
			cyan: 'var(--color-info)',
			amber: 'var(--color-warning)',
			orange: 'var(--color-warning)',
			teal: '#14b8a6',
		};
		return map[color] ?? 'var(--color-accent)';
	}

	function getSeverityColor(severity: string): string {
		const map: Record<string, string> = {
			success: 'var(--color-success)',
			warning: 'var(--color-warning)',
			critical: 'var(--color-danger)',
			info: 'var(--color-info)',
		};
		return map[severity] ?? 'var(--color-info)';
	}

	function getActivityTypeColor(type: string): string {
		const map: Record<string, string> = {
			invoice: 'var(--color-accent)',
			report: 'var(--color-violet)',
			customer: 'var(--color-success)',
			alert: 'var(--color-warning)',
			import: 'var(--color-info)',
			order: 'var(--color-success)',
			payment: 'var(--color-success)',
			processing: 'var(--color-accent)',
		};
		return map[type] ?? 'var(--color-text-tertiary)';
	}
</script>

<svelte:head>
	<title>Dashboard — SME Insight Hub</title>
	<meta name="description" content="Executive dashboard with real-time KPIs, analytics, and AI business insights" />
</svelte:head>

<div class="dashboard">
	<!-- Page Header -->
	<header class="page-header animate-fade-in">
		<div>
			<h1 class="page-title">
				{localeStore.t('dashboard.welcome')}, <span class="text-gradient">Rafiq</span>
			</h1>
			<p class="page-subtitle">{localeStore.t('dashboard.overview_subtitle')}</p>
		</div>
		<div class="header-actions">
			<button class="btn-outline">
				<Activity size={16} />
				Last 30 days
			</button>
			<button class="btn-primary">
				<ExternalLink size={16} />
				Export
			</button>
		</div>
	</header>

	<!-- KPI Cards Grid -->
	<section class="kpi-grid" aria-label="Key Performance Indicators">
		{#each kpis as kpi, i}
			{@const Icon = kpi.icon}
			<article
				class="kpi-card animate-fade-in-up"
				style="animation-delay: {i * 60}ms"
			>
				<div class="kpi-header">
					<div class="kpi-icon" style="background: {getColorVar(kpi.color)}15; color: {getColorVar(kpi.color)}">
						<Icon size={18} />
					</div>
					<button class="kpi-more" aria-label="More options">
						<MoreHorizontal size={16} />
					</button>
				</div>

				<div class="kpi-body">
					<span class="kpi-label">{localeStore.isBangla ? kpi.titleBn : kpi.title}</span>
					<span class="kpi-value">{kpi.formatted}</span>
				</div>

				<div class="kpi-footer">
					<div
						class="kpi-change"
						class:positive={kpi.direction === 'up' && kpi.id !== 'expenses'}
						class:negative={kpi.direction === 'down' || (kpi.direction === 'up' && kpi.id === 'expenses')}
					>
						{#if kpi.direction === 'up'}
							<ArrowUpRight size={14} />
						{:else}
							<ArrowDownRight size={14} />
						{/if}
						<span>{Math.abs(kpi.change)}%</span>
					</div>

					<svg class="sparkline" viewBox="0 0 80 28" preserveAspectRatio="none">
						<path
							d={sparklinePath(kpi.sparkline)}
							fill="none"
							stroke={getColorVar(kpi.color)}
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							opacity="0.7"
						/>
					</svg>
				</div>
			</article>
		{/each}
	</section>

	<!-- Charts + Insights Row -->
	<div class="main-grid">
		<!-- Revenue Trend Chart Placeholder -->
		<section class="chart-card large animate-fade-in-up" style="animation-delay: 500ms">
			<div class="card-header">
				<h2 class="card-title">Revenue Trend</h2>
				<div class="card-actions">
					<button class="period-btn active">12M</button>
					<button class="period-btn">6M</button>
					<button class="period-btn">3M</button>
					<button class="period-btn">1M</button>
				</div>
			</div>
			<div class="chart-placeholder">
				<div class="chart-demo">
					<svg viewBox="0 0 600 200" class="demo-chart">
						<!-- Grid lines -->
						{#each [0, 1, 2, 3, 4] as i}
							<line x1="0" y1={i * 50} x2="600" y2={i * 50} stroke="var(--color-border)" stroke-width="0.5" opacity="0.3" />
						{/each}
						<!-- Revenue area -->
						<path d="M0 180 L50 160 L100 140 L150 150 L200 120 L250 130 L300 100 L350 110 L400 80 L450 90 L500 60 L550 50 L600 40 L600 200 L0 200 Z"
							fill="url(#revenueGrad)" opacity="0.3" />
						<path d="M0 180 L50 160 L100 140 L150 150 L200 120 L250 130 L300 100 L350 110 L400 80 L450 90 L500 60 L550 50 L600 40"
							fill="none" stroke="var(--color-success)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
						<!-- Target line -->
						<line x1="0" y1="100" x2="600" y2="100" stroke="var(--color-violet)" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.6" />
						<defs>
							<linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
								<stop offset="0%" stop-color="var(--color-success)" stop-opacity="0.4" />
								<stop offset="100%" stop-color="var(--color-success)" stop-opacity="0" />
							</linearGradient>
						</defs>
					</svg>
					<div class="chart-labels">
						{#each ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] as month}
							<span>{month}</span>
						{/each}
					</div>
				</div>
				<div class="chart-legend">
					<div class="legend-item">
						<span class="legend-dot" style="background: var(--color-success)"></span>
						<span>Revenue</span>
					</div>
					<div class="legend-item">
						<span class="legend-dot" style="background: var(--color-violet)"></span>
						<span>Target</span>
					</div>
				</div>
			</div>
		</section>

		<!-- AI Insights Panel -->
		<section class="insights-card animate-fade-in-up" style="animation-delay: 600ms">
			<div class="card-header">
				<h2 class="card-title">
					<Sparkles size={18} style="color: var(--color-accent)" />
					{localeStore.t('dashboard.ai_insights')}
				</h2>
				<a href="/bi/analytics" class="view-all-link">
					{localeStore.t('dashboard.view_all')}
					<ChevronRight size={14} />
				</a>
			</div>
			<div class="insights-list">
				{#each insights as insight, i}
					{@const Icon = insight.icon}
					<div
						class="insight-item"
						style="animation-delay: {700 + i * 80}ms"
					>
						<div class="insight-icon" style="background: {getSeverityColor(insight.severity)}15; color: {getSeverityColor(insight.severity)}">
							<Icon size={16} />
						</div>
						<div class="insight-content">
							<div class="insight-header">
								<span class="insight-title">{localeStore.isBangla ? insight.titleBn : insight.title}</span>
								<span class="insight-metric" style="color: {getSeverityColor(insight.severity)}">{insight.metric}</span>
							</div>
							<p class="insight-desc">{localeStore.isBangla ? insight.descBn : insight.desc}</p>
						</div>
					</div>
				{/each}
			</div>
		</section>
	</div>

	<!-- Secondary Charts Row -->
	<div class="charts-row">
		<!-- Expense Breakdown -->
		<section class="chart-card animate-fade-in-up" style="animation-delay: 800ms">
			<div class="card-header">
				<h2 class="card-title">Expense Breakdown</h2>
			</div>
			<div class="donut-chart-container">
				<svg viewBox="0 0 200 200" class="donut-chart">
					<!-- Donut segments -->
					<circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-success)" stroke-width="24" stroke-dasharray="110 330" stroke-dashoffset="-10" opacity="0.9" />
					<circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-accent)" stroke-width="24" stroke-dasharray="95 345" stroke-dashoffset="-120" opacity="0.9" />
					<circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-violet)" stroke-width="24" stroke-dasharray="60 380" stroke-dashoffset="-215" opacity="0.9" />
					<circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-warning)" stroke-width="24" stroke-dasharray="50 390" stroke-dashoffset="-275" opacity="0.9" />
					<circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-info)" stroke-width="24" stroke-dasharray="30 410" stroke-dashoffset="-325" opacity="0.9" />
					<circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-danger)" stroke-width="24" stroke-dasharray="45 395" stroke-dashoffset="-355" opacity="0.9" />
					<!-- Center text -->
					<text x="100" y="95" text-anchor="middle" fill="var(--color-text-primary)" font-size="18" font-weight="700" font-family="var(--font-sans)">৳1.82Cr</text>
					<text x="100" y="115" text-anchor="middle" fill="var(--color-text-tertiary)" font-size="10" font-family="var(--font-sans)">Total Expenses</text>
				</svg>
				<div class="donut-legend">
					{#each [
						{ label: 'Salaries', value: '৳65L', color: 'var(--color-success)' },
						{ label: 'Operations', value: '৳42L', color: 'var(--color-accent)' },
						{ label: 'Marketing', value: '৳21L', color: 'var(--color-violet)' },
						{ label: 'Rent', value: '৳18L', color: 'var(--color-warning)' },
						{ label: 'Utilities', value: '৳9L', color: 'var(--color-info)' },
						{ label: 'Other', value: '৳27L', color: 'var(--color-danger)' },
					] as item}
						<div class="donut-legend-item">
							<span class="legend-dot" style="background: {item.color}"></span>
							<span class="legend-label">{item.label}</span>
							<span class="legend-value">{item.value}</span>
						</div>
					{/each}
				</div>
			</div>
		</section>

		<!-- Sales by Category -->
		<section class="chart-card animate-fade-in-up" style="animation-delay: 900ms">
			<div class="card-header">
				<h2 class="card-title">Sales by Category</h2>
			</div>
			<div class="bar-chart-container">
				{#each [
					{ label: 'Electronics', current: 85, prev: 72, value: '৳85L' },
					{ label: 'Healthcare', current: 46, prev: 38, value: '৳46L' },
					{ label: 'Clothing', current: 52, prev: 48, value: '৳52L' },
					{ label: 'Food', current: 41, prev: 39, value: '৳41L' },
					{ label: 'Furniture', current: 38, prev: 42, value: '৳38L' },
					{ label: 'Stationery', current: 22, prev: 19, value: '৳22L' },
				] as cat}
					<div class="bar-row">
						<span class="bar-label">{cat.label}</span>
						<div class="bar-track">
							<div class="bar-fill prev" style="width: {cat.prev}%"></div>
							<div class="bar-fill current" style="width: {cat.current}%"></div>
						</div>
						<span class="bar-value">{cat.value}</span>
					</div>
				{/each}
				<div class="chart-legend" style="margin-top: 12px;">
					<div class="legend-item">
						<span class="legend-dot" style="background: var(--color-accent)"></span>
						<span>Current</span>
					</div>
					<div class="legend-item">
						<span class="legend-dot" style="background: var(--color-text-muted)"></span>
						<span>Previous</span>
					</div>
				</div>
			</div>
		</section>

		<!-- Sales by Region -->
		<section class="chart-card animate-fade-in-up" style="animation-delay: 1000ms">
			<div class="card-header">
				<h2 class="card-title">Sales by Region</h2>
			</div>
			<div class="region-chart-container">
				{#each [
					{ name: 'Dhaka', namebn: 'ঢাকা', value: 12000000, pct: 100, formatted: '৳1.2Cr' },
					{ name: 'Chittagong', namebn: 'চট্টগ্রাম', value: 5500000, pct: 46, formatted: '৳55L' },
					{ name: 'Rajshahi', namebn: 'রাজশাহী', value: 2800000, pct: 23, formatted: '৳28L' },
					{ name: 'Khulna', namebn: 'খুলনা', value: 2200000, pct: 18, formatted: '৳22L' },
					{ name: 'Sylhet', namebn: 'সিলেট', value: 1800000, pct: 15, formatted: '৳18L' },
					{ name: 'Rangpur', namebn: 'রংপুর', value: 1200000, pct: 10, formatted: '৳12L' },
				] as region}
					<div class="region-row">
						<div class="region-info">
							<span class="region-name">{localeStore.isBangla ? region.namebn : region.name}</span>
							<span class="region-value">{region.formatted}</span>
						</div>
						<div class="region-bar-track">
							<div class="region-bar-fill" style="width: {region.pct}%"></div>
						</div>
					</div>
				{/each}
			</div>
		</section>
	</div>

	<!-- Activity Feed -->
	<section class="activity-card animate-fade-in-up" style="animation-delay: 1100ms">
		<div class="card-header">
			<h2 class="card-title">
				<Clock size={18} style="color: var(--color-text-tertiary)" />
				{localeStore.t('dashboard.activity')}
			</h2>
			<a href="/admin/activity" class="view-all-link">
				{localeStore.t('dashboard.view_all')}
				<ChevronRight size={14} />
			</a>
		</div>
		<div class="activity-list">
			{#each activities as act, i}
				{@const Icon = act.icon}
				<div class="activity-item" style="animation-delay: {1200 + i * 60}ms">
					<div class="activity-icon" style="color: {getActivityTypeColor(act.type)}">
						<Icon size={16} />
					</div>
					<div class="activity-content">
						<span class="activity-title">{act.title}</span>
						<span class="activity-desc">{act.desc}</span>
					</div>
					<span class="activity-time">{act.time}</span>
				</div>
			{/each}
		</div>
	</section>
</div>

<style>
	.dashboard {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	/* ── Page Header ──────────────────────────────────── */
	.page-header {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 16px;
		flex-wrap: wrap;
	}

	.page-title {
		font-size: 1.75rem;
		font-weight: 700;
		margin: 0;
		letter-spacing: -0.03em;
		line-height: 1.2;
	}

	.page-subtitle {
		font-size: 0.875rem;
		color: var(--color-text-secondary);
		margin: 6px 0 0 0;
	}

	.header-actions {
		display: flex;
		gap: 8px;
	}

	.btn-primary, .btn-outline {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 8px 16px;
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		font-weight: 500;
		font-family: inherit;
		cursor: pointer;
		transition: all var(--transition-fast);
		white-space: nowrap;
	}

	.btn-primary {
		background: var(--color-accent);
		color: white;
		border: none;
	}

	.btn-primary:hover {
		background: var(--color-accent-hover);
		box-shadow: 0 0 20px var(--color-accent-glow);
	}

	.btn-outline {
		background: transparent;
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border);
	}

	.btn-outline:hover {
		background: var(--color-bg-hover);
		border-color: var(--color-border-hover);
		color: var(--color-text-primary);
	}

	/* ── KPI Grid ─────────────────────────────────────── */
	.kpi-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 16px;
	}

	.kpi-card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 18px;
		transition: all var(--transition-fast);
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}

	.kpi-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 2px;
		opacity: 0;
		transition: opacity var(--transition-fast);
	}

	.kpi-card:hover {
		border-color: var(--color-border-hover);
		box-shadow: var(--shadow-md);
		transform: translateY(-1px);
	}

	.kpi-card:hover::before {
		opacity: 1;
	}

	.kpi-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 14px;
	}

	.kpi-icon {
		width: 36px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: var(--radius-md);
	}

	.kpi-more {
		width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: none;
		border: none;
		color: var(--color-text-muted);
		border-radius: var(--radius-sm);
		cursor: pointer;
		opacity: 0;
		transition: all var(--transition-fast);
	}

	.kpi-card:hover .kpi-more {
		opacity: 1;
	}

	.kpi-more:hover {
		background: var(--color-bg-hover);
		color: var(--color-text-secondary);
	}

	.kpi-body {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.kpi-label {
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}

	.kpi-value {
		font-size: 1.375rem;
		font-weight: 700;
		color: var(--color-text-primary);
		letter-spacing: -0.02em;
		font-variant-numeric: tabular-nums;
	}

	.kpi-footer {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 14px;
	}

	.kpi-change {
		display: inline-flex;
		align-items: center;
		gap: 2px;
		font-size: 0.75rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: var(--radius-full);
	}

	.kpi-change.positive {
		color: var(--color-success);
		background: var(--color-success-muted);
	}

	.kpi-change.negative {
		color: var(--color-danger);
		background: var(--color-danger-muted);
	}

	.sparkline {
		width: 80px;
		height: 28px;
		flex-shrink: 0;
	}

	/* ── Card Styles ──────────────────────────────────── */
	.chart-card, .insights-card, .activity-card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		overflow: hidden;
	}

	.card-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 16px 20px;
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.card-title {
		font-size: 0.875rem;
		font-weight: 600;
		margin: 0;
		display: flex;
		align-items: center;
		gap: 8px;
		color: var(--color-text-primary);
	}

	.card-actions {
		display: flex;
		gap: 4px;
	}

	.period-btn {
		padding: 4px 10px;
		font-size: 0.6875rem;
		font-weight: 500;
		font-family: inherit;
		background: transparent;
		border: 1px solid var(--color-border);
		color: var(--color-text-tertiary);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.period-btn.active, .period-btn:hover {
		background: var(--color-accent-muted);
		color: var(--color-accent-light);
		border-color: var(--color-accent);
	}

	.view-all-link {
		display: flex;
		align-items: center;
		gap: 4px;
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-accent);
		text-decoration: none;
		transition: color var(--transition-fast);
	}

	.view-all-link:hover {
		color: var(--color-accent-hover);
	}

	/* ── Main Grid ────────────────────────────────────── */
	.main-grid {
		display: grid;
		grid-template-columns: 1.6fr 1fr;
		gap: 16px;
	}

	.chart-card.large {
		grid-column: 1;
	}

	.chart-placeholder {
		padding: 20px;
	}

	.chart-demo {
		position: relative;
	}

	.demo-chart {
		width: 100%;
		height: 180px;
	}

	.chart-labels {
		display: flex;
		justify-content: space-between;
		padding: 8px 0 0;
		font-size: 0.6875rem;
		color: var(--color-text-muted);
	}

	.chart-legend {
		display: flex;
		gap: 16px;
		padding: 8px 0 0;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}

	.legend-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		flex-shrink: 0;
	}

	/* ── Charts Row ───────────────────────────────────── */
	.charts-row {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 16px;
	}

	/* ── Donut Chart ──────────────────────────────────── */
	.donut-chart-container {
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16px;
	}

	.donut-chart {
		width: 160px;
		height: 160px;
	}

	.donut-legend {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.donut-legend-item {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.75rem;
	}

	.legend-label {
		flex: 1;
		color: var(--color-text-secondary);
	}

	.legend-value {
		font-weight: 600;
		font-variant-numeric: tabular-nums;
		color: var(--color-text-primary);
	}

	/* ── Bar Chart ────────────────────────────────────── */
	.bar-chart-container {
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.bar-row {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.bar-label {
		width: 80px;
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		text-align: right;
		flex-shrink: 0;
	}

	.bar-track {
		flex: 1;
		height: 20px;
		background: var(--color-bg-tertiary);
		border-radius: var(--radius-sm);
		position: relative;
		overflow: hidden;
	}

	.bar-fill {
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		border-radius: var(--radius-sm);
		transition: width 0.6s ease-out;
	}

	.bar-fill.current {
		background: var(--color-accent);
		z-index: 2;
	}

	.bar-fill.prev {
		background: var(--color-text-muted);
		opacity: 0.3;
		z-index: 1;
	}

	.bar-value {
		width: 50px;
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-primary);
		font-variant-numeric: tabular-nums;
		flex-shrink: 0;
	}

	/* ── Region Chart ─────────────────────────────────── */
	.region-chart-container {
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.region-row {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.region-info {
		display: flex;
		justify-content: space-between;
	}

	.region-name {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}

	.region-value {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-primary);
		font-variant-numeric: tabular-nums;
	}

	.region-bar-track {
		height: 6px;
		background: var(--color-bg-tertiary);
		border-radius: var(--radius-full);
		overflow: hidden;
	}

	.region-bar-fill {
		height: 100%;
		background: var(--gradient-accent);
		border-radius: var(--radius-full);
		transition: width 0.8s ease-out;
	}

	/* ── AI Insights ──────────────────────────────────── */
	.insights-list {
		padding: 8px;
	}

	.insight-item {
		display: flex;
		gap: 12px;
		padding: 12px;
		border-radius: var(--radius-md);
		transition: background var(--transition-fast);
		cursor: pointer;
	}

	.insight-item:hover {
		background: var(--color-bg-hover);
	}

	.insight-icon {
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: var(--radius-sm);
		flex-shrink: 0;
	}

	.insight-content {
		flex: 1;
		min-width: 0;
	}

	.insight-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 8px;
		margin-bottom: 4px;
	}

	.insight-title {
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.insight-metric {
		font-size: 0.75rem;
		font-weight: 700;
		font-variant-numeric: tabular-nums;
		flex-shrink: 0;
	}

	.insight-desc {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		margin: 0;
		line-height: 1.5;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}

	/* ── Activity Feed ────────────────────────────────── */
	.activity-list {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
	}

	.activity-item {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 14px 20px;
		border-bottom: 1px solid var(--color-border-subtle);
		transition: background var(--transition-fast);
		cursor: pointer;
	}

	.activity-item:hover {
		background: var(--color-bg-hover);
	}

	.activity-item:nth-child(odd) {
		border-right: 1px solid var(--color-border-subtle);
	}

	.activity-icon {
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		opacity: 0.8;
	}

	.activity-content {
		flex: 1;
		min-width: 0;
	}

	.activity-title {
		display: block;
		font-size: 0.8125rem;
		font-weight: 500;
		color: var(--color-text-primary);
	}

	.activity-desc {
		display: block;
		font-size: 0.75rem;
		color: var(--color-text-tertiary);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		margin-top: 2px;
	}

	.activity-time {
		font-size: 0.6875rem;
		color: var(--color-text-muted);
		flex-shrink: 0;
		white-space: nowrap;
	}

	/* ── Responsive ───────────────────────────────────── */
	@media (max-width: 1280px) {
		.kpi-grid { grid-template-columns: repeat(4, 1fr); }
		.charts-row { grid-template-columns: repeat(2, 1fr); }
	}

	@media (max-width: 1024px) {
		.kpi-grid { grid-template-columns: repeat(2, 1fr); }
		.main-grid { grid-template-columns: 1fr; }
		.charts-row { grid-template-columns: 1fr; }
		.activity-list { grid-template-columns: 1fr; }
		.activity-item:nth-child(odd) { border-right: none; }
	}

	@media (max-width: 640px) {
		.kpi-grid { grid-template-columns: 1fr; }
		.page-header { flex-direction: column; }
		.header-actions { width: 100%; }
	}
</style>
