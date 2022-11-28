# Copyright (c) 2022, Finbyz tech pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data



def get_data(filters):
	conditions = ""
	if filters.get('from_date') and filters.get('to_date'):
		conditions += f" and si.posting_date BETWEEN '{filters.get('from_date')}' and '{filters.get('to_date')}'"
	if filters.get('item_code'):
		conditions += f" and i.item_code = '{filters.get('item_code')}'"

	data =  frappe.db.sql(f""" Select i.item_code , sii.qty/1000 as qty_in_mt , sii.packing_size , sii.rate , sii.qty , sii.fob_value , si.port_of_discharge , (sii.fob_value/sii.qty) as fbqty
                From `tabItem` as i
                left join `tabSales Invoice Item` as sii ON sii.item_code = i.name
                left join  `tabSales Invoice` as si On si.name = sii.parent
                Where sii.item_code != 'Opening Invoice Item' and si.docstatus = 1 and si.gst_category = 'Overseas' {conditions}

                """,as_dict=True)
	return data

def get_columns(filters = None):
	columns = [

		{ "label": _("Item"),"fieldname": "item_code","fieldtype": "Link","options":"Item","width": 130},
		{ "label": _("Quantity in MT"),"fieldname": "qty_in_mt","fieldtype": "Float","width": 130},
		{ "label": _("Packing Size"),"fieldname": "packing_size","fieldtype": "Float","options":"Item","width": 130},
		{ "label": _("Rate"),"fieldname": "rate","fieldtype": "Float","width": 130},
		{ "label": _("Qty"),"fieldname": "qty","fieldtype": "Float","width": 130},
		{ "label": _("Fob Value"),"fieldname": "fob_value","fieldtype": "Float","width": 130},
		{ "label": _("Port Of Discharge"),"fieldname": "port_of_discharge","fieldtype": "Data","width": 130},
		{ "label": _("Fob Value / Value"),"fieldname": "fbqty","fieldtype": "Float","width": 130},
	]
	return columns