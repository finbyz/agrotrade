import frappe

def on_cancel(self, method):
    update_ref(self)

def update_ref(self):
    if self.brc_document:
        frappe.db.set_value("BRC Management", self.brc_document, "invoice_no", None)
        self.db_set("brc_document", None)