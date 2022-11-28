from frappe import _


def get_data():
	return {
		"fieldname": "journal_entry_ref",
		"non_standard_fieldnames": {
			"Journal Entry": "cheque_no",
		},
		"transactions": [
			{
				"label": _("Journal Entry"),
				"items": [
					"Journal Entry"]
			}
		],
	}
