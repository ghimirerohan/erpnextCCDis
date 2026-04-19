/**
 * Offline support for dailyrecoentry: cache driver reco reads, queue payment writes.
 */
const DB_NAME = 'dailyrecoentry-offline-v1'
const DB_VERSION = 1
const QUEUE_STORE = 'paymentQueue'
const CACHE_STORE = 'recoCache'

const UPDATE_METHOD = 'custom_erp.api.payment_reco.update_payment_entry'

function emitQueueEvent(count) {
	window.dispatchEvent(
		new CustomEvent('dailyrecoentry-offline-queue', { detail: { count } })
	)
}

function openDb() {
	return new Promise((resolve, reject) => {
		const req = indexedDB.open(DB_NAME, DB_VERSION)
		req.onerror = () => reject(req.error)
		req.onsuccess = () => resolve(req.result)
		req.onupgradeneeded = (e) => {
			const db = e.target.result
			if (!db.objectStoreNames.contains(QUEUE_STORE)) {
				db.createObjectStore(QUEUE_STORE, { keyPath: 'id', autoIncrement: true })
			}
			if (!db.objectStoreNames.contains(CACHE_STORE)) {
				db.createObjectStore(CACHE_STORE, { keyPath: 'key' })
			}
		}
	})
}

function cacheKey(driverName) {
	return driverName || '__default__'
}

export async function setCachedDriverReco(driverName, apiResponse) {
	try {
		const db = await openDb()
		await new Promise((resolve, reject) => {
			const tx = db.transaction(CACHE_STORE, 'readwrite')
			tx.objectStore(CACHE_STORE).put({
				key: cacheKey(driverName),
				payload: apiResponse,
				cachedAt: Date.now(),
			})
			tx.oncomplete = () => resolve()
			tx.onerror = () => reject(tx.error)
		})
	} catch (e) {
		console.warn('[recoOffline] cache write failed', e)
	}
}

export async function getCachedDriverReco(driverName) {
	try {
		const db = await openDb()
		return await new Promise((resolve, reject) => {
			const tx = db.transaction(CACHE_STORE, 'readonly')
			const req = tx.objectStore(CACHE_STORE).get(cacheKey(driverName))
			req.onsuccess = () => resolve(req.result?.payload ?? null)
			req.onerror = () => reject(req.error)
		})
	} catch (e) {
		console.warn('[recoOffline] cache read failed', e)
		return null
	}
}

async function getQueueCount() {
	try {
		const db = await openDb()
		return await new Promise((resolve, reject) => {
			const tx = db.transaction(QUEUE_STORE, 'readonly')
			const req = tx.objectStore(QUEUE_STORE).count()
			req.onsuccess = () => resolve(req.result)
			req.onerror = () => reject(req.error)
		})
	} catch {
		return 0
	}
}

async function enqueuePaymentUpdate(paymentData) {
	const db = await openDb()
	await new Promise((resolve, reject) => {
		const tx = db.transaction(QUEUE_STORE, 'readwrite')
		tx.objectStore(QUEUE_STORE).add({ payload: paymentData, createdAt: Date.now() })
		tx.oncomplete = () => resolve()
		tx.onerror = () => reject(tx.error)
	})
	const n = await getQueueCount()
	emitQueueEvent(n)
}

async function drainQueue(callFn) {
	const db = await openDb()
	const items = await new Promise((resolve, reject) => {
		const out = []
		const tx = db.transaction(QUEUE_STORE, 'readonly')
		const req = tx.objectStore(QUEUE_STORE).openCursor()
		req.onsuccess = (e) => {
			const c = e.target.result
			if (c) {
				out.push({ id: c.primaryKey, ...c.value })
				c.continue()
			} else resolve(out)
		}
		req.onerror = () => reject(req.error)
	})

	for (const row of items) {
		try {
			const r = await callFn(UPDATE_METHOD, row.payload)
			if (r && r.success) {
				await new Promise((resolve, reject) => {
					const tx2 = db.transaction(QUEUE_STORE, 'readwrite')
					tx2.objectStore(QUEUE_STORE).delete(row.id)
					tx2.oncomplete = () => resolve()
					tx2.onerror = () => reject(tx2.error)
				})
			} else {
				break
			}
		} catch {
			break
		}
	}
	const n = await getQueueCount()
	emitQueueEvent(n)
}

function isLikelyNetworkError(err) {
	if (!navigator.onLine) return true
	const msg = (err && (err.message || err.toString())) || ''
	if (/network|failed to fetch|load failed|internet|offline/i.test(msg)) return true
	if (err && (err.status === 0 || err.status === 503)) return true
	return false
}

/**
 * Call update_payment_entry, or enqueue when offline / network failure.
 * @returns {Promise<{success: boolean, message?: string, queued?: boolean}>}
 */
export async function callUpdatePaymentEntry(callFn, paymentData) {
	if (!navigator.onLine) {
		await enqueuePaymentUpdate(paymentData)
		return { success: true, queued: true, message: 'Queued for sync when online' }
	}
	try {
		const response = await callFn(UPDATE_METHOD, paymentData)
		if (response && response.success) {
			return response
		}
		return response || { success: false, message: 'Unknown error' }
	} catch (e) {
		if (isLikelyNetworkError(e)) {
			await enqueuePaymentUpdate(paymentData)
			return { success: true, queued: true, message: 'Queued for sync when online' }
		}
		throw e
	}
}

export async function getPendingPaymentQueueCount() {
	return getQueueCount()
}

let syncInitialized = false

export function initRecoOfflineSync(callFn) {
	if (syncInitialized || typeof window === 'undefined') return
	syncInitialized = true

	const runFlush = () => {
		if (!navigator.onLine) return
		drainQueue(callFn).catch((e) => console.warn('[recoOffline] flush', e))
	}

	window.addEventListener('online', runFlush)
	// First load: try draining leftover queue
	setTimeout(runFlush, 2000)
}
