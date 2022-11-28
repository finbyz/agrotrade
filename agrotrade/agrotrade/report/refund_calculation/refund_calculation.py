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
			"label": _("INVOICE NO"),
			"fieldname": "invoice_no",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 150
		},
		{
			"label": _("INOVICE DATE"),
			"fieldname": "invoice_date",
			"fieldtype": "Date", 
			"width": 100
		},
		{
			"label": _("SB NO"), 
			"fieldname": "sb_no",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("SB DATE"), 
			"fieldname": "sb_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("EGM NO"), 
			"fieldname": "egm_no",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("EGM DATE"), 
			"fieldname": "egm_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("PORT CODE"), 
			"fieldname": "port_code",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("INVOICE VALUE"), 
			"fieldname": "invoice_value",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("FOB VALUE"), 
			"fieldname": "fob_value",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("W/L"), 
			"fieldname": "wl",
			"fieldtype": "Currency",
			"width": 100
		}]

	return columns
def get_data(filters):
	
	data = frappe.db.sql(f"""
	SELECT 
		si.name as invoice_no,si.posting_date as invoice_date,si.shipping_bill_number as sb_no,si.shipping_bill_date as sb_date,
		si.egm_no as egm_no,si.egm_date, 
		si.port_code as port_code ,si.total_fob_value as fob_value,si.base_grand_total as invoice_value,
		IF(si.base_grand_total < si.total_fob_value,si.base_grand_total,si.total_fob_value) as wl
	FROM
		`tabSales Invoice` si
	Where
		si.docstatus = 1 and
		 si.posting_date between '{filters.from_date}' and '{filters.to_date}' and si.gst_category = 'Overseas'
	ORDER BY
		si.name
	 """, as_dict = 1)
	return data