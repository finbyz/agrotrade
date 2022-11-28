import frappe
from frappe.utils import flt


@frappe.whitelist()
def pe_on_submit(self, method):
	fwd_uti(self)

def fwd_uti(self):
	for row in self.get('forwards'):
		target_doc = frappe.get_doc("Forward Booking", row.forward_contract)
		if not frappe.db.get_value("Forward Booking Utilization", filters={"parent": row.forward_contract, "voucher_type": "Payment Entry", "voucher_no": self.name}):
			target_doc.append("payment_entries", {
				"date": self.posting_date,
				"party_type": self.party_type,
				"party": self.party,
				"paid_amount" : row.amount_utilized,
				"voucher_type": "Payment Entry",
				"voucher_no" : self.name,
			})
		target_doc.save()
@frappe.whitelist()
def pe_on_cancel(self, method):
	fwd_uti_cancel(self)
	remove_pe_from_brc(self,method)

def remove_pe_from_brc(self,method):
    voucher_no = self.name
    data = frappe.db.sql(f"""SELECT brc.name as brc , brcp.name
                            from `tabBRC Management` as brc
                            left join `tabBRC Payment` as brcp on brcp.parent = brc.name     
                            where brcp.voucher_type = "Payment Entry" and brcp.voucher_no = '{voucher_no}'
                            """, as_dict=1)

    for row in data:
        frappe.db.delete("BRC Payment",row.name)

def fwd_uti_cancel(self):
	if self.name == "ACC-PAY-2022-00220":pass
	for row in self.get('forwards'):
		doc = frappe.get_doc("Forward Booking", row.forward_contract)
		to_remove = [row for row in doc.payment_entries if row.voucher_no == self.name and row.voucher_type == "Payment Entry"]
		[doc.remove(row) for row in to_remove]
		doc.save()

@frappe.whitelist()
def si_on_submit(self, method):
	blank_fields = []
	if self.naming_series == "company_series./.fiscal./.###":
		for field in ['po_no','po_date','tax_category','pre_carriage_by','country_of_origin','country_of_destination','final_destination','bl_no','bl_date','shipping_terms','port_of_discharge','port_of_loading','gst_category','export_type','invoice_copy','reverse_charge','port_code','shipping_bill_number','shipping_bill_date','lut_no']:
			if not self.get(field):
				blank_fields.append("Please Enter " + frappe.get_meta(self.doctype).get_field(field).label)
		if blank_fields:
			frappe.throw(blank_fields)


def add_invoice_entries_with_bill_no(self, non_reconciled_invoices):
	#Populate 'invoices' with JVs and Invoices to reconcile against
	self.set('invoices', [])

	for entry in non_reconciled_invoices:
		inv = self.append('invoices', {})
		inv.invoice_type = entry.get('voucher_type')
		inv.invoice_number = entry.get('voucher_no')
		inv.invoice_date = entry.get('posting_date')
		inv.amount = flt(entry.get('invoice_amount'))
		inv.currency = entry.get('currency')
		inv.outstanding_amount = flt(entry.get('outstanding_amount'))
		if entry.get('voucher_type') =="Purchase Invoice":
			inv.supplier_invoice_no=frappe.db.get_value("Purchase Invoice",entry.get('voucher_no'),'bill_no')
			inv.supplier_invoice_date=frappe.db.get_value("Purchase Invoice",entry.get('voucher_no'),'bill_date')
