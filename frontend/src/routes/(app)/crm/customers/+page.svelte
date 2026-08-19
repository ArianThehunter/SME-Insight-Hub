<!--
  CRM Customers — Customer relationship management view with engagement tiering and direct outreach.
-->
<script lang="ts">
	import { Users, Search, Plus, Mail, Phone, MapPin, Building, Star, Filter } from '@lucide/svelte';

	let searchQuery = $state('');
	let selectedTier = $state('all');

	const customers = [
		{
			id: '1',
			name: 'Rahman Textiles Ltd.',
			contact: 'Mr. Anisur Rahman',
			email: 'anis@rahman.com.bd',
			phone: '+880 1712-345678',
			location: 'Narsingdi, Dhaka',
			tier: 'Enterprise',
			ltv: '৳ 24,50,000',
			status: 'Active'
		},
		{
			id: '2',
			name: 'Dhaka Electronics Hub',
			contact: 'Tanvir Hossain',
			email: 'tanvir@dhaka-elec.com',
			phone: '+880 1812-345678',
			location: 'Elephant Road, Dhaka',
			tier: 'Mid-Market',
			ltv: '৳ 18,25,000',
			status: 'Active'
		},
		{
			id: '3',
			name: 'Chittagong Spice Co.',
			contact: 'Kazi Faruk',
			email: 'faruk@ctgspice.com',
			phone: '+880 1912-345678',
			location: 'Khatunganj, Chittagong',
			tier: 'Small Business',
			ltv: '৳ 6,78,000',
			status: 'Active'
		},
		{
			id: '4',
			name: 'Sylhet Tea Gardens',
			contact: 'Mrs. Nusrat Jahan',
			email: 'nusrat@sylhettea.com',
			phone: '+880 1512-345678',
			location: 'Sreemangal, Sylhet',
			tier: 'Enterprise',
			ltv: '৳ 42,50,000',
			status: 'Active'
		},
		{
			id: '5',
			name: 'Bogura Steel Corp.',
			contact: 'Haji Golam Mostafa',
			email: 'mostafa@bogurasteel.com',
			phone: '+880 1712-998877',
			location: 'Santahar, Bogura',
			tier: 'Enterprise',
			ltv: '৳ 1,25,00,000',
			status: 'Active'
		}
	];

	const filtered = $derived(
		customers.filter((c) => {
			const matchSearch =
				!searchQuery ||
				c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				c.contact.toLowerCase().includes(searchQuery.toLowerCase());
			const matchTier =
				selectedTier === 'all' || c.tier.toLowerCase() === selectedTier.toLowerCase();
			return matchSearch && matchTier;
		})
	);
</script>

<svelte:head><title>CRM Customers — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Customer Relationship Management</h1>
			<p class="page-subtitle">
				Accounts, contacts, deal history, and tier management across Bangladesh
			</p>
		</div>
		<div class="header-actions">
			<a href="/sales/customers" class="btn-primary">
				<Plus size={16} />
				Add New Account
			</a>
		</div>
	</header>

	<div class="card filter-bar">
		<div class="search-box">
			<Search size={14} />
			<input
				type="text"
				placeholder="Search accounts, contacts, or cities..."
				bind:value={searchQuery}
				aria-label="Search accounts"
			/>
		</div>
		<select class="select-input" bind:value={selectedTier} aria-label="Filter by tier">
			<option value="all">All Tiers</option>
			<option value="enterprise">Enterprise</option>
			<option value="mid-market">Mid-Market</option>
			<option value="small business">Small Business</option>
		</select>
	</div>

	<div class="crm-grid">
		{#each filtered as c}
			<div class="card account-card">
				<div class="account-header">
					<div class="avatar-box">
						{c.name[0]}
					</div>
					<div class="header-details">
						<h3 class="account-name">{c.name}</h3>
						<span class="account-contact">{c.contact}</span>
					</div>
					<span class="tier-pill tier-{c.tier.toLowerCase().replace(' ', '-')}">{c.tier}</span>
				</div>

				<div class="account-body">
					<div class="info-row"><Mail size={13} /> <span>{c.email}</span></div>
					<div class="info-row"><Phone size={13} /> <span>{c.phone}</span></div>
					<div class="info-row"><MapPin size={13} /> <span>{c.location}</span></div>
				</div>

				<div class="account-footer">
					<span class="ltv-label">Lifetime Value</span>
					<span class="ltv-val">{c.ltv}</span>
				</div>
			</div>
		{/each}
	</div>
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
		padding: 7px 14px;
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		font-weight: 600;
		cursor: pointer;
		background: var(--color-accent);
		color: white;
		border: none;
		text-decoration: none;
	}

	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.filter-bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		margin: 20px 0 16px;
		gap: 12px;
	}
	.search-box {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-tertiary);
	}
	.search-box input {
		flex: 1;
		background: none;
		border: none;
		outline: none;
		font-size: 0.8125rem;
		color: var(--color-text-primary);
	}
	.select-input {
		padding: 6px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: 0.8125rem;
	}

	.crm-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: 16px;
	}
	.account-card {
		padding: 18px;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.account-header {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.avatar-box {
		width: 38px;
		height: 38px;
		border-radius: 50%;
		background: var(--color-accent);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
		font-size: 0.9375rem;
		flex-shrink: 0;
	}
	.header-details {
		flex: 1;
		min-width: 0;
	}
	.account-name {
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.account-contact {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}
	.tier-pill {
		font-size: 0.625rem;
		font-weight: 700;
		text-transform: uppercase;
		padding: 2px 8px;
		border-radius: 999px;
	}
	.tier-enterprise {
		background: color-mix(in srgb, var(--color-accent) 15%, transparent);
		color: var(--color-accent);
	}
	.tier-mid-market {
		background: color-mix(in srgb, #38bdf8 15%, transparent);
		color: #0ea5e9;
	}
	.tier-small-business {
		background: color-mix(in srgb, #f59e0b 15%, transparent);
		color: #d97706;
	}

	.account-body {
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		background: var(--color-bg-primary);
		padding: 10px;
		border-radius: var(--radius-md);
	}
	.info-row {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.account-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: auto;
		padding-top: 6px;
	}
	.ltv-label {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		text-transform: uppercase;
	}
	.ltv-val {
		font-size: 0.9375rem;
		font-weight: 700;
		color: var(--color-success);
		font-variant-numeric: tabular-nums;
	}
</style>
