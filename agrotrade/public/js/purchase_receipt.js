cur_frm.fields_dict.broker.get_query = function(doc) {
	return {
		filters: {
			"supplier_group": "Broker"
		}
	}
};

frappe.ui.form.on('Purchase Receipt', {
	broker: function(frm) {
        if (frm.doc.broker) {
			frappe.call({
				method:"erpnext.accounts.party.get_party_details",
				args:{
					party_type: "Supplier",
					party: frm.doc.broker
				},
				callback: function(r){
					var address = null;
					if (r.message){
						address = r.message.address_display.replaceAll('<br>',' ')
					}
					frm.set_value('broker_address',address)
					frm.refresh();
				}
			})
        }else{
			frm.set_value('broker_address',null);
		}
	}
})
