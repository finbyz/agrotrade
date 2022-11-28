// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

// {% include "erpnext/accounts/report/item_wise_sales_register/item_wise_sales_register.js" %}
// {% include "erpnext/regional/report/india_gst_common/india_gst_common.js" %}
// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Item-wise Sales Register"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "mode_of_payment",
			"label": __("Mode of Payment"),
			"fieldtype": "Link",
			"options": "Mode of Payment"
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname": "brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand"
		},
		{
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		},
		{
			"label": __("Group By"),
			"fieldname": "group_by",
			"fieldtype": "Select",
			"options": ["Customer Group", "Customer", "Item Group", "Item", "Territory", "Invoice"]
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	}
}

function fetch_gstins(report) {
	var company_gstins = report.get_filter('company_gstin');
	var company = report.get_filter_value('company');
	if (company) {
		frappe.call({
			method:'erpnext.regional.india.utils.get_gstins_for_company',
			async: false,
			args: {
				company: company
			},
			callback: function(r) {
				r.message.unshift("");
				company_gstins.df.options = r.message;
				company_gstins.refresh();
			}
		});
	} else {
		company_gstins.df.options = [""];
		company_gstins.refresh();
	}
}

let filters = frappe.query_reports["Item-wise Sales Register"]["filters"];

// Add GSTIN filter
filters = filters.concat({
    "fieldname":"company_gstin",
    "label": __("Company GSTIN"),
    "fieldtype": "Select",
    "placeholder":"Company GSTIN",
    "options": [""],
    "width": "80"
},
{
    "fieldname":"is_return",
    "label": __("Return Entries"),
    "fieldtype": "Check"
},
// {
//     "fieldname":"invoice_type",
//     "label": __("Invoice Type"),
//     "fieldtype": "Select",
//     "placeholder":"Invoice Type",
//     "options": ["", "Regular", "SEZ", "Export", "Deemed Export"]
// },
{
    "fieldname":"gst_category",
    "label": __("GST Category"),
    "fieldtype": "Select",
    "placeholder":"GST Category",
    "options": ["", "Registered Regular","Registered Composition","Unregistered","SEZ","Overseas","Consumer","Deemed Export","UIN Holders"]
});

// Handle company on change
for (var i = 0; i < filters.length; ++i) {
    if (filters[i].fieldname === 'company') {
        filters[i].on_change = fetch_gstins;
    }
}

frappe.query_reports["GST Itemised Sales Register"] = { "filters": filters, "onload": fetch_gstins };
