# Copyright (c) 2022, FinByz Tech Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []

	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_columns(filters):

	condition = f"and posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"

	# cols = frappe.db.sql(f"""
	# 	SELECT 
	# 		name
	# 	FROM
	# 		`tabSales Invoice`
	# 	WHERE
	# 		docstatus = 1 and is_return = 0 and is_opening = 'No' {condition}
	# """, as_dict = 1)
	cols = frappe.db.sql(f"""
		SELECT 
			bill_no
		FROM
			`tabPurchase Invoice`
		WHERE
			docstatus = 1 and is_return = 0 and is_opening = 'No' and supplier = "MULTITECH GLOBAL LOGISTICS & SERVICES - 3" {condition}
		""", as_dict = 1)

	columns = [
		{"label": _("Item Code"),"fieldname": "item_code","fieldtype": "Link","options": "Item", "width": 200},
		{"label": _("Item Name"),"fieldname": "item_name","fieldtype": "Data", "width": 200},
		{"label": _("HSN Code"),"fieldname": "gst_hsn_code","fieldtype": "Link","options": "GST HSN Code", "width": 200},
	]
	for row in cols:
		columns += [{"label": _(f"{row.bill_no}"),"fieldname": f"{row.bill_no}","fieldtype": "Data","align": 'right', "width": 200},]

	return columns

def get_data(filters):
	condition = f"and pi.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"

	# data = frappe.db.sql(f"""
	# 	SELECT
	# 		si.name, sii.item_code, sii.item_name, sii.gst_hsn_code, sii.base_amount, si.base_total, si.base_grand_total
	# 	FROM
	# 		`tabSales Invoice Item` as sii
	# 		JOIN `tabSales Invoice` as si on si.name = sii.parent
	# 	WHERE
	# 		si.docstatus = 1 and si.is_return = 0 and si.is_opening = 'No' {condition}
	# """, as_dict = 1)
	data = frappe.db.sql(f"""
		SELECT
			pi.name, pi.bill_no, pii.item_code, pii.item_name, pii.gst_hsn_code, pii.base_amount, pi.base_total, pi.base_grand_total
		FROM
			`tabPurchase Invoice Item` as pii
		JOIN `tabPurchase Invoice` as pi on pi.name = pii.parent
		WHERE
			pi.docstatus = 1 and pi.is_return = 0 and pi.is_opening = 'No' and pi.supplier = "MULTITECH GLOBAL LOGISTICS & SERVICES - 3" {condition}
			""", as_dict = 1)

	si_dict = {}
	si_data = []
	add_data = []
	si_list = []
	tax_dict = {}
	tax_lst = []

	taxable_dict = [{'gst_hsn_code': 'Total Taxable value'}]
	total_dict = [{'gst_hsn_code': 'Total'}]

	for row in data:
		if si_dict.get(row.item_code):
			si_dict[row.item_code][row.bill_no] = row.base_amount
		else:
			si_dict[row.item_code] = {'item_code': row.item_code, 'item_name': row.item_name, row.bill_no: row.base_amount, 'gst_hsn_code': row.gst_hsn_code}

		taxable_dict[0][row.bill_no] = row.base_total
		total_dict[0][row.bill_no] = row.base_grand_total

		
		if row.bill_no not in si_list:
			si_list.append(row.bill_no)

			taxes = frappe.db.get_all("Purchase Taxes and Charges", {'parent': row.name}, ['account_head', 'base_tax_amount', 'add_deduct_tax'])

			if taxes:
				for t in taxes:
					if t.add_deduct_tax == "Deduct":
						t.base_tax_amount = t.base_tax_amount * -1
					if tax_dict.get(t.account_head):
						tax_dict[t.account_head].update({row.bill_no : t.base_tax_amount})
					else:
						tax_dict.update({t.account_head : {'gst_hsn_code': t.account_head, row.bill_no : t.base_tax_amount}})

	for tax in tax_dict:
		tax_lst.append(tax_dict[tax])

	for row in si_dict:
		if si_dict[row]:
			si_data.append(si_dict[row])

	add_data = taxable_dict + tax_lst + total_dict
	return si_data + add_data