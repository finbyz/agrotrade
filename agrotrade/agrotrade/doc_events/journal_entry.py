import frappe
def validate (self,method):
    if self.party:
        if frappe.db.get_value("Employee" , self.party ,'pan_number'):
            pan = frappe.db.get_value("Employee" , self.party ,'pan_number')
            self.pan = pan

def on_cancel(self,method):
    if self.cheque_no:
        forward_booking = frappe.db.exists("Forward Booking",self.cheque_no)
        if forward_booking:
            date = frappe.db.sql(f""" SELECT date From `tabForward Booking Cancellation` Where parent = '{forward_booking}' and journal_entry = '{self.name}'""",as_dict=True)
            frappe.db.set_value("Journal Entry",self.name,'posting_date',date[0].date)
            doc_forward_booking =  frappe.get_doc("Forward Booking",forward_booking)
            for row in doc_forward_booking.cancellation_details:
                if row.journal_entry == self.name:
                    frappe.db.set_value("Forward Booking Cancellation",row.name,'journal_entry',"")
                # frappe.db.sql(f""" DELETE From  `tabForward Booking Cancellation` Where journal_entry = '{self.name}' """)
            # frappe.db.set_value("Forward Booking",forward_booking,'total_cancelled',None)
            # frappe.db.set_value("Forward Booking",forward_booking,'can_avg_rate',None)
            # frappe.db.set_value("Forward Booking",forward_booking,'rate_diff',None)
            # frappe.db.set_value("Forward Booking",forward_booking,'diff_amount',None)

