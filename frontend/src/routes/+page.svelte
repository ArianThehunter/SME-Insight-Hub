<!--
  Root route — redirects authenticated users to dashboard, others to login.
  /demo shortcut → demo dashboard without login.
-->
<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth.svelte';

	if (browser) {
		if (authStore.isAuthenticated) {
			goto('/dashboard');
		} else {
			goto('/login');
		}
	}
</script>
