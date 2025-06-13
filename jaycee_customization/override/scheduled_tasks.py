
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


# import frappe
# from frappe.utils import getdate, nowdate
# from datetime import datetime
# import calendar

# def add_compensatory_leaves():
#     today = getdate(nowdate())
    
#     # Calculate previous month and year
#     if today.month == 1:
#         prev_month = 12
#         prev_year = today.year - 1
#     else:
#         prev_month = today.month - 1
#         prev_year = today.year

#     start_of_month = datetime(prev_year, prev_month, 1).date()
#     end_of_month = datetime(prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1]).date()
    
#     leave_type = "Compensatory Off"

#     employees = frappe.db.get_list("Employee", fields=["name", "company"])

#     for emp in employees:
#         # Check if leave allocation already exists for this employee, leave type, and that month
#         existing_allocation = frappe.db.exists(
#             "Leave Allocation",
#             {
#                 "employee": emp["name"],
#                 "leave_type": leave_type,
#                 "from_date": ("<=", end_of_month),
#                 "to_date": (">=", start_of_month),
#                 "docstatus": 1,
#                 "new_leaves_allocated":2
#             }
#         )

#         if existing_allocation:
#             frappe.msgprint(f"[Leave Allocation Skipped] Employee: {emp['name']} already has allocation: {existing_allocation}")
#             continue

#         # Create and submit new Leave Allocation
#         try:
#             doc = frappe.get_doc({
#                 "doctype": "Leave Allocation",
#                 "employee": emp["name"],
#                 "leave_type": leave_type,
#                 "from_date": start_of_month,
#                 "to_date": end_of_month,
#                 "new_leaves_allocated": 2,
#                 "company": emp["company"],
#                 "carry_forward":1,
#                 "docstatus": 0
#             })
#             doc.insert()
#             doc.submit()
#             frappe.msgprint(f"[Leave Allocation Created] Employee: {emp['name']} - Allocation ID: {doc.name}")
#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), f"Leave Allocation Failed for {emp['name']}")


# import frappe
# from frappe.utils import getdate, nowdate
# from datetime import datetime
# import calendar

# def get_unused_leaves(employee, leave_type, till_date):
#     result = frappe.db.sql("""
#         SELECT 
#             SUM(CASE WHEN leaves > 0 THEN leaves ELSE 0 END) AS allocated,
#             SUM(CASE WHEN leaves < 0 THEN ABS(leaves) ELSE 0 END) AS used
#         FROM `tabLeave Ledger Entry`
#         WHERE employee = %s
#           AND leave_type = %s
#           AND creation <= %s
#           AND docstatus = 1
#     """, (employee, leave_type, till_date), as_dict=True)

#     allocated = result[0].allocated or 0
#     used = result[0].used or 0
#     return round(allocated - used, 2)

# def add_compensatory_leaves():
#     today = getdate(nowdate())

#     # Previous month/year
#     if today.month == 1:
#         prev_month = 12
#         prev_year = today.year - 1
#     else:
#         prev_month = today.month - 1
#         prev_year = today.year

#     start_of_prev_month = datetime(prev_year, prev_month, 1).date()
#     end_of_prev_month = datetime(prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1]).date()
#     start_of_current_month = datetime(today.year, today.month, 1).date()
#     end_of_current_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).date()

#     leave_type = "Compensatory Off"
#     employees = frappe.db.get_list("Employee", fields=["name", "company"])

#     for emp in employees:
#         employee = emp["name"]
#         company = emp["company"]

#         # Check if already allocated for this month
#         existing_allocation = frappe.db.exists(
#             "Leave Allocation",
#             {
#                 "employee": employee,
#                 "leave_type": leave_type,
#                 "from_date": ("<=", end_of_current_month),
#                 "to_date": (">=", start_of_current_month),
#                 "docstatus": 1,
#                 "new_leaves_allocated": 2
#             }
#         )

#         if existing_allocation:
#             frappe.msgprint(f"[Skipped] Employee: {employee} already has allocation: {existing_allocation}")
#             continue

#         # Carry forward unused leaves from last month
#         unused_leaves = get_unused_leaves(employee, leave_type, end_of_prev_month)

#         try:
#             doc = frappe.get_doc({
#                 "doctype": "Leave Allocation",
#                 "employee": employee,
#                 "leave_type": leave_type,
#                 "from_date": start_of_current_month,
#                 "to_date": end_of_current_month,
#                 "new_leaves_allocated": 2,
#                 "company": company,
#                 "carry_forward": 1 if unused_leaves > 0 else 0,
#                 "docstatus": 0
#             })
#             doc.insert()
#             doc.submit()

#             frappe.msgprint(f"[Created] {employee} → Allocation: {doc.name} | Carried: {unused_leaves}")

#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), f"[Failed] Leave Allocation for {employee}")


import frappe
from frappe.utils import nowdate, getdate
from datetime import datetime, timedelta

def add_compensatory_leaves():
    leave_type = "Monthly Paid Leave"
    today = getdate(nowdate())
   
    current_year = today.year 
    current_month = today.month 

    from_date = datetime(current_year, current_month, 1)
    to_date = datetime(current_year, current_month, 1) + timedelta(days=32)
    to_date = datetime(to_date.year, to_date.month, 1) - timedelta(days=1)

    active_employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name", "company"])

    for emp in active_employees:
        existing = frappe.get_all("Leave Allocation", filters={
            "employee": emp.name,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            "docstatus": 1
        })

        if not existing:
            previous_alloc = frappe.get_all(
                "Leave Allocation",
                filters={
                    "employee": emp.name,
                    "leave_type": leave_type,
                    "docstatus": 1
                },
                order_by="to_date desc",
                limit=1,
                fields=["name", "total_leaves_allocated", "from_date", "to_date"]
            )

            carry_forwarded = 0
            if previous_alloc:
                total_allocated = previous_alloc[0]["total_leaves_allocated"]
                prev_from = previous_alloc[0]["from_date"]
                prev_to = previous_alloc[0]["to_date"]

                # Count leaves taken in the previous allocation period
                leaves_taken = frappe.db.count("Leave Application", {
                    "employee": emp.name,
                    "leave_type": leave_type,
                    "docstatus": 1,
                    "from_date": (">=", prev_from),
                    "to_date": ("<=", prev_to)
                })

                carry_forwarded = max(total_allocated - leaves_taken, 0)

            total_leaves = 2 + carry_forwarded

            alloc = frappe.new_doc("Leave Allocation")
            alloc.employee = emp.name
            alloc.leave_type = leave_type
            alloc.from_date = from_date
            alloc.to_date = to_date
            alloc.carry_forward = 1
            alloc.new_leaves_allocated = 2
            alloc.total_leaves_allocated = total_leaves
            alloc.company = emp.company
            alloc.submit()
