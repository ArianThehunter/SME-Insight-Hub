<!--
  Admin Users — Manage organization team members, roles, and access status.
-->
<script lang="ts">
	import {
		Users,
		Plus,
		Search,
		Mail,
		Shield,
		CheckCircle2,
		XCircle,
		MoreHorizontal
	} from '@lucide/svelte';

	let searchQuery = $state('');

	const users = [
		{
			id: '1',
			name: 'Rafiq Ahmed',
			email: 'admin@acmecorp.com',
			role: 'Organization Owner',
			roleKey: 'org_owner',
			department: 'Executive',
			status: 'Active',
			lastActive: 'Just now'
		},
		{
			id: '2',
			name: 'Nadia Islam',
			email: 'nadia@acmecorp.com',
			role: 'Accountant',
			roleKey: 'accountant',
			department: 'Finance',
			status: 'Active',
			lastActive: '25m ago'
		},
		{
			id: '3',
			name: 'Zubair Hossain',
			email: 'zubair@acmecorp.com',
			role: 'Sales Officer',
			roleKey: 'sales_officer',
			department: 'Sales',
			status: 'Active',
			lastActive: '2h ago'
		},
		{
			id: '4',
			name: 'Sultana Begum',
			email: 'sultana@acmecorp.com',
			role: 'Inventory Officer',
			roleKey: 'inventory_officer',
			department: 'Operations',
			status: 'Active',
			lastActive: '1d ago'
		},
		{
			id: '5',
			name: 'Tareq Rahman',
			email: 'tareq@acmecorp.com',
			role: 'Viewer / Auditor',
			roleKey: 'viewer',
			department: 'Compliance',
			status: 'Invited',
			lastActive: 'Pending'
		}
	];

	const filtered = $derived(
		users.filter(
			(u) =>
				!searchQuery ||
				u.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				u.email.toLowerCase().includes(searchQuery.toLowerCase())
		)
	);
</script>

<svelte:head><title>User Management — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Team & User Management</h1>
			<p class="page-subtitle">
				Control organizational access, assign roles, and manage invitations
			</p>
		</div>
		<div class="header-actions">
			<button class="btn-primary">
				<Plus size={16} />
				Invite Team Member
			</button>
		</div>
	</header>

	<div class="card filter-bar">
		<div class="search-box">
			<Search size={14} />
			<input
				type="text"
				placeholder="Search team members by name or email..."
				bind:value={searchQuery}
				aria-label="Search users"
			/>
		</div>
	</div>

	<div class="card table-card">
		<table class="data-table">
			<thead>
				<tr>
					<th>Team Member</th>
					<th>Assigned Role</th>
					<th>Department</th>
					<th>Status</th>
					<th>Last Active</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				{#each filtered as u}
					<tr>
						<td>
							<div class="user-cell">
								<div class="avatar">{u.name[0]}</div>
								<div>
									<span class="user-name">{u.name}</span>
									<span class="user-email">{u.email}</span>
								</div>
							</div>
						</td>
						<td><span class="role-badge"><Shield size={12} /> {u.role}</span></td>
						<td>{u.department}</td>
						<td>
							<span class="status-pill status-{u.status.toLowerCase()}">{u.status}</span>
						</td>
						<td class="text-muted">{u.lastActive}</td>
						<td>
							<button class="action-btn" title="Edit member permissions">Edit</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
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
	}

	.card {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}
	.filter-bar {
		padding: 12px 16px;
		margin: 20px 0 16px;
	}
	.search-box {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 12px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		color: var(--color-text-tertiary);
		max-width: 400px;
	}
	.search-box input {
		flex: 1;
		background: none;
		border: none;
		outline: none;
		font-size: 0.8125rem;
		color: var(--color-text-primary);
	}

	.table-card {
		overflow: hidden;
	}
	.data-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.8125rem;
	}
	.data-table th {
		text-align: left;
		padding: 10px 18px;
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
		text-transform: uppercase;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-bg-primary);
	}
	.data-table td {
		padding: 12px 18px;
		border-bottom: 1px solid var(--color-border);
		color: var(--color-text-primary);
	}
	.data-table tr:last-child td {
		border-bottom: none;
	}

	.user-cell {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.avatar {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		background: var(--color-accent);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
		font-size: 0.8125rem;
		flex-shrink: 0;
	}
	.user-name {
		font-weight: 600;
		color: var(--color-text-primary);
		display: block;
	}
	.user-email {
		font-size: 0.6875rem;
		color: var(--color-text-tertiary);
	}

	.role-badge {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-size: 0.75rem;
		font-weight: 600;
		background: var(--color-bg-primary);
		padding: 2px 8px;
		border-radius: 4px;
		border: 1px solid var(--color-border);
	}
	.status-pill {
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
	}
	.status-active {
		background: color-mix(in srgb, var(--color-success) 15%, transparent);
		color: var(--color-success);
	}
	.status-invited {
		background: color-mix(in srgb, #f59e0b 15%, transparent);
		color: #d97706;
	}
	.text-muted {
		color: var(--color-text-tertiary);
	}
	.action-btn {
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		padding: 4px 10px;
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		color: var(--color-text-primary);
	}
	.action-btn:hover {
		border-color: var(--color-accent);
		color: var(--color-accent);
	}
</style>
