import frappe

@frappe.whitelist()
def get_voucher_no(doctype, txt, searchfield, start, page_len, filters):
    if filters.get('loan_account') :
         return frappe.db.sql(f"""
            SELECT jea.parent
            FROM `tabJournal Entry Account` as jea
            left join `tabJournal Entry` as je on je.name = jea.parent
            Where jea.account = '{filters.get('loan_account')}'
        """,as_list=True)
   
@frappe.whitelist()
def get_payment_entry(doctype, txt, searchfield, start, page_len, filters):
    if filters.get('loan_account') :
         return frappe.db.sql(f"""
            SELECT re.name
            From `tabPayment Entry` as re 
            Where re.paid_from = '{filters.get('loan_account')}'
        """,as_list=True)