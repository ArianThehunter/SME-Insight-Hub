/**
 * Authentication store — manages JWT tokens and current user state.
 */

import { browser } from '$app/environment';
import { goto } from '$app/navigation';

export interface UserProfile {
	id: string;
	email: string;
	full_name: string;
	full_name_bn?: string;
	avatar_url?: string;
	phone?: string;
	is_active: boolean;
	role: {
		name: string;
		display_name: string;
	};
	organization: {
		id: string;
		name: string;
		name_bn?: string;
		slug: string;
		logo_url?: string;
		currency: string;
	};
}

function createAuthStore() {
	let user = $state<UserProfile | null>(null);
	let accessToken = $state<string | null>(null);
	let isLoading = $state(true);

	if (browser) {
		const savedToken = localStorage.getItem('sme-access-token');
		const savedUser = localStorage.getItem('sme-user');
		if (savedToken && savedUser) {
			accessToken = savedToken;
			try {
				user = JSON.parse(savedUser);
			} catch {
				user = null;
			}
		}
		isLoading = false;
	}

	return {
		get user() { return user; },
		get accessToken() { return accessToken; },
		get isAuthenticated() { return !!accessToken && !!user; },
		get isLoading() { return isLoading; },
		get orgId() { return user?.organization?.id; },
		get role() { return user?.role?.name ?? 'viewer'; },

		login(token: string, refreshToken: string, profile: UserProfile) {
			accessToken = token;
			user = profile;
			if (browser) {
				localStorage.setItem('sme-access-token', token);
				localStorage.setItem('sme-refresh-token', refreshToken);
				localStorage.setItem('sme-user', JSON.stringify(profile));
			}
		},

		logout() {
			accessToken = null;
			user = null;
			if (browser) {
				localStorage.removeItem('sme-access-token');
				localStorage.removeItem('sme-refresh-token');
				localStorage.removeItem('sme-user');
				goto('/login');
			}
		},

		updateUser(updates: Partial<UserProfile>) {
			if (user) {
				user = { ...user, ...updates };
				if (browser) {
					localStorage.setItem('sme-user', JSON.stringify(user));
				}
			}
		},

		setLoading(loading: boolean) {
			isLoading = loading;
		}
	};
}

export const authStore = createAuthStore();
