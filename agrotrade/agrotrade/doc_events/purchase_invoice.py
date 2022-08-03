import frappe,erpnext
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
from frappe import _, throw
from frappe.utils import cint, cstr, flt,  get_link_to_form
from six import iteritems


from erpnext.assets.doctype.asset.asset import is_cwip_accounting_enabled
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account
from erpnext.buying.utils import check_on_hold_or_closed_status
from erpnext.controllers.accounts_controller import validate_account_head
from erpnext.controllers.buying_controller import BuyingController
from erpnext.stock import get_warehouse_account_map
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import (
	get_item_account_wise_additional_cost,
	update_billed_amount_based_on_po,
)


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


def set_expense_account(self, for_validate=False):
    auto_accounting_for_stock = erpnext.is_perpetual_inventory_enabled(self.company)

    if auto_accounting_for_stock:
        stock_not_billed_account = self.get_company_default("stock_received_but_not_billed")
        stock_items = self.get_stock_items()

    asset_items = [d.is_fixed_asset for d in self.items if d.is_fixed_asset]
    if len(asset_items) > 0:
        asset_received_but_not_billed = self.get_company_default("asset_received_but_not_billed")

    if self.update_stock:
        self.validate_item_code()
        self.validate_warehouse(for_validate)
        if auto_accounting_for_stock:
            warehouse_account = get_warehouse_account_map(self.company)

    for item in self.get("items"):
        # in case of auto inventory accounting,
        # expense account is always "Stock Received But Not Billed" for a stock item
        # except opening entry, drop-ship entry and fixed asset items
        if item.item_code:
            asset_category = frappe.get_cached_value("Item", item.item_code, "asset_category")

        if auto_accounting_for_stock and item.item_code in stock_items \
            and self.is_opening == 'No' and not item.is_fixed_asset \
            and (not item.po_detail or
                not frappe.db.get_value("Purchase Order Item", item.po_detail, "delivered_by_supplier")):
            
            if self.is_return and not self.update_stock :
                #finbyz changes ignore validation if expense head need to be changed
                return

            if self.update_stock and (not item.from_warehouse):
                if for_validate and item.expense_account and item.expense_account != warehouse_account[item.warehouse]["account"]:
                    msg = _("Row {0}: Expense Head changed to {1} because account {2} is not linked to warehouse {3} or it is not the default inventory account").format(
                        item.idx, frappe.bold(warehouse_account[item.warehouse]["account"]), frappe.bold(item.expense_account), frappe.bold(item.warehouse))
                    frappe.msgprint(msg, title=_("Expense Head Changed"))
                item.expense_account = warehouse_account[item.warehouse]["account"]
            else:
                # check if 'Stock Received But Not Billed' account is credited in Purchase receipt or not
                if item.purchase_receipt:
                    negative_expense_booked_in_pr = frappe.db.sql("""select name from `tabGL Entry`
                        where voucher_type='Purchase Receipt' and voucher_no=%s and account = %s""",
                        (item.purchase_receipt, stock_not_billed_account))

                    if negative_expense_booked_in_pr:
                        if for_validate and item.expense_account and item.expense_account != stock_not_billed_account:
                            msg = _("Row {0}: Expense Head changed to {1} because expense is booked against this account in Purchase Receipt {2}").format(
                                item.idx, frappe.bold(stock_not_billed_account), frappe.bold(item.purchase_receipt))
                            frappe.msgprint(msg, title=_("Expense Head Changed"))

                        item.expense_account = stock_not_billed_account
                else:
                    # If no purchase receipt present then book expense in 'Stock Received But Not Billed'
                    # This is done in cases when Purchase Invoice is created before Purchase Receipt
                    if for_validate and item.expense_account and item.expense_account != stock_not_billed_account:
                        msg = _("Row {0}: Expense Head changed to {1} as no Purchase Receipt is created against Item {2}.").format(
                            item.idx, frappe.bold(stock_not_billed_account), frappe.bold(item.item_code))
                        msg += "<br>"
                        msg += _("This is done to handle accounting for cases when Purchase Receipt is created after Purchase Invoice")
                        frappe.msgprint(msg, title=_("Expense Head Changed"))

                    item.expense_account = stock_not_billed_account

        elif item.is_fixed_asset and not is_cwip_accounting_enabled(asset_category):
            asset_category_account = get_asset_category_account('fixed_asset_account', item=item.item_code,
                company = self.company)
            if not asset_category_account:
                form_link = get_link_to_form('Asset Category', asset_category)
                throw(
                    _("Please set Fixed Asset Account in {} against {}.").format(form_link, self.company),
                    title=_("Missing Account")
                )
            item.expense_account = asset_category_account
        elif item.is_fixed_asset and item.pr_detail:
            item.expense_account = asset_received_but_not_billed
        elif not item.expense_account and for_validate:
            throw(_("Expense account is mandatory for item {0}").format(item.item_code or item.item_name))
