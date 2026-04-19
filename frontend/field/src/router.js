import { createRouter, createWebHistory } from 'vue-router'
import { ensureWebsiteAuth, FIELD_APP_ROLES, websiteLoginUrl } from '@shared/frappe-boot'
import Dashboard from './pages/Dashboard.vue'
import PaymentEntry from './pages/PaymentEntry.vue'
import CreditHistory from './pages/CreditHistory.vue'
import DayClose from './pages/DayClose.vue'
import AccessDenied from './pages/AccessDenied.vue'

const router = createRouter({
	history: createWebHistory('/field-app'),
	routes: [
		{ path: '/', component: Dashboard },
		{ path: '/payment', component: PaymentEntry },
		{ path: '/payment/:customer', component: PaymentEntry, props: true },
		{ path: '/credits', component: CreditHistory },
		{ path: '/close', component: DayClose },
		{ name: 'access-denied', path: '/access-denied', component: AccessDenied },
	],
})

router.beforeEach((to, _from, next) => {
	if (to.name === 'access-denied') {
		next()
		return
	}
	const auth = ensureWebsiteAuth({ roles: FIELD_APP_ROLES })
	if (!auth.ok && auth.reason === 'guest') {
		const dest = `${window.location.pathname}${window.location.search || ''}`
		window.location.href = websiteLoginUrl(dest)
		return
	}
	if (!auth.ok && auth.reason === 'role') {
		next({ name: 'access-denied' })
		return
	}
	next()
})

export default router
