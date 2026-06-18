<!--
  Root page — Redirects based on auth status.
-->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.svelte';

	onMount(() => {
		if (authStore.isAuthenticated) {
			goto('/dashboard');
		} else {
			goto('/login');
		}
	});
</script>

<div style="display: flex; align-items: center; justify-content: center; height: 100vh; background: var(--color-bg-primary);">
	<div style="text-align: center;">
		<div class="animate-pulse-soft" style="font-size: 2rem; font-weight: 700; color: var(--color-accent);">SME Insight Hub</div>
		<p style="color: var(--color-text-secondary); margin-top: 8px;">Redirecting...</p>
	</div>
</div>
