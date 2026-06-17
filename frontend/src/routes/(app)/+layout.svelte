<!--
  App shell layout — Sidebar + TopNav + Content area.
  All authenticated routes are nested under (app)/.
-->
<script lang="ts">
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import TopNav from '$lib/components/layout/TopNav.svelte';
	import { sidebarStore } from '$lib/stores/sidebar.svelte';

	let { children } = $props();
</script>

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
</style>
