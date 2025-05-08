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
            "label": "Payroll Month From",
            "fieldtype": "Select",
            "options": [
               " ", "JAN - 25", "FEB - 25", "MAR - 25", "APR - 25", "MAY - 25", "JUN - 25",
                "JUL - 25", "AUG - 25", "SEP - 25", "OCT - 25", "NOV - 25", "DEC - 25"
            ]
        },
       
    ]
};
