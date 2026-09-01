from unittest.mock import patch

import frappe

from custom_erp.api.payment_reco import get_all_active_recos


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
