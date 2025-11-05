// PWA Installability Detection and Debugging for Android Chrome
// This module helps diagnose why PWAs might not be installable

export function checkPWAInstallability() {
  const checks = {
    serviceWorker: false,
    manifest: false,
    https: false,
    icons: false,
    displayStandalone: false,
    installPrompt: null,
    errors: []
  };

  // Check HTTPS
  checks.https = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
  if (!checks.https) {
    checks.errors.push('❌ Not served over HTTPS (required for PWA installation)');
  }

  // Check Service Worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(registrations => {
      checks.serviceWorker = registrations.length > 0;
      if (checks.serviceWorker) {
        console.log('✅ Service Worker registered:', registrations.map(r => r.scope));
      } else {
        checks.errors.push('❌ No service worker registered');
      }
      logInstallabilityStatus(checks);
    }).catch(err => {
      checks.errors.push('❌ Error checking service workers: ' + err.message);
      logInstallabilityStatus(checks);
    });
  } else {
    checks.errors.push('❌ Service Workers not supported in this browser');
  }

  // Check Manifest
  const manifestLink = document.querySelector('link[rel="manifest"]');
  if (manifestLink) {
    checks.manifest = true;
    const manifestUrl = manifestLink.href;
    
    // Try to fetch and validate manifest
    fetch(manifestUrl)
      .then(response => response.json())
      .then(manifest => {
        // Check display mode
        checks.displayStandalone = manifest.display === 'standalone' || manifest.display === 'fullscreen';
        if (!checks.displayStandalone) {
          checks.errors.push('❌ Manifest display is not "standalone" or "fullscreen"');
        }

        // Check icons
        if (manifest.icons && manifest.icons.length > 0) {
          const hasRequiredIcons = manifest.icons.some(icon => 
            (icon.sizes === '192x192' || icon.sizes.includes('192')) &&
            (icon.sizes === '512x512' || icon.sizes.includes('512'))
          );
          checks.icons = hasRequiredIcons;
          if (!hasRequiredIcons) {
            checks.errors.push('❌ Manifest missing required icons (192x192 and/or 512x512)');
          }
        } else {
          checks.errors.push('❌ Manifest has no icons');
        }

        // Check start_url and scope
        if (!manifest.start_url) {
          checks.errors.push('❌ Manifest missing start_url');
        } else {
          // Verify start_url is accessible
          const startUrl = new URL(manifest.start_url, window.location.origin);
          console.log('📍 Start URL:', startUrl.href);
        }
        
        if (!manifest.scope) {
          checks.errors.push('❌ Manifest missing scope');
        } else {
          console.log('📍 Scope:', manifest.scope);
        }

        // Check id field (important for multi-app PWAs)
        if (!manifest.id) {
          console.warn('⚠️ Manifest missing "id" field (recommended for multi-app PWAs)');
        } else {
          console.log('📍 Manifest ID:', manifest.id);
        }
        
        // Critical: Verify display mode
        if (manifest.display !== 'standalone' && manifest.display !== 'fullscreen') {
          checks.errors.push(`❌ Manifest display is "${manifest.display}" but should be "standalone" or "fullscreen"`);
        }

        console.log('📋 Manifest loaded:', manifest.name, 'Scope:', manifest.scope, 'Start URL:', manifest.start_url);
        logInstallabilityStatus(checks);
      })
      .catch(err => {
        checks.errors.push('❌ Error loading manifest: ' + err.message);
        logInstallabilityStatus(checks);
      });
  } else {
    checks.errors.push('❌ No manifest link found in document');
  }

  // Store deferredPrompt globally for install button
  let deferredPrompt;
  window.deferredPrompt = null;
  
  // Listen for beforeinstallprompt event (Android Chrome)
  window.addEventListener('beforeinstallprompt', (e) => {
    console.log('📱 beforeinstallprompt event fired - PWA is installable!');
    console.log('📱 Install prompt details:', {
      platforms: e.platforms,
      userChoice: 'Available after prompt'
    });
    e.preventDefault();
    deferredPrompt = e;
    window.deferredPrompt = e;
    checks.installPrompt = e;
    logInstallabilityStatus(checks);
    
    // Show custom install prompt if needed
    // You can trigger this from a button in your UI
  });

  // Listen for appinstalled event
  window.addEventListener('appinstalled', () => {
    console.log('✅ PWA was installed successfully!');
    deferredPrompt = null;
  });

  // Log initial status
  setTimeout(() => logInstallabilityStatus(checks), 2000);

  return checks;
}

function logInstallabilityStatus(checks) {
  console.log('\n🔍 PWA Installability Check:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('✅ HTTPS:', checks.https ? 'Yes' : 'No');
  console.log('✅ Service Worker:', checks.serviceWorker ? 'Registered' : 'Not Registered');
  console.log('✅ Manifest:', checks.manifest ? 'Found' : 'Not Found');
  console.log('✅ Icons:', checks.icons ? 'Valid' : 'Invalid');
  console.log('✅ Display Standalone:', checks.displayStandalone ? 'Yes' : 'No');
  console.log('✅ Install Prompt:', checks.installPrompt ? 'Available' : 'Not Available');
  
  if (checks.errors.length > 0) {
    console.log('\n❌ Issues found:');
    checks.errors.forEach(error => console.log('  ' + error));
  } else {
    console.log('\n✅ All checks passed! PWA should be installable.');
  }
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
}

// Export function to trigger install prompt
export function showInstallPrompt() {
  if (window.deferredPrompt) {
    window.deferredPrompt.prompt();
    window.deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('✅ User accepted the install prompt');
      } else {
        console.log('❌ User dismissed the install prompt');
      }
      window.deferredPrompt = null;
    });
  } else {
    console.warn('⚠️ Install prompt not available. PWA may not meet installability criteria.');
    checkPWAInstallability();
  }
}

