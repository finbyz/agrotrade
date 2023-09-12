import frappe

from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
from frappe.utils import cint, comma_or, flt, getdate, nowdate

#Finbyz changes for forward contract
class CustomPaymentEntry(PaymentEntry):
    def set_unallocated_amount(self):
        if self.is_forward_contract_payment_entry:
            unallocated_amount = self.unallocated_amount
        else: 
            self.unallocated_amount = 0
        if self.party:
            total_deductions = sum(flt(d.amount) for d in self.get("deductions"))
            included_taxes = self.get_included_taxes()
            if (
                self.payment_type == "Receive"
                and self.base_total_allocated_amount < self.base_received_amount + total_deductions
                and self.total_allocated_amount
                < flt(self.paid_amount) + (total_deductions / self.source_exchange_rate)
            ):
                self.unallocated_amount = (
                    self.base_received_amount + total_deductions - self.base_total_allocated_amount
                ) / self.source_exchange_rate
                self.unallocated_amount -= included_taxes
            elif (
                self.payment_type == "Pay"
                and self.base_total_allocated_amount < (self.base_paid_amount - total_deductions)
                and self.total_allocated_amount
                < flt(self.received_amount) + (total_deductions / self.target_exchange_rate)
            ):
                self.unallocated_amount = (
                    self.base_paid_amount - (total_deductions + self.base_total_allocated_amount)
                ) / self.target_exchange_rate
                self.unallocated_amount -= included_taxes
