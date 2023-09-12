# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.meta import get_field_precision
from frappe.model.naming import set_name_from_naming_options
from frappe.utils import flt, fmt_money
from six import iteritems
from erpnext.accounts.doctype.gl_entry.gl_entry import GLEntry
import erpnext
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_checks_for_pl_and_bs_accounts,
)
from erpnext.accounts.doctype.accounting_dimension_filter.accounting_dimension_filter import (
	get_dimension_filter_map,
)
from erpnext.accounts.party import validate_party_frozen_disabled, validate_party_gle_currency
from erpnext.accounts.utils import get_account_currency, get_fiscal_year
from erpnext.exceptions import (
	InvalidAccountCurrency,
	InvalidAccountDimensionError,
	MandatoryAccountDimensionError,
)

exclude_from_linked_with = True



class CustomGLEntry(GLEntry):
	def validate(self):
		self.flags.ignore_submit_comment = True
		self.validate_and_set_fiscal_year()
		self.pl_must_have_cost_center()

		if not self.flags.from_repost:
			self.check_mandatory()
			self.validate_cost_center()
			self.check_pl_account()
			self.validate_party()
			self.validate_currency()

	def on_update(self):
		adv_adj = self.flags.adv_adj
		if not self.flags.from_repost:
			self.validate_account_details(adv_adj)
			self.validate_dimensions_for_pl_and_bs()
			self.validate_allowed_dimensions()
			validate_balance_type(self.account, adv_adj)
			validate_frozen_account(self.account, adv_adj)

			# Update outstanding amt on against voucher
			if (
				self.against_voucher_type in ["Journal Entry", "Sales Invoice", "Purchase Invoice", "Fees"]
				and self.against_voucher
				and self.flags.update_outstanding == "Yes"
				and not frappe.flags.is_reverse_depr_entry
			):
				update_outstanding_amt(
					self.account, self.party_type, self.party, self.against_voucher_type, self.against_voucher
				)