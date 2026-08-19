<!--
  Scheduled Reports — Configure recurring automated report dispatch (email & cloud delivery).
-->
<script lang="ts">
	import { Clock, Plus, Mail, CheckCircle2, Trash2, ToggleLeft, ToggleRight, Calendar } from '@lucide/svelte';

	interface ScheduledItem {
		id: string;
		name: string;
		recipients: string;
		schedule: string;
		format: string;
		active: boolean;
	}

	let schedules = $state<ScheduledItem[]>([
		{ id: '1', name: 'Weekly Executive Briefing', recipients: 'director@acmecorp.com.bd', schedule: 'Every Monday at 9:00 AM', format: 'PDF', active: true },
		{ id: '2', name: 'Monthly VAT Return Digest', recipients: 'accountant@acmecorp.com.bd', schedule: '1st of every month', format: 'Excel (CSV)', active: true },
		{ id: '3', name: 'Daily Cash Movement Alert', recipients: 'finance@acmecorp.com.bd', schedule: 'Daily at 6:00 PM', format: 'Email Summary', active: false },
	]);

	function toggleActive(id: string) {
		schedules = schedules.map(s => s.id === id ? { ...s, active: !s.active } : s);
	}

	function deleteSchedule(id: string) {
		schedules = schedules.filter(s => s.id !== id);
	}
</script>

<svelte:head><title>Scheduled Reports — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in">
	<header class="page-header">
		<div>
			<h1 class="page-title">Scheduled Report Dispatches</h1>
			<p class="page-subtitle">Automate automated email deliveries of your core financial and operational reports</p>
		</div>
		<div class="header-actions">
			<button class="btn-primary">
				<Plus size={16} />
				Schedule New Report
			</button>
		</div>
	</header>

	<div class="schedule-list">
		{#each schedules as item}
			<div class="card schedule-item">
				<div class="sched-icon-wrap">
					<Clock size={20} />
				</div>
				<div class="sched-info">
					<div class="sched-title-row">
						<h3 class="sched-title">{item.name}</h3>
						<span class="sched-format">{item.format}</span>
					</div>
					<p class="sched-recipients"><Mail size={13} /> {item.recipients}</p>
					<span class="sched-timing"><Calendar size={13} /> {item.schedule}</span>
				</div>
				<div class="sched-actions">
					<button class="toggle-btn" onclick={() => toggleActive(item.id)} aria-label="Toggle active status">
						{#if item.active}
							<span class="active-badge"><CheckCircle2 size={13} /> Active</span>
						{:else}
							<span class="inactive-badge">Paused</span>
						{/if}
					</button>
					<button class="btn-icon danger" onclick={() => deleteSchedule(item.id)} aria-label="Delete schedule">
						<Trash2 size={15} />
					</button>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.page-title { font-size: 1.5rem; font-weight: 700; color: var(--color-text-primary); margin: 0; letter-spacing: -0.02em; }
	.page-subtitle { font-size: 0.8125rem; color: var(--color-text-secondary); margin: 4px 0 0; }
	.btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: var(--radius-md); font-size: 0.8125rem; font-weight: 600; cursor: pointer; background: var(--color-accent); color: white; border: none; }

	.schedule-list { display: flex; flex-direction: column; gap: 12px; margin-top: 20px; }
	.card { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
	.schedule-item { padding: 18px; display: flex; align-items: center; gap: 16px; }
	.sched-icon-wrap { width: 42px; height: 42px; border-radius: var(--radius-md); background: color-mix(in srgb, var(--color-accent) 10%, transparent); color: var(--color-accent); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.sched-info { flex: 1; }
	.sched-title-row { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
	.sched-title { font-size: 0.9375rem; font-weight: 600; color: var(--color-text-primary); margin: 0; }
	.sched-format { font-size: 0.6875rem; font-weight: 600; background: var(--color-bg-primary); padding: 1px 6px; border-radius: 4px; border: 1px solid var(--color-border); color: var(--color-text-secondary); }
	.sched-recipients { font-size: 0.75rem; color: var(--color-text-secondary); margin: 0 0 2px; display: flex; align-items: center; gap: 6px; }
	.sched-timing { font-size: 0.75rem; color: var(--color-text-tertiary); display: flex; align-items: center; gap: 6px; }

	.sched-actions { display: flex; align-items: center; gap: 12px; }
	.toggle-btn { background: none; border: none; cursor: pointer; padding: 0; }
	.active-badge { display: inline-flex; align-items: center; gap: 4px; font-size: 0.75rem; font-weight: 600; padding: 4px 10px; border-radius: 999px; background: color-mix(in srgb, var(--color-success) 15%, transparent); color: var(--color-success); }
	.inactive-badge { display: inline-flex; font-size: 0.75rem; font-weight: 600; padding: 4px 10px; border-radius: 999px; background: var(--color-bg-primary); color: var(--color-text-tertiary); border: 1px solid var(--color-border); }
	.btn-icon { background: none; border: none; cursor: pointer; color: var(--color-text-tertiary); padding: 6px; border-radius: var(--radius-sm); }
	.btn-icon.danger:hover { color: var(--color-danger); }
</style>
