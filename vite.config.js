import path from "node:path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { VitePWA } from "vite-plugin-pwa"
import { defineConfig } from "vite"
import fs from "fs-extra"

// Define all apps
const apps = [
	'qrpay',
	'qrpay-admin',
	'scanner',
	'pay-dashboard',
	'uploadsales',
	'uploadreco',
	'dailyrecoentry',
	'dailytrnxs',
	'home',
	'testlogin'
]

// Create HTML input configuration for multi-page build
const buildInput = {}
apps.forEach(appName => {
	// We expect index.html to be in the app root directory: {app}/index.html
	const htmlPath = path.resolve(__dirname, `${appName}/index.html`)
	if (fs.existsSync(htmlPath)) {
		buildInput[appName] = htmlPath
	}
})

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		frappeui({
			frappeProxy: true,
			jinjaBootData: true,
			lucideIcons: true,
			buildConfig: {
				// Provide a template path (won't be used for multi-page builds)
				indexHtmlPath: "custom_erp/www/qrpay.html",
				emptyOutDir: false,
				sourcemap: false,
			},
		}),
		vue(),
		// PWA plugin disabled for memory reasons in dev env
		// ...apps.map((appName) =>
		// 	VitePWA({
		// 		registerType: 'prompt',
		// 		manifest: false,
		// 		filename: `sw-${appName}.js`,
		// 		strategies: 'generateSW',
		// 		srcDir: `${appName}/src`, // Source for service worker logic if any
		// 		workbox: {
		// 			navigateFallback: `/${appName}/index.html`,
		// 			cleanupOutdatedCaches: true,
		// 			globPatterns: ['**/*.{js,css,html,png,jpg,jpeg,svg,gif,woff,woff2}'],
		// 			maximumFileSizeToCacheInBytes: 10 * 1024 * 1024,
		// 			runtimeCaching: [
		// 				{
		// 					urlPattern: /^\/api\/.*/i,
		// 					handler: 'NetworkFirst',
		// 					options: {
		// 						cacheName: `${appName}-api-cache`,
		// 						networkTimeoutSeconds: 10,
		// 						expiration: {
		// 							maxEntries: 200,
		// 							maxAgeSeconds: 86400
		// 						},
		// 						cacheableResponse: {
		// 							statuses: [0, 200]
		// 						}
		// 					}
		// 				},
		// 				{
		// 					urlPattern: /\.(?:png|jpg|jpeg|svg|webp|ico)$/,
		// 					handler: 'CacheFirst',
		// 					options: {
		// 						cacheName: `${appName}-img-cache`,
		// 						expiration: {
		// 							maxEntries: 200,
		// 							maxAgeSeconds: 60 * 60 * 24 * 30
		// 						}
		// 					}
		// 				}
		// 			]
		// 		},
		// 		devOptions: {
		// 			enabled: true,
		// 			type: 'module'
		// 		}
		// 	})
		// ),
		// Custom plugin to handle multi-page routing in dev mode
		{
			name: 'multi-app-dev',
			configureServer(server) {
				server.middlewares.use((req, res, next) => {
					const url = req.url || '/'
					
					// Check if this is a request for one of our app paths
					const pathMatch = url.match(/^\/([^\/\?]+)/)
					if (pathMatch) {
						const appName = pathMatch[1]
						if (apps.includes(appName)) {
							// Handle requests for app root or app HTML
							if (url === `/${appName}`) {
								// Redirect to trailing slash version to ensure relative assets work
								res.writeHead(301, { 'Location': `/${appName}/` })
								res.end()
								return
							} else if (url === `/${appName}/` || url === `/${appName}/index.html`) {
								// Serve the app's HTML file
								req.url = `/${appName}/index.html`
							}
							// Handle requests for app's main.js or other assets
							else if (url.startsWith(`/${appName}/`)) {
								// Check if it's a file request (has extension)
								const urlPath = url.split('?')[0];
								const hasExtension = /\.[a-zA-Z0-9]+$/.test(urlPath);
								
								if (hasExtension) {
									// Rewrite to src/apps path
									// const rest = url.substring(`/${appName}/`.length)
									// req.url = `/src/apps/${appName}/${rest}`
                                    // NO, we are now in root structure.
                                    // If url is /qrpay/src/main.js, it works naturally.
                                    // If url is /qrpay/assets/..., it works naturally.
								} else {
									// Serve index.html for SPA routing
									req.url = `/${appName}/index.html`
								}
							}
						}
					}
					next()
				})
			}
		},
		// Custom plugin to organize build output
		{
			name: 'multi-app-build',
			enforce: 'post',
			closeBundle: async () => {
				const outDir = path.resolve(process.cwd(), 'custom_erp/public/frontend')
				
				if (!fs.existsSync(outDir)) {
					console.warn('⚠️  Output directory not found')
					return
				}
				
				console.log(`\n📦 Organizing build output for ${apps.length} apps...\n`)
				
				// Process each app - build directly to {appname}/ directory
				for (const appName of apps) {
					const appDir = path.join(outDir, appName)
					await fs.ensureDir(appDir)
					
					// Find HTML file - Vite outputs it in {appName}/index.html
					const indexSrc1 = path.join(outDir, `${appName}/index.html`)
					const indexSrc2 = path.join(outDir, `${appName}.html`)
					
					let indexSrc = null
					if (fs.existsSync(indexSrc1)) {
						indexSrc = indexSrc1
					} else if (fs.existsSync(indexSrc2)) {
						indexSrc = indexSrc2
					}
					
					if (indexSrc) {
						const htmlContent = await fs.readFile(indexSrc, 'utf-8')
						// Update asset paths to be relative to the app directory
						let updatedHtml = htmlContent
							.replace(/\/assets\//g, './assets/')
							.replace(/href="\/manifest-/g, 'href="./manifest-') // Handle manifest path
							.replace(/\/assets\/custom_erp\/frontend\/favicon\.png/g, '/assets/custom_erp/frontend/favicon.png')
							.replace(/\/assets\/custom_erp\/frontend\/registerSW\.js/g, '')
							.replace(/id="vite-plugin-pwa:register-sw"/g, '')
						
						// Remove all registerSW script tags and empty script tags
						updatedHtml = updatedHtml.replace(/<script[^>]*registerSW\.js[^>]*><\/script>/g, '')
						updatedHtml = updatedHtml.replace(/<script[^>]*src=""><\/script>/g, '')
						updatedHtml = updatedHtml.replace(/<script\s+src=""><\/script>/g, '')
						
						// Add single service worker registration script before closing head tag
						if (!updatedHtml.includes('sw-' + appName + '.js')) {
							updatedHtml = updatedHtml.replace('</head>', `  <script src="./sw-${appName}.js"></script>\n  </head>`)
						}
						
						await fs.writeFile(path.join(appDir, 'index.html'), updatedHtml)
						console.log(`✅ Moved and updated index.html to ${appName}/index.html`)
					} else {
						console.warn(`⚠️  HTML file not found for ${appName}`)
					}
					
					// Copy service worker
					const swSrc = path.join(outDir, `sw-${appName}.js`)
					if (fs.existsSync(swSrc)) {
						await fs.copyFile(swSrc, path.join(appDir, `sw-${appName}.js`))
						console.log(`✅ Copied sw-${appName}.js`)
					}
					
					// Copy app-specific assets (if any)
					const appAssetsSrc = path.join(outDir, 'assets', `${appName}-*.js`)
					// Assets are shared, so we'll copy the entire assets directory once
				}
				
				// Copy shared assets to each app directory
				const assetsSrc = path.join(outDir, 'assets')
				if (fs.existsSync(assetsSrc)) {
					for (const appName of apps) {
						const appDir = path.join(outDir, appName)
						const assetsDest = path.join(appDir, 'assets')
						await fs.copy(assetsSrc, assetsDest, { overwrite: true })
					}
					console.log(`✅ Copied shared assets to all apps`)
				}
				
				// Copy workbox files to each app directory
				const workboxFiles = await fs.readdir(outDir).catch(() => [])
				for (const file of workboxFiles) {
					if (file.startsWith('workbox-') && file.endsWith('.js')) {
						for (const appName of apps) {
							const appDir = path.join(outDir, appName)
							await fs.copyFile(
								path.join(outDir, file),
								path.join(appDir, file)
							)
						}
					}
				}
				
				// Clean up root artifacts if needed (optional)
                // Remove the {appName} folders from root of outDir if we copied them inside themselves? 
                // Wait, outDir is public/frontend.
                // We are building to public/frontend.
                // Vite builds {appName}/index.html inside public/frontend.
                // We are then processing it in place?
                // The logic says: const appDir = path.join(outDir, appName)
                // If vite output is already in outDir/appName, then we are just updating index.html in place.
                // That seems fine.
				
				console.log(`\n✨ Build output organized for ${apps.length} apps!\n`)
			}
		},
	],
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: "custom_erp/public/frontend",
		emptyOutDir: true,
		target: "es2015",
		sourcemap: false,
		minify: false,
		rollupOptions: {
			input: buildInput,
			output: {
				entryFileNames: (chunkInfo) => {
					// Group assets by app name
					const appName = chunkInfo.name
					return `assets/${appName}-[hash].js`
				},
				chunkFileNames: 'assets/[name]-[hash].js',
				assetFileNames: 'assets/[name]-[hash].[ext]',
				manualChunks: {
					vendor: ['vue', 'vue-router'],
					ui: ['frappe-ui'],
				},
				sourcemapPathTransform: (relativeSourcePath) => {
                    // Adjust sourcemaps
					const normalized = relativeSourcePath.replace(/^.*\/custom_erp\//, '../')
					return normalized.replace(/^\/.*\/custom_erp\//, '../')
				},
			},
		},
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"), // This might be broken if src doesn't exist. We should probably remove this or point it to something safe.
            // Better:
            "@shared": path.resolve(__dirname, "shared"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs"],
	},
	server: {
		host: true,
		port: 8080,
		strictPort: true,
		allowedHosts: true,
		hmr: {
			protocol: "ws",
		},
		proxy: {
			'^/(app|api|assets|files|private)': {
				target: 'http://127.0.0.1:8000',
				ws: true,
				changeOrigin: true
			},
			'^/socket.io': {
				target: 'http://127.0.0.1:9000',
				ws: true,
				changeOrigin: true
			}
		},
	},
})
