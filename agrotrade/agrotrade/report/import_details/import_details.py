# Copyright (c) 2022, FinByz Tech Pvt Ltd and contributors
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
		{
			"label": _("Part Name"),
			"fieldname": "party_name",
			"fieldtype": "Link",
			"options":"Supplier", 
			"width": 200
		},
		{
			"label": _("Invoice No"),
			"fieldname": "invoice_no",
			"fieldtype": "Data", 
			"width": 200
		},
		{
			"label": _("BE NO"),
			"fieldname": "be_no",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("BE Date"),
			"fieldname": "be_date",
			"fieldtype": "Date", 
			"width": 200
		},
		{
			"label": _("Taxable Value"),
			"fieldname": "taxable_value",
			"fieldtype": "Currency", 
			"width": 150
		},
		{
			"label": _("IGST"),
			"fieldname": "igst",
			"fieldtype": "Currency", 
			"width": 150
		},]

	return columns
def get_data(filters):
	
	data = frappe.db.sql("""
		SELECT 
			pi.supplier as party_name ,pi.name as invoice_no ,pi.base_total_taxes_and_charges as igst ,pi.base_total as taxable_value
		from
			`tabPurchase Invoice` pi
		where
			pi.currency != "INR" and
			 pi.docstatus = 1 
			and pi.posting_date between '{}' and '{}'
		
	""".format(filters.from_date,filters.to_date),as_dict = 1)
	
	return data