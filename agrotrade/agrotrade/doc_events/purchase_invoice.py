import frappe
from frappe.utils import flt, cstr, cint
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice

def validate_with_previous_doc(self):
    """
        Finbyz Changes: Validate Broker with Previous Doc if broker applicable else Supplier
    """
    supplier_or_broker = "supplier"
    if self.is_broker_applicable:
        supplier_or_broker = "broker"

    super(PurchaseInvoice, self).validate_with_previous_doc({
        "Purchase Order": {
            "ref_dn_field": "purchase_order",
            "compare_fields": [[supplier_or_broker, "="], ["company", "="], ["currency", "="]],
        },
        "Purchase Order Item": {
            "ref_dn_field": "po_detail",
            "compare_fields": [["project", "="], ["item_code", "="], ["uom", "="]],
            "is_child_table": True,
            "allow_duplicate_prev_row_id": True
        },
        "Purchase Receipt": {
            "ref_dn_field": "purchase_receipt",
            "compare_fields": [[supplier_or_broker, "="], ["company", "="], ["currency", "="]],
        },
        "Purchase Receipt Item": {
            "ref_dn_field": "pr_detail",
            "compare_fields": [["project", "="], ["item_code", "="], ["uom", "="]],
            "is_child_table": True
        }
    })

    if cint(frappe.db.get_single_value('Buying Settings', 'maintain_same_rate')) and not self.is_return:
        self.validate_rate_with_reference_doc([
            ["Purchase Order", "purchase_order", "po_detail"],
            ["Purchase Receipt", "purchase_receipt", "pr_detail"]
        ])