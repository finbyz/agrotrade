import frappe
from frappe.utils import flt,cint
from finbyzerp.api import naming_series_name
from erpnext.accounts.utils import get_fiscal_year
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

def get_fiscal(date):
	fy = get_fiscal_year(date)[0]
	fiscal = frappe.db.get_value("Fiscal Year", fy, 'fiscal')

	return fiscal if fiscal else fy.split("-")[0][2:] + fy.split("-")[1][2:]

def before_naming(self, method):
	if not self.get('amended_from') and not self.get('name'):
		date = self.get("transaction_date") or self.get("posting_date") or  self.get("manufacturing_date") or self.get('date') or getdate()
		fiscal = get_fiscal(date)
		self.fiscal = fiscal
		if not self.get('company_series'):
			self.company_series = None
		
		if self.doctype == "Purchase Invoice" and self.naming_series in ["DN-GST/.company_series./.fiscal./.###" , "DN-NON-GST/.company_series./.fiscal./.###"]:
			if self.get('series_value'):
				if self.series_value > 0:
					name = naming_series_name(self.naming_series, fiscal, self.company_series)
					check = frappe.db.get_value('Series', name, 'current', order_by="name")
					if check == 0:
						pass
					elif not check:
						frappe.db.sql("insert into tabSeries (name, current) values ('{}', 0)".format(name))

					frappe.db.sql("update `tabSeries` set current = {} where name = '{}'".format(cint(self.series_value) - 1, name))
		else:
			if self.get('series_value'):
				if self.series_value > 0:
					name = naming_series_name(self.naming_series, fiscal, self.company_series)
					check = frappe.db.get_value('Series', name, 'current', order_by="name")
					if check == 0:
						pass
					elif not check:
						frappe.db.sql("insert into tabSeries (name, current) values ('{}', 0)".format(name))

					frappe.db.sql("update `tabSeries` set current = {} where name = '{}'".format(cint(self.series_value) - 1, name))

