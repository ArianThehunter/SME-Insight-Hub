<!--
  PlaceholderPage.svelte — Reusable placeholder for pages under construction.
-->
<script lang="ts">
	import { Construction, ArrowLeft } from '@lucide/svelte';

	let { title = 'Page', description = 'This feature is coming soon.', icon }: {
		title?: string;
		description?: string;
		icon?: any;
	} = $props();
</script>

<div class="placeholder-page">
	<div class="placeholder-content animate-fade-in-up">
		<div class="placeholder-icon">
			{#if icon}
				{@const Icon = icon}
				<Icon size={32} />
			{:else}
				<Construction size={32} />
			{/if}
		</div>
		<h1 class="placeholder-title">{title}</h1>
		<p class="placeholder-desc">{description}</p>
		<div class="placeholder-badges">
			<span class="badge">Enterprise Feature</span>
			<span class="badge accent">Coming Soon</span>
		</div>
	</div>
</div>

<style>
	.placeholder-page {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 60vh;
	}

	.placeholder-content {
		text-align: center;
		max-width: 400px;
	}

	.placeholder-icon {
		width: 72px;
		height: 72px;
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 0 auto 20px;
		background: var(--color-accent-muted);
		color: var(--color-accent);
		border-radius: var(--radius-xl);
	}

	.placeholder-title {
		font-size: 1.5rem;
		font-weight: 700;
		margin: 0 0 8px 0;
		color: var(--color-text-primary);
		letter-spacing: -0.02em;
	}

	.placeholder-desc {
		font-size: 0.875rem;
		color: var(--color-text-secondary);
		line-height: 1.6;
		margin: 0 0 20px 0;
	}

	.placeholder-badges {
		display: flex;
		justify-content: center;
		gap: 8px;
	}

	.badge {
		padding: 4px 12px;
		font-size: 0.6875rem;
		font-weight: 600;
		border-radius: var(--radius-full);
		background: var(--color-bg-tertiary);
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border);
	}

	.badge.accent {
		background: var(--color-accent-muted);
		color: var(--color-accent-light);
		border-color: transparent;
	}
</style>
