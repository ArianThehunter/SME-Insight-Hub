/**
 * i18n store — Bilingual support for English and Bangla.
 */

import { browser } from '$app/environment';

type Locale = 'en' | 'bn';

const translations: Record<Locale, Record<string, string>> = {
	en: {
		// Navigation
		'nav.dashboard': 'Dashboard',
		'nav.overview': 'Overview',
		'nav.executive_summary': 'Executive Summary',
		'nav.kpi_center': 'KPI Center',
		'nav.sales': 'Sales',
		'nav.sales_analytics': 'Sales Analytics',
		'nav.orders': 'Orders',
		'nav.revenue': 'Revenue',
		'nav.customers': 'Customers',
		'nav.inventory': 'Inventory',
		'nav.products': 'Products',
		'nav.warehouses': 'Warehouses',
		'nav.suppliers': 'Suppliers',
		'nav.stock_alerts': 'Stock Alerts',
		'nav.finance': 'Finance',
		'nav.expenses': 'Expenses',
		'nav.invoices': 'Invoices',
		'nav.cash_flow': 'Cash Flow',
		'nav.profit_loss': 'Profit & Loss',
		'nav.bi': 'Business Intelligence',
		'nav.analytics': 'Analytics',
		'nav.data_explorer': 'Data Explorer',
		'nav.kpi_builder': 'KPI Builder',
		'nav.custom_reports': 'Custom Reports',
		'nav.forecasting': 'Forecasting',
		'nav.documents': 'Documents',
		'nav.upload_pdf': 'Upload PDF',
		'nav.ocr_processing': 'OCR Processing',
		'nav.extraction_queue': 'Extraction Queue',
		'nav.parsed_data': 'Parsed Data',
		'nav.csv_export': 'CSV Export',
		'nav.reports': 'Reports',
		'nav.monthly_reports': 'Monthly Reports',
		'nav.quarterly_reports': 'Quarterly Reports',
		'nav.annual_reports': 'Annual Reports',
		'nav.scheduled_reports': 'Scheduled Reports',
		'nav.crm': 'CRM',
		'nav.leads': 'Leads',
		'nav.segmentation': 'Segmentation',
		'nav.retention': 'Retention',
		'nav.admin': 'Administration',
		'nav.users': 'Users',
		'nav.roles': 'Roles',
		'nav.permissions': 'Permissions',
		'nav.audit_logs': 'Audit Logs',
		'nav.activity_logs': 'Activity Logs',
		'nav.settings': 'Settings',
		'nav.organization': 'Organization',
		'nav.localization': 'Localization',
		'nav.branding': 'Branding',
		'nav.api_keys': 'API Keys',
		'nav.integrations': 'Integrations',

		// Dashboard
		'dashboard.welcome': 'Welcome back',
		'dashboard.overview_subtitle': 'Here\'s what\'s happening with your business today.',
		'dashboard.ai_insights': 'AI Insights',
		'dashboard.activity': 'Recent Activity',
		'dashboard.view_all': 'View All',

		// KPIs
		'kpi.revenue': 'Revenue',
		'kpi.expenses': 'Expenses',
		'kpi.profit': 'Profit',
		'kpi.cash_flow': 'Cash Flow',
		'kpi.customers': 'Customers',
		'kpi.inventory_value': 'Inventory Value',
		'kpi.outstanding_invoices': 'Outstanding Invoices',
		'kpi.growth': 'Growth',
		'kpi.vs_last_period': 'vs last period',

		// Actions
		'action.search': 'Search...',
		'action.notifications': 'Notifications',
		'action.profile': 'Profile',
		'action.logout': 'Logout',
		'action.login': 'Sign In',
		'action.register': 'Create Account',
		'action.save': 'Save',
		'action.cancel': 'Cancel',
		'action.export': 'Export',
		'action.filter': 'Filter',

		// Common
		'common.loading': 'Loading...',
		'common.no_data': 'No data available',
		'common.error': 'Something went wrong',
		'common.retry': 'Retry',
		'common.showing': 'Showing',
		'common.of': 'of',
		'common.results': 'results',
	},
	bn: {
		// Navigation
		'nav.dashboard': 'ড্যাশবোর্ড',
		'nav.overview': 'সারসংক্ষেপ',
		'nav.executive_summary': 'নির্বাহী সারাংশ',
		'nav.kpi_center': 'কেপিআই কেন্দ্র',
		'nav.sales': 'বিক্রয়',
		'nav.sales_analytics': 'বিক্রয় বিশ্লেষণ',
		'nav.orders': 'অর্ডার',
		'nav.revenue': 'রাজস্ব',
		'nav.customers': 'গ্রাহক',
		'nav.inventory': 'মজুদ',
		'nav.products': 'পণ্য',
		'nav.warehouses': 'গুদাম',
		'nav.suppliers': 'সরবরাহকারী',
		'nav.stock_alerts': 'মজুদ সতর্কতা',
		'nav.finance': 'অর্থ',
		'nav.expenses': 'ব্যয়',
		'nav.invoices': 'চালান',
		'nav.cash_flow': 'নগদ প্রবাহ',
		'nav.profit_loss': 'লাভ ও ক্ষতি',
		'nav.bi': 'ব্যবসায়িক বুদ্ধিমত্তা',
		'nav.analytics': 'বিশ্লেষণ',
		'nav.data_explorer': 'ডেটা অনুসন্ধান',
		'nav.kpi_builder': 'কেপিআই নির্মাতা',
		'nav.custom_reports': 'কাস্টম রিপোর্ট',
		'nav.forecasting': 'পূর্বাভাস',
		'nav.documents': 'নথি',
		'nav.upload_pdf': 'পিডিএফ আপলোড',
		'nav.ocr_processing': 'OCR প্রক্রিয়াকরণ',
		'nav.extraction_queue': 'নিষ্কাশন সারি',
		'nav.parsed_data': 'পার্সড ডেটা',
		'nav.csv_export': 'CSV রপ্তানি',
		'nav.reports': 'প্রতিবেদন',
		'nav.monthly_reports': 'মাসিক প্রতিবেদন',
		'nav.quarterly_reports': 'ত্রৈমাসিক প্রতিবেদন',
		'nav.annual_reports': 'বার্ষিক প্রতিবেদন',
		'nav.scheduled_reports': 'নির্ধারিত প্রতিবেদন',
		'nav.crm': 'সিআরএম',
		'nav.leads': 'লিড',
		'nav.segmentation': 'বিভাগীকরণ',
		'nav.retention': 'ধারণ',
		'nav.admin': 'প্রশাসন',
		'nav.users': 'ব্যবহারকারী',
		'nav.roles': 'ভূমিকা',
		'nav.permissions': 'অনুমতি',
		'nav.audit_logs': 'অডিট লগ',
		'nav.activity_logs': 'কার্যকলাপ লগ',
		'nav.settings': 'সেটিংস',
		'nav.organization': 'সংস্থা',
		'nav.localization': 'স্থানীয়করণ',
		'nav.branding': 'ব্র্যান্ডিং',
		'nav.api_keys': 'API কী',
		'nav.integrations': 'ইন্টিগ্রেশন',

		// Dashboard
		'dashboard.welcome': 'আবার স্বাগতম',
		'dashboard.overview_subtitle': 'আজ আপনার ব্যবসায়ের অবস্থা দেখুন।',
		'dashboard.ai_insights': 'AI অন্তর্দৃষ্টি',
		'dashboard.activity': 'সাম্প্রতিক কার্যকলাপ',
		'dashboard.view_all': 'সব দেখুন',

		// KPIs
		'kpi.revenue': 'রাজস্ব',
		'kpi.expenses': 'ব্যয়',
		'kpi.profit': 'মুনাফা',
		'kpi.cash_flow': 'নগদ প্রবাহ',
		'kpi.customers': 'গ্রাহক',
		'kpi.inventory_value': 'মজুদ মূল্য',
		'kpi.outstanding_invoices': 'বকেয়া চালান',
		'kpi.growth': 'প্রবৃদ্ধি',
		'kpi.vs_last_period': 'আগের সময়কালের তুলনায়',

		// Actions
		'action.search': 'অনুসন্ধান...',
		'action.notifications': 'বিজ্ঞপ্তি',
		'action.profile': 'প্রোফাইল',
		'action.logout': 'লগ আউট',
		'action.login': 'সাইন ইন',
		'action.register': 'অ্যাকাউন্ট তৈরি করুন',
		'action.save': 'সংরক্ষণ',
		'action.cancel': 'বাতিল',
		'action.export': 'রপ্তানি',
		'action.filter': 'ফিল্টার',

		// Common
		'common.loading': 'লোড হচ্ছে...',
		'common.no_data': 'কোনো তথ্য নেই',
		'common.error': 'কিছু ভুল হয়েছে',
		'common.retry': 'পুনরায় চেষ্টা',
		'common.showing': 'দেখাচ্ছে',
		'common.of': 'এর মধ্যে',
		'common.results': 'ফলাফল',
	}
};

function createLocaleStore() {
	let locale = $state<Locale>('en');

	if (browser) {
		const saved = localStorage.getItem('sme-locale') as Locale;
		if (saved && (saved === 'en' || saved === 'bn')) {
			locale = saved;
		}
	}

	return {
		get current() { return locale; },
		get isBangla() { return locale === 'bn'; },

		t(key: string): string {
			return translations[locale]?.[key] ?? translations.en[key] ?? key;
		},

		setLocale(l: Locale) {
			locale = l;
			if (browser) localStorage.setItem('sme-locale', l);
		},

		toggle() {
			const next: Locale = locale === 'en' ? 'bn' : 'en';
			locale = next;
			if (browser) localStorage.setItem('sme-locale', next);
		},

		formatNumber(num: number, useBanglaDigits = false): string {
			if (locale === 'bn' || useBanglaDigits) {
				const banglaDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
				const formatted = new Intl.NumberFormat('en-IN').format(num);
				return formatted.replace(/[0-9]/g, (d) => banglaDigits[parseInt(d)]);
			}
			return new Intl.NumberFormat('en-IN').format(num);
		},

		formatCurrency(amount: number, currency = 'BDT'): string {
			const symbol = currency === 'BDT' ? '৳' : currency === 'USD' ? '$' : currency;
			if (locale === 'bn') {
				const banglaDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
				const formatted = new Intl.NumberFormat('en-IN').format(amount);
				const bangla = formatted.replace(/[0-9]/g, (d) => banglaDigits[parseInt(d)]);
				return `${symbol}${bangla}`;
			}
			return `${symbol}${new Intl.NumberFormat('en-IN').format(amount)}`;
		}
	};
}

export const localeStore = createLocaleStore();
