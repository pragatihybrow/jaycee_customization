# Copyright (c) 2025, Pragati Dike and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, formatdate
import calendar

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
    conditions = {}
    if filters.get("payment_date"):
        conditions["posting_date"] = getdate(filters.get("payment_date"))
    if filters.get("credit_narration"):
        conditions["credit_narration"] = ["like", f"%{filters.get('credit_narration')}%"]

    salary_slips = frappe.get_all(
        "Salary Slip", 
        fields=["employee", "posting_date", "net_pay", "name", "company", "bank_name"], 
        filters=conditions
    )

    data = []
    for slip in salary_slips:
        employee = frappe.get_doc("Employee", slip.employee)
        company_abbr = frappe.db.get_value("Company", slip.company, "abbr") or ""
        # month_year = slip.posting_date.strftime("%b %Y").upper()
        from dateutil.relativedelta import relativedelta

        month_year = (slip.posting_date - relativedelta(months=1)).strftime("%b %Y").upper()


        # payment_type = "IFT" if slip.bank_name == "Kotak Mahindra Bank Ltd" else "NEFT"
        payment_type = "IFT" if employee.ifsc_code and employee.ifsc_code.startswith("KKBK") else "NEFT"



        row = {
            "client_code": "JAYCEEBUI",
            "product_code": "RPAY",
            "payment_type": payment_type,
            "payment_ref_no": "",
            "payment_date": slip.posting_date,
            "dr_ac_no": "9412291051",  # Placeholder
            "amount": slip.net_pay,
            "beneficiary_code": "",
            "beneficiary_name": employee.employee_name,
            "ifsc_code": employee.ifsc_code,
            "beneficiary_acc_no": employee.bank_ac_no,
            "beneficiary_email": employee.company_email,
            "beneficiary_mobile": employee.cell_number,
            "debit_narration": employee.employee_name,
            "credit_narration": f"{company_abbr} Salary for {month_year}",
            "enrichment_1": "-",
            "enrichment_2": "-"
        }
        data.append(row)

    return data


# def get_data(filters):
#     salary_slips = frappe.get_all(
#         "Salary Slip", 
#         fields=["employee", "posting_date", "net_pay", "name", "company", "bank_name"], 
#         # filters={"docstatus": 1}
#     )

#     data = []
#     for slip in salary_slips:
#         employee = frappe.get_doc("Employee", slip.employee)
#         company_abbr = frappe.db.get_value("Company", slip.company, "abbr") or ""
#         month_year = slip.posting_date.strftime("%b %Y").upper()

#         # Payment type logic based on bank name
#         payment_type = "IFT" if slip.bank_name == "Kotak Mahindra Bank Ltd" else "NEFT"

#         row = {
#             "client_code": "JAYCEEBUI",
#             "product_code": "RPAY",
#             "payment_type": payment_type,
#             "payment_ref_no":"",
#             "payment_date": slip.posting_date,
#             "dr_ac_no": "9412291051",  # Replace with actual company account number
#             "amount": slip.net_pay,
#             "beneficiary_code": "",
#             "beneficiary_name": employee.employee_name,
#             "ifsc_code": employee.ifsc_code,
#             "beneficiary_acc_no": employee.bank_ac_no,
#             "beneficiary_email": employee.company_email,
#             "beneficiary_mobile": employee.cell_number,
#             "debit_narration": employee.employee_name,
#             "credit_narration": f"{company_abbr} Salary for {month_year}",
#             "enrichment_1": "-",
#             "enrichment_2": "-"
#         }
#         data.append(row)

#     return data
