frappe.query_reports["Salary Report"] = {
	"filters": [
		{
			"fieldname": "payment_date",
			"label": "Payment Date",
			"fieldtype": "Date",
			// "default": frappe.datetime.get_today()
		}
	]
};
