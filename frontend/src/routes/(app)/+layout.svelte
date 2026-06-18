<!--
  App shell layout — Sidebar + TopNav + Content area.
  All authenticated routes are nested under (app)/.
  Includes auth guard that redirects to /login if not authenticated.
-->
<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import TopNav from '$lib/components/layout/TopNav.svelte';
	import { authStore } from '$lib/stores/auth.svelte';
	import { sidebarStore } from '$lib/stores/sidebar.svelte';

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

		<main
			class="app-content"
			class:sidebar-collapsed={sidebarStore.collapsed}
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

	.app-content {
		margin-left: var(--sidebar-width);
		margin-top: var(--topnav-height);
		min-height: calc(100vh - var(--topnav-height));
		transition: margin-left var(--transition-slow);
		background: var(--color-bg-primary);
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
