// Copyright (c) 2022, Finbyz tech pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["QUARTERLY RETURN OF SPICES EXPORT FORM B"] = {
	"filters": [
		{
			"label":"Fiscal Year",
			"fieldname":"fiscal_year",
			"fieldtype":"Link",
			"options":"Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year")
		},
		{
			"label":"Month",
			"fieldname":"month",
			"fieldtype":"Select",
			"options":["January","February","March","April","May","June","July","August","September","October","November","December"],
			"default": new Date().toLocaleString('en-US', {month: 'long'})
		}
	]
};
