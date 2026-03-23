/**
 * A4 PDF for driver reconciliation customer list (shared across custom_erp frontends).
 * Boxed table, S.N., Nepali-style amounts, blank Payments column.
 *
 * Note: jsPDF built-in fonts only support "normal" and "bold". ~font-weight 500
 * is approximated with normal weight + standard text color (not bold).
 */
import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";
import NepaliDate from "nepali-date-converter";

/** Indian/Nepali lakh-crore grouping, two decimals (amounts only). */
export function formatNepaliAmount(value) {
	const n = Number(value);
	if (!Number.isFinite(n)) return "0.00";
	return new Intl.NumberFormat("en-IN", {
		minimumFractionDigits: 2,
		maximumFractionDigits: 2,
	}).format(n);
}

function safeFilenamePart(name) {
	return String(name || "reco")
		.replace(/[^\w\s-]/g, "")
		.replace(/\s+/g, "-")
		.slice(0, 48);
}

/** Bikram Sambat (English month names) + AD line for Kathmandu calendar day. */
function formatHeaderDates() {
	const now = new Date();
	const nd = NepaliDate.fromAD(now);
	const bsEn = nd.format("DD MMMM YYYY", "en");
	const adEn = new Intl.DateTimeFormat("en-GB", {
		day: "numeric",
		month: "long",
		year: "numeric",
		timeZone: "Asia/Kathmandu",
	}).format(now);
	return { line: `${bsEn} (BS) · ${adEn}`, bsEn, adEn };
}

/**
 * @param {object} opts
 * @param {object} opts.reco — { driver_name, loadsheet_number, name }
 * @param {object} opts.summary — for total (uses net_total_amount)
 * @param {Array} opts.lines — reco line items
 * @param {string} opts.driverName — display name
 */
export function downloadDriverRecoPdf({ reco, summary, lines, driverName }) {
	if (!lines?.length) {
		return { ok: false, message: "No lines to export." };
	}

	const sorted = [...lines].sort((a, b) =>
		String(a.customer_name || "").localeCompare(
			String(b.customer_name || ""),
			undefined,
			{
				sensitivity: "base",
			},
		),
	);

	const doc = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });
	const pageW = doc.internal.pageSize.getWidth();
	const margin = 12;
	let y = margin;

	const { line: dateLine } = formatHeaderDates();

	doc.setFontSize(9.5);
	doc.setFont("helvetica", "normal");
	doc.text(`Date: ${dateLine}`, margin, y);
	y += 6;

	const loadsheet = reco?.loadsheet_number?.trim?.() || "";
	const leftBits = [
		driverName || reco?.driver_name || "Driver",
		loadsheet,
	].filter(Boolean);
	const leftTitle = leftBits.join(", ");

	doc.setFontSize(11);
	doc.setFont("helvetica", "bold");
	doc.text(leftTitle, margin, y);

	const totalSum =
		Number(summary?.net_total_amount) ||
		sorted.reduce((s, l) => s + (Number(l.net_total_amount) || 0), 0);
	const totalLabel = `Total  ${formatNepaliAmount(totalSum)}`;
	doc.setFont("helvetica", "normal");
	doc.setFontSize(10);
	const totalW = doc.getTextWidth(totalLabel);
	doc.text(totalLabel, pageW - margin - totalW, y);
	y += 7;

	doc.setFontSize(7.5);
	doc.setTextColor(80, 80, 80);
	doc.text(
		"Amounts in NPR (Nepali grouping). Use Payments for remarks: cash, QR, cheque, return, etc.",
		margin,
		y,
	);
	doc.setTextColor(0, 0, 0);
	y += 4;

	const body = sorted.map((line, i) => [
		String(i + 1),
		String(line.customer || ""),
		String(line.customer_name || ""),
		formatNepaliAmount(line.net_total_amount),
		"",
	]);

	const innerW = pageW - margin * 2;
	const colSn = 11;
	const colOutlet = 24;
	const colAmt = 30;
	const colPay = 38;
	const colCust = innerW - colSn - colOutlet - colAmt - colPay;

	const padTight = { top: 0.8, right: 1, bottom: 0.8, left: 1 };
	const payMinMm = 6.8;

	// Body: normal weight (~w500 in CSS terms; PDF has no true medium master font)
	const bodyTextRgb = [38, 38, 38];

	autoTable(doc, {
		startY: y,
		head: [["S.N.", "Outlet code", "Customer", "Amount", "Payments"]],
		body,
		styles: {
			fontSize: 9,
			fontStyle: "normal",
			cellPadding: padTight,
			lineColor: [50, 50, 50],
			lineWidth: 0.15,
			valign: "middle",
			overflow: "linebreak",
			textColor: bodyTextRgb,
		},
		headStyles: {
			fillColor: [235, 236, 240],
			textColor: 20,
			fontStyle: "bold",
			fontSize: 8.5,
			halign: "center",
			valign: "middle",
			cellPadding: { top: 1.2, right: 1, bottom: 1.2, left: 1 },
		},
		columnStyles: {
			0: { cellWidth: colSn, halign: "center", fontStyle: "normal" },
			1: { cellWidth: colOutlet, font: "courier", fontStyle: "normal" },
			2: { cellWidth: colCust, fontStyle: "normal" },
			3: { cellWidth: colAmt, halign: "right", fontStyle: "normal" },
			4: { cellWidth: colPay, halign: "left", fontStyle: "normal" },
		},
		margin: { left: margin, right: margin },
		theme: "grid",
		didParseCell: (data) => {
			if (data.section === "body" && data.column.index === 4) {
				data.cell.styles.minCellHeight = payMinMm;
				data.cell.styles.cellPadding = {
					top: 1,
					right: 1.2,
					bottom: 1.4,
					left: 1.2,
				};
			}
		},
	});

	const safe = safeFilenamePart(driverName || reco?.driver_name);
	const d = new Date().toISOString().slice(0, 10);
	doc.save(`driver-reco-${safe}-${d}.pdf`);
	return { ok: true };
}
