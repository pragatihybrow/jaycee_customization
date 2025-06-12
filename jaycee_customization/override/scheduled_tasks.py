
# import frappe
# from frappe.utils import getdate, nowdate
# import calendar

# def add_compensatory_leaves():
#     today = getdate(nowdate())
#     start_of_month = today.replace(day=1)
#     end_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])
#     leave_type = "Paid Leave"

#     employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])

#     for emp in employees:
#         # Check if leave allocation already exists for this employee, leave type, and month
#         existing_allocation = frappe.db.exists(
#             "Leave Allocation",
#             {
#                 "employee": emp["name"],
#                 "leave_type": leave_type,
#                 "from_date": ("<=", end_of_month),
#                 "to_date": (">=", start_of_month),
#                 "docstatus": 1,
#             }
#         )

#         if existing_allocation:
#             frappe.logger().info(f"[Leave Allocation Skipped] Employee: {emp['name']} already has allocation: {existing_allocation}")
#             continue

#         # Create and submit new Leave Allocation
#         try:
#             doc = frappe.get_doc({
#                 "doctype": "Leave Allocation",
#                 "employee": emp["name"],
#                 "leave_type": leave_type,
#                 "from_date": start_of_month,
#                 "to_date": end_of_month,
#                 "new_leaves_allocated": 2,  # Allocating 2 Paid Leaves
#                 "company": emp["company"],
#                 "docstatus": 0
#             })
#             doc.insert()
#             doc.submit()
#             frappe.logger().info(f"[Leave Allocation Created] Employee: {emp['name']} - Allocation ID: {doc.name}")
#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), f"Leave Allocation Failed for {emp['name']}")


import frappe
from frappe.utils import getdate, nowdate
from datetime import datetime
import calendar

def add_compensatory_leaves():
    today = getdate(nowdate())
    
    # Calculate previous month and year
    if today.month == 1:
        prev_month = 12
        prev_year = today.year - 3
    else:
        prev_month = today.month - 3
        prev_year = today.year

    start_of_month = datetime(prev_year, prev_month, 1).date()
    end_of_month = datetime(prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1]).date()
    
    leave_type = "Paid Leave"

    employees = frappe.db.get_list("Employee", fields=["name", "company"])

    for emp in employees:
        # Check if leave allocation already exists for this employee, leave type, and that month
        existing_allocation = frappe.db.exists(
            "Leave Allocation",
            {
                "employee": emp["name"],
                "leave_type": leave_type,
                "from_date": ("<=", end_of_month),
                "to_date": (">=", start_of_month),
                "docstatus": 1,
                "new_leaves_allocated":2
            }
        )

        if existing_allocation:
            frappe.msgprint(f"[Leave Allocation Skipped] Employee: {emp['name']} already has allocation: {existing_allocation}")
            continue

        # Create and submit new Leave Allocation
        try:
            doc = frappe.get_doc({
                "doctype": "Leave Allocation",
                "employee": emp["name"],
                "leave_type": leave_type,
                "from_date": start_of_month,
                "to_date": end_of_month,
                "new_leaves_allocated": 2,
                "company": emp["company"],
                "docstatus": 0
            })
            doc.insert()
            doc.submit()
            frappe.msgprint(f"[Leave Allocation Created] Employee: {emp['name']} - Allocation ID: {doc.name}")
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Leave Allocation Failed for {emp['name']}")
