from agrotrade.agrotrade.report.accounts_receivable_agrotrade.accounts_receivable_agrotrade import ReceivablePayableReport

def execute(filters=None):
	args = {
		"party_type": "Supplier",
		"naming_by": ["Buying Settings", "supp_master_name"],
	}
	final_data=[]
	columns, data, col, chart, row, skip_total_row=ReceivablePayableReport(filters).run(args)
	for each in data:
		if filters.get('outstanding_amount'):
			if each.get('outstanding') >= filters.get('outstanding_amount'):
				final_data.append(each)
		else:
			final_data.append(each)
	return columns, final_data, col, chart, row, skip_total_row