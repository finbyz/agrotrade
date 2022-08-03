import frappe
def validate (self,method):
    if self.party:
        if frappe.db.get_value("Employee" , self.party ,'pan_number'):
            pan = frappe.db.get_value("Employee" , self.party ,'pan_number')
            self.pan = pan

        