# Copyright (c) 2022, Finbyz tech pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{ "label": _("Item Code"),"fieldname": "item_code","fieldtype": "Link","options":"Item","width": 180},
		{ "label": _("Item Name"),"fieldname": "item_name","fieldtype": "Data","width": 200},
		{ "label": _("State Name"),"fieldname": "gst_state","fieldtype": "Data","width": 150},
		{ "label": _("Quantity"),"fieldname": "qty","fieldtype": "Float","width": 120},
		{ "label": _("Purchase Amount"),"fieldname": "purchase_amount","fieldtype": "Currency","width": 120}
	]
	return columns

def get_data(filters):
	condition = f" and pi.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"

	return frappe.db.sql(f"""
		SELECT
			pii.item_code, pii.item_name, adrs.gst_state, sum(pii.qty) as qty, sum(pii.base_amount) as purchase_amount
		FROM
			`tabPurchase Invoice Item` as pii
		JOIN
			`tabPurchase Invoice` as pi on pi.name = pii.parent
		LEFT JOIN
			`tabAddress` as adrs on adrs.name = pi.supplier_address
		WHERE
			pi.docstatus = 1 and pi.is_return = 0 and pi.is_opening = 0 and pi.naming_series = 'RM.-.company_series./.fiscal./.###' {condition}
		GROUP BY
			pii.item_code, adrs.gst_state
	""", as_dict = 1)