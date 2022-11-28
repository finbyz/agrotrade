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
		{ "label": _("Month"),"fieldname": "month","fieldtype": "Data","width": 80},
		{ "label": _("Item Code"),"fieldname": "item_code","fieldtype": "Link","options":"Item","width": 140},
		{ "label": _("Item Name"),"fieldname": "item_name","fieldtype": "Data","width": 180},
		{ "label": _("Port of Shipment"),"fieldname": "port_of_loading","fieldtype": "Link","options":"Port Details","width": 130},
		{ "label": _("Country of Exported"),"fieldname": "country_of_destination","fieldtype": "Link","options":"Country","width": 120},
		{ "label": _("Packing Size"),"fieldname": "packing_size","fieldtype": "Float","width": 120},
		{ "label": _("Quantity"),"fieldname": "qty","fieldtype": "Float","width": 120},
		{ "label": _("FOB Value"),"fieldname": "fob_value","fieldtype": "Currency","width": 120},
		{ "label": _("FOB Unit Value"),"fieldname": "fob_unit_value","fieldtype": "Currency","width": 120},
	]
	return columns

def get_data(filters):
	conidtion = ""
	
	if filters.get('fiscal_year'):
		conidtion += f" and si.fiscal in (select fiscal from `tabFiscal Year` where name = '{filters.get('fiscal_year')}')"

	if filters.get('month'):
		conidtion += f" and MONTHNAME(si.posting_date) = '{filters.get('month')}'"

	return frappe.db.sql(f"""
		Select 
			si.name, sii.item_code, sii.item_name, si.port_of_loading, si.country_of_destination, sii.packing_size, sum(sii.qty) as qty, sum(sii.fob_value) as fob_value,
			(sum(sii.fob_value) / sum(sii.qty)) as fob_unit_value, MONTHNAME(si.posting_date) as month, si.is_opening
		FROM
			`tabSales Invoice Item` as sii
		JOIN
			`tabSales Invoice` as si on si.name = sii.parent
		WHERE
			si.is_opening = 'No' and si.docstatus = 1 and si.is_return = 0 and si.gst_category = 'Overseas' {conidtion}
		GROUP BY
			sii.item_code, si.port_of_loading, si.country_of_destination, sii.packing_size
	""", as_dict = 1)
