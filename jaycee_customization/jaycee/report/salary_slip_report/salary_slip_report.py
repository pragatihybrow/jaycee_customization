# Copyright (c) 2025, Pragati Dike and contributors
# For license information, please see license.txt


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
        {"label": "Employee Number", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 140},
        {"label": "Job Title", "fieldname": "designation", "fieldtype": "Data", "width": 120},
        {"label": "Date Of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 110},
        {"label": "Gender", "fieldname": "gender", "fieldtype": "Data", "width": 80},
        {"label": "Date Of Birth", "fieldname": "date_of_birth", "fieldtype": "Date", "width": 110},
        {"label": "Location", "fieldname": "branch", "fieldtype": "Data", "width": 100},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 120},
        {"label": "Worker Type", "fieldname": "employment_type", "fieldtype": "Data", "width": 100},
        {"label": "Cost Center", "fieldname": "cost_center", "fieldtype": "Link", "options": "Cost Center", "width": 120},
        {"label": "Business Unit", "fieldname": "business_unit", "fieldtype": "Data", "width": 120},
        {"label": "PAN Number", "fieldname": "pan_number", "fieldtype": "Data", "width": 120},
        {"label": "Payroll Month", "fieldname": "payroll_month", "fieldtype": "Data", "width": 110},
        {"label": "Payroll Type", "fieldname": "payroll_frequency", "fieldtype": "Data", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
        {"label": "Status Description", "fieldname": "salary_slip_status", "fieldtype": "Data", "width": 130},
        {"label": "Actual Payable days", "fieldname": "payment_days", "fieldtype": "Float", "width": 110},
        {"label": "Working days", "fieldname": "total_working_days", "fieldtype": "Float", "width": 110},
        {"label": "Loss of Pay Days", "fieldname": "leave_without_pay", "fieldtype": "Float", "width": 110},
        {"label": "Days Payable", "fieldname": "days_payable", "fieldtype": "Float", "width": 100},
        {"label": "Payable Units", "fieldname": "payable_units", "fieldtype": "Data", "width": 100},
        {"label": "Remuneration Amount", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 120},
        {"label": "Basic", "fieldname": "base", "fieldtype": "Currency", "width": 100},
        {"label": "HRA", "fieldname": "hra", "fieldtype": "Currency", "width": 100},
        {"label": "Special Allowance", "fieldname": "special_allowance", "fieldtype": "Currency", "width": 130},
        {"label": "Travel Reimbursement (LTA)", "fieldname": "lta", "fieldtype": "Currency", "width": 180},
        {"label": "Gross(A)", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 100},
        {"label": "PF Employee", "fieldname": "pf_employee_contribution", "fieldtype": "Currency", "width": 100},
        {"label": "PF - Employer", "fieldname": "pf_employer_contribution", "fieldtype": "Currency", "width": 100},
        {"label": "PF - Other Charges", "fieldname": "pf_other", "fieldtype": "Currency", "width": 130},
        {"label": "ESI Employee", "fieldname": "esi_employee_contribution", "fieldtype": "Currency", "width": 100},
        {"label": "ESI Employer", "fieldname": "esi_employer_contribution", "fieldtype": "Currency", "width": 100},
        {"label": "Total Contributions(B)", "fieldname": "total_contributions", "fieldtype": "Currency", "width": 150},
        {"label": "Professional Tax", "fieldname": "professional_tax", "fieldtype": "Currency", "width": 120},
        {"label": "Loan EMI", "fieldname": "loan_emi", "fieldtype": "Currency", "width": 100},
        {"label": "Ad Hoc Deduction", "fieldname": "ad_hoc_deduction", "fieldtype": "Currency", "width": 130},
        {"label": "Total Income Tax", "fieldname": "income_tax", "fieldtype": "Currency", "width": 120},
        {"label": "Total Deductions(C)", "fieldname": "total_deduction", "fieldtype": "Currency", "width": 140},
        {"label": "Net Pay(A-B-C)", "fieldname": "net_pay", "fieldtype": "Currency", "width": 140},
        {"label": "Cash Advance(D)", "fieldname": "cash_advance", "fieldtype": "Currency", "width": 120},
        {"label": "Settlement Against Advance(E)", "fieldname": "settlement_against_advance", "fieldtype": "Currency", "width": 180},
        {"label": "Need-Based Items", "fieldname": "need_based_items", "fieldtype": "Currency", "width": 120},
        {"label": "Total Reimbursements(F)", "fieldname": "total_reimbursement", "fieldtype": "Currency", "width": 160},
        {"label": "Total Net Pay(A-B-C+D+E+F)", "fieldname": "total_net_pay", "fieldtype": "Currency", "width": 180}
    ]

def get_data(filters):
    salary_slips = frappe.get_all("Salary Slip", filters=filters, fields=["*"])
    data = []

    for s in salary_slips:
        employee_doc = frappe.get_value(
            "Employee",
            s.employee,
            ["date_of_joining", "gender", "date_of_birth", "pan_number", "employment_type", "payroll_cost_center", "company"],
            as_dict=True
        ) or {}

        payroll_month = getdate(s.start_date).strftime('%b').upper() + " - " + getdate(s.start_date).strftime('%Y')

        # Initialize contribution/deduction components
        pf_employee_contribution = pf_employer_contribution = pf_other = 0
        esi_employee = esi_employer = 0

        # Initialize earning components
        base = hra = special_allowance = lta = 0

        # Get earnings
        earnings = frappe.get_all(
            "Salary Detail",
            filters={"parent": s.name, "parenttype": "Salary Slip", "parentfield": "earnings"},
            fields=["salary_component", "amount"]
        )

        for e in earnings:
            if e.salary_component == "Basic":
                base = e.amount
            elif e.salary_component == "House Rent Allowance":
                hra = e.amount
            elif e.salary_component == "Special Allowance":
                special_allowance = e.amount
            elif e.salary_component == "Travel Reimbursement (LTA)":
                lta = e.amount

        # Get deductions
        deductions = frappe.get_all(
            "Salary Detail",
            filters={"parent": s.name, "parenttype": "Salary Slip", "parentfield": "deductions"},
            fields=["salary_component", "amount"]
        )

        for d in deductions:
            if d.salary_component == "PF employee":
                pf_employee_contribution = d.amount
            elif d.salary_component == "PF employer":
                pf_employer_contribution = d.amount
            elif d.salary_component == "PF - Other Charges":
                pf_other = d.amount
            elif d.salary_component == "ESIC employee":
                esi_employee = d.amount
            elif d.salary_component == "ESIC employer":
                esi_employer = d.amount
            elif d.salary_component == "Professional Tax":
                professional_tax = d.amount
            elif d.salary_component == "Income Tax":
                income_tax = d.amount
            elif d.salary_component == "ESIC employer":
                esi_employer = d.amount
            elif d.salary_component == "Loan EMI":
                loan_emi = d.amount

        total_contributions = pf_employee_contribution + pf_employer_contribution + pf_other + esi_employee + esi_employer
        total_net_pay = (s.net_pay or 0) + (s.cash_advance or 0) + (s.settlement_against_advance or 0) + (s.total_reimbursement or 0)

        data.append({
            "employee": s.employee,
            "employee_name": s.employee_name,
            "designation": s.designation,
            "date_of_joining": employee_doc.date_of_joining,
            "gender": employee_doc.gender,
            "date_of_birth": employee_doc.date_of_birth,
            "branch": s.branch,
            "department": s.department,
            "employment_type": employee_doc.employment_type,
            "cost_center": employee_doc.payroll_cost_center,
            "business_unit": employee_doc.company,
            "pan_number": employee_doc.pan_number,
            "payroll_month": payroll_month,
            "payroll_frequency": s.payroll_frequency,
            "status": "ExecutedAsSalary",
            "salary_slip_status": "ExecutedAsSalary",
            "payment_days": s.payment_days,
            "total_working_days": s.total_working_days,
            "leave_without_pay": s.leave_without_pay,
            "days_payable": s.payment_days,
            "payable_units": f"{int(s.payment_days or 0)}/{int(s.total_working_days or 1)} Days",
            "gross_pay": s.gross_pay,
            "base": base,
            "hra": hra,
            "special_allowance": special_allowance,
            "lta": lta,
            "pf_employee_contribution": pf_employee_contribution,
            "pf_employer_contribution": pf_employer_contribution,
            "pf_other": pf_other,
            "esi_employee_contribution": esi_employee,
            "esi_employer_contribution": esi_employer,
            "total_contributions": s.custom_total_deduction_amount,
            "professional_tax": s.professional_tax,
            "loan_emi": s.loan_emi,
            "ad_hoc_deduction": s.ad_hoc_deduction,
            "income_tax": s.income_tax,
            "total_deduction": s.total_deduction,
            "net_pay": s.net_pay,
            "cash_advance": s.cash_advance,
            "settlement_against_advance": s.settlement_against_advance,
            "need_based_items": s.need_based_items,
            "total_reimbursement": s.total_reimbursement,
            "total_net_pay": total_net_pay
        })

    return data
