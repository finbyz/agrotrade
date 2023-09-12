// cur_frm.fields_dict.broker.set_query = function(doc) {
// 	return {
// 		filters: {
// 			"supplier_group": "Broker"
// 		}
// 	}
// };

frappe.ui.form.on('Sales Invoice', {
	naming_series: function(frm){
		const naming_series=["company_series./.fiscal./.###",'GST./.fiscal./.###','IGST./.fiscal./.###','TAX/.fiscal./.###']
		if(frm.doc.naming_series && naming_series.includes(frm.doc.naming_series)){
			frm.set_value("update_stock", 1)
		}
		else{
			frm.set_value("update_stock", 0)
		}
	},
	onload: function(frm){
		frm.trigger('remove_export_fields')
		if (frm.doc.__islocal) {
			console.log("ghjj")
    		frm.set_value("duty_drawback_jv","");
    		frm.set_value("meis_jv","");
	    }
		frm.set_query('broker', () => {
			return {
				filters: {
					"supplier_group": "Broker"
				}
			}
		})
	},
	refresh: function(frm){
		if (frm.doc.__islocal) {
			console.log("ghjj")
    		frm.set_value("duty_drawback_jv","");
    		frm.set_value("meis_jv","");
		frm.doc.items.forEach(d=>{
			frappe.model.set_value(d.doctype, d.name, "sales_order", null)
		})
	}
	},
	broker: function(frm) {
        if (frm.doc.broker) {x
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
	},
	remove_export_fields:function(frm){
		if(frm.doc.customer_address){
			if(frappe.db.get_value("Address",frm.doc.customer_address,"country") != "india"){
				// cur_frm.set_df_property("accounting_dimensions_section", "hidden", 1);
				// cur_frm.set_df_property("timesheets", "hidden", 1);
				// cur_frm.set_df_property("section_break_49", "hidden", 1);
				// cur_frm.set_df_property("transporter_info", "hidden", 1);
				// cur_frm.set_df_property("edit_printing_settings", "hidden", 1);
				// // cur_frm.set_df_property("gst_section", "hidden", 1);
				// cur_frm.set_df_property("sales_team_section_break", "hidden", 1);
				// cur_frm.set_df_property("section_break2", "hidden", 1);
				// cur_frm.set_df_property("subscription_section", "hidden", 1);
				// cur_frm.set_df_property("more_information", "hidden", 1);
			}
		}
	},
	customer_address:function(frm){
		frm.trigger('remove_export_fields')
    },
	validate: function(frm){
        if (frm.doc.notify_party_address_table){
            frm.doc.notify_party_address_table.forEach( function(row) {
                if (row.notify_party) {
                    return frappe.call({
                        method: "frappe.contacts.doctype.address.address.get_address_display",
                        args: {
                            "address_dict": row.notify_party
                        },
                        callback: function (r) {
                            if (r.message)
                            frappe.model.set_value(row.doctype,row.name,"notify_address_display", r.message);
                        }
                    });
                }
            });
        }
    },
})
frappe.ui.form.on('Notify Party Address', {
	notify_party: function (frm, cdt, cdn) {
        let d = locals[cdt][cdn];
		if (d.notify_party) {
			return frappe.call({
				method: "frappe.contacts.doctype.address.address.get_address_display",
				args: {
					"address_dict": d.notify_party
				},
				callback: function (r) {
					if (r.message)
					frappe.model.set_value(cdt, cdn,"notify_address_display", r.message);
				}
			});
		}else{
			frappe.model.set_value(cdt, cdn,"notify_address_display", " ");
		}
		
	}
})
frappe.ui.form.on('Sales Invoice Item', {
	refresh:function(frm){
		console.log(frm)
		frm.doc.items.forEach(d=>{
			console.log("Calels")
			// if (frm.doc.__islocal) {

			// }
		})
	}

});