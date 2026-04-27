app_name = "custom_erp"
app_title = "Custom Erp"
app_publisher = "Rohan Ghimire"
app_description = "Customization Of ERPNext Through Overrides and Extensions"
app_email = "ghimirerohan@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "custom_erp",
# 		"logo": "/assets/custom_erp/logo.png",
# 		"title": "Custom Erp",
# 		"route": "/custom_erp",
# 		"has_permission": "custom_erp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/custom_erp/css/custom_erp.css"
# app_include_css = [
#    "/assets/custom_erp/css/nepali.datepicker.v5.0.5.min.css"
# ]
# app_include_js = [
#    "/assets/custom_erp/js/nepali.datepicker.v5.0.5.min.js",
#    "/assets/custom_erp/js/override_date.js",
#    "/assets/custom_erp/js/sajan.nepaliFunctions.min.js"
# ]

fixtures = [
    {
        "dt": "Role",
        "filters": [["role_name", "in", ["Field User", "CC Admin"]]],
    },
    # Tracks added/modified fields, even in core doctypes
    "Custom Field",
    # Tracks changes to field properties (read-only, default values, etc.)
    "Property Setter",
    # Tracks changes to print formats
    "Print Format",
    # Tracks custom scripts (JS customizations)
    "Custom Script",
    # Tracks workflow rules & states
    "Workflow",
    "Workflow State",
    "Workflow Action",
    # Tracks custom reports
    "Report",
    # Tracks role changes
    "Role",
    # Tracks client-side scripts attached to reports
    "Report Script",
    # Tracks custom pages
    "Page",
]


# include js, css files in header of web template
# web_include_css = "/assets/custom_erp/css/custom_erp.css"
# web_include_js = "/assets/custom_erp/js/custom_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "custom_erp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "custom_erp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "custom_erp.utils.jinja_methods",
# 	"filters": "custom_erp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "custom_erp.install.before_install"
after_install = "custom_erp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "custom_erp.uninstall.before_uninstall"
# after_uninstall = "custom_erp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "custom_erp.utils.before_app_install"
# after_app_install = "custom_erp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "custom_erp.utils.before_app_uninstall"
# after_app_uninstall = "custom_erp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "custom_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "hourly": [
        "custom_erp.api.fonepay.scheduled_process_unprocessed_qrs"
    ],
}

# Testing
# -------

# before_tests = "custom_erp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "custom_erp.event.get_events"
# }

# Apply valuation overrides via monkey patch in app startup; keep whitelisted overrides minimal
override_whitelisted_methods = {
	"erpnext.stock.get_item_details.get_valuation_rate": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.get_valuation_rate_for_item_details"
}

# Whitelist Fonepay API methods
whitelisted_methods = [
	"custom_erp.api.fonepay.create_dynamic_qr",
	"custom_erp.api.fonepay.listen_to_ws",
	"custom_erp.api.fonepay.check_qr_status",
	"custom_erp.api.fonepay.finalize_payment_from_ws",
	"custom_erp.api.fonepay.process_unprocessed_qrs",
	"custom_erp.api.fonepay.scheduled_process_unprocessed_qrs",
	# ADDED BY AI: UPLOAD_SALES - Upload Sales API methods
	"custom_erp.api.uploadsales.transform_and_preview",
	"custom_erp.api.uploadsales.enqueue_import_job",
	"custom_erp.api.uploadsales.get_drivers",
	"custom_erp.api.uploadsales.get_vehicles",
	"custom_erp.api.uploadsales.get_job_progress",
	"custom_erp.api.uploadsales.run_data_import",
	"custom_erp.api.uploadsales.test_api",
	"custom_erp.api.uploadsales.test_api_v2",
	"custom_erp.api.uploadsales.debug_import_status",
	"custom_erp.api.uploadsales.download_error_csv",
	# ADDED BY AI: DAILY_PAYMENT_RECO - Payment Reconciliation API methods
	"custom_erp.api.payment_reco.parse_and_validate_csv",
	"custom_erp.api.payment_reco.get_drivers_list",
	"custom_erp.api.payment_reco.create_payment_recos",
	"custom_erp.api.payment_reco.get_all_active_recos",
	"custom_erp.api.payment_reco.get_driver_reco_data",
	"custom_erp.api.payment_reco.update_payment_entry",
	"custom_erp.api.payment_reco.generate_qr_no_payment_entry",
	"custom_erp.api.payment_reco.compress_and_attach_image",
	"custom_erp.api.payment_reco.create_cheque_taageta",
	"custom_erp.api.payment_reco.get_current_nepali_date",
	"custom_erp.api.payment_reco.settle_all_pending_as_cash",
	"custom_erp.api.payment_reco.reassign_pending_reco_lines",
    # ADDED BY AI: AI_ASSISTANT - Gemini Live Relay methods
    "custom_erp.api.live_relay.start_conversation",
    "custom_erp.api.live_relay.push_audio_chunk",
    "custom_erp.api.live_relay.stop_conversation",
    "custom_erp.api.live_relay.test_gemini_connection"
]

on_login = "custom_erp.oauth_hooks.assign_roles_on_login"

# --- Print Format Type ---
# Register ReportBro as a custom print format type
# no custom print format types

# --- Document Events ---
# Consolidated so Sales Invoice normalization runs before core validations
# IMPORTANT: The stock valuation hooks have been modified to preserve Sales Invoice rates
# while still updating valuation_rate for stock purposes. See stock_ledger_override.py for details.
doc_events = {
    "Sales Invoice": {
        # "before_validate": "custom_erp.custom_erp.sales_invoice.sales_invoice.before_validate",
        "before_insert": [
            "custom_erp.custom_erp.sales_invoice.sales_invoice.before_insert",
            "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate_before_gl_creation",
        ],
        "before_save":[
             "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        ],
        "on_submit": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
    },
    "Purchase Invoice": {
        "before_save": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "on_submit": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "before_insert": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate_before_gl_creation",
    },
    "Stock Entry": {
        "before_save": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "on_submit": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "before_insert": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate_before_gl_creation",
    },
    "Delivery Note": {
        "before_save": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "on_submit": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "before_insert": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate_before_gl_creation",
    },
    "Purchase Receipt": {
        "before_save": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "on_submit": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "before_insert": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate_before_gl_creation",
    },
    "Stock Reconciliation": {
        "before_save": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "on_submit": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        "before_insert": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate_before_gl_creation",
    },
    # "Stock Reconciliation": {
    #     "before_save": "custom_erp.custom_erp.stock_reconciliation.stock_reconciliation.before_save",
        
    # },
    "Stock Ledger Entry": {
        "before_insert": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_sle_fixed_valuation_rate",
    },
    "Payment Entry": {
        "on_submit": "custom_erp.api.realtime.on_payment_entry_submit",
    },
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "custom_erp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# DISABLED: Causing redirect errors - apps work via website_route_rules
# before_request = ["custom_erp.utils.before_request"]
# after_request = ["custom_erp.utils.after_request"]

# API Endpoints
# ----------------

# Include Nepali Date Picker library and custom date controls
app_include_js = [
    "/assets/custom_erp/js/invoice_scanner.js"
]

app_include_css = []

# Boot session hook to add Nepali calendar setting to frappe.boot
# boot_session = "custom_erp.boot.get_boot_settings"

# Ensure our monkey patches are applied at session start and after migration
on_session_creation = [
	"custom_erp.custom_erp.stock_valuation.stock_ledger_override.force_apply_overrides",
	# "custom_erp.patches.website_auth_override.override_website_auth"  # Disabled - render_page doesn't exist
]

after_migrate = [
	"custom_erp.custom_erp.stock_valuation.stock_ledger_override.force_apply_overrides",
	# "custom_erp.patches.website_auth_override.override_website_auth"  # Disabled - render_page doesn't exist
]

# Job Events
# ----------
# before_job = ["custom_erp.utils.before_job"]
# after_job = ["custom_erp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"custom_erp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
override_doctype_class = {
	"Purchase Invoice": "custom_erp.custom_erp.purchase_invoice.purchase_invoice_override.PurchaseInvoiceOverride",
	# Ensure Opening Invoice Creation Tool uses our override to sanitize CSV values
	# and inject a default placeholder item where item fields are blank
	"Opening Invoice Creation Tool": "custom_erp.custom_erp.opening_invoice_tool.opening_invoice_creation_tool_override.OpeningInvoiceCreationToolOverride",
	# Stock Reconciliation override for UOM conversion and serial/batch bundle handling
	# "Stock Reconciliation": "custom_erp.custom_erp.stock_reconciliation.stock_reconciliation_override.StockReconciliationOverride",
	# Repost Item Valuation override to allow cancellation when cancelling Stock Reconciliation
	"Repost Item Valuation": "custom_erp.custom_erp.stock_reconciliation.repost_item_valuation_override.RepostItemValuationOverride"
}

# Route each app at root level
# PWA routes: sw.js and manifest.json are served via API endpoints (custom_erp.api.pwa)
website_route_rules = [
    # QRPay
    {"from_route": "/qrpay", "to_route": "qrpay"},
    {"from_route": "/qrpay/<path:subpath>", "to_route": "qrpay"},
    # QRPay Admin
    {"from_route": "/qrpay-admin", "to_route": "qrpay-admin"},
    {"from_route": "/qrpay-admin/<path:subpath>", "to_route": "qrpay-admin"},
    # Scanner
    {"from_route": "/scanner", "to_route": "scanner"},
    {"from_route": "/scanner/<path:subpath>", "to_route": "scanner"},
    # Pay Dashboard
    {"from_route": "/pay-dashboard", "to_route": "pay-dashboard"},
    {"from_route": "/pay-dashboard/<path:subpath>", "to_route": "pay-dashboard"},
    # Upload Sales
    {"from_route": "/uploadsales", "to_route": "uploadsales"},
    {"from_route": "/uploadsales/<path:subpath>", "to_route": "uploadsales"},
    # Upload Reco
    {"from_route": "/uploadreco", "to_route": "uploadreco"},
    {"from_route": "/uploadreco/<path:subpath>", "to_route": "uploadreco"},
    # Daily Reco Entry
    {"from_route": "/dailyrecoentry", "to_route": "dailyrecoentry"},
    {"from_route": "/dailyrecoentry/<path:subpath>", "to_route": "dailyrecoentry"},
    # Home
    {"from_route": "/home", "to_route": "home"},
    {"from_route": "/home/<path:subpath>", "to_route": "home"},
    # Test Login
    {"from_route": "/testlogin", "to_route": "testlogin"},
    {"from_route": "/testlogin/<path:subpath>", "to_route": "testlogin"},
    # CCDis v2 — Field / Admin SPAs
    {"from_route": "/field-app", "to_route": "field-app"},
    {"from_route": "/field-app/<path:subpath>", "to_route": "field-app"},
    {"from_route": "/admin-app", "to_route": "admin-app"},
    {"from_route": "/admin-app/<path:subpath>", "to_route": "admin-app"},
]

