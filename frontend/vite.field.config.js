import path from 'path'
import { fileURLToPath } from 'url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'
import { VitePWA } from 'vite-plugin-pwa'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const appName = 'field-app'
const basePath = `/assets/custom_erp/frontend/${appName}/`
const outDir = path.resolve(__dirname, `../custom_erp/public/frontend/${appName}`)
const indexHtmlPath = path.resolve(__dirname, `../custom_erp/www/${appName}.html`)

export default defineConfig({
	base: basePath,
	plugins: [
		frappeui({
			lucideIcons: true,
			frappeProxy: true,
			jinjaBootData: true,
			buildConfig: {
				outDir,
				baseUrl: basePath,
				indexHtmlPath,
				emptyOutDir: true,
				sourcemap: true,
			},
		}),
		vue(),
		VitePWA({
			registerType: 'autoUpdate',
			manifest: {
				name: 'CC Field App',
				short_name: 'CCField',
				theme_color: '#0F6E56',
				icons: [
					{
						src: '/assets/custom_erp/frontend/icons/dailyrecoentry/icon-192x192.png',
						sizes: '192x192',
						type: 'image/png',
					},
					{
						src: '/assets/custom_erp/frontend/icons/dailyrecoentry/icon-512x512.png',
						sizes: '512x512',
						type: 'image/png',
					},
				],
			},
		}),
	],
	root: path.resolve(__dirname, 'field'),
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'field/src'),
			'@shared': path.resolve(__dirname, 'shared'),
		},
	},
	build: {
		outDir,
		emptyOutDir: true,
		chunkSizeWarningLimit: 1500,
		sourcemap: true,
		rollupOptions: {
			input: path.resolve(__dirname, 'field/index.html'),
		},
	},
})
