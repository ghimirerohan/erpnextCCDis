import path from "node:path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { VitePWA } from "vite-plugin-pwa"
import { defineConfig } from "vite"
// ADDED BY AI: MULTI_PWA - Import fs-extra for file operations
import fs from "fs-extra"

// ADDED BY AI: AUTO-DETECT ROUTES - Function to dynamically extract routes from router.js
function getRoutesFromRouter() {
	const routerPath = path.resolve(process.cwd(), 'src/router.js');
	const routerContent = fs.readFileSync(routerPath, 'utf-8');
	
	// Extract route paths using regex
	const routeMatches = routerContent.match(/path:\s*["']([^"']+)["']/g) || [];
	const routes = routeMatches.map(match => {
		const pathMatch = match.match(/path:\s*["']([^"']+)["']/);
		return pathMatch ? pathMatch[1] : null;
	}).filter(Boolean);
	
	// Filter out routes that shouldn't be PWAs (login, account routes, etc.)
	const excludedRoutes = ['/account/login', '/'];
	const validRoutes = routes
		.filter(route => !excludedRoutes.includes(route))
		.map(route => route.replace(/^\//, '')) // Remove leading slash
		.filter(route => route.length > 0) // Filter out empty routes
		.filter((route, index, self) => self.indexOf(route) === index); // Remove duplicates
	
	return validRoutes;
}

// Get all routes dynamically
const allRoutes = getRoutesFromRouter();
const allPwaRoutes = allRoutes.concat(['home']);

// Log detected routes at config load (for debugging)
console.log(`\n🔍 Auto-detected ${allPwaRoutes.length} PWA routes: ${allPwaRoutes.join(', ')}\n`);

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
		// ADDED BY AI: MULTI_PWA - Dynamic PWA plugin instances for ALL routes detected from router
		...(allPwaRoutes.map((name) => // Auto-generated for all routes + home
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
		)),
		// ADDED BY AI: MULTI_PWA - Custom plugin to duplicate build output to sub-app folders
		{
			name: 'pwa-jsapp-dup',
			enforce: 'post',
			closeBundle: async () => {
				// Wait for PWA service workers to be generated (increased timeout for slower builds)
				const waitForFile = async (filePath, maxWait = 15000) => {
					const start = Date.now();
					while (!fs.existsSync(filePath)) {
						if (Date.now() - start > maxWait) return false;
						await new Promise(resolve => setTimeout(resolve, 200));
					}
					return true;
				};
				
				// AUTO-DETECT: Get all routes dynamically (including home)
				const subapps = getRoutesFromRouter().concat(['home']);
				// frappe-ui plugin overrides outDir to frontend
				const outDir = path.resolve(process.cwd(), '../custom_erp/public/frontend');
				
				if (!fs.existsSync(outDir)) {
					console.warn('⚠️  Output directory not found; skipping duplication');
					return;
				}
				
				console.log(`\n📦 Duplicating PWA assets to sub-app folders for ${subapps.length} routes...\n`);
				console.log(`   Detected routes: ${subapps.join(', ')}\n`);
				
				// Create jsapp directory structure within frontend
				const jsappDir = path.join(outDir, 'jsapp');
				await fs.ensureDir(jsappDir);
				
				// Copy workbox files once (they're shared across all apps)
				const workboxFiles = await fs.readdir(outDir).catch(() => []);
				for (const file of workboxFiles) {
					if (file.startsWith('workbox-') && file.endsWith('.js')) {
						const workboxDest = path.join(jsappDir, file);
						if (!fs.existsSync(workboxDest)) {
							await fs.copyFile(
								path.join(outDir, file),
								workboxDest
							);
						}
					}
				}
				
				// Process each route/app
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
					
					// Copy manifest files if they exist
					const manifestSrc = path.join(outDir, `manifest-${app}.json`);
					if (fs.existsSync(manifestSrc)) {
						await fs.copyFile(manifestSrc, path.join(jsappDir, `manifest-${app}.json`));
						await fs.copyFile(manifestSrc, path.join(appDir, `manifest-${app}.json`));
					}
					
					// Copy icon directories if they exist
					const iconSrc = path.join(outDir, `${app}-icons`);
					if (fs.existsSync(iconSrc) && fs.statSync(iconSrc).isDirectory()) {
						const iconDest = path.join(jsappDir, `${app}-icons`);
						await fs.copy(iconSrc, iconDest, { overwrite: true });
					}
					
					// Copy all assets directory to each app folder (for complete standalone PWAs)
					const assetsSrc = path.join(outDir, 'assets');
					if (fs.existsSync(assetsSrc) && fs.statSync(assetsSrc).isDirectory()) {
						const assetsDest = path.join(appDir, 'assets');
						await fs.copy(assetsSrc, assetsDest, { overwrite: true });
					}
				}
				
				// Copy registerSW.js to jsapp root and all sub-apps
				const registerSWSrc = path.join(outDir, 'registerSW.js');
				if (fs.existsSync(registerSWSrc)) {
					await fs.copyFile(registerSWSrc, path.join(jsappDir, 'registerSW.js'));
					for (const app of subapps) {
						const appDir = path.join(jsappDir, app);
						await fs.copyFile(registerSWSrc, path.join(appDir, 'registerSW.js'));
					}
				}
				
				console.log(`\n✨ PWA assets duplicated to frontend/jsapp/ structure for ${subapps.length} routes!\n`);
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
				// Use relative paths in source maps to avoid hardcoded absolute paths
				// This ensures source maps work on any server regardless of absolute path
				sourcemapPathTransform: (relativeSourcePath) => {
					// Normalize any absolute paths to relative paths
					// Remove any workspace/development or similar prefixes
					const normalized = relativeSourcePath.replace(/^.*\/custom_erp\/frontend\//, '../')
					return normalized.replace(/^\/.*\/custom_erp\/frontend\//, '../')
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
