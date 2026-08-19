<!--
  Settings Profile — User personal profile, security, and password reset.
-->
<script lang="ts">
	import { User, Mail, Phone, Lock, Save, CheckCircle2, Shield } from '@lucide/svelte';
	import { authStore } from '$lib/stores/auth.svelte';

	let fullName = $state(authStore.user?.full_name ?? 'Rafiq Ahmed');
	let fullNameBn = $state(authStore.user?.full_name_bn ?? 'রফিক আহমেদ');
	let email = $state(authStore.user?.email ?? 'admin@acmecorp.com');
	let phone = $state(authStore.user?.phone ?? '+880 1712-345678');
	let role = $state(authStore.user?.role?.display_name ?? 'Organization Owner');
	let saved = $state(false);

	function saveProfile(e: Event) {
		e.preventDefault();
		authStore.updateUser({ full_name: fullName, full_name_bn: fullNameBn, phone });
		saved = true;
		setTimeout(() => (saved = false), 3000);
	}
</script>

<svelte:head><title>User Profile — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Personal Profile & Security</h1>
			<p class="page-subtitle">
				Manage your personal credentials, contact info, and security preferences
			</p>
		</div>
	</header>

	<form onsubmit={saveProfile} class="settings-form">
		<div class="card form-card">
			<div class="profile-header-box">
				<div class="avatar-large">
					{(fullName[0] || 'U').toUpperCase()}
				</div>
				<div>
					<h2 class="profile-name">{fullName}</h2>
					<span class="profile-role"><Shield size={13} /> {role}</span>
				</div>
			</div>

			<div class="form-grid">
				<div class="form-group">
					<label for="prof-name">Full Name (English)</label>
					<input id="prof-name" type="text" bind:value={fullName} required />
				</div>
				<div class="form-group">
					<label for="prof-name-bn">পুরো নাম (বাংলা)</label>
					<input id="prof-name-bn" type="text" bind:value={fullNameBn} />
				</div>
			</div>

			<div class="form-grid">
				<div class="form-group">
					<label for="prof-email">Email Address</label>
					<input id="prof-email" type="email" bind:value={email} disabled />
				</div>
				<div class="form-group">
					<label for="prof-phone">Mobile Phone</label>
					<input id="prof-phone" type="text" bind:value={phone} />
				</div>
			</div>
		</div>

		<div class="card form-card">
			<h2 class="card-title">Change Password</h2>
			<div class="form-grid">
				<div class="form-group">
					<label for="curr-pass">Current Password</label>
					<input id="curr-pass" type="password" placeholder="••••••••" />
				</div>
				<div class="form-group">
					<label for="new-pass">New Password</label>
					<input id="new-pass" type="password" placeholder="••••••••" />
				</div>
			</div>
		</div>

		<div class="form-footer">
			{#if saved}
				<span class="save-msg"><CheckCircle2 size={16} /> Profile updated!</span>
			{/if}
			<button type="submit" class="btn-primary">
				<Save size={16} />
				Save Profile
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
	.card-title {
		font-size: 0.9375rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
	}

	.profile-header-box {
		display: flex;
		align-items: center;
		gap: 16px;
		padding-bottom: 14px;
		border-bottom: 1px solid var(--color-border);
	}
	.avatar-large {
		width: 56px;
		height: 56px;
		border-radius: 50%;
		background: var(--color-accent);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 800;
		font-size: 1.375rem;
	}
	.profile-name {
		font-size: 1.125rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0 0 2px;
	}
	.profile-role {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		display: inline-flex;
		align-items: center;
		gap: 4px;
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
	.form-group input {
		padding: 8px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: 0.8125rem;
	}
	.form-group input:disabled {
		opacity: 0.6;
		cursor: not-allowed;
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
