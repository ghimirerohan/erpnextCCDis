# Progressive Web App (PWA) Setup

This Vue.js application is now configured as a full-featured Progressive Web App (PWA) that can be installed on mobile devices and behave as a standalone application.

## Features

### ✅ Installation
- **Android**: Install from Chrome/Edge browser via "Add to Home Screen" or "Install App" prompt
- **iOS/Safari**: Add to Home Screen from the Share menu
- **Desktop**: Install from Chrome/Edge address bar icon

### ✅ Standalone Mode
- Runs as a standalone app without browser UI
- Full-screen experience
- Custom app icon and splash screen
- Native app-like feel

### ✅ Offline Support
- Service worker caches essential assets
- Works offline after first visit
- Smart caching strategies for different resource types:
  - **Static Assets**: Cached for instant loading
  - **Images**: Cached for 30 days
  - **Fonts**: Cached for 1 year
  - **API Calls**: Network-first with 5-minute cache fallback

### ✅ Auto-Updates
- Automatically checks for new versions
- Prompts user to reload when updates are available
- Seamless update process

## Development

### Running in Development Mode
```bash
npm run dev
```

The PWA features are enabled in development mode for testing.

### Building for Production
```bash
npm run build
```

This will generate:
- Optimized production build
- Service worker file
- Web app manifest
- All PWA assets

### Generating Icons
If you need to regenerate PWA icons from the favicon:
```bash
npm run generate-icons
```

## Testing PWA Features

### Desktop (Chrome/Edge)
1. Run the app in dev or production mode
2. Open Chrome DevTools > Application tab
3. Check "Manifest" to verify manifest configuration
4. Check "Service Workers" to verify service worker registration
5. Test offline by checking "Offline" in Network tab

### Android
1. Open the app in Chrome
2. Chrome will show an install prompt
3. Or tap the menu (⋮) > "Add to Home Screen" or "Install App"
4. The app will be installed with its icon
5. Open from home screen to use in standalone mode

### iOS/Safari
1. Open the app in Safari
2. Tap the Share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Enter app name and tap "Add"
5. Open from home screen to use in standalone mode

## Configuration Files

### `vite.config.js`
- VitePWA plugin configuration
- Service worker settings
- Cache strategies
- Offline support

### `public/manifest.json`
- App metadata (name, description, icons)
- Display mode set to "standalone"
- Theme and background colors
- Orientation preferences

### `index.html`
- PWA meta tags
- Apple-specific meta tags for iOS
- Theme color configuration
- Manifest link

### `src/main.js`
- Service worker registration
- Update prompt logic
- Offline ready notification

## Icons

PWA icons are located in `public/icons/`:
- `icon-72x72.png` - Small screens
- `icon-96x96.png` - Small screens
- `icon-128x128.png` - Standard screens
- `icon-144x144.png` - Windows tile
- `icon-152x152.png` - iOS devices
- `icon-192x192.png` - Android standard
- `icon-384x384.png` - High-res displays
- `icon-512x512.png` - Splash screens

Plus `public/apple-touch-icon.png` (180x180) for iOS.

## Customization

### Changing App Name
Update in these files:
- `public/manifest.json` - "name" and "short_name"
- `vite.config.js` - VitePWA manifest config
- `index.html` - title and meta tags

### Changing Theme Color
Update in these files:
- `public/manifest.json` - "theme_color" and "background_color"
- `vite.config.js` - VitePWA manifest config
- `index.html` - theme-color meta tag

### Changing Icons
1. Replace `public/favicon.png` with your new icon
2. Run `npm run generate-icons` to regenerate all PWA icons

### Customizing Cache Strategy
Edit the `workbox.runtimeCaching` section in `vite.config.js`:
- `CacheFirst`: Cache first, network fallback (good for static assets)
- `NetworkFirst`: Network first, cache fallback (good for API calls)
- `StaleWhileRevalidate`: Serve from cache, update in background

## Browser Support

### Full PWA Support
- Chrome/Edge 67+ (Android, Desktop, iOS)
- Samsung Internet 8.2+
- Firefox 79+ (limited features)

### Add to Home Screen Only
- Safari 11.3+ (iOS)
- Safari 13+ (macOS)

## Troubleshooting

### PWA Not Installing
1. Ensure you're using HTTPS (or localhost)
2. Check manifest.json is accessible
3. Verify all icons exist and are valid
4. Check service worker is registered (DevTools > Application)

### Updates Not Working
1. Clear browser cache
2. Unregister old service workers
3. Rebuild and redeploy the app

### Offline Mode Not Working
1. Visit the app while online first (to cache assets)
2. Check service worker is active
3. Verify cache strategy in vite.config.js

## Security Notes

- PWA requires HTTPS in production (localhost is exempt)
- Service workers have access to cached resources
- Always validate and sanitize data from cache
- Keep service worker file at root or one level up from app

## Additional Resources

- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [VitePWA Plugin](https://vite-pwa-org.netlify.app/)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)

