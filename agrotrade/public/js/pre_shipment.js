cur_frm.set_query("voucher_no", "repayments", function(doc, cdt, cdn)  {
	var row = frappe.get_doc(cdt, cdn);
	if(row.voucher_type == "Journal Entry"){
		return {
			query: "agrotrade.agrotrade.doc_events.pre_shipment.get_voucher_no",
			filters: {'loan_account': doc.loan_account }
		}
	}
	if(row.voucher_type == "Payment Entry")	{
		return {
			query: "agrotrade.agrotrade.doc_events.pre_shipment.get_payment_entry",
			filters: {'loan_account': doc.loan_account }
		}
	}
});
