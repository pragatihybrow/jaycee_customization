// Copyright (c) 2025, Pragati Dike and contributors
// For license information, please see license.txt

frappe.query_reports["Salary Slip Report"] = {
	"filters": [
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company"
        },
		{
            "fieldname": "payroll_month_from",
            "label": "From Date",
            "fieldtype": "Date",
            
        },
        {
            "fieldname": "payroll_month_to",
            "label": "To Date",
            "fieldtype": "Date",
            
        }
    ]
};
