import { userResource, setAuthErrorCallback } from "../../shared/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session, setNavigationCallbacks } from "../../shared/data/session"

// Store the intended route before redirecting to login
let intendedRoute = null
let router = null

// Set auth error callback IMMEDIATELY before router is created
setAuthErrorCallback(() => {
	const currentPath = window.location.pathname
	if (!currentPath.includes('/login')) {
		if (router && router.currentRoute.value.name !== "Login") {
			intendedRoute = router.currentRoute.value.fullPath
			try {
				router.replace({ name: "Login" })
			} catch (e) {
				window.location.replace('/dailytrnxs/login')
			}
		} else {
			window.location.replace('/dailytrnxs/login')
		}
	}
})

const routes = [
	{
		path: "/",
		name: "DailyTransactions",
		component: () => import("./DailyTransactions.vue"),
	},
	{
		name: "Login",
		path: "/login",
		component: () => import("../../shared/components/Login.vue"),
	},
]

router = createRouter({
	history: createWebHistory("/dailytrnxs"),
	routes,
})

setNavigationCallbacks({
	onLoginSuccess: (defaultRoute) => {
		let targetRoute = intendedRoute || "/"
		
		if (defaultRoute && defaultRoute.startsWith('/dailytrnxs')) {
			targetRoute = defaultRoute.replace('/dailytrnxs', '') || "/"
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
		next(intendedRoute || { name: "DailyTransactions" })
		intendedRoute = null
	} else if (to.name !== "Login" && !isLoggedIn) {
		intendedRoute = to.fullPath
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router

