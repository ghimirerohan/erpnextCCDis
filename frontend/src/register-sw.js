// ADDED BY AI: MULTI_PWA - Service worker registration module
export async function registerScopedSW() {
  if (!('serviceWorker' in navigator)) {
    console.warn('Service Workers not supported in this browser');
    return;
  }

  // Detect current app from pathname
  const segs = window.location.pathname.split('/').filter(Boolean);
  let app = 'qrpay';
  if (segs.length >= 2 && segs[0] === 'jsapp') {
    app = segs[1];
  } else if (segs.length >= 1) {
    app = segs[0];
  }

  const swFilename = `sw-${app}.js`;
  const swUrlUnderApp = `/jsapp/${app}/${swFilename}`;
  const swUrlRoot = `/jsapp/${swFilename}`;
  const scope = `/jsapp/${app}/`;

  console.log(`🔧 Registering SW for app: ${app}, scope: ${scope}`);

  // Try to register service worker with multiple URL patterns
  async function tryRegister(url) {
    try {
      const registration = await navigator.serviceWorker.register(url, { scope });
      console.log('✅ Registered SW:', url, 'scope:', scope);
      
      // Check for updates periodically
      if (registration) {
        setInterval(() => {
          registration.update();
        }, 60 * 60 * 1000); // Check every hour
      }
      
      return true;
    } catch (err) {
      console.warn('❌ Failed registering SW', url, err.message);
      return false;
    }
  }

  // Try app-specific path first, then root path
  if (!(await tryRegister(swUrlUnderApp))) {
    await tryRegister(swUrlRoot);
  }
}

