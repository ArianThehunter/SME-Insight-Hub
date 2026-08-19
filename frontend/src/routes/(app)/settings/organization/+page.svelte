<!--
  Settings Organization — Organization profile, registration info, Trade License & TIN numbers.
-->
<script lang="ts">
	import { Building2, Save, CheckCircle2, MapPin, Phone, Mail, FileText } from '@lucide/svelte';
	import { authStore } from '$lib/stores/auth.svelte';

	let orgName = $state(authStore.user?.organization?.name ?? 'Acme Corporation Ltd.');
	let orgNameBn = $state(authStore.user?.organization?.name_bn ?? 'একমি কর্পোরেশন লিমিটেড');
	let tradeLicense = $state('TRAD/DNCC/024819/2024');
	let tin = $state('4819-2048-1120');
	let bin = $state('002481920-0101');
	let address = $state('House 42, Road 11, Banani, Dhaka-1213');
	let phone = $state('+880 1712-000000');
	let email = $state('info@acmecorp.com.bd');
	let saved = $state(false);

	function saveOrg(e: Event) {
		e.preventDefault();
		saved = true;
		setTimeout(() => saved = false, 3000);
	}
</script>

<svelte:head><title>Organization Settings — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Organization Profile & Compliance</h1>
			<p class="page-subtitle">Manage company identification, statutory trade credentials, and registered office details</p>
		</div>
	</header>

	<form onsubmit={saveOrg} class="settings-form">
		<div class="card form-card">
			<h2 class="card-title">Legal Entity Information</h2>
			<div class="form-grid">
				<div class="form-group">
					<label for="org-name">Company Name (English)</label>
					<input id="org-name" type="text" bind:value={orgName} required />
				</div>
				<div class="form-group">
					<label for="org-name-bn">কোম্পানির নাম (বাংলা)</label>
					<input id="org-name-bn" type="text" bind:value={orgNameBn} />
				</div>
			</div>

			<div class="form-grid three-col">
				<div class="form-group">
					<label for="trade-lic">Trade License Number</label>
					<input id="trade-lic" type="text" bind:value={tradeLicense} />
				</div>
				<div class="form-group">
					<label for="tin-num">e-TIN Number</label>
					<input id="tin-num" type="text" bind:value={tin} />
				</div>
				<div class="form-group">
					<label for="bin-num">BIN (VAT Registration)</label>
					<input id="bin-num" type="text" bind:value={bin} />
				</div>
			</div>
		</div>

		<div class="card form-card">
			<h2 class="card-title">Registered Contact & Office</h2>
			<div class="form-grid">
				<div class="form-group">
					<label for="org-email">Official Email</label>
					<input id="org-email" type="email" bind:value={email} required />
				</div>
				<div class="form-group">
					<label for="org-phone">Contact Phone</label>
					<input id="org-phone" type="text" bind:value={phone} required />
				</div>
			</div>
			<div class="form-group">
				<label for="org-addr">Physical Address</label>
				<input id="org-addr" type="text" bind:value={address} required />
			</div>
		</div>

		<div class="form-footer">
			{#if saved}
				<span class="save-msg"><CheckCircle2 size={16} /> Saved successfully!</span>
			{/if}
			<button type="submit" class="btn-primary">
				<Save size={16} />
				Save Organization Details
			</button>
		</div>
	</form>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 8px 18px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-accent); color: white; border: none; }

	.settings-form { display: flex; flex-direction: column; gap: 16px; margin-top: 20px; max-width: 840px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.form-card { padding: 20px; display: flex; flex-direction: column; gap: 16px; }
	.card-title { font-size: 0.9375rem; font-weight: 700; color: var(--color-text-primary); margin: 0; }

	.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
	.form-grid.three-col { grid-template-columns: repeat(3, 1fr); }
	@media (max-width: 768px) { .form-grid, .form-grid.three-col { grid-template-columns: 1fr; } }

	.form-group { display: flex; flex-direction: column; gap: 6px; }
	.form-group label { font-size: 0.75rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }
	.form-group input { padding: 8px 12px; background: var(--color-bg-primary); border: 1px solid var(--color-border); border-radius: var(--radius-md); color: var(--color-text-primary); font-size: 0.8125rem; }

	.form-footer { display: flex; justify-content: flex-end; align-items: center; gap: 12px; }
	.save-msg { display: inline-flex; align-items: center; gap: 6px; font-size: 0.8125rem; color: var(--color-success); font-weight: 600; }
</style>
