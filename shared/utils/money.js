/**
 * Money helpers for Daily Reco / Fonepay.
 * - roundMoney: max 2 decimal places (paisa)
 * - ceilRupees: whole rupees, rounding UP (cash, QR, cheque)
 */

export function roundMoney(value) {
	const n = Number(value)
	if (!Number.isFinite(n)) return 0
	return Math.round((n + Number.EPSILON) * 100) / 100
}

export function ceilRupees(value) {
	const n = Number(value)
	if (!Number.isFinite(n) || n <= 0) return 0
	return Math.ceil(n - 1e-9)
}
