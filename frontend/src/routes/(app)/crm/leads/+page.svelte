<!--
  CRM Leads — Sales pipeline with deal stages (New, Qualified, Proposal, Negotiation, Won).
-->
<script lang="ts">
	import { UserPlus, Plus, DollarSign, ArrowRight, CheckCircle2, XCircle } from '@lucide/svelte';

	interface Lead {
		id: string;
		company: string;
		contact: string;
		value: string;
		source: string;
		stage: 'New' | 'Qualified' | 'Proposal' | 'Negotiation' | 'Won';
	}

	let leads = $state<Lead[]>([
		{
			id: '1',
			company: 'Pran-RFL Distributor',
			contact: 'Kamrul Hasan',
			value: '৳ 35,00,000',
			source: 'Referral',
			stage: 'Negotiation'
		},
		{
			id: '2',
			company: 'Apex Footwear Dealer',
			contact: 'Saiful Islam',
			value: '৳ 18,50,000',
			source: 'Cold Outreach',
			stage: 'Proposal'
		},
		{
			id: '3',
			company: 'Beximco Pharma Depot',
			contact: 'Dr. Rafiqul Bari',
			value: '৳ 62,00,000',
			source: 'Inbound Web',
			stage: 'Qualified'
		},
		{
			id: '4',
			company: 'Akij Ceramics Outlet',
			contact: 'Moinul Haque',
			value: '৳ 12,00,000',
			source: 'Trade Show',
			stage: 'New'
		},
		{
			id: '5',
			company: 'Square Toiletries Retail',
			contact: 'Nadeem Ahmed',
			value: '৳ 48,00,000',
			source: 'Direct Inbound',
			stage: 'Won'
		}
	]);

	const stages = ['New', 'Qualified', 'Proposal', 'Negotiation', 'Won'] as const;
</script>

<svelte:head><title>Leads Pipeline — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Sales Leads & Deals Pipeline</h1>
			<p class="page-subtitle">Kanban deal flow and lead conversion tracking for sales reps</p>
		</div>
		<div class="header-actions">
			<button class="btn-primary">
				<Plus size={16} />
				Add Deal / Lead
			</button>
		</div>
	</header>

	<div class="pipeline-board">
		{#each stages as stg}
			{@const stageLeads = leads.filter((l) => l.stage === stg)}
			<div class="pipeline-col">
				<div class="col-header">
					<span class="stage-name">{stg}</span>
					<span class="stage-count">{stageLeads.length}</span>
				</div>
				<div class="cards-wrap">
					{#each stageLeads as deal}
						<div class="card deal-card">
							<div class="deal-top">
								<h3 class="deal-company">{deal.company}</h3>
								<span class="deal-val">{deal.value}</span>
							</div>
							<span class="deal-contact">{deal.contact}</span>
							<span class="deal-source">Source: {deal.source}</span>
						</div>
					{/each}
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
	}

	.pipeline-board {
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		gap: 14px;
		margin-top: 20px;
		overflow-x: auto;
		min-height: 480px;
	}
	@media (max-width: 1100px) {
		.pipeline-board {
			grid-template-columns: repeat(5, 260px);
		}
	}

	.pipeline-col {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.col-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-bottom: 8px;
		border-bottom: 1px solid var(--color-border);
	}
	.stage-name {
		font-size: 0.8125rem;
		font-weight: 700;
		color: var(--color-text-primary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}
	.stage-count {
		font-size: 0.6875rem;
		font-weight: 700;
		background: var(--color-bg-primary);
		padding: 2px 8px;
		border-radius: 999px;
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border);
	}

	.cards-wrap {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.deal-card {
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 4px;
		cursor: pointer;
		transition:
			transform 0.15s,
			border-color 0.15s;
	}
	.deal-card:hover {
		transform: translateY(-2px);
		border-color: var(--color-accent);
	}
	.deal-top {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 6px;
	}
	.deal-company {
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--color-text-primary);
		margin: 0;
	}
	.deal-val {
		font-size: 0.75rem;
		font-weight: 700;
		color: var(--color-accent);
		white-space: nowrap;
	}
	.deal-contact {
		font-size: 0.6875rem;
		color: var(--color-text-secondary);
	}
	.deal-source {
		font-size: 0.625rem;
		color: var(--color-text-tertiary);
		margin-top: 4px;
	}
</style>
