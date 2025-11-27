import { exec} from 'child_process';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import { promisify } from 'util';

const execAsync = promisify(exec);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const apps = [
	'qrpay',
	'qrpay-admin',
	'scanner',
	'pay-dashboard',
	'uploadsales',
	'uploadreco',
	'dailyrecoentry',
	'home',
	'testlogin'
];

const publicFrontendDir = path.resolve(__dirname, 'custom_erp/public/frontend');
const wwwDir = path.resolve(__dirname, 'custom_erp/www');
const publicDir = path.resolve(__dirname, 'public');

console.log('🚀 Building all apps individually...\n');

// Clean output directory
await fs.emptyDir(publicFrontendDir);

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

// Build each app with its own base path
for (const appName of apps) {
    console.log(`\n📦 Building ${appName}...`);
    
    const basePath = `/assets/custom_erp/frontend/${appName}/`;
    
    try {
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
        // Vite creates nested structure: appName/appName/index.html, we need to move it up
        const nestedIndexPath = path.join(publicFrontendDir, appName, appName, 'index.html');
        const indexHtmlPath = path.join(publicFrontendDir, appName, 'index.html');
        const wwwHtmlPath = path.join(wwwDir, `${appName}.html`);
        
        // Move index.html from nested location to correct location
        if (fs.existsSync(nestedIndexPath)) {
            await fs.move(nestedIndexPath, indexHtmlPath, { overwrite: true });
            // Clean up empty nested directory
            await fs.remove(path.join(publicFrontendDir, appName, appName));
        }
        
        if (fs.existsSync(indexHtmlPath)) {
            let content = await fs.readFile(indexHtmlPath, 'utf-8');
            
            // Copy manifest to app directory if exists
            const manifestName = `manifest-${appName}.json`;
            const manifestSrc = path.join(publicDir, manifestName);
            const manifestDest = path.join(publicFrontendDir, appName, manifestName);
            if (fs.existsSync(manifestSrc)) {
                await fs.copy(manifestSrc, manifestDest);
                console.log(`   ✅ Copied ${manifestName}`);
            }
            
            // Update manifest path in HTML to point to the app's own manifest
            content = content.replace(
                /href="[^"]*manifest[^"]*\.json"/g,
                `href="${basePath}manifest-${appName}.json"`
            );
            
            // Also fix the link tag for manifest
            if (!content.includes(`${basePath}manifest-${appName}.json`)) {
                content = content.replace(
                    '</head>',
                    `    <link rel="manifest" href="${basePath}manifest-${appName}.json" />\n  </head>`
                );
            }
            
            // Create a simple service worker for this app
            const swContent = `
// Service Worker for ${appName}
const CACHE_NAME = '${appName}-v1';
const APP_SCOPE = '/${appName}/';

// Install event
self.addEventListener('install', (event) => {
  console.log('[SW ${appName}] Installing...');
  self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
  console.log('[SW ${appName}] Activating...');
  event.waitUntil(clients.claim());
});

// Fetch event - network first, then cache
self.addEventListener('fetch', (event) => {
  // Only handle requests for this app's scope
  if (!event.request.url.includes(APP_SCOPE) && 
      !event.request.url.includes('/api/') && 
      !event.request.url.includes('/assets/')) {
    return;
  }
  
  event.respondWith(
    fetch(event.request)
      .catch(() => caches.match(event.request))
  );
});
`;
            const swPath = path.join(publicFrontendDir, appName, `sw-${appName}.js`);
            await fs.writeFile(swPath, swContent);
            console.log(`   ✅ Created sw-${appName}.js`);
            
            // Write to www directory
            await fs.writeFile(wwwHtmlPath, content);
            console.log(`   ✅ Created ${appName}.html in www/`);
        }
        
    } catch (error) {
        console.error(`❌ Failed to build ${appName}:`, error.message);
        process.exit(1);
    }
}

console.log('\n✨ All apps built successfully!\n');
