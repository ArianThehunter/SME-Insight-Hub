<!--
  Login page — Premium glassmorphic login with demo mode support.
-->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth.svelte';
	import { Eye, EyeOff, LogIn, Zap, BarChart3, Shield, Globe } from '@lucide/svelte';

	let email = $state('');
	let password = $state('');
	let showPassword = $state(false);
	let isSubmitting = $state(false);
	let errorMessage = $state('');

	async function handleLogin(e: Event) {
		e.preventDefault();
		if (!email || !password) {
			errorMessage = 'Please enter your email and password.';
			return;
		}

		isSubmitting = true;
		errorMessage = '';

		try {
			// TODO: Replace with real API call when backend DB is connected
			// const response = await api.post('/auth/login', { email, password });
			// authStore.login(response.data.access_token, response.data.refresh_token, response.data.user);

			// For now, demo login with form values
			authStore.loginDemo();
			await goto('/dashboard');
		} catch (err: any) {
			errorMessage = err.message || 'Login failed. Please try again.';
		} finally {
			isSubmitting = false;
		}
	}

	function handleDemoLogin() {
		authStore.loginDemo();
		goto('/dashboard');
	}

	const features = [
		{ icon: BarChart3, label: 'Real-time Analytics', desc: 'Track KPIs and business metrics' },
		{ icon: Shield, label: 'Enterprise Security', desc: 'Role-based access control' },
		{ icon: Globe, label: 'Bilingual Support', desc: 'English & Bangla interface' },
	];
</script>

<svelte:head>
	<title>Sign In — SME Insight Hub</title>
	<meta name="description" content="Sign in to SME Insight Hub to manage your business intelligence, analytics, and operations." />
</svelte:head>

<div class="login-container animate-fade-in">
	<!-- Left: Branding Panel -->
	<div class="branding-panel">
		<div class="brand-content">
			<div class="brand-logo">
				<div class="logo-icon">
					<Zap size={28} />
				</div>
				<span class="logo-text">SME Insight Hub</span>
			</div>
			<h1 class="brand-headline">Intelligent Business<br />Management Platform</h1>
			<p class="brand-sub">AI-powered analytics, document processing, and business intelligence for modern SMEs.</p>

			<div class="feature-list">
				{#each features as feat, i}
					{@const Icon = feat.icon}
					<div class="feature-item stagger-{i + 1} animate-fade-in-up">
						<div class="feature-icon">
							<Icon size={18} />
						</div>
						<div>
							<div class="feature-label">{feat.label}</div>
							<div class="feature-desc">{feat.desc}</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
		<div class="brand-footer">
			<span>© 2026 SME Insight Hub</span>
		</div>
	</div>

	<!-- Right: Login Form -->
	<div class="form-panel">
		<div class="form-wrapper">
			<!-- Mobile logo -->
			<div class="mobile-logo">
				<div class="logo-icon small">
					<Zap size={20} />
				</div>
				<span class="logo-text">SME Insight Hub</span>
			</div>

			<div class="form-header">
				<h2 class="form-title">Welcome back</h2>
				<p class="form-subtitle">Sign in to your account to continue</p>
			</div>

			{#if errorMessage}
				<div class="error-alert animate-scale-in">
					<span>{errorMessage}</span>
				</div>
			{/if}

			<form onsubmit={handleLogin} class="login-form">
				<div class="form-group">
					<label for="login-email" class="form-label">Email address</label>
					<input
						id="login-email"
						type="email"
						bind:value={email}
						placeholder="admin@acmecorp.com"
						class="form-input"
						autocomplete="email"
						required
					/>
				</div>

				<div class="form-group">
					<div class="label-row">
						<label for="login-password" class="form-label">Password</label>
						<a href="/forgot-password" class="forgot-link">Forgot password?</a>
					</div>
					<div class="input-wrapper">
						<input
							id="login-password"
							type={showPassword ? 'text' : 'password'}
							bind:value={password}
							placeholder="Enter your password"
							class="form-input"
							autocomplete="current-password"
							required
						/>
						<button
							type="button"
							class="toggle-password"
							onclick={() => showPassword = !showPassword}
							aria-label={showPassword ? 'Hide password' : 'Show password'}
						>
							{#if showPassword}
								<EyeOff size={16} />
							{:else}
								<Eye size={16} />
							{/if}
						</button>
					</div>
				</div>

				<button
					type="submit"
					class="btn-primary"
					disabled={isSubmitting}
				>
					{#if isSubmitting}
						<span class="spinner"></span>
						Signing in...
					{:else}
						<LogIn size={18} />
						Sign in
					{/if}
				</button>
			</form>

			<div class="divider">
				<span>or continue with</span>
			</div>

			<button class="btn-demo" onclick={handleDemoLogin}>
				<Zap size={18} />
				Sign in with Demo Account
			</button>

			<p class="signup-prompt">
				Don't have an account? <a href="/register" class="signup-link">Create one</a>
			</p>
		</div>
	</div>
</div>

<style>
	.login-container {
		display: flex;
		width: 100%;
		max-width: 960px;
		min-height: 580px;
		border-radius: var(--radius-xl);
		overflow: hidden;
		box-shadow: var(--shadow-xl);
		position: relative;
		z-index: 1;
		border: 1px solid var(--color-border);
	}

	/* ── Branding Panel ─────────────────────────────────────── */
	.branding-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		padding: 40px;
		background: linear-gradient(145deg, #0c1929 0%, #111e33 50%, #0f1a2e 100%);
		position: relative;
		overflow: hidden;
	}

	.branding-panel::before {
		content: '';
		position: absolute;
		inset: 0;
		background:
			radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
			radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
		pointer-events: none;
	}

	.brand-content {
		position: relative;
		z-index: 1;
	}

	.brand-logo {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 40px;
	}

	.logo-icon {
		width: 44px;
		height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: var(--radius-lg);
		background: var(--gradient-accent);
		color: white;
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
	}

	.logo-icon.small {
		width: 36px;
		height: 36px;
	}

	.logo-text {
		font-size: 1.125rem;
		font-weight: 700;
		color: #f1f5f9;
		letter-spacing: -0.02em;
	}

	.brand-headline {
		font-size: 1.75rem;
		font-weight: 800;
		color: white;
		line-height: 1.2;
		letter-spacing: -0.03em;
		margin: 0 0 12px 0;
	}

	.brand-sub {
		font-size: 0.875rem;
		color: #94a3b8;
		line-height: 1.6;
		margin: 0 0 32px 0;
	}

	.feature-list {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.feature-item {
		display: flex;
		align-items: flex-start;
		gap: 12px;
	}

	.feature-icon {
		width: 36px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: var(--radius-md);
		background: rgba(59, 130, 246, 0.1);
		color: #60a5fa;
		flex-shrink: 0;
	}

	.feature-label {
		font-size: 0.8125rem;
		font-weight: 600;
		color: #e2e8f0;
	}

	.feature-desc {
		font-size: 0.75rem;
		color: #64748b;
		margin-top: 2px;
	}

	.brand-footer {
		position: relative;
		z-index: 1;
		font-size: 0.6875rem;
		color: #475569;
	}

	/* ── Form Panel ─────────────────────────────────────────── */
	.form-panel {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 40px;
		background: var(--color-bg-secondary);
	}

	.form-wrapper {
		width: 100%;
		max-width: 360px;
	}

	.mobile-logo {
		display: none;
		align-items: center;
		gap: 10px;
		margin-bottom: 24px;
	}

	.form-header {
		margin-bottom: 28px;
	}

	.form-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0 0 6px 0;
		letter-spacing: -0.02em;
	}

	.form-subtitle {
		font-size: 0.875rem;
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
		margin-bottom: 20px;
	}

	/* ── Form ───────────────────────────────────────────────── */
	.login-form {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.label-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.form-label {
		font-size: 0.8125rem;
		font-weight: 500;
		color: var(--color-text-secondary);
	}

	.forgot-link {
		font-size: 0.75rem;
		color: var(--color-accent);
		text-decoration: none;
		font-weight: 500;
	}

	.forgot-link:hover {
		text-decoration: underline;
	}

	.input-wrapper {
		position: relative;
	}

	.form-input {
		width: 100%;
		padding: 10px 14px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
		background: var(--color-bg-primary);
		color: var(--color-text-primary);
		font-size: 0.875rem;
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

	.toggle-password {
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
		align-items: center;
	}

	.toggle-password:hover {
		color: var(--color-text-secondary);
	}

	.btn-primary {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		width: 100%;
		padding: 11px 20px;
		border-radius: var(--radius-md);
		border: none;
		background: var(--gradient-accent);
		color: white;
		font-size: 0.875rem;
		font-weight: 600;
		font-family: inherit;
		cursor: pointer;
		transition: opacity var(--transition-fast), transform var(--transition-fast), box-shadow var(--transition-fast);
		box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
	}

	.btn-primary:hover:not(:disabled) {
		opacity: 0.92;
		box-shadow: 0 4px 16px rgba(59, 130, 246, 0.35);
		transform: translateY(-1px);
	}

	.btn-primary:active:not(:disabled) {
		transform: translateY(0);
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

	/* ── Divider ────────────────────────────────────────────── */
	.divider {
		display: flex;
		align-items: center;
		gap: 12px;
		margin: 20px 0;
	}

	.divider::before,
	.divider::after {
		content: '';
		flex: 1;
		height: 1px;
		background: var(--color-border);
	}

	.divider span {
		font-size: 0.75rem;
		color: var(--color-text-tertiary);
		white-space: nowrap;
	}

	/* ── Demo Button ───────────────────────────────────────── */
	.btn-demo {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		width: 100%;
		padding: 11px 20px;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
		background: var(--color-bg-tertiary);
		color: var(--color-text-primary);
		font-size: 0.875rem;
		font-weight: 500;
		font-family: inherit;
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.btn-demo:hover {
		background: var(--color-bg-hover);
		border-color: var(--color-accent);
		color: var(--color-accent-light);
		box-shadow: 0 0 0 3px var(--color-accent-muted);
	}

	/* ── Footer ─────────────────────────────────────────────── */
	.signup-prompt {
		text-align: center;
		font-size: 0.8125rem;
		color: var(--color-text-tertiary);
		margin-top: 24px;
	}

	.signup-link {
		color: var(--color-accent);
		text-decoration: none;
		font-weight: 500;
	}

	.signup-link:hover {
		text-decoration: underline;
	}

	/* ── Responsive ──────────────────────────────────────── */
	@media (max-width: 768px) {
		.login-container {
			flex-direction: column;
			max-width: 440px;
			min-height: auto;
		}

		.branding-panel {
			display: none;
		}

		.mobile-logo {
			display: flex;
		}

		.form-panel {
			padding: 28px;
		}
	}
</style>
