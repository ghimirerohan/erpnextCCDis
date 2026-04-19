import { createRouter, createWebHistory } from 'vue-router'
import { ensureWebsiteAuth, ADMIN_APP_ROLES, websiteLoginUrl } from '@shared/frappe-boot'
import FieldSummary from './pages/FieldSummary.vue'
import CashRegister from './pages/CashRegister.vue'
import Advances from './pages/Advances.vue'
import EmployeeDetail from './pages/EmployeeDetail.vue'
import AccessDenied from './pages/AccessDenied.vue'

const router = createRouter({
	history: createWebHistory('/admin-app'),
	routes: [
		{ path: '/', component: FieldSummary },
		{ path: '/register', component: CashRegister },
		{ path: '/advances', component: Advances },
		{ path: '/employee/:id', component: EmployeeDetail, props: true },
		{ name: 'access-denied', path: '/access-denied', component: AccessDenied },
	],
})

router.beforeEach((to, _from, next) => {
	if (to.name === 'access-denied') {
		next()
		return
	}
	const auth = ensureWebsiteAuth({ roles: ADMIN_APP_ROLES })
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
