<!--
  Settings Localization — Language, timezone, currency, and fiscal calendar preferences.
-->
<script lang="ts">
	import { Globe, Save, CheckCircle2 } from '@lucide/svelte';
	import { localeStore } from '$lib/stores/locale.svelte';

	let language = $state(localeStore.current);
	let currency = $state('BDT');
	let timezone = $state('Asia/Dhaka');
	let fiscalYear = $state('July');
	let saved = $state(false);

	function saveLocalization(e: Event) {
		e.preventDefault();
		localeStore.setLocale(language as 'en' | 'bn');
		saved = true;
		setTimeout(() => (saved = false), 3000);
	}
</script>

<svelte:head><title>Localization Settings — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Regional & Localization Preferences</h1>
			<p class="page-subtitle">
				Configure primary language (English / বাংলা), base operating currency, and fiscal cycle
			</p>
		</div>
	</header>

	<form onsubmit={saveLocalization} class="settings-form">
		<div class="card form-card">
			<div class="form-grid">
				<div class="form-group">
					<label for="lang-select">Interface Language</label>
					<select id="lang-select" bind:value={language}>
						<option value="en">English (US / International)</option>
						<option value="bn">বাংলা (Bengali)</option>
					</select>
				</div>
				<div class="form-group">
					<label for="curr-select">Default Currency</label>
					<select id="curr-select" bind:value={currency}>
						<option value="BDT">BDT (৳ - Bangladeshi Taka)</option>
						<option value="USD">USD ($ - US Dollar)</option>
						<option value="EUR">EUR (€ - Euro)</option>
					</select>
				</div>
			</div>

			<div class="form-grid">
				<div class="form-group">
					<label for="tz-select">Timezone</label>
					<select id="tz-select" bind:value={timezone}>
						<option value="Asia/Dhaka">Asia/Dhaka (GMT+6)</option>
					</select>
				</div>
				<div class="form-group">
					<label for="fiscal-select">Fiscal Year Start Month</label>
					<select id="fiscal-select" bind:value={fiscalYear}>
						<option value="July">July (Bangladesh Standard)</option>
						<option value="January">January (Calendar Year)</option>
					</select>
				</div>
			</div>
		</div>

		<div class="form-footer">
			{#if saved}
				<span class="save-msg"><CheckCircle2 size={16} /> Preferences updated!</span>
			{/if}
			<button type="submit" class="btn-primary">
				<Save size={16} />
				Save Localization
			</button>
		</div>
	</form>
</div>

<style>
	.page-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
		letter-spacing: -0.02em;
	}
	.page-subtitle {
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
		margin: 4px 0 0;
	}
	.btn-primary {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 8px 18px;
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		font-weight: 600;
		cursor: pointer;
		background: var(--color-accent);
		color: white;
		border: none;
	}

	.settings-form {
		display: flex;
		flex-direction: column;
		gap: 16px;
		margin-top: 20px;
		max-width: 720px;
	}
	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.form-card {
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.form-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 14px;
	}
	@media (max-width: 600px) {
		.form-grid {
			grid-template-columns: 1fr;
		}
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.form-group label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}
	.form-group select {
		padding: 8px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: 0.8125rem;
	}

	.form-footer {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		gap: 12px;
	}
	.save-msg {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		font-size: 0.8125rem;
		color: var(--color-success);
		font-weight: 600;
	}
</style>
