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

console.log('🚀 Building all apps individually...\n');

// Clean output directory
await fs.emptyDir(publicFrontendDir);

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
            const manifestSrc = path.join(__dirname, 'public', manifestName);
            const manifestDest = path.join(publicFrontendDir, appName, manifestName);
            if (fs.existsSync(manifestSrc)) {
                await fs.copy(manifestSrc, manifestDest);
                console.log(`   ✅ Copied ${manifestName}`);
            }
            
            // Fix manifest path in HTML (make it relative to base)
            content = content.replace(`href="${basePath}manifest-${appName}.json"`, `href="${basePath}manifest-${appName}.json"`);
            
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

