import { userResource, setAuthErrorCallback } from "../../shared/data/user"
import { createRouter, createWebHistory } from 'vue-router'
import { session, setNavigationCallbacks } from '../../shared/data/session'
import QRPayHorlicks from './QRPayHorlicks.vue'
import Login from '../../shared/components/Login.vue'

const routes = [
  {
    path: "/",
    name: "QRPayHorlicks",
    component: QRPayHorlicks,
    meta: { requiresAuth: true }
  },
  {
    name: "Login",
    path: "/login",
    component: Login,
  },
  {
    path: '/previous-transactions',
    name: 'PreviousTransactions',
    component: () => import('./PreviousTransactions.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory("/qrpayhorlicks"),
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
    if (defaultRoute && defaultRoute.startsWith('/qrpayhorlicks')) {
      // Extract relative path from /qrpayhorlicks/...
      targetRoute = defaultRoute.replace('/qrpayhorlicks', '') || "/"
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
    next(intendedRoute || { name: "QRPayHorlicks" })
    intendedRoute = null
  } else if (to.name !== "Login" && !isLoggedIn) {
    intendedRoute = to.fullPath
    next({ name: "Login" })
  } else {
    next()
  }
})

export default router
