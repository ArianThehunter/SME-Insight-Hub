<!--
  TopNav.svelte — Top navigation bar with search, notifications, user menu, and controls.
-->
<script lang="ts">
	import { sidebarStore } from '$lib/stores/sidebar.svelte';
	import { themeStore } from '$lib/stores/theme.svelte';
	import { localeStore } from '$lib/stores/locale.svelte';
	import { authStore } from '$lib/stores/auth.svelte';
	import {
		Search, Bell, Sun, Moon, Menu,
		Languages, ChevronDown, LogOut, User, Settings,
		Sparkles, Loader, Building2
	} from '@lucide/svelte';

	let showUserMenu = $state(false);
	let showNotifications = $state(false);
	let searchQuery = $state('');
	let searchFocused = $state(false);

	function closeMenus() {
		showUserMenu = false;
		showNotifications = false;
	}

	const demoNotifications = [
		{ id: 1, title: 'Invoice processed', desc: 'INV-2024-0847 extracted with 96% confidence', time: '12m ago', read: false },
		{ id: 2, title: 'Low stock alert', desc: 'Wireless Mouse MX-200 below reorder level', time: '1h ago', read: false },
		{ id: 3, title: 'Report ready', desc: 'May 2024 Executive Summary generated', time: '2h ago', read: true },
		{ id: 4, title: 'New customer', desc: 'ABC Trading Co. registered', time: '3h ago', read: true },
	];
</script>

<svelte:window onclick={closeMenus} />

<header class="topnav" role="banner">
	<div class="topnav-left">
		<!-- Mobile menu toggle -->
		<button class="mobile-menu-btn" onclick={() => sidebarStore.toggleMobile()} aria-label="Toggle menu">
			<Menu size={20} />
		</button>

		<!-- Search -->
		<div class="search-container" class:focused={searchFocused}>
			<Search size={16} />
			<input
				type="text"
				placeholder={localeStore.t('action.search')}
				bind:value={searchQuery}
				onfocus={() => searchFocused = true}
				onblur={() => searchFocused = false}
				class="search-input"
				aria-label="Search"
			/>
			<kbd class="search-shortcut">⌘K</kbd>
		</div>
	</div>

	<div class="topnav-right">
		<!-- AI Assistant shortcut -->
		<a href="/ai-assistant" class="topnav-btn ai-btn" title="AI Assistant">
			<Sparkles size={18} />
			<span class="btn-label">AI</span>
		</a>

		<!-- Report status -->
		<button class="topnav-btn" title="Report generation status">
			<Loader size={18} class="report-icon" />
			<span class="status-dot success"></span>
		</button>

		<!-- Language toggle -->
		<button
			class="topnav-btn lang-btn"
			onclick={(e: MouseEvent) => { e.stopPropagation(); localeStore.toggle(); }}
			title={localeStore.isBangla ? 'Switch to English' : 'বাংলায় পরিবর্তন করুন'}
			aria-label="Toggle language"
		>
			<Languages size={18} />
			<span class="lang-label">{localeStore.isBangla ? 'BN' : 'EN'}</span>
		</button>

		<!-- Theme toggle -->
		<button
			class="topnav-btn"
			onclick={(e: MouseEvent) => { e.stopPropagation(); themeStore.toggle(); }}
			title={themeStore.isDark ? 'Switch to light mode' : 'Switch to dark mode'}
			aria-label="Toggle theme"
		>
			{#if themeStore.isDark}
				<Sun size={18} />
			{:else}
				<Moon size={18} />
			{/if}
		</button>

		<!-- Notifications -->
		<div class="dropdown-container">
			<button
				class="topnav-btn notification-btn"
				onclick={(e: MouseEvent) => { e.stopPropagation(); showNotifications = !showNotifications; showUserMenu = false; }}
				title={localeStore.t('action.notifications')}
				aria-label="Notifications"
				aria-haspopup="true"
				aria-expanded={showNotifications}
			>
				<Bell size={18} />
				<span class="notification-badge">3</span>
			</button>

			{#if showNotifications}
				<div class="dropdown notification-dropdown" role="menu" onclick={(e: MouseEvent) => e.stopPropagation()}>
					<div class="dropdown-header">
						<h3>Notifications</h3>
						<button class="mark-read">Mark all read</button>
					</div>
					<div class="dropdown-body">
						{#each demoNotifications as notif}
							<div class="notification-item" class:unread={!notif.read}>
								<div class="notification-content">
									<p class="notification-title">{notif.title}</p>
									<p class="notification-desc">{notif.desc}</p>
								</div>
								<span class="notification-time">{notif.time}</span>
							</div>
						{/each}
					</div>
					<div class="dropdown-footer">
						<a href="/notifications">View all notifications</a>
					</div>
				</div>
			{/if}
		</div>

		<!-- Company selector -->
		<div class="company-selector">
			<Building2 size={16} />
			<span class="company-name">
				{authStore.user?.organization?.name ?? 'Rahman Enterprise'}
			</span>
		</div>

		<!-- User menu -->
		<div class="dropdown-container">
			<button
				class="user-menu-trigger"
				onclick={(e: MouseEvent) => { e.stopPropagation(); showUserMenu = !showUserMenu; showNotifications = false; }}
				aria-haspopup="true"
				aria-expanded={showUserMenu}
			>
				<div class="user-avatar">
					{(authStore.user?.full_name?.[0] ?? 'R').toUpperCase()}
				</div>
				<div class="user-info">
					<span class="user-name">{authStore.user?.full_name ?? 'Rafiq Ahmed'}</span>
					<span class="user-role">{authStore.user?.role?.display_name ?? 'Organization Owner'}</span>
				</div>
				<ChevronDown size={14} />
			</button>

			{#if showUserMenu}
				<div class="dropdown user-dropdown" role="menu" onclick={(e: MouseEvent) => e.stopPropagation()}>
					<a href="/settings/profile" class="dropdown-item" role="menuitem">
						<User size={16} />
						<span>Profile</span>
					</a>
					<a href="/settings/organization" class="dropdown-item" role="menuitem">
						<Settings size={16} />
						<span>Settings</span>
					</a>
					<div class="dropdown-divider"></div>
					<button class="dropdown-item danger" onclick={() => authStore.logout()} role="menuitem">
						<LogOut size={16} />
						<span>Sign Out</span>
					</button>
				</div>
			{/if}
		</div>
	</div>
</header>

<style>
	.topnav {
		position: fixed;
		top: 0;
		right: 0;
		left: var(--sidebar-width);
		height: var(--topnav-height);
		background: var(--color-bg-secondary);
		border-bottom: 1px solid var(--color-border);
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 20px;
		z-index: 30;
		transition: left var(--transition-slow);
		gap: 12px;
	}

	:global(.sidebar.collapsed) ~ .topnav,
	:global(aside.collapsed) ~ .topnav {
		left: var(--sidebar-collapsed-width);
	}

	.topnav-left {
		display: flex;
		align-items: center;
		gap: 12px;
		flex: 1;
		max-width: 500px;
	}

	.topnav-right {
		display: flex;
		align-items: center;
		gap: 4px;
	}

	/* ── Mobile Menu ──────────────────────────────────── */
	.mobile-menu-btn {
		display: none;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border: none;
		background: transparent;
		color: var(--color-text-secondary);
		border-radius: var(--radius-sm);
		cursor: pointer;
	}

	/* ── Search ──────────────────────────────────────── */
	.search-container {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 14px;
		background: var(--color-bg-tertiary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		width: 100%;
		transition: all var(--transition-fast);
		color: var(--color-text-tertiary);
	}

	.search-container.focused {
		border-color: var(--color-accent);
		box-shadow: 0 0 0 3px var(--color-accent-muted);
		background: var(--color-bg-elevated);
	}

	.search-input {
		flex: 1;
		background: none;
		border: none;
		outline: none;
		color: var(--color-text-primary);
		font-size: 0.8125rem;
		font-family: inherit;
	}

	.search-input::placeholder {
		color: var(--color-text-muted);
	}

	.search-shortcut {
		font-family: var(--font-mono);
		font-size: 0.6875rem;
		padding: 2px 6px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		color: var(--color-text-muted);
		white-space: nowrap;
	}

	/* ── Buttons ──────────────────────────────────────── */
	.topnav-btn {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 6px;
		width: 36px;
		height: 36px;
		border: none;
		background: transparent;
		color: var(--color-text-secondary);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.topnav-btn:hover {
		background: var(--color-bg-hover);
		color: var(--color-text-primary);
	}

	.ai-btn {
		width: auto;
		padding: 0 12px;
		gap: 6px;
		background: var(--color-accent-muted);
		color: var(--color-accent-light);
		text-decoration: none;
		font-size: 0.8125rem;
		font-weight: 600;
	}

	.ai-btn:hover {
		background: var(--color-accent);
		color: white;
	}

	.btn-label {
		font-size: 0.75rem;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.lang-btn {
		width: auto;
		padding: 0 10px;
		gap: 4px;
	}

	.lang-label {
		font-size: 0.6875rem;
		font-weight: 600;
		letter-spacing: 0.05em;
	}

	.status-dot {
		position: absolute;
		top: 8px;
		right: 8px;
		width: 6px;
		height: 6px;
		border-radius: 50%;
	}

	.status-dot.success {
		background: var(--color-success);
	}

	:global(.report-icon) {
		opacity: 0.5;
	}

	/* ── Notifications ────────────────────────────────── */
	.notification-badge {
		position: absolute;
		top: 4px;
		right: 4px;
		width: 16px;
		height: 16px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-danger);
		color: white;
		font-size: 0.625rem;
		font-weight: 700;
		border-radius: 50%;
	}

	/* ── Company Selector ─────────────────────────────── */
	.company-selector {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 12px;
		background: var(--color-bg-tertiary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		white-space: nowrap;
	}

	.company-name {
		max-width: 120px;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	/* ── User Menu ────────────────────────────────────── */
	.user-menu-trigger {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 4px 8px 4px 4px;
		border: none;
		background: transparent;
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: all var(--transition-fast);
		color: var(--color-text-secondary);
	}

	.user-menu-trigger:hover {
		background: var(--color-bg-hover);
	}

	.user-avatar {
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--gradient-accent);
		color: white;
		font-size: 0.8125rem;
		font-weight: 700;
		border-radius: var(--radius-sm);
		flex-shrink: 0;
	}

	.user-info {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		text-align: left;
	}

	.user-name {
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--color-text-primary);
		white-space: nowrap;
	}

	.user-role {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		white-space: nowrap;
	}

	/* ── Dropdown ──────────────────────────────────────── */
	.dropdown-container {
		position: relative;
	}

	.dropdown {
		position: absolute;
		top: calc(100% + 8px);
		right: 0;
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-xl);
		overflow: hidden;
		animation: scaleIn var(--transition-fast) ease-out;
		z-index: 50;
	}

	.notification-dropdown {
		width: 360px;
	}

	.user-dropdown {
		width: 200px;
		padding: 4px;
	}

	.dropdown-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 14px 16px;
		border-bottom: 1px solid var(--color-border);
	}

	.dropdown-header h3 {
		font-size: 0.875rem;
		font-weight: 600;
		margin: 0;
	}

	.mark-read {
		font-size: 0.75rem;
		color: var(--color-accent);
		background: none;
		border: none;
		cursor: pointer;
		font-weight: 500;
	}

	.dropdown-body {
		max-height: 320px;
		overflow-y: auto;
	}

	.notification-item {
		display: flex;
		justify-content: space-between;
		gap: 12px;
		padding: 12px 16px;
		border-bottom: 1px solid var(--color-border-subtle);
		transition: background var(--transition-fast);
		cursor: pointer;
	}

	.notification-item:hover {
		background: var(--color-bg-hover);
	}

	.notification-item.unread {
		background: var(--color-accent-muted);
	}

	.notification-content {
		flex: 1;
		min-width: 0;
	}

	.notification-title {
		font-size: 0.8125rem;
		font-weight: 500;
		margin: 0 0 2px 0;
		color: var(--color-text-primary);
	}

	.notification-desc {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		margin: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.notification-time {
		font-size: 0.6875rem;
		color: var(--color-text-muted);
		white-space: nowrap;
		flex-shrink: 0;
	}

	.dropdown-footer {
		padding: 10px 16px;
		border-top: 1px solid var(--color-border);
		text-align: center;
	}

	.dropdown-footer a {
		font-size: 0.75rem;
		color: var(--color-accent);
		text-decoration: none;
		font-weight: 500;
	}

	.dropdown-item {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px 12px;
		border-radius: var(--radius-sm);
		color: var(--color-text-secondary);
		text-decoration: none;
		font-size: 0.8125rem;
		background: none;
		border: none;
		width: 100%;
		cursor: pointer;
		transition: all var(--transition-fast);
		text-align: left;
	}

	.dropdown-item:hover {
		background: var(--color-bg-hover);
		color: var(--color-text-primary);
	}

	.dropdown-item.danger {
		color: var(--color-danger);
	}

	.dropdown-item.danger:hover {
		background: var(--color-danger-bg);
	}

	.dropdown-divider {
		height: 1px;
		background: var(--color-border);
		margin: 4px 0;
	}

	/* ── Responsive ───────────────────────────────────── */
	@media (max-width: 1024px) {
		.topnav {
			left: 0;
		}

		.mobile-menu-btn {
			display: flex;
		}

		.company-selector,
		.search-shortcut {
			display: none;
		}

		.user-info {
			display: none;
		}
	}

	@media (max-width: 640px) {
		.topnav-right {
			gap: 2px;
		}

		.ai-btn .btn-label,
		.lang-label {
			display: none;
		}

		.ai-btn {
			width: 36px;
			padding: 0;
		}

		.notification-dropdown {
			width: calc(100vw - 32px);
			right: -60px;
		}
	}
</style>
