import frappeUIPreset from 'frappe-ui/tailwind'

export default {
	presets: [frappeUIPreset],
	content: [
		'./field/index.html',
		'./field/src/**/*.{vue,js}',
		'./admin/index.html',
		'./admin/src/**/*.{vue,js}',
		'./shared/**/*.{vue,js}',
		'./node_modules/frappe-ui/src/components/**/*.{vue,js}',
	],
}
