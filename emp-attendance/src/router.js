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
        window.location.replace('/emp-attendance/login')
      }
    } else {
      window.location.replace('/emp-attendance/login')
    }
  }
})

const routes = [
  {
    path: "/",
    name: "AttendanceList",
    component: () => import("./AttendanceList.vue"),
  },
  {
    path: "/employee/:employeeId",
    name: "EmployeeHistory",
    component: () => import("./EmployeeHistory.vue"),
    props: true,
  },
  {
    name: "Login",
    path: "/login",
    component: () => import("../../shared/components/Login.vue"),
  },
]

router = createRouter({
  history: createWebHistory("/emp-attendance"),
  routes,
})

setNavigationCallbacks({
  onLoginSuccess: (defaultRoute) => {
    let targetRoute = intendedRoute || "/"
    
    if (defaultRoute && defaultRoute.startsWith('/emp-attendance')) {
      targetRoute = defaultRoute.replace('/emp-attendance', '') || "/"
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
    next(intendedRoute || { name: "AttendanceList" })
    intendedRoute = null
  } else if (to.name !== "Login" && !isLoggedIn) {
    intendedRoute = to.fullPath
    next({ name: "Login" })
  } else {
    next()
  }
})

export default router

