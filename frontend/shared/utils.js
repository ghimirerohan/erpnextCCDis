export function fmtNPR(amount) {
	return `NPR ${Number(amount || 0).toLocaleString('en-NP', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

export function fmtDate(dateStr) {
	if (!dateStr) return ''
	return new Date(dateStr).toLocaleDateString('en-NP', {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
	})
}

export const PAYMENT_MODES = ['Cash', 'QR', 'Cheque', 'Credit', 'Return']

export const MODE_COLORS = {
	Cash: 'green',
	QR: 'blue',
	Cheque: 'orange',
	Credit: 'red',
	Return: 'gray',
}

export const NPR_DENOMS = [1000, 500, 100, 50, 20, 10, 5, 2, 1]
