import { io } from 'socket.io-client'

export function initSocket() {
	if (typeof window === 'undefined') return null
	if (window.__ccdis_socket) return window.__ccdis_socket
	const host = window.location.origin
	const socket = io(host, {
		path: '/socket.io',
		withCredentials: true,
		transports: ['websocket', 'polling'],
	})
	window.__ccdis_socket = socket
	return socket
}
