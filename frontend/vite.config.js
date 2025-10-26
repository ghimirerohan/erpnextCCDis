import path from "node:path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { VitePWA } from "vite-plugin-pwa"
import { defineConfig } from "vite"
// ADDED BY AI: MULTI_PWA - Import fs-extra for file operations
import fs from "fs-extra"

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		frappeui({
			frappeProxy: true,
			jinjaBootData: true,
			lucideIcons: true,
			buildConfig: {
				indexHtmlPath: "../custom_erp/www/jsapp.html",
				emptyOutDir: true,
				sourcemap: true,
			},
		}),
		vue(),
		// ADDED BY AI: MULTI_PWA - Three separate PWA plugin instances for each sub-app
		...['qrpay', 'qrpay-admin', 'scanner'].map((name) =>
			VitePWA({
				registerType: 'prompt',
				manifest: false, // Using separate JSON manifest files
				filename: `sw-${name}.js`,
				strategies: 'generateSW',
				srcDir: 'src',
				workbox: {
					navigateFallback: `/jsapp/${name}/index.html`,
					cleanupOutdatedCaches: true,
					globPatterns: ['**/*.{js,css,html,png,jpg,jpeg,svg,gif,woff,woff2}'],
					maximumFileSizeToCacheInBytes: 10 * 1024 * 1024, // 10 MB
					runtimeCaching: [
						{
							urlPattern: /^\/api\/.*/i,
							handler: 'NetworkFirst',
							options: {
								cacheName: `${name}-api-cache`,
								networkTimeoutSeconds: 10,
								expiration: {
									maxEntries: 200,
									maxAgeSeconds: 86400 // 1 day
								},
								cacheableResponse: {
									statuses: [0, 200]
								}
							}
						},
						{
							urlPattern: /\.(?:png|jpg|jpeg|svg|webp|ico)$/,
							handler: 'CacheFirst',
							options: {
								cacheName: `${name}-img-cache`,
								expiration: {
									maxEntries: 200,
									maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
								}
							}
						},
						{
							urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
							handler: 'CacheFirst',
							options: {
								cacheName: `${name}-google-fonts-cache`,
								expiration: {
									maxEntries: 10,
									maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
								},
								cacheableResponse: {
									statuses: [0, 200]
								}
							}
						},
						{
							urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
							handler: 'CacheFirst',
							options: {
								cacheName: `${name}-gstatic-fonts-cache`,
								expiration: {
									maxEntries: 10,
									maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
								},
								cacheableResponse: {
									statuses: [0, 200]
								}
							}
						}
					]
				},
				devOptions: {
					enabled: true,
					type: 'module'
				}
			})
		),
		// ADDED BY AI: MULTI_PWA - Custom plugin to duplicate build output to sub-app folders
		{
			name: 'pwa-jsapp-dup',
			enforce: 'post',
			closeBundle: async () => {
				// Wait for PWA service workers to be generated
				const waitForFile = async (filePath, maxWait = 5000) => {
					const start = Date.now();
					while (!fs.existsSync(filePath)) {
						if (Date.now() - start > maxWait) return false;
						await new Promise(resolve => setTimeout(resolve, 100));
					}
					return true;
				};
				
				const subapps = ['qrpay', 'qrpay-admin', 'scanner'];
				// frappe-ui plugin overrides outDir to frontend
				const outDir = path.resolve(process.cwd(), '../custom_erp/public/frontend');
				
				if (!fs.existsSync(outDir)) {
					console.warn('⚠️  Output directory not found; skipping duplication');
					return;
				}
				
				console.log('\n📦 Duplicating PWA assets to sub-app folders...\n');
				
				// Create jsapp directory structure within frontend
				const jsappDir = path.join(outDir, 'jsapp');
				await fs.ensureDir(jsappDir);
				
				for (const app of subapps) {
					const appDir = path.join(jsappDir, app);
					await fs.ensureDir(appDir);
					
					// Copy index.html to each sub-app folder
					const indexSrc = path.join(outDir, 'index.html');
					if (fs.existsSync(indexSrc)) {
						await fs.copyFile(indexSrc, path.join(appDir, 'index.html'));
						console.log(`✅ Copied index.html to jsapp/${app}/`);
					}
					
					// Wait for and copy service worker to jsapp root and sub-app folder
					const swSrc = path.join(outDir, `sw-${app}.js`);
					if (await waitForFile(swSrc)) {
						await fs.copyFile(swSrc, path.join(jsappDir, `sw-${app}.js`));
						await fs.copyFile(swSrc, path.join(appDir, `sw-${app}.js`));
						console.log(`✅ Copied sw-${app}.js to jsapp/ and jsapp/${app}/`);
					} else {
						console.warn(`⚠️  Service worker timeout: ${swSrc}`);
					}
					
					// Copy workbox files if they exist
					const workboxFiles = await fs.readdir(outDir);
					for (const file of workboxFiles) {
						if (file.startsWith('workbox-') && file.endsWith('.js')) {
							await fs.copyFile(
								path.join(outDir, file),
								path.join(jsappDir, file)
							);
						}
					}
				}
				
				// Copy manifest files
				for (const app of subapps) {
					const manifestSrc = path.join(outDir, `manifest-${app}.json`);
					if (fs.existsSync(manifestSrc)) {
						await fs.copyFile(manifestSrc, path.join(jsappDir, `manifest-${app}.json`));
					}
					
					// Copy icon directories
					const iconSrc = path.join(outDir, `${app}-icons`);
					if (fs.existsSync(iconSrc)) {
						await fs.copy(iconSrc, path.join(jsappDir, `${app}-icons`));
					}
				}
				
				console.log('\n✨ PWA assets duplicated to frontend/jsapp/ structure!\n');
			}
		},
	],
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: "../custom_erp/public/jsapp",
		emptyOutDir: true,
		target: "es2015",
		sourcemap: true, // Enable source maps for debugging
		minify: false,
		rollupOptions: {
			output: {
				manualChunks: {
					vendor: ['vue', 'vue-router'],
					ui: ['frappe-ui'],
				},
			},
		},
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core"],
	},
	server: {
		// Listen on all interfaces so it's reachable over LAN/Docker
		host: true,
		port: 8080,
		strictPort: true,
		allowedHosts: true,
		// Ensure HMR works from other devices on the network
		hmr: {
			host: "192.168.1.75",
			port: 8080,
			protocol: "ws",
		},
	},
})
