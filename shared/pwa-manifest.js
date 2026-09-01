// Point the document at an in-scope Web App Manifest (/{app}/manifest.json).
// Out-of-scope /api/method manifests are not installable on Chrome/Safari.

const APP_THEME_COLORS = {
  qrpay: '#10b981',
  'qrpay-horlicks': '#f97316',
  'qrpay-admin': '#7c3aed',
  scanner: '#f59e0b',
  'pay-dashboard': '#2563eb',
  uploadsales: '#059669',
  uploadreco: '#dc2626',
  dailyrecoentry: '#0891b2',
  dailytrnxs: '#7c3aed',
  home: '#6366f1',
  testlogin: '#64748b',
  'ai-assistant': '#7c3aed',
  'emp-attendance': '#059669',
}

export function getSpaAppName() {
  return window.location.pathname.split('/').filter(Boolean)[0] || 'home'
}

export function ensureInScopeManifest() {
  const appName = getSpaAppName()
  const href = `/${appName}/manifest.json`

  let link = document.querySelector('link[rel="manifest"]')
  if (!link) {
    link = document.createElement('link')
    link.rel = 'manifest'
    document.head.appendChild(link)
  }
  if (!link.getAttribute('href')?.endsWith(`/${appName}/manifest.json`)) {
    link.setAttribute('href', href)
  }

  const theme = APP_THEME_COLORS[appName] || '#0f172a'
  let themeMeta = document.querySelector('meta[name="theme-color"]')
  if (!themeMeta) {
    themeMeta = document.createElement('meta')
    themeMeta.name = 'theme-color'
    document.head.appendChild(themeMeta)
  }
  themeMeta.content = theme

  const iconHref = `/assets/custom_erp/frontend/icons/${appName}/icon-192x192.png`
  if (!document.querySelector('link[rel="apple-touch-icon"]')) {
    const apple = document.createElement('link')
    apple.rel = 'apple-touch-icon'
    apple.href = iconHref
    document.head.appendChild(apple)
  }
}
