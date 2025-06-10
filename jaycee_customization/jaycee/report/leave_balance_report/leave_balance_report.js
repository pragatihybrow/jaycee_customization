// Copyright (c) 2025, Pragati Dike and contributors
// For license information, please see license.txt

frappe.query_reports["Leave Balance Report"] = {
	"filters": [
		{
			"fieldname": "employee",
			"label": "Employee",
			"fieldtype": "Link",
			"options": "Employee"
		  },
	]
};
