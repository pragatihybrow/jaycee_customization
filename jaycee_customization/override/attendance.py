
# import frappe
# from frappe.utils import getdate, now_datetime

# def add_comp_off_directly(attendance, method):
#     attendance_date = getdate(attendance.attendance_date)

#     # Check if it's a Sunday (Python: 6 = Sunday) and if the employee is Present
#     if attendance_date.weekday() == 6 and attendance.status == "Present":
#         employee = attendance.employee
#         leave_type = "Compensatory Off"

#         # Check if "Compensatory Off" leave type exists
#         if not frappe.db.exists("Leave Type", leave_type):
#             frappe.throw(f"Leave Type '{leave_type}' does not exist. Please create it first.")

#         # Check if Leave Allocation exists for the employee
#         leave_allocation = frappe.get_value(
#             "Leave Allocation",
#             {"employee": employee, "leave_type": leave_type, "docstatus": 1},  # Only submitted allocations
#             ["name", "total_leaves_allocated"]
#         )

#         if leave_allocation:
#             allocation_name, total_leaves = leave_allocation
#             new_total = total_leaves + 1

#             # Update the existing Leave Allocation
#             frappe.db.set_value("Leave Allocation", allocation_name, "total_leaves_allocated", new_total)
#             frappe.msgprint(f"✅ 1 Comp-Off Leave added for {employee} on {attendance_date}. New Balance: {new_total}")
#         else:
#             # Create a new Leave Allocation if none exists
#             allocation = frappe.get_doc({
#                 "doctype": "Leave Allocation",
#                 "employee": employee,
#                 "leave_type": leave_type,
#                 "from_date": now_datetime().date(),
#                 "to_date": now_datetime().date().replace(year=now_datetime().date().year + 1),  # 1-year validity
#                 "total_leaves_allocated": 1,
#                 "docstatus": 1  # Auto-submit
#             })
#             allocation.insert(ignore_permissions=True)
#             frappe.msgprint(f"✅ New Comp-Off Leave Allocation created for {employee} with 1 leave.")

# def after_submit(attendance, method):
#     add_comp_off_directly(attendance, method)


import frappe
from frappe.utils import getdate, now_datetime

def add_comp_off_directly(attendance, method):
    attendance_date = getdate(attendance.attendance_date)

    # Check if the employee was present
    if attendance.status != "Present":
        return

    employee = attendance.employee
    leave_type = "Compensatory Off"

    # Check if attendance date is Sunday or Holiday
    is_sunday = attendance_date.weekday() == 6  # Sunday
    is_holiday = frappe.db.exists("Holiday", {
        "holiday_date": attendance_date,
        "parent": frappe.db.get_value("Employee", employee, "holiday_list")
    })

    if not (is_sunday or is_holiday):
        return  # Not eligible for comp-off

    # Check if Compensatory Off leave type exists
    if not frappe.db.exists("Leave Type", leave_type):
        frappe.throw(f"Leave Type '{leave_type}' does not exist. Please create it first.")

    # Check if Leave Allocation exists
    leave_allocation = frappe.get_value(
        "Leave Allocation",
        {"employee": employee, "leave_type": leave_type, "docstatus": 1},
        ["name", "total_leaves_allocated"]
    )

    if leave_allocation:
        allocation_name, total_leaves = leave_allocation
        new_total = total_leaves + 1

        frappe.db.set_value("Leave Allocation", allocation_name, "total_leaves_allocated", new_total)
        frappe.msgprint(f"✅ 1 Comp-Off Leave added for {employee} on {attendance_date}. New Balance: {new_total}")
    else:
        # Create a new Leave Allocation
        from_date = now_datetime().date()
        to_date = from_date.replace(year=from_date.year + 1)

        allocation = frappe.get_doc({
            "doctype": "Leave Allocation",
            "employee": employee,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            "total_leaves_allocated": 1,
            "docstatus": 1  # Submitted
        })
        allocation.insert(ignore_permissions=True)
        frappe.msgprint(f"✅ New Comp-Off Leave Allocation created for {employee} with 1 leave.")

def after_submit(attendance, method):
    add_comp_off_directly(attendance, method)
