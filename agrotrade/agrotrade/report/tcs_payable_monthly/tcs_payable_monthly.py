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
	columns = []
	columns += [{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 120},
		{"label": _("Voucher #"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 140},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
		{"label": _("TCS Rate"), "fieldname": "rate", "fieldtype": "Percent","width": 80},
		{"label": _("Total Amount"), "fieldname": "total_amount", "fieldtype": "Currency","width": 120},
		{"label": _("Amount"), "fieldname": "credit", "fieldtype": "Currency","width": 120},
	]
	return columns

def get_data(filters):
	return frappe.db.sql(f"""
		SELECT 
			gl.credit, gl.voucher_type, gl.voucher_no, (gl.credit / stc.rate) * 100 as total_amount, si.customer, si.posting_date, stc.rate
		FROM
			`tabGL Entry` as gl
			INNER JOIN `tabAccount` as acc on gl.account = acc.name and acc.parent_account = 'TCS  PAYABLE F.Y.22-23 - LSPL'
			JOIN `tabSales Invoice` as si on si.name = gl.voucher_no and si.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'
			JOIN `tabSales Taxes and Charges` as stc on stc.parent = si.name and stc.account_head = gl.account
		WHERE
			gl.voucher_type = 'Sales Invoice' and gl.is_opening = 'No' 
	""", as_dict = 1)