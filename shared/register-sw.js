// Service Worker Registration for Android Chrome PWA.
// SW is served in-scope at /{app}/sw.js (PWAAssetRenderer + Service-Worker-Allowed).

export async function registerScopedSW() {
    if (!('serviceWorker' in navigator)) {
        console.warn('⚠️ Service Workers not supported');
        return null;
    }

    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const appName = pathParts[0] || 'home';
    const scope = `/${appName}/`;
    const swUrl = `/${appName}/sw.js`;

    console.log(`🔧 PWA Setup for: ${appName}`);
    console.log(`   SW URL: ${swUrl}`);
    console.log(`   Scope: ${scope}`);

    if (canonicalizeAppUrl(appName, scope)) {
        return null;
    }

    try {
        const existingRegs = await navigator.serviceWorker.getRegistrations();
        for (const reg of existingRegs) {
            const script = reg.active?.scriptURL || reg.waiting?.scriptURL || reg.installing?.scriptURL || '';
            const sameScope = reg.scope === window.location.origin + scope;
            const isApiSw = script.includes('/api/method/custom_erp.api.pwa.get_service_worker');
            if (!sameScope || isApiSw) {
                console.log(`🗑️ Removing old SW: ${reg.scope} ${script}`);
                await reg.unregister();
            }
        }

        const registration = await navigator.serviceWorker.register(swUrl, {
            scope: scope,
            updateViaCache: 'none'
        });

        console.log('✅ Service Worker registered');
        console.log(`   Scope: ${registration.scope}`);

        const sw = registration.installing || registration.waiting || registration.active;
        if (sw && sw.state !== 'activated') {
            await new Promise((resolve) => {
                if (sw.state === 'activated') {
                    resolve();
                    return;
                }
                sw.addEventListener('statechange', () => {
                    if (sw.state === 'activated') resolve();
                });
                setTimeout(resolve, 10000);
            });
        }

        logPWAStatus(appName);
        reloadOnceToClaimControl(appName, registration);
        return registration;
    } catch (error) {
        console.error('❌ Service Worker registration failed:', error);
        if (error.message && error.message.includes('path restriction')) {
            console.error('💡 Scope is restricted. /{app}/sw.js must send Service-Worker-Allowed.');
        }
        return null;
    }
}

function canonicalizeAppUrl(appName, scope) {
    // SW scope /{app}/ does not control /{app} (no trailing slash). Reloading
    // that URL forever looks like a refresh loop after every PWA deploy.
    const { pathname, search, hash } = window.location;
    if (pathname === `/${appName}`) {
        window.location.replace(`${scope}${search}${hash}`);
        return true;
    }
    return false;
}

function reloadOnceToClaimControl(appName, registration) {
    if (navigator.serviceWorker.controller || !registration?.active) {
        return;
    }
    const key = `pwa-sw-claim-reload:${appName}`;
    try {
        if (sessionStorage.getItem(key)) {
            console.warn('⚠️ Service Worker is active but not controlling this page. Not reloading again.');
            return;
        }
        sessionStorage.setItem(key, '1');
    } catch {
        return;
    }
    setTimeout(() => {
        if (!navigator.serviceWorker.controller) {
            console.log('🔄 Reloading once so the service worker can control this page');
            window.location.reload();
        }
    }, 2000);
}

function logPWAStatus(appName) {
    console.log('\n📱 PWA Installation Checklist:');
    const isHttps = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname.endsWith('.localhost');
    console.log(`   ${isHttps ? '✅' : '❌'} HTTPS: ${location.protocol} ${location.hostname}`);

    const manifestLink = document.querySelector('link[rel="manifest"]');
    if (manifestLink) {
        console.log(`   ✅ Manifest: ${manifestLink.href}`);
        fetch(manifestLink.href)
            .then(async (r) => {
                const data = await r.json();
                const manifest = data.message && data.name == null ? data.message : data;
                if (data.message && data.name == null) {
                    console.log('   ❌ Manifest is Frappe-wrapped {message}; Chrome cannot install this');
                }
                console.log(`   ${manifest.display === 'standalone' || manifest.display === 'fullscreen' ? '✅' : '❌'} Display: ${manifest.display}`);
                console.log(`   ✅ Start URL: ${manifest.start_url}`);
                console.log(`   ✅ Scope: ${manifest.scope}`);
                console.log(`   ✅ Icons: ${manifest.icons?.length || 0}`);
            })
            .catch((e) => console.log(`   ❌ Manifest fetch failed: ${e.message}`));
    } else {
        console.log('   ❌ No manifest link found');
    }
}

let deferredPrompt = null;

window.addEventListener('beforeinstallprompt', (e) => {
    console.log('🎉 beforeinstallprompt fired - App is installable!');
    e.preventDefault();
    deferredPrompt = e;
    window.deferredPrompt = e;
    window.dispatchEvent(new CustomEvent('pwa-install-available', { detail: e }));
});

window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed successfully!');
    deferredPrompt = null;
    window.deferredPrompt = null;
});

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

export function isInstallAvailable() {
    return deferredPrompt !== null;
}
