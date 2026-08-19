<!--
  App shell layout — Sidebar + TopNav + Content area.
  All authenticated routes are nested under (app)/.
  Includes auth guard that redirects to /login if not authenticated.
  Shows demo mode banner when authStore.isDemo is true.
-->
<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import TopNav from '$lib/components/layout/TopNav.svelte';
	import { authStore } from '$lib/stores/auth.svelte';
	import { sidebarStore } from '$lib/stores/sidebar.svelte';
	import { FlaskConical, X } from '@lucide/svelte';

	let { children } = $props();

	// Auth guard — redirect to login if not authenticated
	$effect(() => {
		if (browser && !authStore.isLoading && !authStore.isAuthenticated) {
			goto('/login');
		}
	});
</script>

{#if authStore.isAuthenticated}
	<div class="app-shell">
		<Sidebar />
		<TopNav />

		{#if authStore.isDemo}
			<div class="demo-banner" role="status">
				<FlaskConical size={14} />
				<span>
					<strong>Demo Mode</strong> — You're viewing sample data.
					<a href="/login" class="demo-link">Sign in</a> or
					<a href="/register" class="demo-link">create an account</a> to use your own data.
				</span>
				<button class="demo-close" onclick={() => authStore.logout()} aria-label="Exit demo">
					<X size={14} />
				</button>
			</div>
		{/if}

		<main
			class="app-content"
			class:sidebar-collapsed={sidebarStore.collapsed}
			class:has-demo-banner={authStore.isDemo}
		>
			<div class="content-inner">
				{@render children()}
			</div>
		</main>
	</div>
{:else}
	<div class="auth-loading">
		<div class="loading-spinner"></div>
		<p>Loading...</p>
	</div>
{/if}

<style>
	.app-shell {
		min-height: 100vh;
	}

	/* ── Demo Banner ──────────────────────────────────── */
	.demo-banner {
		position: fixed;
		top: var(--topnav-height);
		left: var(--sidebar-width);
		right: 0;
		z-index: 25;
		background: linear-gradient(90deg, #f59e0b, #d97706);
		color: #1c1200;
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 20px;
		font-size: 0.8125rem;
		font-weight: 500;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
		transition: left var(--transition-slow);
	}

	.demo-banner span {
		flex: 1;
	}

	.demo-link {
		color: #1c1200;
		font-weight: 700;
		text-decoration: underline;
		text-underline-offset: 2px;
	}

	.demo-close {
		background: none;
		border: none;
		cursor: pointer;
		padding: 2px;
		color: #1c1200;
		opacity: 0.7;
		transition: opacity 0.15s;
		display: flex;
		align-items: center;
	}

	.demo-close:hover {
		opacity: 1;
	}

	/* ── Main Content ─────────────────────────────────── */
	.app-content {
		margin-left: var(--sidebar-width);
		margin-top: var(--topnav-height);
		min-height: calc(100vh - var(--topnav-height));
		transition: margin-left var(--transition-slow);
		background: var(--color-bg-primary);
	}

	.app-content.has-demo-banner {
		margin-top: calc(var(--topnav-height) + 33px);
	}

	.app-content.sidebar-collapsed {
		margin-left: var(--sidebar-collapsed-width);
	}

	.content-inner {
		padding: var(--page-padding);
		max-width: var(--content-max-width);
		margin: 0 auto;
	}

	@media (max-width: 1024px) {
		.app-content,
		.app-content.sidebar-collapsed {
			margin-left: 0;
		}
		.demo-banner {
			left: 0;
		}
	}

	.auth-loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		gap: 12px;
		color: var(--color-text-secondary);
		font-size: 0.875rem;
	}

	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid var(--color-border);
		border-top-color: var(--color-accent);
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}
</style>
