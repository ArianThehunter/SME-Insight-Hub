/**
 * API service — Centralized HTTP client with JWT injection and error handling.
 */

import { browser } from '$app/environment';

const API_BASE = browser
	? (import.meta.env.PUBLIC_API_URL || '/api/v1')
	: '/api/v1';

export interface ApiResponse<T = unknown> {
	success: boolean;
	message?: string;
	data?: T;
	errors?: Record<string, string[]>;
}

export class ApiError extends Error {
	status: number;
	errors?: Record<string, string[]>;

	constructor(message: string, status: number, errors?: Record<string, string[]>) {
		super(message);
		this.name = 'ApiError';
		this.status = status;
		this.errors = errors;
	}
}

function getAccessToken(): string | null {
	if (!browser) return null;
	return localStorage.getItem('sme-access-token');
}

function getRefreshToken(): string | null {
	if (!browser) return null;
	return localStorage.getItem('sme-refresh-token');
}

async function refreshAccessToken(): Promise<string | null> {
	const refreshToken = getRefreshToken();
	if (!refreshToken) return null;

	try {
		const res = await fetch(`${API_BASE}/auth/refresh`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ refresh_token: refreshToken }),
		});

		if (!res.ok) return null;

		const json = await res.json();
		const newToken = json.data?.access_token;
		const newRefresh = json.data?.refresh_token;

		if (newToken && browser) {
			localStorage.setItem('sme-access-token', newToken);
			if (newRefresh) localStorage.setItem('sme-refresh-token', newRefresh);
		}

		return newToken;
	} catch {
		return null;
	}
}

/**
 * Core fetch wrapper with automatic JWT injection and token refresh.
 */
export async function apiFetch<T = unknown>(
	endpoint: string,
	options: RequestInit = {},
): Promise<T> {
	const url = `${API_BASE}${endpoint}`;
	const token = getAccessToken();

	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		...(options.headers as Record<string, string> || {}),
	};

	if (token) {
		headers['Authorization'] = `Bearer ${token}`;
	}

	let res = await fetch(url, { ...options, headers });

	// Auto-refresh on 401
	if (res.status === 401 && token) {
		const newToken = await refreshAccessToken();
		if (newToken) {
			headers['Authorization'] = `Bearer ${newToken}`;
			res = await fetch(url, { ...options, headers });
		}
	}

	if (!res.ok) {
		let errorData: any = {};
		try {
			errorData = await res.json();
		} catch { /* ignore parse error */ }

		throw new ApiError(
			errorData.message || errorData.detail || `Request failed (${res.status})`,
			res.status,
			errorData.errors,
		);
	}

	// Handle 204 No Content
	if (res.status === 204) return undefined as T;

	return res.json();
}

// ── Convenience Methods ──────────────────────────────────────────
export const api = {
	get: <T>(endpoint: string) => apiFetch<T>(endpoint),

	post: <T>(endpoint: string, data?: unknown) =>
		apiFetch<T>(endpoint, {
			method: 'POST',
			body: data ? JSON.stringify(data) : undefined,
		}),

	put: <T>(endpoint: string, data?: unknown) =>
		apiFetch<T>(endpoint, {
			method: 'PUT',
			body: data ? JSON.stringify(data) : undefined,
		}),

	patch: <T>(endpoint: string, data?: unknown) =>
		apiFetch<T>(endpoint, {
			method: 'PATCH',
			body: data ? JSON.stringify(data) : undefined,
		}),

	delete: <T>(endpoint: string) =>
		apiFetch<T>(endpoint, { method: 'DELETE' }),
};
