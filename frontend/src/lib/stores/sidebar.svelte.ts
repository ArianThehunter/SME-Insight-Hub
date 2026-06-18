/**
 * Sidebar store — manages sidebar collapse state.
 */

import { browser } from '$app/environment';

function createSidebarStore() {
	let collapsed = $state(false);
	let mobileOpen = $state(false);

	if (browser) {
		const saved = localStorage.getItem('sme-sidebar-collapsed');
		if (saved !== null) collapsed = saved === 'true';
	}

	return {
		get collapsed() { return collapsed; },
		get mobileOpen() { return mobileOpen; },

		toggle() {
			collapsed = !collapsed;
			if (browser) localStorage.setItem('sme-sidebar-collapsed', String(collapsed));
		},

		collapse() {
			collapsed = true;
			if (browser) localStorage.setItem('sme-sidebar-collapsed', 'true');
		},

		expand() {
			collapsed = false;
			if (browser) localStorage.setItem('sme-sidebar-collapsed', 'false');
		},

		toggleMobile() { mobileOpen = !mobileOpen; },
		openMobile() { mobileOpen = true; },
		closeMobile() { mobileOpen = false; },
	};
}

export const sidebarStore = createSidebarStore();
