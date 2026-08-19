<!--
  Settings Branding — Company logo, invoice headers, and theme accents.
-->
<script lang="ts">
	import { Palette, Upload, Image, Save, CheckCircle2 } from '@lucide/svelte';

	let accentColor = $state('#0ea5e9');
	let invoiceFooter = $state('Thank you for doing business with Acme Corporation Ltd. | VAT Registration No: 002481920-0101');
	let saved = $state(false);

	function saveBranding(e: Event) {
		e.preventDefault();
		saved = true;
		setTimeout(() => saved = false, 3000);
	}
</script>

<svelte:head><title>Branding Settings — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Corporate Branding & Invoice Styling</h1>
			<p class="page-subtitle">Customize organizational logos, PDF document headers, and invoice branding</p>
		</div>
	</header>

	<form onsubmit={saveBranding} class="settings-form">
		<div class="card form-card">
			<h2 class="card-title">Company Logo & Icon</h2>
			<div class="logo-upload-wrap">
				<div class="logo-preview">
					<span>ACME</span>
				</div>
				<div class="upload-btn-wrap">
					<button type="button" class="btn-secondary">
						<Upload size={14} />
						Upload New Logo
					</button>
					<span class="upload-hint">PNG or SVG recommended. Max 2MB.</span>
				</div>
			</div>
		</div>

		<div class="card form-card">
			<h2 class="card-title">Invoice Letterhead & Footnote</h2>
			<div class="form-group">
				<label for="inv-footer">Default Invoice Footer Notice</label>
				<textarea id="inv-footer" rows="3" bind:value={invoiceFooter}></textarea>
			</div>
		</div>

		<div class="form-footer">
			{#if saved}
				<span class="save-msg"><CheckCircle2 size={16} /> Branding saved!</span>
			{/if}
			<button type="submit" class="btn-primary">
				<Save size={16} />
				Save Branding
			</button>
		</div>
	</form>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 8px 18px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-accent); color: white; border: none; }
	.btn-secondary { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-bg-primary); color: var(--color-text-primary); border: 1px solid var(--color-border); }

	.settings-form { display: flex; flex-direction: column; gap: 16px; margin-top: 20px; max-width: 720px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.form-card { padding: 20px; display: flex; flex-direction: column; gap: 16px; }
	.card-title { font-size: 0.9375rem; font-weight: 700; color: var(--color-text-primary); margin: 0; }

	.logo-upload-wrap { display: flex; align-items: center; gap: 16px; }
	.logo-preview { width: 64px; height: 64px; border-radius: var(--radius-md); background: var(--color-accent); color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; }
	.upload-btn-wrap { display: flex; flex-direction: column; gap: 4px; }
	.upload-hint { font-size: 0.6875rem; color: var(--color-text-tertiary); }

	.form-group { display: flex; flex-direction: column; gap: 6px; }
	.form-group label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }
	.form-group textarea { padding: 8px 12px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; resize: vertical; }

	.form-footer { display: flex; justify-content: flex-end; align-items: center; gap: 12px; }
	.save-msg { display: inline-flex; align-items: center; gap: 6px; font-size: 0.8125rem; color: var(--color-success); font-weight: 600; }
</style>
