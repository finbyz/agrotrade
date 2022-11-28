frappe.listview_settings['Pre Shipment'] = {
	add_fields: ["status"],
	get_indicator: function(doc) {
		if(doc.status==="Outstanding"){
			return [__("Outstanding"), "orange", "status,=,Outstanding"];

		} else if (doc.status==="Partially Paid")
			return [__("Partially Paid"), "blue", "status,=,Partially Paid"];

        else if (doc.status==="Paid")
			return [__("Paid"), "green", "status,=,Paid"];

		else if (doc.status==="Cancelled")
			return [__("Cancelled"), "red", "status,=,Cancelled"];

        else (doc.status==="Draft")
			return [__("Draft"), "yellow", "status,=,Draft"]
    }}