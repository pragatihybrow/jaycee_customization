# # Copyright (c) 2025, Pragati Dike and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.utils import getdate
# from collections import defaultdict
# from calendar import month_name, monthrange

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
#         {"label": "Leave Allocated", "fieldname": "allocated", "fieldtype": "Float", "width": 120},
#         {"label": "Leave Taken", "fieldname": "taken_link", "fieldtype": "HTML", "width": 120},
#         {"label": "Balance", "fieldname": "balance", "fieldtype": "Float", "width": 100},
#     ]

# def get_data(filters):
#     employee = filters.get("employee") if filters else None
#     if not employee:
#         frappe.throw("Please select an Employee to generate the report.")

#     ledger_entries = frappe.db.sql(f"""
#         SELECT from_date, to_date, leaves, transaction_type
#         FROM `tabLeave Ledger Entry`
#         WHERE docstatus = 1 AND employee = %s
#         ORDER BY from_date
#     """, (employee,), as_dict=True)

#     monthly_summary = defaultdict(lambda: {"allocated": 0, "taken": 0})

#     for entry in ledger_entries:
#         month_key = getdate(entry.from_date).strftime("%Y-%m")
#         if entry.transaction_type == "Leave Allocation":
#             monthly_summary[month_key]["allocated"] += entry.leaves
#         elif entry.transaction_type == "Leave Application":
#             monthly_summary[month_key]["taken"] += abs(entry.leaves)

#     sorted_months = sorted(monthly_summary.keys())
#     cumulative_balance = 0
#     final_data = []

#     for month in sorted_months:
#         allocated = monthly_summary[month]["allocated"]
#         taken = monthly_summary[month]["taken"]
#         cumulative_balance += allocated - taken

#         # Display as "Month Year"
#         year = int(month.split("-")[0])
#         mon = int(month.split("-")[1])
#         month_display = f"{month_name[mon]} {year}"

#         # Calculate full month date range
#         last_day = monthrange(year, mon)[1]
#         from_date = f"{month}-01"
#         to_date = f"{month}-{last_day:02d}"

#         # Create clickable link showing all leave apps for that month
#         leave_link = f"""
#             <a href="/app/leave-application?view=list&employee={employee}"
#                target="_blank" style="text-decoration: underline; color: #007bff;">
#                {taken}
#             </a>
#         """

#         final_data.append({
#             "month": month_display,
#             "allocated": allocated,
#             "taken_link": leave_link,
#             "balance": cumulative_balance
#         })

#     return final_data



# Copyright (c) 2025, Pragati Dike and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from collections import defaultdict
from calendar import month_name, monthrange

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
        {"label": "Leave Allocated", "fieldname": "allocated", "fieldtype": "Float", "width": 120},
        {"label": "Leave Taken", "fieldname": "taken_link", "fieldtype": "HTML", "width": 120},
        {"label": "Unpaid Leave", "fieldname": "unpaid_leave", "fieldtype": "Float", "width": 120},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Float", "width": 100},
    ]

def get_data(filters):
    employee = filters.get("employee") if filters else None
    if not employee:
        frappe.throw("Please select an Employee to generate the report.")

    ledger_entries = frappe.db.sql("""
        SELECT from_date, to_date, leaves, transaction_type, leave_type
        FROM `tabLeave Ledger Entry`
        WHERE docstatus = 1 AND employee = %s
        ORDER BY from_date
    """, (employee,), as_dict=True)

    monthly_summary = defaultdict(lambda: {"allocated": 0, "taken": 0, "unpaid": 0})

    for entry in ledger_entries:
        month_key = getdate(entry.from_date).strftime("%Y-%m")

        if entry.transaction_type == "Leave Allocation":
            monthly_summary[month_key]["allocated"] += entry.leaves

        elif entry.transaction_type == "Leave Application":
            if entry.leave_type == "Unpaid Leave":
                monthly_summary[month_key]["unpaid"] += abs(entry.leaves)
            else:
                monthly_summary[month_key]["taken"] += abs(entry.leaves)

    sorted_months = sorted(monthly_summary.keys())
    cumulative_balance = 0
    final_data = []

    for month in sorted_months:
        allocated = monthly_summary[month]["allocated"]
        taken = monthly_summary[month]["taken"]
        unpaid = monthly_summary[month]["unpaid"]
        cumulative_balance += allocated - taken  # Exclude unpaid from balance

        year = int(month.split("-")[0])
        mon = int(month.split("-")[1])
        month_display = f"{month_name[mon]} {year}"

        last_day = monthrange(year, mon)[1]
        from_date = f"{month}-01"
        to_date = f"{month}-{last_day:02d}"

        # Link to all leave applications (not filtered by type)
        leave_link = f"""
            <a href="/app/leave-application?view=list&employee={employee}"
               target="_blank" style="text-decoration: underline; color: #007bff;">
               {taken}
            </a>
        """

        final_data.append({
            "month": month_display,
            "allocated": allocated,
            "taken_link": leave_link,
            "unpaid_leave": unpaid,
            "balance": cumulative_balance
        })

    return final_data
