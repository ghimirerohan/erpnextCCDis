import { userResource, setAuthErrorCallback } from "../../shared/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session, setNavigationCallbacks } from "../../shared/data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("./Home.vue"),
	},
	{
		name: "Login",
		path: "/login",
		component: () => import("../../shared/components/Login.vue"),
	},
]

const router = createRouter({
	history: createWebHistory("/home"),
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
		// Use intended route if available, otherwise go to app root
		let targetRoute = intendedRoute || "/"
		
		// If defaultRoute is provided and it's within our app scope
		if (defaultRoute && defaultRoute.startsWith('/home')) {
			// Extract relative path from /home/...
			targetRoute = defaultRoute.replace('/home', '') || "/"
		}
		
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
		next(intendedRoute || { name: "Home" })
		intendedRoute = null
	} else if (to.name !== "Login" && !isLoggedIn) {
		intendedRoute = to.fullPath
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router
