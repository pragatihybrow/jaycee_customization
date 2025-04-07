# Copyright (c) 2025, Pragati Dike and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Client Code", "fieldname": "client_code", "fieldtype": "Data", "width": 120},
        {"label": "Product Code", "fieldname": "product_code", "fieldtype": "Data", "width": 120},
        {"label": "Payment Type", "fieldname": "payment_type", "fieldtype": "Data", "width": 120},
        {"label": "Payment Ref No", "fieldname": "payment_ref_no", "fieldtype": "Data", "width": 150},
        {"label": "Payment Date", "fieldname": "payment_date", "fieldtype": "Date", "width": 120},
        {"label": "Dr Ac No", "fieldname": "dr_ac_no", "fieldtype": "Data", "width": 150},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Beneficiary Code", "fieldname": "beneficiary_code", "fieldtype": "Data", "width": 150},
        {"label": "Beneficiary Name", "fieldname": "beneficiary_name", "fieldtype": "Data", "width": 150},
        {"label": "IFSC Code", "fieldname": "ifsc_code", "fieldtype": "Data", "width": 120},
        {"label": "Beneficiary ACC No", "fieldname": "beneficiary_acc_no", "fieldtype": "Data", "width": 150},
        {"label": "Beneficiary Email", "fieldname": "beneficiary_email", "fieldtype": "Data", "width": 200},
        {"label": "Beneficiary Mobile", "fieldname": "beneficiary_mobile", "fieldtype": "Data", "width": 150},
        {"label": "Debit Narration", "fieldname": "debit_narration", "fieldtype": "Data", "width": 200},
        {"label": "Credit Narration", "fieldname": "credit_narration", "fieldtype": "Data", "width": 200},
        {"label": "Enrichment 1", "fieldname": "enrichment_1", "fieldtype": "Data", "width": 150},
        {"label": "Enrichment 2", "fieldname": "enrichment_2", "fieldtype": "Data", "width": 150}
    ]

def get_data(filters):
    salary_slips = frappe.get_all(
        "Salary Slip", 
        fields=["employee", "posting_date", "net_pay", "name"], 
        filters={"docstatus": 1}
    )

    data = []
    for slip in salary_slips:
        employee = frappe.get_doc("Employee", slip.employee)

        # Note:
        # 'bank_ac_no' and 'ifsc_code' are fields in the Employee doctype.
        # They are used as 'Beneficiary ACC No' and 'IFSC Code' in the report output.

        row = {
            "client_code": "JAYCEEBUI",  # Static value - update as needed
            "product_code": "RPAY",      # Static value - update as needed
            "payment_type": "Salary",
            "payment_ref_no": slip.name,
            "payment_date": slip.posting_date,
            "dr_ac_no": "1234567890",    # Replace with actual company account number
            "amount": slip.net_pay,
            "beneficiary_code": employee.name,
            "beneficiary_name": employee.employee_name,
            "ifsc_code": employee.ifsc_code,
            "beneficiary_acc_no": employee.bank_ac_no,
            "beneficiary_email": employee.company_email,
            "beneficiary_mobile": employee.cell_number,
            "debit_narration": f"Salary Payment {slip.name}",
            "credit_narration": f"Salary Credited {employee.employee_name}",
            "enrichment_1": "-",  # Additional fields if needed
            "enrichment_2": "-"
        }
        data.append(row)

    return data
