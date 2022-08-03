cur_frm.fields_dict.broker.get_query = function(doc) {
	return {
		filters: {
			"supplier_group": "Broker"
		}
	}
};

frappe.ui.form.on('Purchase Invoice', {
	naming_series: function(frm){
		if(frm.doc.naming_series && frm.doc.naming_series == "RM.-.company_series./.fiscal./.###"){
			frm.set_value("update_stock", 1)
		}
		else{
			frm.set_value("update_stock", 0)
		}
	},
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
