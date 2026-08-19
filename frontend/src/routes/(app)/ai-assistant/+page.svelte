<!--
  AI Assistant — Natural language conversational queries over your business records and financial insights.
-->
<script lang="ts">
	import { Sparkles, Send, Bot, User, ArrowRight, Lightbulb, FileText } from '@lucide/svelte';

	interface Message {
		role: 'assistant' | 'user';
		text: string;
		time: string;
	}

	let query = $state('');
	let isTyping = $state(false);

	let messages = $state<Message[]>([
		{
			role: 'assistant',
			text: 'Hello! I am your AI Business Analyst for SME Insight Hub. You can ask me questions about your revenue trends, top customers, inventory reorder risks, or VAT calculations in both English and বাংলা.',
			time: 'Just now'
		}
	]);

	const samplePrompts = [
		'Which customers contributed to 80% of our revenue this month?',
		'What is our projected cash runway for Q3 2026?',
		'Show me all products below reorder level in Chittagong warehouse.',
		'গত মাসে আমাদের মোট লাভ এবং ভ্যাট কত ছিল?'
	];

	function askSample(prompt: string) {
		query = prompt;
		sendMessage();
	}

	async function sendMessage() {
		if (!query.trim()) return;
		const userText = query.trim();
		query = '';

		messages = [...messages, { role: 'user', text: userText, time: 'Just now' }];

		isTyping = true;
		await new Promise((r) => setTimeout(r, 1200));

		let reply: string;
		if (userText.includes('80%') || userText.includes('revenue')) {
			reply =
				'Based on current sales records, 4 key enterprise accounts drive 74.2% of total revenue: Rahman Textiles Ltd. (৳ 24.5L), Bogura Steel Corp. (৳ 1.25 Cr), Sylhet Tea Gardens (৳ 42.5L), and Dhaka Electronics Hub (৳ 18.25L).';
		} else if (userText.includes('লাভ') || userText.includes('ভ্যাট') || userText.includes('VAT')) {
			reply =
				'গত মাসে (জুলাই ২০২৬) আপনার মোট বিক্রয় ছিল ৳ ৩২,৪৫,০০০ এবং নিট মুনাফা ছিল ৳ ১২,৬৫,০০০ (মুনাফার হার ৩৮.৯%)। মোট ১৫% হারে সরকারি ভ্যাট (NBR Mushak 6.3) ধার্য হয়েছে ৳ ৪,৮৬,৭৫০।';
		} else if (userText.includes('reorder') || userText.includes('inventory')) {
			reply =
				'Alert: 2 items are currently below minimum safety stock threshold — Wireless Mouse MX-200 (4 pcs left, reorder at 10) and Rechargeable LED Light (8 pcs left, reorder at 20). Recommended supplier: Gazipur Electronics Hub.';
		} else {
			reply = `Analysis complete for: "${userText}". Total operating margin stands healthy at 38.4%, with liquid cash balance sufficient for 52 days of projected operating outflow.`;
		}

		messages = [...messages, { role: 'assistant', text: reply, time: 'Just now' }];
		isTyping = false;
	}
</script>

<svelte:head><title>AI Assistant — SME Insight Hub</title></svelte:head>

<div class="page animate-fade-in chat-page">
	<header class="page-header">
		<div>
			<h1 class="page-title">
				<Sparkles size={22} class="ai-sparkle" /> AI Business Intelligence Assistant
			</h1>
			<p class="page-subtitle">
				Ask questions about your sales, accounting ledger, inventory alerts, and NBR tax in plain
				English or বাংলা
			</p>
		</div>
	</header>

	<div class="chat-container card">
		<div class="messages-wrap">
			{#each messages as msg}
				<div class="message-row {msg.role}">
					<div class="avatar-box">
						{#if msg.role === 'assistant'}
							<Bot size={16} />
						{:else}
							<User size={16} />
						{/if}
					</div>
					<div class="message-bubble">
						<p class="message-text">{msg.text}</p>
						<span class="message-time">{msg.time}</span>
					</div>
				</div>
			{/each}
			{#if isTyping}
				<div class="message-row assistant">
					<div class="avatar-box"><Bot size={16} /></div>
					<div class="message-bubble typing">
						<span class="dot"></span><span class="dot"></span><span class="dot"></span>
					</div>
				</div>
			{/if}
		</div>

		<!-- Sample prompt chips -->
		<div class="prompt-chips">
			<span class="chips-label"><Lightbulb size={13} /> Try asking:</span>
			{#each samplePrompts as p}
				<button class="chip-btn" onclick={() => askSample(p)}>
					{p}
				</button>
			{/each}
		</div>

		<!-- Input Box -->
		<form
			onsubmit={(e) => {
				e.preventDefault();
				sendMessage();
			}}
			class="input-form"
		>
			<input
				type="text"
				placeholder="Ask any question about your financial data, orders, or stock levels..."
				bind:value={query}
				aria-label="Ask AI Assistant"
			/>
			<button type="submit" class="send-btn" disabled={!query.trim() || isTyping}>
				<Send size={16} />
			</button>
		</form>
	</div>
</div>

<style>
	.page-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
		letter-spacing: -0.02em;
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.ai-sparkle {
		color: var(--color-accent);
	}
	.page-subtitle {
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
		margin: 4px 0 0;
	}

	.chat-container {
		display: flex;
		flex-direction: column;
		height: calc(100vh - 210px);
		min-height: 520px;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		margin-top: 16px;
		overflow: hidden;
	}

	.messages-wrap {
		flex: 1;
		overflow-y: auto;
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	.message-row {
		display: flex;
		gap: 12px;
		max-width: 80%;
	}
	.message-row.user {
		align-self: flex-end;
		flex-direction: row-reverse;
	}
	.message-row.assistant {
		align-self: flex-start;
	}

	.avatar-box {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}
	.message-row.assistant .avatar-box {
		background: color-mix(in srgb, var(--color-accent) 15%, transparent);
		color: var(--color-accent);
	}
	.message-row.user .avatar-box {
		background: var(--color-accent);
		color: white;
	}

	.message-bubble {
		padding: 12px 16px;
		border-radius: var(--radius-lg);
		font-size: 0.8125rem;
		line-height: 1.5;
	}
	.message-row.assistant .message-bubble {
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		color: var(--color-text-primary);
	}
	.message-row.user .message-bubble {
		background: var(--color-accent);
		color: white;
	}
	.message-text {
		margin: 0 0 4px;
	}
	.message-time {
		font-size: 0.625rem;
		opacity: 0.7;
	}

	.message-bubble.typing {
		display: flex;
		gap: 4px;
		padding: 12px 18px;
	}
	.dot {
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background: var(--color-text-tertiary);
		animation: pulse 1s infinite alternate;
	}
	.dot:nth-child(2) {
		animation-delay: 0.2s;
	}
	.dot:nth-child(3) {
		animation-delay: 0.4s;
	}

	.prompt-chips {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 10px 16px;
		border-top: 1px solid var(--color-border);
		background: var(--color-bg-primary);
		overflow-x: auto;
		flex-wrap: nowrap;
	}
	.chips-label {
		font-size: 0.6875rem;
		font-weight: 600;
		color: var(--color-text-tertiary);
		display: flex;
		align-items: center;
		gap: 4px;
		white-space: nowrap;
	}
	.chip-btn {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: 999px;
		padding: 4px 10px;
		font-size: 0.6875rem;
		color: var(--color-text-secondary);
		cursor: pointer;
		white-space: nowrap;
		transition: all 0.15s;
	}
	.chip-btn:hover {
		border-color: var(--color-accent);
		color: var(--color-accent);
	}

	.input-form {
		display: flex;
		gap: 8px;
		padding: 12px 16px;
		border-top: 1px solid var(--color-border);
		background: var(--color-bg-primary);
	}
	.input-form input {
		flex: 1;
		padding: 10px 14px;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		font-size: 0.8125rem;
		color: var(--color-text-primary);
		outline: none;
	}
	.input-form input:focus {
		border-color: var(--color-accent);
	}
	.send-btn {
		width: 40px;
		height: 40px;
		border-radius: var(--radius-md);
		background: var(--color-accent);
		color: white;
		border: none;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: opacity 0.15s;
	}
	.send-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
</style>
