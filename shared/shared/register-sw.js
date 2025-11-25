// ADDED BY AI: MULTI_PWA - Service worker registration module
// Fixed for Android Chrome PWA installation requirements
export async function registerScopedSW() {
  if (!('serviceWorker' in navigator)) {
    console.warn('Service Workers not supported in this browser');
    return null;
  }

  // Detect current app from pathname (root-level paths)
  const segs = window.location.pathname.split('/').filter(Boolean);
  let app = 'home';
  if (segs.length >= 1 && segs[0] !== '') {
    app = segs[0];
  }
  
  // Normalize app name
  if (!app || app === '') {
    app = 'home';
  }

  const swFilename = `sw-${app}.js`;
  // Service worker scope and URL for root-level apps
  const scope = `/${app}/`;
  const swUrl = `/${app}/${swFilename}`;

  console.log(`🔧 Registering SW for app: ${app}, scope: ${scope}`);

  // Unregister any existing service workers that might conflict
  try {
    const registrations = await navigator.serviceWorker.getRegistrations();
    for (const registration of registrations) {
      // Only unregister if it's for a different scope
      if (registration.scope !== window.location.origin + scope) {
        console.log(`🗑️ Unregistering conflicting SW: ${registration.scope}`);
        await registration.unregister();
      }
    }
  } catch (err) {
    console.warn('⚠️ Error checking existing registrations:', err);
  }

  // Try to register service worker with proper error handling
  async function tryRegister(url, targetScope) {
    try {
      // For Android Chrome, the scope must be exactly correct
      const registration = await navigator.serviceWorker.register(url, { 
        scope: targetScope,
        updateViaCache: 'none' // Ensure fresh updates
      });
      
      console.log('✅ Registered SW:', url, 'scope:', targetScope);
      
      // Wait for service worker to be active (critical for Android Chrome)
      let serviceWorker = registration.installing || registration.waiting || registration.active;
      
      if (serviceWorker) {
        if (serviceWorker.state === 'activated') {
          console.log('✅ Service Worker is active');
        } else {
          // Wait for activation
          await new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
              reject(new Error('Service Worker activation timeout'));
            }, 10000); // 10 second timeout
            
            serviceWorker.addEventListener('statechange', () => {
              if (serviceWorker.state === 'activated') {
                clearTimeout(timeout);
                console.log('✅ Service Worker activated');
                resolve();
              } else if (serviceWorker.state === 'redundant') {
                clearTimeout(timeout);
                reject(new Error('Service Worker became redundant'));
              }
            });
            
            // If already active, resolve immediately
            if (serviceWorker.state === 'activated') {
              clearTimeout(timeout);
              resolve();
            }
          }).catch(err => {
            console.warn('⚠️ Service Worker activation warning:', err);
          });
        }
      }
      
      // Check for updates periodically
      if (registration) {
        setInterval(() => {
          registration.update();
        }, 60 * 60 * 1000); // Check every hour
      }
      
      // Verify service worker is controlling the page
      if (registration.active) {
        console.log('✅ Service Worker is active and controlling:', registration.active.scriptURL);
        
        // Check if service worker is actually controlling the page
        if (navigator.serviceWorker.controller) {
          console.log('✅ Service Worker is controlling this page');
        } else {
          console.warn('⚠️ Service Worker registered but not yet controlling the page. Page reload may be needed.');
        }
      }
      
      return registration;
    } catch (err) {
      console.warn('❌ Failed registering SW', url, err.message);
      console.warn('Error details:', err);
      return null;
    }
  }

  // Try to register service worker
  let registration = await tryRegister(swUrl, scope);
  
  // Final verification for Android Chrome PWA installation
  if (registration) {
    console.log('🔍 Final PWA Installation Check:');
    console.log('  - Service Worker:', registration.active ? 'Active ✅' : 'Not Active ❌');
    console.log('  - Scope:', registration.scope);
    console.log('  - Controlling Page:', navigator.serviceWorker.controller ? 'Yes ✅' : 'No (may need reload)');
    console.log('  - HTTPS:', window.location.protocol === 'https:' ? 'Yes ✅' : `No (${window.location.protocol})`);
    
    // Check manifest
    const manifestLink = document.querySelector('link[rel="manifest"]');
    if (manifestLink) {
      console.log('  - Manifest:', manifestLink.href);
      fetch(manifestLink.href)
        .then(r => r.json())
        .then(manifest => {
          console.log('  - Manifest Display:', manifest.display);
          console.log('  - Manifest Start URL:', manifest.start_url);
          console.log('  - Manifest Scope:', manifest.scope);
          
          if (manifest.display !== 'standalone' && manifest.display !== 'fullscreen') {
            console.error('❌ CRITICAL: Manifest display is not "standalone" or "fullscreen"');
          }
        })
        .catch(err => console.warn('⚠️ Could not fetch manifest:', err));
    }
  }
  
  return registration;
}


