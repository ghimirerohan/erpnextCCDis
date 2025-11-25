import { userResource, setAuthErrorCallback } from "../../shared/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session, setNavigationCallbacks } from "../../shared/data/session"

const routes = [
	{
		path: "/",
		name: "UploadSales",
		component: () => import("./UploadSales.vue"),
	},
	{
		name: "Login",
		path: "/login",
		component: () => import("../../shared/components/Login.vue"),
	},
]

const router = createRouter({
	history: createWebHistory("/uploadsales"),
	routes,
})

let intendedRoute = null

setAuthErrorCallback(() => {
	if (router.currentRoute.value.name !== "Login") {
		intendedRoute = router.currentRoute.value.fullPath
		router.replace({ name: "Login" })
	}
})

setNavigationCallbacks({
	onLoginSuccess: (defaultRoute) => {
		// CRITICAL: Ignore any /jsapp/ paths from server - always use app's own routes
		let targetRoute = intendedRoute || "/"
		
		// If defaultRoute is provided and it's NOT a /jsapp/ path and it's within our app scope
		if (defaultRoute && !defaultRoute.includes('/jsapp/') && defaultRoute.startsWith('/uploadsales')) {
			// Extract relative path from /uploadsales/...
			targetRoute = defaultRoute.replace('/uploadsales', '') || "/"
		} else if (defaultRoute && !defaultRoute.includes('/jsapp/') && defaultRoute === '/') {
			// Server gave us root, use app root
			targetRoute = "/"
		}
		// Otherwise ignore defaultRoute if it contains /jsapp/ or is outside our scope
		
		intendedRoute = null
		router.replace(targetRoute)
	},
	onLogoutSuccess: () => {
		router.replace({ name: "Login" })
	},
})

router.beforeEach(async (to, from, next) => {
	if (to.name !== "Login" && from.name !== "Login") {
		intendedRoute = to.fullPath
	}

	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
		if (error?.exc_type === "AuthenticationError" && to.name !== "Login") {
			intendedRoute = to.fullPath
			next({ name: "Login" })
			return
		}
	}

	if (to.name === "Login" && isLoggedIn) {
		next(intendedRoute || { name: "UploadSales" })
		intendedRoute = null
	} else if (to.name !== "Login" && !isLoggedIn) {
		intendedRoute = to.fullPath
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router

