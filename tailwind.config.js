import frappeUIPreset from 'frappe-ui/src/tailwind/preset'

export default {
	presets: [frappeUIPreset],
	content: [
		"./index.html",
		"./qrpay/**/*.{vue,js,ts,jsx,tsx,html}",
		"./qrpay-admin/**/*.{vue,js,ts,jsx,tsx,html}",
		"./scanner/**/*.{vue,js,ts,jsx,tsx,html}",
		"./pay-dashboard/**/*.{vue,js,ts,jsx,tsx,html}",
		"./uploadsales/**/*.{vue,js,ts,jsx,tsx,html}",
		"./uploadreco/**/*.{vue,js,ts,jsx,tsx,html}",
		"./dailyrecoentry/**/*.{vue,js,ts,jsx,tsx,html}",
		"./home/**/*.{vue,js,ts,jsx,tsx,html}",
		"./testlogin/**/*.{vue,js,ts,jsx,tsx,html}",
		"./shared/**/*.{vue,js,ts,jsx,tsx}",
		"./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
	],
	theme: {
		extend: {},
	},
	plugins: [],
}
