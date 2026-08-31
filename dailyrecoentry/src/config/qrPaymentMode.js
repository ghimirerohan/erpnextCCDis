/**
 * Toggle Fonepay QR behaviour for Daily Reco Entry.
 * - 'static': show fixed placard image + mandatory remarks (no Fonepay API / no Fonepay QR Transaction link).
 * - 'dynamic': original flow (create_dynamic_qr_for_company, WebSocket, check_status, link transaction doc).
 */
export const QR_PAYMENT_MODE = 'dynamic' // 'static' | 'dynamic'

export const STATIC_FONEPAY_QR_IMAGE_URL =
	'/assets/custom_erp/images/fonepay-static-qr.png'

export function isStaticQrMode() {
	return QR_PAYMENT_MODE === 'static'
}

export function isDynamicQrMode() {
	return QR_PAYMENT_MODE === 'dynamic'
}
