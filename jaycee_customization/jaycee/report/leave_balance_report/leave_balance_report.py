# # Copyright (c) 2025, Pragati Dike and contributors
# # For license information, please see license.txt



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

    # --- Step 1: Get leave allocations (only new leaves, ignore carry forward)
    leave_allocations = frappe.get_all(
        "Leave Allocation",
        filters={
            "employee": employee,
            "docstatus": 1,
            "expired":0
        },
        fields=["from_date", "to_date", "new_leaves_allocated"]
    )

    monthly_summary = defaultdict(lambda: {"allocated": 0, "taken": 0, "unpaid": 0})

    for alloc in leave_allocations:
        month_key = getdate(alloc.from_date).strftime("%Y-%m")
        monthly_summary[month_key]["allocated"] += alloc.new_leaves_allocated or 0

    # --- Step 2: Get leaves taken
    leave_apps = frappe.get_all(
        "Leave Application",
        filters={
            "employee": employee,
            "docstatus": 1
        },
        fields=["from_date", "to_date", "total_leave_days", "leave_type"]
    )

    for app in leave_apps:
        month_key = getdate(app.from_date).strftime("%Y-%m")
        if app.leave_type == "Unpaid Leave":
            monthly_summary[month_key]["unpaid"] += app.total_leave_days or 0
        else:
            monthly_summary[month_key]["taken"] += app.total_leave_days or 0

    # --- Step 3: Compile final result
    sorted_months = sorted(monthly_summary.keys())
    cumulative_balance = 0
    final_data = []

    for month in sorted_months:
        allocated = monthly_summary[month]["allocated"]
        taken = monthly_summary[month]["taken"]
        unpaid = monthly_summary[month]["unpaid"]
        cumulative_balance += allocated - taken

        year = int(month.split("-")[0])
        mon = int(month.split("-")[1])
        month_display = f"{month_name[mon]} - {year}"

        last_day = monthrange(year, mon)[1]
        from_date = f"{month}-01"
        to_date = f"{month}-{last_day:02d}"

        leave_link = f"""
            <a href="/app/leave-application?view=list&employee={employee}&from_date={from_date}&to_date={to_date}"
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
