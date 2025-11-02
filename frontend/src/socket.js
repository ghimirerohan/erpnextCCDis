import { io } from "socket.io-client"

let socket = null
export function initSocket() {
	try {
		const host = window.location.hostname
		const siteName = window.site_name || window.frappe?.boot?.sites?.[0]?.split('/').pop() || ''
		const port = window.location.port ? `:${window.location.port}` : ""
		const protocol = window.location.protocol === "https:" ? "https" : "http"
		const url = `${protocol}://${host}${port}/${siteName}`

		socket = io(url, {
			withCredentials: true,
			reconnectionAttempts: 5,
			timeout: 20000,
			transports: ['polling', 'websocket'],
		})
		return socket
	} catch (error) {
		console.warn("Socket.io initialization failed:", error)
		// Return a mock socket to prevent errors
		return {
			on: () => {},
			emit: () => {},
			disconnect: () => {},
			connect: () => {},
		}
	}
}

export function useSocket() {
	return socket
}
