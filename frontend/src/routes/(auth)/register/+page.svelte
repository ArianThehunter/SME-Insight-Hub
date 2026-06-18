<!--
  Register page — Create new account and organization.
-->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth.svelte';
	import { Eye, EyeOff, UserPlus, Zap, ArrowLeft } from '@lucide/svelte';

	let fullName = $state('');
	let email = $state('');
	let orgName = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let showPassword = $state(false);
	let isSubmitting = $state(false);
	let errorMessage = $state('');

	async function handleRegister(e: Event) {
		e.preventDefault();
		if (password !== confirmPassword) {
			errorMessage = 'Passwords do not match.';
			return;
		}
		if (password.length < 8) {
			errorMessage = 'Password must be at least 8 characters.';
			return;
		}

		isSubmitting = true;
		errorMessage = '';

		try {
			// TODO: Replace with real API call
			authStore.loginDemo();
			await goto('/dashboard');
		} catch (err: any) {
			errorMessage = err.message || 'Registration failed.';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<svelte:head>
	<title>Create Account — SME Insight Hub</title>
	<meta name="description" content="Create your SME Insight Hub account and start managing your business with AI-powered intelligence." />
</svelte:head>

<div class="register-card animate-fade-in-up">
	<div class="card-inner">
		<a href="/login" class="back-link">
			<ArrowLeft size={16} />
			Back to login
		</a>

		<div class="brand-logo">
			<div class="logo-icon">
				<Zap size={20} />
			</div>
			<span class="logo-text">SME Insight Hub</span>
		</div>

		<div class="form-header">
			<h1 class="form-title">Create your account</h1>
			<p class="form-subtitle">Start your free trial — no credit card required</p>
		</div>

		{#if errorMessage}
			<div class="error-alert animate-scale-in">{errorMessage}</div>
		{/if}

		<form onsubmit={handleRegister} class="register-form">
			<div class="form-row">
				<div class="form-group">
					<label for="reg-name" class="form-label">Full Name</label>
					<input
						id="reg-name"
						type="text"
						bind:value={fullName}
						placeholder="Rafiq Ahmed"
						class="form-input"
						required
					/>
				</div>
				<div class="form-group">
					<label for="reg-org" class="form-label">Organization Name</label>
					<input
						id="reg-org"
						type="text"
						bind:value={orgName}
						placeholder="Acme Corporation"
						class="form-input"
						required
					/>
				</div>
			</div>

			<div class="form-group">
				<label for="reg-email" class="form-label">Email address</label>
				<input
					id="reg-email"
					type="email"
					bind:value={email}
					placeholder="you@company.com"
					class="form-input"
					autocomplete="email"
					required
				/>
			</div>

			<div class="form-row">
				<div class="form-group">
					<label for="reg-password" class="form-label">Password</label>
					<div class="input-wrapper">
						<input
							id="reg-password"
							type={showPassword ? 'text' : 'password'}
							bind:value={password}
							placeholder="Min 8 characters"
							class="form-input"
							autocomplete="new-password"
							required
						/>
						<button type="button" class="toggle-pwd" onclick={() => showPassword = !showPassword}>
							{#if showPassword}<EyeOff size={15} />{:else}<Eye size={15} />{/if}
						</button>
					</div>
				</div>
				<div class="form-group">
					<label for="reg-confirm" class="form-label">Confirm Password</label>
					<input
						id="reg-confirm"
						type="password"
						bind:value={confirmPassword}
						placeholder="Repeat password"
						class="form-input"
						autocomplete="new-password"
						required
					/>
				</div>
			</div>

			<button type="submit" class="btn-primary" disabled={isSubmitting}>
				{#if isSubmitting}
					<span class="spinner"></span>Creating account...
				{:else}
					<UserPlus size={18} /> Create Account
				{/if}
			</button>
		</form>

		<p class="terms">
			By creating an account, you agree to our
			<a href="/terms">Terms of Service</a> and
			<a href="/privacy">Privacy Policy</a>.
		</p>
	</div>
</div>

<style>
	.register-card {
		width: 100%;
		max-width: 520px;
		border-radius: var(--radius-xl);
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		box-shadow: var(--shadow-xl);
		position: relative;
		z-index: 1;
	}

	.card-inner {
		padding: 36px 40px;
	}

	.back-link {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		font-size: 0.8125rem;
		color: var(--color-text-tertiary);
		text-decoration: none;
		margin-bottom: 20px;
		transition: color var(--transition-fast);
	}

	.back-link:hover {
		color: var(--color-accent);
	}

	.brand-logo {
		display: flex;
		align-items: center;
		gap: 10px;
		margin-bottom: 24px;
	}

	.logo-icon {
		width: 36px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: var(--radius-md);
		background: var(--gradient-accent);
		color: white;
	}

	.logo-text {
		font-size: 1rem;
		font-weight: 700;
		color: var(--color-text-primary);
	}

	.form-header {
		margin-bottom: 24px;
	}

	.form-title {
		font-size: 1.375rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0 0 4px 0;
		letter-spacing: -0.02em;
	}

	.form-subtitle {
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
		margin: 0;
	}

	.error-alert {
		padding: 10px 14px;
		background: var(--color-danger-muted);
		border: 1px solid rgba(239, 68, 68, 0.2);
		border-radius: var(--radius-md);
		color: var(--color-danger-light);
		font-size: 0.8125rem;
		margin-bottom: 16px;
	}

	.register-form {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 12px;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}

	.form-label {
		font-size: 0.8125rem;
		font-weight: 500;
		color: var(--color-text-secondary);
	}

	.input-wrapper {
		position: relative;
	}

	.form-input {
		width: 100%;
		padding: 9px 12px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
		background: var(--color-bg-primary);
		color: var(--color-text-primary);
		font-size: 0.8125rem;
		font-family: inherit;
		transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
		outline: none;
	}

	.form-input::placeholder {
		color: var(--color-text-muted);
	}

	.form-input:focus {
		border-color: var(--color-accent);
		box-shadow: 0 0 0 3px var(--color-accent-muted);
	}

	.toggle-pwd {
		position: absolute;
		right: 10px;
		top: 50%;
		transform: translateY(-50%);
		background: none;
		border: none;
		color: var(--color-text-tertiary);
		cursor: pointer;
		padding: 4px;
		display: flex;
	}

	.btn-primary {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		width: 100%;
		padding: 11px 20px;
		margin-top: 4px;
		border-radius: var(--radius-md);
		border: none;
		background: var(--gradient-accent);
		color: white;
		font-size: 0.875rem;
		font-weight: 600;
		font-family: inherit;
		cursor: pointer;
		transition: opacity var(--transition-fast), transform var(--transition-fast);
		box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
	}

	.btn-primary:hover:not(:disabled) {
		opacity: 0.92;
		transform: translateY(-1px);
	}

	.btn-primary:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.spinner {
		width: 16px;
		height: 16px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top-color: white;
		border-radius: 50%;
		animation: spin 0.6s linear infinite;
	}

	.terms {
		text-align: center;
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		margin: 20px 0 0 0;
		line-height: 1.5;
	}

	.terms a {
		color: var(--color-accent);
		text-decoration: none;
	}

	.terms a:hover {
		text-decoration: underline;
	}

	@media (max-width: 560px) {
		.card-inner {
			padding: 28px 24px;
		}
		.form-row {
			grid-template-columns: 1fr;
		}
	}
</style>
