/**
 * Authentication store — manages JWT tokens, current user state, and demo mode.
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

/** Demo user profile used when no real backend is available. */
const DEMO_USER: UserProfile = {
	id: 'demo-user-001',
	email: 'admin@acmecorp.com',
	full_name: 'Rafiq Ahmed',
	full_name_bn: 'রফিক আহমেদ',
	phone: '+880 1712-345678',
	is_active: true,
	role: {
		name: 'org_owner',
		display_name: 'Organization Owner',
	},
	organization: {
		id: 'demo-org-001',
		name: 'Acme Corporation Ltd.',
		name_bn: 'একমি কর্পোরেশন লিমিটেড',
		slug: 'acme-corp',
		currency: 'BDT',
	},
};

function createAuthStore() {
	let user = $state<UserProfile | null>(null);
	let accessToken = $state<string | null>(null);
	let isLoading = $state(true);
	let isDemo = $state(false);

	if (browser) {
		const savedToken = localStorage.getItem('sme-access-token');
		const savedUser = localStorage.getItem('sme-user');
		const savedDemo = localStorage.getItem('sme-demo-mode');
		if (savedToken && savedUser) {
			accessToken = savedToken;
			isDemo = savedDemo === 'true';
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
		get isDemo() { return isDemo; },
		get orgId() { return user?.organization?.id; },
		get role() { return user?.role?.name ?? 'viewer'; },

		login(token: string, refreshToken: string, profile: UserProfile) {
			accessToken = token;
			user = profile;
			isDemo = false;
			if (browser) {
				localStorage.setItem('sme-access-token', token);
				localStorage.setItem('sme-refresh-token', refreshToken);
				localStorage.setItem('sme-user', JSON.stringify(profile));
				localStorage.removeItem('sme-demo-mode');
			}
		},

		/** Demo login — no backend required. Creates mock session. */
		loginDemo() {
			const demoToken = 'demo-jwt-token-' + Date.now();
			accessToken = demoToken;
			user = DEMO_USER;
			isDemo = true;
			if (browser) {
				localStorage.setItem('sme-access-token', demoToken);
				localStorage.setItem('sme-refresh-token', 'demo-refresh');
				localStorage.setItem('sme-user', JSON.stringify(DEMO_USER));
				localStorage.setItem('sme-demo-mode', 'true');
			}
		},

		logout() {
			accessToken = null;
			user = null;
			isDemo = false;
			if (browser) {
				localStorage.removeItem('sme-access-token');
				localStorage.removeItem('sme-refresh-token');
				localStorage.removeItem('sme-user');
				localStorage.removeItem('sme-demo-mode');
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
