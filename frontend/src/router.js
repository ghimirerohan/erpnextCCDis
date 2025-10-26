import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
	},
	{
		name: "Login",
		path: "/account/login",
		component: () => import("@/pages/Login.vue"),
	},
  {
    name: "Scanner",
    path: "/scanner",
    component: () => import("@/pages/Scanner.vue"),
  },
  {
    name: "QRPay",
    path: "/qrpay",
    component: () => import("@/pages/QRPay.vue"),
  },
  {
    name: "QRPayAdmin",
    path: "/qrpay-admin",
    component: () => import("@/pages/QRPayAdmin.vue"),
  },
  {
    name: "UploadSales",
    path: "/uploadsales",
    component: () => import("@/apps/uploadsales/UploadSales.vue"),
  },
]

const router = createRouter({
	history: createWebHistory("/jsapp"),
	routes,
})

router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

  if (to.name === "Login" && isLoggedIn) {
		next({ name: "Home" })
  } else if (to.name !== "Login" && !isLoggedIn) {
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router
