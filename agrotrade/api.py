import frappe


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
				"paid_amount" : self.paid_amount,
				"voucher_type": "Payment Entry",
				"voucher_no" : self.name,
			})
		target_doc.save()
@frappe.whitelist()
def pe_on_cancel(self, method):
	fwd_uti_cancel(self)

def fwd_uti_cancel(self):
	for row in self.get('forwards'):
		doc = frappe.get_doc("Forward Booking", row.forward_contract)
		to_remove = [row for row in doc.payment_entries if row.voucher_no == self.name and row.voucher_type == "Payment Entry"]
		[doc.remove(row) for row in to_remove]
		doc.save()