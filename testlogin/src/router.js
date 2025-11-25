import { userResource, setAuthErrorCallback } from "../../shared/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session, setNavigationCallbacks } from "../../shared/data/session"

// Store the intended route before redirecting to login
let intendedRoute = null
let router = null

// Set auth error callback IMMEDIATELY before router is created
// This ensures it's set before userResource is accessed
setAuthErrorCallback(() => {
	// Prevent any default redirects - always redirect to this app's login
	const currentPath = window.location.pathname
	// Don't redirect if already on login page or account/login
	if (!currentPath.includes('/login') && !currentPath.includes('/account/login')) {
		// Use replace to prevent back button issues and prevent default redirects
		if (router && router.currentRoute.value.name !== "Login") {
			intendedRoute = router.currentRoute.value.fullPath
			// Try router first, but if it fails, use window.location
			try {
				router.replace({ name: "Login" })
			} catch (e) {
				window.location.replace('/testlogin/login')
			}
		} else {
			window.location.replace('/testlogin/login')
		}
	}
})

const routes = [
	{
		path: "/",
		name: "TestLogin",
		component: () => import("./TestLogin.vue"),
	},
	{
		name: "Login",
		path: "/login",
		component: () => import("../../shared/components/Login.vue"),
	},
]

router = createRouter({
	history: createWebHistory("/testlogin"),
	routes,
})

setNavigationCallbacks({
	onLoginSuccess: (defaultRoute) => {
		// CRITICAL: Ignore any /jsapp/ paths from server - always use app's own routes
		let targetRoute = intendedRoute || "/"
		
		// If defaultRoute is provided and it's NOT a /jsapp/ path and it's within our app scope
		if (defaultRoute && !defaultRoute.includes('/jsapp/') && defaultRoute.startsWith('/testlogin')) {
			// Extract relative path from /testlogin/...
			targetRoute = defaultRoute.replace('/testlogin', '') || "/"
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
	// If going to login, store the intended route
	if (to.name !== "Login" && from.name !== "Login") {
		intendedRoute = to.fullPath
	}

	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
		// If we get an auth error and we're not already going to login, redirect
		if (error?.exc_type === "AuthenticationError" && to.name !== "Login") {
			intendedRoute = to.fullPath
			next({ name: "Login" })
			return
		}
	}

	if (to.name === "Login" && isLoggedIn) {
		// If already logged in and trying to access login, go to intended route or home
		next(intendedRoute || { name: "TestLogin" })
		intendedRoute = null
	} else if (to.name !== "Login" && !isLoggedIn) {
		// Not logged in and trying to access protected route
		intendedRoute = to.fullPath
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router

