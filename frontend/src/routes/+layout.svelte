<!--
  Root layout — Imports global CSS.
-->
<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

{@render children()}
