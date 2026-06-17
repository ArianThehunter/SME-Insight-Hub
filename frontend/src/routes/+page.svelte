<!--
  Root page — redirects to dashboard.
-->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		goto('/dashboard');
	});
</script>

<div style="display: flex; align-items: center; justify-content: center; height: 100vh; background: var(--color-bg-primary);">
	<div style="text-align: center;">
		<div class="animate-pulse-soft" style="font-size: 2rem; font-weight: 700; color: var(--color-accent);">SME Insight Hub</div>
		<p style="color: var(--color-text-secondary); margin-top: 8px;">Loading...</p>
	</div>
</div>
