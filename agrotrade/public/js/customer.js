frappe.ui.form.on("Customer", {
    refresh: function(frm) {
		if(!frm.doc.__islocal) {
			// custom buttons
			frm.add_custom_button(__('Party Monthly Summary'), function () {
				frappe.set_route('query-report', 'Party Monthly Summary',{party_type: 'Customer', party: frm.doc.name});
			}, __('View'));
		}
	}
})