import frappe
from frappe import _, bold
from frappe.utils import flt
from erpnext.regional.india.utils import get_gst_accounts
from erpnext.regional.india.e_invoice.utils import update_other_charges

def update_invoice_taxes(invoice, invoice_value_details):
	gst_accounts = get_gst_accounts(invoice.company)
	gst_accounts_list = [d for accounts in gst_accounts.values() for d in accounts if d]

	invoice_value_details.total_cgst_amt = 0
	invoice_value_details.total_sgst_amt = 0
	invoice_value_details.total_igst_amt = 0
	invoice_value_details.total_cess_amt = 0
	invoice_value_details.total_other_charges = 0
	considered_rows = []

	for t in invoice.taxes:
		tax_amount = t.base_tax_amount_after_discount_amount
		if t.account_head in gst_accounts_list:
			if t.account_head in gst_accounts.cess_account:
				# using after discount amt since item also uses after discount amt for cess calc
				invoice_value_details.total_cess_amt += abs(t.base_tax_amount_after_discount_amount)

			for tax_type in ['igst', 'cgst', 'sgst']:
				if t.account_head in gst_accounts[f'{tax_type}_account']:

					invoice_value_details[f'total_{tax_type}_amt'] += abs(tax_amount)
				update_other_charges(t, invoice_value_details, gst_accounts_list, invoice, considered_rows)
		#finbyz changes 
		else:
			export_reverse_charge_account = frappe.db.get_value("GST Account",{'company':invoice.company,"parent": "GST Settings"},'export_reverse_charge_account')
			if t.account_head == export_reverse_charge_account:
				invoice_value_details.base_total_other_taxes = t.base_tax_amount
				invoice_value_details.total_other_taxes = t.tax_amount

			else:
				invoice_value_details.total_other_charges += abs(t.base_tax_amount_after_discount_amount)
		#finbyz changes end
	return invoice_value_details

def get_invoice_value_details(invoice):
	invoice_value_details = frappe._dict(dict())
	invoice_value_details.base_total = abs(sum([i.taxable_value for i in invoice.get('items')]))
	invoice_value_details.invoice_discount_amt = 0

	invoice_value_details.round_off = invoice.base_rounding_adjustment
	invoice_value_details.base_grand_total = abs(invoice.base_rounded_total) or abs(invoice.base_grand_total)
	invoice_value_details.grand_total = abs(invoice.rounded_total) or abs(invoice.grand_total)

	invoice_value_details = update_invoice_taxes(invoice, invoice_value_details)
	#finbyz changes 
	invoice_value_details.base_grand_total -= flt(invoice_value_details.base_total_other_taxes)
	invoice_value_details.grand_total -= flt(invoice_value_details.total_other_taxes)
	#finbyz changes end

	return invoice_value_details