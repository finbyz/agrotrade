// Copyright (c) 2022, Finbyz tech pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */
var d = new Date();
var dt = new Date(d.getFullYear(),d.getMonth(),1);
frappe.query_reports["TCS Payable Monthly"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default":dt,
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
	]
};
