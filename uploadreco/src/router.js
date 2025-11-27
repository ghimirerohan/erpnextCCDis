import { userResource, setAuthErrorCallback } from "../../shared/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session, setNavigationCallbacks } from "../../shared/data/session"

const routes = [
	{
		path: "/",
		name: "UploadReco",
		component: () => import("./UploadReco.vue"),
	},
	{
		name: "Login",
		path: "/login",
		component: () => import("../../shared/components/Login.vue"),
	},
]

const router = createRouter({
	history: createWebHistory("/uploadreco"),
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
		if (defaultRoute && defaultRoute.startsWith('/uploadreco')) {
			// Extract relative path from /uploadreco/...
			targetRoute = defaultRoute.replace('/uploadreco', '') || "/"
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
		next(intendedRoute || { name: "UploadReco" })
		intendedRoute = null
	} else if (to.name !== "Login" && !isLoggedIn) {
		intendedRoute = to.fullPath
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router
