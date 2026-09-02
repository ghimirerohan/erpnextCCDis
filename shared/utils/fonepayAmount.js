/**
 * Fonepay dynamic QR rejects / freezes on paisa (.xx).
 * Always charge whole rupees, rounding UP (ceiling).
 * 100 -> 100, 100.01 -> 101, 0.50 -> 1
 */
export function ceilFonepayAmount(value) {
	const n = Number(value)
	if (!Number.isFinite(n) || n <= 0) return 0
	const rupees = Number(n.toFixed(2))
	return Math.ceil(rupees)
}
