from . import __version__ as app_version

app_name = "agrotrade"
app_title = "Agrotrade"
app_publisher = "Finbyz tech pvt ltd"
app_description = "Custom App for AgroTrade"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@finbyz.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/agrotrade/css/agrotrade.css"
app_include_js = [
	# "/assets/js/agrotrade.min.js",
	"agrotrade.bundle.js"
]
# include js, css files in header of web template
# web_include_css = "/assets/agrotrade/css/agrotrade.css"
# web_include_js = "/assets/agrotrade/js/agrotrade.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "agrotrade/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
app_include_css = [
    # "/assets/agrotrade/css/dialogue.css"
    "agrotrade.bundle.css"
	]

# include js in doctype views
doctype_js = {
	"Purchase Order" : "public/js/purchase_order.js",
	"Purchase Receipt" : "public/js/purchase_receipt.js",
	"Purchase Invoice" : "public/js/purchase_invoice.js",
	"Sales Invoice" : "public/js/doctypes_js/sales_invoice.js", 
	"Journal Entry":"public/js/journal_entry.js",
	"Pre Shipment":"public/js/pre_shipment.js",
	"Customer":"public/js/customer.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "agrotrade.install.before_install"
# after_install = "agrotrade.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "agrotrade.uninstall.before_uninstall"
# after_uninstall = "agrotrade.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "agrotrade.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Payment Entry": "agrotrade.agrotrade.doc_events.payment_entry.CustomPaymentEntry",
	"GL Entry": "agrotrade.agrotrade.doc_events.gl_entry.CustomGLEntry"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"on_submit": "agrotrade.api.si_on_submit",
		"on_cancel": "agrotrade.agrotrade.doc_events.sales_invoice.on_cancel"
	},
	"Payment Entry": {
		"on_submit": "agrotrade.api.pe_on_submit",
		"before_cancel": "agrotrade.api.pe_on_cancel",
	},
	"Batch": {
		'before_naming': "agrotrade.batch_valuation.override_batch_autoname",
	},
	"Purchase Receipt": {
		"validate": [
			"agrotrade.batch_valuation.pr_validate",
		],
		"on_cancel": "agrotrade.batch_valuation.pr_on_cancel",
	},
	"Purchase Invoice": {
		"validate": "agrotrade.batch_valuation.pi_validate",
		"on_cancel": "agrotrade.batch_valuation.pi_on_cancel",
	},
	"Landed Cost Voucher": {
		"validate": [
			"agrotrade.batch_valuation.lcv_validate",
		],
		"on_submit": "agrotrade.batch_valuation.lcv_on_submit",
		"on_cancel": [
			"agrotrade.batch_valuation.lcv_on_cancel",
		],
	},
	'Journal Entry':{
		'validate':"agrotrade.agrotrade.doc_events.journal_entry.validate",
		'on_cancel':"agrotrade.agrotrade.doc_events.journal_entry.on_cancel"
	},
	"Rodtap Claimed Management":{
		"on_submit":"agrotrade.agrotrade.doctype.rodtap_claimed_management.rodtap_claimed_management.create_jv_on_submit"
	},

	
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"agrotrade.tasks.all"
# 	],
# 	"daily": [
# 		"agrotrade.tasks.daily"
# 	],
# 	"hourly": [
# 		"agrotrade.tasks.hourly"
# 	],
# 	"weekly": [
# 		"agrotrade.tasks.weekly"
# 	]
# 	"monthly": [
# 		"agrotrade.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "agrotrade.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "agrotrade.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "agrotrade.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"agrotrade.auth.validate"
# ]

from agrotrade.batch_valuation_overrides import get_supplied_items_cost,set_incoming_rate_buying,set_incoming_rate_selling,get_rate_for_return,get_incoming_rate,process_sle,get_args_for_incoming_rate

# Buying controllers
from erpnext.controllers.buying_controller import BuyingController
BuyingController.get_supplied_items_cost = get_supplied_items_cost
BuyingController.set_incoming_rate = set_incoming_rate_buying

# Selling controllers
from erpnext.controllers.selling_controller import SellingController
SellingController.set_incoming_rate = set_incoming_rate_selling

# sales and purchase return
from erpnext.controllers import sales_and_purchase_return
sales_and_purchase_return.get_rate_for_return =  get_rate_for_return

# Document Events
# ---------------
# Hook on document methods and events
import erpnext
erpnext.stock.utils.get_incoming_rate = get_incoming_rate

# stock_ledger
from erpnext.stock.stock_ledger import update_entries_after
update_entries_after.process_sle =  process_sle

# stock entry
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
StockEntry.get_args_for_incoming_rate = get_args_for_incoming_rate

# e invoice override
import erpnext

# from agrotrade.e_invoice_override import update_invoice_taxes,get_invoice_value_details
# erpnext.regional.india.e_invoice.utils.update_invoice_taxes = update_invoice_taxes
# erpnext.regional.india.e_invoice.utils.get_invoice_value_details = get_invoice_value_details


from erpnext.accounts.doctype.payment_reconciliation.payment_reconciliation import PaymentReconciliation
from agrotrade.api import add_invoice_entries_with_bill_no
PaymentReconciliation.add_invoice_entries =add_invoice_entries_with_bill_no


# Broker Changes
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt
from agrotrade.agrotrade.doc_events.purchase_receipt import validate_with_previous_doc as pr_validate_with_previous_doc
PurchaseReceipt.validate_with_previous_doc = pr_validate_with_previous_doc

from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
from agrotrade.agrotrade.doc_events.purchase_invoice import validate_with_previous_doc as pi_validate_with_previous_doc
PurchaseInvoice.validate_with_previous_doc = pi_validate_with_previous_doc

#Gross Profit Report Override
from erpnext.accounts.report.gross_profit import gross_profit
from agrotrade.agrotrade.report.gross_profit import execute
gross_profit.execute = execute

from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
from agrotrade.agrotrade.doc_events.purchase_invoice import set_expense_account as set_expense_account_custom
PurchaseInvoice.set_expense_account = set_expense_account_custom

from india_compliance.gst_india.report.gst_itemised_sales_register import gst_itemised_sales_register
from  agrotrade.agrotrade.report.gst_itemised_sales_register import execute as sales_register_execute
gst_itemised_sales_register.execute = sales_register_execute

# from india_compliance.gst_india.report.gst_itemised_purchase_register import gst_itemised_purchase_register
from india_compliance.gst_india.report.gst_itemised_purchase_register import gst_itemised_purchase_register
from agrotrade.agrotrade.report.gst_itemised_purchase_register import execute as purchase_register_execute
gst_itemised_purchase_register.execute = purchase_register_execute


# from agrotrade.api import before_naming
# from finbyzerp import api
# api.before_naming = before_naming


from erpnext.accounts.report.tds_payable_monthly import tds_payable_monthly
from agrotrade.agrotrade.report.tds_payable_monthly import execute
tds_payable_monthly.execute = execute


from erpnext.selling.report.sales_order_analysis import sales_order_analysis
from agrotrade.agrotrade.report.sales_order_analysis import execute
sales_order_analysis.execute = execute


from erpnext.accounts.report.general_ledger import general_ledger
from agrotrade.agrotrade.report.general_ledger import execute
general_ledger.execute = execute