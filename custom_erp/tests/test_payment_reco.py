from unittest.mock import patch

import frappe

from custom_erp.api.payment_reco import (
	_apply_collection_rounding,
	format_reco_option_label,
	get_all_active_recos,
	pick_default_reco,
)
from custom_erp.money import ceil_rupees, round_money


def test_round_money_clamps_to_two_decimals():
	assert round_money(150.376) == 150.38
	assert round_money(150.374) == 150.37
	assert round_money("100.1") == 100.10
	assert round_money(None) == 0.0
	assert round_money(1.005) in (1.00, 1.01)


def test_ceil_rupees_rounds_paisa_up():
	assert ceil_rupees(100) == 100
	assert ceil_rupees(100.01) == 101
	assert ceil_rupees(150.37) == 151
	assert ceil_rupees(0) == 0
	assert ceil_rupees(-5) == 0


def test_apply_collection_rounding_cash_and_cheque_like_qr():
	result = _apply_collection_rounding(
		150.37, 0, 0, 0, 150.37, 0, 0
	)
	assert result["cash"] == 151
	assert result["additional"] == 0.63
	assert result["remaining"] == 0
	assert result["credit"] == 0

	result = _apply_collection_rounding(
		150.37, 0, 0, 0, 0, 0, 150.37
	)
	assert result["cheque"] == 151
	assert result["additional"] == 0.63
	assert result["remaining"] == 0

	result = _apply_collection_rounding(
		150.37, 0, 0, 0, 0, 150.37, 0
	)
	assert result["qr"] == 151
	assert result["additional"] == 0.63
	assert result["remaining"] == 0


def test_apply_collection_rounding_credit_and_return_stay_two_decimals():
	result = _apply_collection_rounding(
		100.333, 1.111, 2.222, 3.333, 0, 0, 0
	)
	assert result["initial"] == 100.33
	assert result["additional"] == 1.11
	assert result["return_amt"] == 2.22
	assert result["credit"] == 3.33
	# remaining = 100.33 + 1.11 - 2.22 - 3.33 = 95.89
	assert result["remaining"] == 95.89


def test_get_all_active_recos_without_company_does_not_pass_none():
	"""frappe.db.sql wraps a lone None as (None,), which breaks pymysql mogrify."""
	with patch.object(frappe.db, "sql", return_value=[]) as mock_sql:
		result = get_all_active_recos()

	assert result["success"] is True
	assert result["data"] == []
	assert mock_sql.called
	values = mock_sql.call_args[0][1]
	assert values is not None
	assert tuple(values) == ()


def test_get_all_active_recos_with_company_uses_placeholder():
	with patch.object(frappe.db, "sql", return_value=[]) as mock_sql:
		result = get_all_active_recos(company="Test Company")

	assert result["success"] is True
	values = mock_sql.call_args[0][1]
	assert tuple(values) == ("Test Company",)
	assert "%s" in mock_sql.call_args[0][0]


def test_pick_default_reco_prefers_today_even_if_settled():
	options = [
		{"name": "OLD-UNSETTLED", "is_today": False, "settled": 0},
		{"name": "TODAY-SETTLED", "is_today": True, "settled": 1},
	]
	assert pick_default_reco(options)["name"] == "TODAY-SETTLED"
	assert pick_default_reco(options, "OLD-UNSETTLED")["name"] == "OLD-UNSETTLED"
	assert pick_default_reco([{"name": "YESTERDAY", "is_today": False}]) is None
	assert pick_default_reco([], "MISSING") is None


def test_format_reco_option_label_marks_today():
	label = format_reco_option_label("2026-09-05", True, True)
	assert label.startswith("Today — 2026-09-05")
	assert "Settled" in label
	older = format_reco_option_label("2026-09-04", False, False)
	assert older.startswith("2026-09-04")
	assert "Today" not in older
