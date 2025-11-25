
import { execSync } from 'child_process';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

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

console.log('Build script started');

try {
  console.log('Running vite build...');
  execSync('vite build', { stdio: 'inherit' });
  console.log('Vite build completed successfully');
} catch (error) {
  console.error('Vite build failed:', error.message);
  process.exit(1);
}

// Post-build: Update www html files
console.log('Updating www html files...');

const publicFrontendDir = path.resolve(__dirname, 'custom_erp/public/frontend');
const wwwDir = path.resolve(__dirname, 'custom_erp/www');

async function updateWwwFiles() {
    for (const appName of apps) {
        const appDir = path.join(publicFrontendDir, appName);
        const indexHtmlPath = path.join(appDir, 'index.html');
        const wwwHtmlPath = path.join(wwwDir, `${appName}.html`);

        // Copy manifest if exists
        const manifestName = `manifest-${appName}.json`;
        const manifestSrc = path.join(publicFrontendDir, manifestName);
        const manifestDest = path.join(appDir, manifestName);
        if (fs.existsSync(manifestSrc)) {
             await fs.copy(manifestSrc, manifestDest);
             console.log(`✅ Copied ${manifestName} to ${appName}/`);
        }

        if (fs.existsSync(indexHtmlPath)) {
            let content = await fs.readFile(indexHtmlPath, 'utf-8');

            // Replace relative paths with absolute paths for Frappe environment
            // The vite build (via multi-app-build plugin) sets paths to ./assets/
            // We need /assets/custom_erp/frontend/{appName}/assets/
            const assetBase = `/assets/custom_erp/frontend/${appName}/assets/`;
            content = content.replaceAll('./assets/', assetBase);
            
            // Fix manifest path (if relative)
            content = content.replaceAll('./manifest-', `/assets/custom_erp/frontend/${appName}/manifest-`);
            
            // Fix service worker path
            content = content.replaceAll(`./sw-${appName}.js`, `/assets/custom_erp/frontend/${appName}/sw-${appName}.js`);
            
            // Inject import.meta.url base path fix for dynamic imports
            const basePathScript = `<script>window.__VITE_ASSET_BASE__ = '/assets/custom_erp/frontend/${appName}/';</script>`;
            content = content.replace('<head>', `<head>\n    ${basePathScript}`);

            // Inject Jinja boot script if NOT present
            const jinjaScript = `
          <script>
              {% for key in boot %}
              window["{{ key }}"] = {{ boot[key] | tojson }};
              {% endfor %}
          </script>
          </body>`;
            
            if (!content.includes('{% for key in boot %}')) {
                content = content.replace('</body>', jinjaScript);
            }

            await fs.writeFile(wwwHtmlPath, content);
            console.log(`✅ Updated ${appName}.html`);
        } else {
            console.warn(`⚠️  Missing index.html for ${appName}`);
        }
    }
}

updateWwwFiles().then(() => {
    console.log('✨ Build and update complete!');
}).catch(err => {
    console.error('Error updating www files:', err);
    process.exit(1);
});
