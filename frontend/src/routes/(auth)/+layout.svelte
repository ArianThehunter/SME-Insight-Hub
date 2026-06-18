<!--
  Auth layout — Clean centered layout for login/register pages (no sidebar/topnav).
-->
<script lang="ts">
	let { children } = $props();
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
</svelte:head>

<div class="auth-layout">
	<div class="auth-bg-decoration"></div>
	<div class="auth-bg-grid"></div>
	{@render children()}
</div>

<style>
	.auth-layout {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 24px;
		position: relative;
		overflow: hidden;
		background: var(--color-bg-primary);
	}

	.auth-bg-decoration {
		position: absolute;
		inset: 0;
		background:
			radial-gradient(ellipse 80% 60% at 50% -10%, rgba(59, 130, 246, 0.12) 0%, transparent 60%),
			radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
			radial-gradient(ellipse 50% 30% at 10% 90%, rgba(16, 185, 129, 0.06) 0%, transparent 40%);
		pointer-events: none;
	}

	.auth-bg-grid {
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(rgba(59, 130, 246, 0.03) 1px, transparent 1px),
			linear-gradient(90deg, rgba(59, 130, 246, 0.03) 1px, transparent 1px);
		background-size: 60px 60px;
		pointer-events: none;
	}
</style>
