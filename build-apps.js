import { exec } from 'child_process';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import { promisify } from 'util';

const execAsync = promisify(exec);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const allApps = [
	'qrpay',
	'qrpay-horlicks',
	'qrpay-admin',
	'scanner',
	'pay-dashboard',
	'uploadsales',
	'uploadreco',
	'dailyrecoentry',
	'dailytrnxs',
	'home',
	'testlogin',
	'ai-assistant',
	'emp-attendance'
];

/** Set BUILD_APP=dailyrecoentry (or any app id) to build only that SPA + skip CCDis. */
const buildOne = process.env.BUILD_APP?.replace(/[^a-z0-9-]/gi, '') || '';
let apps = allApps;
if (buildOne) {
	if (!allApps.includes(buildOne)) {
		console.error(
			`Unknown BUILD_APP "${process.env.BUILD_APP}". Valid: ${allApps.join(', ')}`
		);
		process.exit(1);
	}
	apps = [buildOne];
}

// App-specific theme colors
const appThemes = {
	'qrpay': { theme: '#10b981', bg: '#ffffff', name: 'QRPay', desc: 'Dynamic Fonepay QR Code Generator' },
	'qrpay-horlicks': { theme: '#f97316', bg: '#ffffff', name: 'QRPay Horlicks', desc: 'Horlicks Fonepay QR Code Generator' },
	'qrpay-admin': { theme: '#7c3aed', bg: '#ffffff', name: 'QRPay Admin', desc: 'QRPay Administration Dashboard' },
	'scanner': { theme: '#f59e0b', bg: '#ffffff', name: 'Scanner', desc: 'Invoice and Document Scanner' },
	'pay-dashboard': { theme: '#2563eb', bg: '#ffffff', name: 'Pay Dashboard', desc: 'Payment Statistics Dashboard' },
	'uploadsales': { theme: '#059669', bg: '#ffffff', name: 'Upload Sales', desc: 'Upload and Process Sales Data' },
	'uploadreco': { theme: '#dc2626', bg: '#ffffff', name: 'Upload Reco', desc: 'Upload Reconciliation Data' },
	'dailyrecoentry': { theme: '#0891b2', bg: '#ffffff', name: 'Daily Reco', desc: 'Daily Reconciliation Entry' },
	'dailytrnxs': { theme: '#7c3aed', bg: '#ffffff', name: 'Daily Transactions', desc: 'Daily Payment Reconciliation Dashboard' },
	'home': { theme: '#6366f1', bg: '#ffffff', name: 'Home', desc: 'Application Home' },
	'testlogin': { theme: '#64748b', bg: '#ffffff', name: 'Test Login', desc: 'Login Test App' },
	'ai-assistant': { theme: '#7c3aed', bg: '#1e293b', name: 'Bidhi', desc: 'AI Voice ERP Assistant' },
	'emp-attendance': { theme: '#059669', bg: '#ffffff', name: 'Employee Attendance', desc: 'Employee Attendance Tracking and Management' }
};

const publicFrontendDir = path.resolve(__dirname, 'custom_erp/public/frontend');
const wwwDir = path.resolve(__dirname, 'custom_erp/www');
const publicDir = path.resolve(__dirname, 'public');

console.log('🚀 Building all apps individually...\n');

if (buildOne) {
    const oneOut = path.join(publicFrontendDir, buildOne);
    await fs.emptyDir(oneOut);
} else {
    await fs.emptyDir(publicFrontendDir);
}

// Copy shared assets first (icons, favicon, etc.)
const iconsDir = path.join(publicDir, 'icons');
const destIconsDir = path.join(publicFrontendDir, 'icons');
if (fs.existsSync(iconsDir)) {
    await fs.copy(iconsDir, destIconsDir);
    console.log('✅ Copied icons directory');
}

// Copy favicon
const faviconSrc = path.join(publicDir, 'favicon.png');
if (fs.existsSync(faviconSrc)) {
    await fs.copy(faviconSrc, path.join(publicFrontendDir, 'favicon.png'));
    console.log('✅ Copied favicon.png');
}

// Copy apple-touch-icon
const appleTouchSrc = path.join(publicDir, 'apple-touch-icon.png');
if (fs.existsSync(appleTouchSrc)) {
    await fs.copy(appleTouchSrc, path.join(publicFrontendDir, 'apple-touch-icon.png'));
    console.log('✅ Copied apple-touch-icon.png');
}

// Generate 192x192 icons from 512x512 for each app using sharp
async function generateIcons(appName) {
    const srcIcon = path.join(publicDir, 'icons', appName, 'icon-512x512.png');
    const destDir = path.join(destIconsDir, appName);
    
    if (!fs.existsSync(srcIcon)) {
        console.log(`   ⚠️ No icon found for ${appName}, using default`);
        return false;
    }
    
    await fs.ensureDir(destDir);
    
    // Copy 512x512
    await fs.copy(srcIcon, path.join(destDir, 'icon-512x512.png'));
    
    // Generate 192x192 using sharp
    try {
        const sharp = (await import('sharp')).default;
        await sharp(srcIcon)
            .resize(192, 192)
            .toFile(path.join(destDir, 'icon-192x192.png'));
        console.log(`   ✅ Generated 192x192 icon for ${appName}`);
        
        // Also generate 144x144 for older Android
        await sharp(srcIcon)
            .resize(144, 144)
            .toFile(path.join(destDir, 'icon-144x144.png'));
            
        return true;
    } catch (err) {
        console.log(`   ⚠️ Could not resize icon for ${appName}: ${err.message}`);
        // Fallback: just copy the 512 as 192 (not ideal but works)
        await fs.copy(srcIcon, path.join(destDir, 'icon-192x192.png'));
        return true;
    }
}

// Build each app with its own base path
for (const appName of apps) {
    console.log(`\n📦 Building ${appName}...`);
    
    const basePath = `/assets/custom_erp/frontend/${appName}/`;
    const theme = appThemes[appName] || appThemes['home'];
    
    try {
        // Generate icons first
        await generateIcons(appName);
        
        // Run vite build using single-app config
        const buildCmd = `npx vite build --config vite-single-app.config.js`;
        
        const { stdout, stderr } = await execAsync(buildCmd, { 
            env: {
                ...process.env,
                VITE_APP_NAME: appName,
                VITE_BASE_PATH: basePath
            }
        });
        
        if (stdout) console.log(stdout);
        if (stderr) console.error(stderr);
        
        console.log(`✅ Built ${appName}`);
        
        // Post-build: Update www HTML file
        const nestedIndexPath = path.join(publicFrontendDir, appName, appName, 'index.html');
        const indexHtmlPath = path.join(publicFrontendDir, appName, 'index.html');
        const wwwHtmlPath = path.join(wwwDir, `${appName}.html`);
        
        // Move index.html from nested location to correct location
        if (fs.existsSync(nestedIndexPath)) {
            await fs.move(nestedIndexPath, indexHtmlPath, { overwrite: true });
            await fs.remove(path.join(publicFrontendDir, appName, appName));
        }
        
        if (fs.existsSync(indexHtmlPath)) {
            let content = await fs.readFile(indexHtmlPath, 'utf-8');
            
            // Generate Android Chrome compatible manifest
            const manifest = {
                "id": `/${appName}/`,
                "name": theme.name,
                "short_name": theme.name.replace(/\s+/g, ''),
                "description": theme.desc,
                "start_url": `/${appName}/`,
                "scope": `/${appName}/`,
                "display": "standalone",
                "orientation": "portrait-primary",
                "background_color": theme.bg,
                "theme_color": theme.theme,
                "icons": [
                    {
                        "src": `/assets/custom_erp/frontend/icons/${appName}/icon-144x144.png`,
                        "sizes": "144x144",
                        "type": "image/png",
                        "purpose": "any"
                    },
                    {
                        "src": `/assets/custom_erp/frontend/icons/${appName}/icon-192x192.png`,
                        "sizes": "192x192",
                        "type": "image/png",
                        "purpose": "any"
                    },
                    {
                        "src": `/assets/custom_erp/frontend/icons/${appName}/icon-512x512.png`,
                        "sizes": "512x512",
                        "type": "image/png",
                        "purpose": "any"
                    },
                    {
                        "src": `/assets/custom_erp/frontend/icons/${appName}/icon-192x192.png`,
                        "sizes": "192x192",
                        "type": "image/png",
                        "purpose": "maskable"
                    },
                    {
                        "src": `/assets/custom_erp/frontend/icons/${appName}/icon-512x512.png`,
                        "sizes": "512x512",
                        "type": "image/png",
                        "purpose": "maskable"
                    }
                ],
                "lang": "en",
                "dir": "ltr",
                "display_override": ["standalone", "minimal-ui", "browser"],
                "categories": ["business", "finance"],
                "prefer_related_applications": false
            };
            
            const manifestPath = path.join(publicFrontendDir, appName, `manifest.json`);
            await fs.writeJson(manifestPath, manifest, { spaces: 2 });
            console.log(`   ✅ Created manifest.json for ${appName}`);
            
            // In-scope manifest (required for Chrome/Safari install). Do not use /api/method.
            const manifestUrl = `/${appName}/manifest.json`;
            const appleIcon = `/assets/custom_erp/frontend/icons/${appName}/icon-192x192.png`;
            content = content.replace(
                /<link[^>]*rel="manifest"[^>]*>/gi,
                `<link rel="manifest" href="${manifestUrl}" />`
            );
            if (!content.includes('rel="manifest"')) {
                content = content.replace(
                    '</head>',
                    `    <link rel="manifest" href="${manifestUrl}" />\n  </head>`
                );
            }
            if (!content.includes('rel="apple-touch-icon"')) {
                content = content.replace(
                    '</head>',
                    `    <link rel="apple-touch-icon" href="${appleIcon}" />\n    <meta name="apple-mobile-web-app-title" content="${theme.name}" />\n    <meta name="apple-mobile-web-app-status-bar-style" content="default" />\n  </head>`
                );
            }
            
            // Create service worker that will be served from the app's root
            // This is critical for Android Chrome - SW must be at or above the scope
            const dailyRecoPrecache =
                appName === 'dailyrecoentry'
                    ? `,\n    '/assets/custom_erp/images/fonepay-static-qr.png'`
                    : '';
            const swCacheSuffix = appName === 'dailyrecoentry' ? 'v3' : 'v2';
            const swContent = `// Service Worker for ${appName} - Android Chrome PWA Compatible
// Version: ${Date.now()}
const CACHE_NAME = '${appName}-cache-${swCacheSuffix}';
const APP_SCOPE = '/${appName}/';

// Assets to precache
const PRECACHE_ASSETS = [
    '/${appName}/',
    '/${appName}/manifest.json',
    '/${appName}/sw.js'${dailyRecoPrecache}
];

// Install event - precache critical assets
self.addEventListener('install', (event) => {
    console.log('[SW ${appName}] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[SW ${appName}] Precaching assets');
                return cache.addAll(PRECACHE_ASSETS).catch(err => {
                    console.warn('[SW ${appName}] Precache failed:', err);
                });
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean old caches and claim clients
self.addEventListener('activate', (event) => {
    console.log('[SW ${appName}] Activating...');
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames
                        .filter(name => name.startsWith('${appName}-') && name !== CACHE_NAME)
                        .map(name => {
                            console.log('[SW ${appName}] Deleting old cache:', name);
                            return caches.delete(name);
                        })
                );
            })
            .then(() => {
                console.log('[SW ${appName}] Claiming clients');
                return self.clients.claim();
            })
    );
});

// Fetch event - network first strategy
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    // Only handle same-origin requests
    if (url.origin !== self.location.origin) {
        return;
    }
    
    // Skip non-GET requests
    if (event.request.method !== 'GET') {
        return;
    }
    
    // Network first, fallback to cache
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Clone and cache successful responses
                if (response.ok) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            })
            .catch(() => {
                return caches.match(event.request);
            })
    );
});

// Handle messages from clients
self.addEventListener('message', (event) => {
    if (event.data === 'skipWaiting') {
        self.skipWaiting();
    }
});
`;
            
            // Save service worker in the app's frontend directory
            const swPath = path.join(publicFrontendDir, appName, 'sw.js');
            await fs.writeFile(swPath, swContent);
            console.log(`   ✅ Created sw.js for ${appName}`);
            
            // Write updated HTML to www directory
            await fs.writeFile(wwwHtmlPath, content);
            console.log(`   ✅ Created ${appName}.html in www/`);
        }
        
    } catch (error) {
        console.error(`❌ Failed to build ${appName}:`, error.message);
        process.exit(1);
    }
}

// CCDis v2 — field-app & admin-app (frappe-ui + Vite in /frontend)
if (!buildOne) {
	console.log('\n📦 Building CCDis field-app & admin-app...\n');
	try {
		const { execSync } = await import('child_process');
		execSync('yarn install && yarn build', {
			cwd: path.join(__dirname, 'frontend'),
			stdio: 'inherit',
			env: { ...process.env, NODE_ENV: 'production' },
		});
		console.log('✅ CCDis SPAs built and www/*.html synced\n');
	} catch (err) {
		console.error('❌ CCDis SPA build failed:', err.message);
		process.exit(1);
	}
} else {
	console.log(`\n⏭️  Skipping CCDis build (BUILD_APP=${buildOne} single-app mode)\n`);
}

console.log('\n✨ All apps built successfully!\n');
console.log('📱 PWA Notes:');
console.log('   - Manifest: /{appName}/manifest.json (in-scope, served by PWAAssetRenderer)');
console.log('   - Service worker: /{appName}/sw.js with Service-Worker-Allowed');
console.log('   - Icons: 192x192 and 512x512 (any + maskable)\n');
