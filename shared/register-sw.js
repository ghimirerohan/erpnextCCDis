// Service Worker Registration for Android Chrome PWA
// Critical: SW must be served with Service-Worker-Allowed header

export async function registerScopedSW() {
    if (!('serviceWorker' in navigator)) {
        console.warn('⚠️ Service Workers not supported');
        return null;
    }

    // Detect app from URL path
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const appName = pathParts[0] || 'home';
    
    // Service worker URL - served via Frappe API with proper headers
    // The API sets Service-Worker-Allowed header to allow controlling the app scope
    const swUrl = `/api/method/custom_erp.api.pwa.get_service_worker?app_name=${appName}`;
    const scope = `/${appName}/`;

    console.log(`🔧 PWA Setup for: ${appName}`);
    console.log(`   SW URL: ${swUrl}`);
    console.log(`   Scope: ${scope}`);

    try {
        // First, unregister any old/conflicting service workers
        const existingRegs = await navigator.serviceWorker.getRegistrations();
        for (const reg of existingRegs) {
            // Keep only the registration for our exact scope
            if (reg.scope !== window.location.origin + scope) {
                console.log(`🗑️ Removing old SW: ${reg.scope}`);
                await reg.unregister();
            }
        }

        // Register the service worker
        const registration = await navigator.serviceWorker.register(swUrl, {
            scope: scope,
            updateViaCache: 'none'
        });

        console.log('✅ Service Worker registered');
        console.log(`   Scope: ${registration.scope}`);

        // Wait for the service worker to be ready
        const sw = registration.installing || registration.waiting || registration.active;
        
        if (sw && sw.state !== 'activated') {
            await new Promise((resolve) => {
                if (sw.state === 'activated') {
                    resolve();
                    return;
                }
                sw.addEventListener('statechange', () => {
                    if (sw.state === 'activated') {
                        resolve();
                    }
                });
                // Timeout after 10 seconds
                setTimeout(resolve, 10000);
            });
        }

        // Check if SW is controlling the page
        if (navigator.serviceWorker.controller) {
            console.log('✅ Service Worker is controlling this page');
        } else {
            console.log('⚠️ Service Worker registered but not yet controlling');
            console.log('   The page will be controlled after reload');
        }

        // Log PWA installation readiness
        logPWAStatus(appName);

        return registration;

    } catch (error) {
        console.error('❌ Service Worker registration failed:', error);
        
        // Provide helpful error messages
        if (error.message.includes('path restriction')) {
            console.error('💡 The service worker scope is restricted.');
            console.error('   Make sure the SW is served with Service-Worker-Allowed header');
        }
        
        return null;
    }
}

function logPWAStatus(appName) {
    console.log('\n📱 PWA Installation Checklist:');
    
    // HTTPS check
    const isHttps = location.protocol === 'https:' || location.hostname === 'localhost';
    console.log(`   ${isHttps ? '✅' : '❌'} HTTPS: ${location.protocol}`);
    
    // Manifest check
    const manifestLink = document.querySelector('link[rel="manifest"]');
    if (manifestLink) {
        console.log(`   ✅ Manifest: ${manifestLink.href}`);
        
        // Fetch and validate manifest
        fetch(manifestLink.href)
            .then(r => r.json())
            .then(m => {
                console.log(`   ✅ Name: ${m.name}`);
                console.log(`   ✅ Start URL: ${m.start_url}`);
                console.log(`   ✅ Display: ${m.display}`);
                console.log(`   ✅ Icons: ${m.icons?.length || 0} defined`);
                
                // Check for required icon sizes
                const has192 = m.icons?.some(i => i.sizes?.includes('192'));
                const has512 = m.icons?.some(i => i.sizes?.includes('512'));
                console.log(`   ${has192 ? '✅' : '❌'} Has 192x192 icon`);
                console.log(`   ${has512 ? '✅' : '❌'} Has 512x512 icon`);
            })
            .catch(e => console.log(`   ❌ Manifest fetch failed: ${e.message}`));
    } else {
        console.log('   ❌ No manifest link found');
    }
    
    // Service Worker check
    navigator.serviceWorker.getRegistrations().then(regs => {
        const appReg = regs.find(r => r.scope.includes(`/${appName}/`));
        if (appReg) {
            console.log(`   ✅ Service Worker: ${appReg.active ? 'Active' : 'Registered'}`);
        } else {
            console.log('   ❌ No Service Worker for this app');
        }
    });
    
    console.log('\n');
}

// Listen for the beforeinstallprompt event (Android Chrome)
let deferredPrompt = null;

window.addEventListener('beforeinstallprompt', (e) => {
    console.log('🎉 beforeinstallprompt fired - App is installable!');
    e.preventDefault();
    deferredPrompt = e;
    window.deferredPrompt = e;
    
    // Dispatch custom event for UI to show install button
    window.dispatchEvent(new CustomEvent('pwa-install-available', { detail: e }));
});

window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed successfully!');
    deferredPrompt = null;
    window.deferredPrompt = null;
});

// Export function to trigger install prompt
export function promptInstall() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((result) => {
            console.log(`Install prompt result: ${result.outcome}`);
            deferredPrompt = null;
        });
        return true;
    }
    return false;
}

// Export function to check if install is available
export function isInstallAvailable() {
    return deferredPrompt !== null;
}
