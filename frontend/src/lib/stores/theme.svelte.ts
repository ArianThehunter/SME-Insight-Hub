/**
 * Theme store — manages dark/light mode with system preference detection.
 */

import { browser } from '$app/environment';

type Theme = 'dark' | 'light';

function createThemeStore() {
	let theme = $state<Theme>('dark');

	if (browser) {
		const saved = localStorage.getItem('sme-theme') as Theme;
		if (saved) {
			theme = saved;
		} else {
			theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
		}
		applyTheme(theme);
	}

	function applyTheme(t: Theme) {
		if (!browser) return;
		document.documentElement.classList.toggle('dark', t === 'dark');
		document.documentElement.classList.toggle('light', t === 'light');
		localStorage.setItem('sme-theme', t);
	}

	return {
		get current() { return theme; },
		get isDark() { return theme === 'dark'; },

		toggle() {
			theme = theme === 'dark' ? 'light' : 'dark';
			applyTheme(theme);
		},

		set(t: Theme) {
			theme = t;
			applyTheme(theme);
		}
	};
}

export const themeStore = createThemeStore();
