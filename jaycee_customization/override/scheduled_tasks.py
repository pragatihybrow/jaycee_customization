import frappe
from frappe.utils import nowdate, getdate

def add_compensatory_leaves():
    current_date = frappe.utils.getdate(frappe.utils.nowdate())


    active_employees = frappe.get_all("Employee", 
        filters={"status": "Active"}, 
        fields=["name", "employee_name", "company", "department", "final_confirmation_date"]
    )

    for employee in active_employees:
        # if employee.final_confirmation_date and frappe.utils.getdate(employee.final_confirmation_date) <= current_date:
        leave_allocation = frappe.new_doc("Leave Allocation")
        leave_allocation.employee = employee.name
        leave_allocation.employee_name = employee.employee_name
        leave_allocation.department = employee.department
        leave_allocation.leave_type = "Paid Leave"  
        leave_allocation.company = employee.company
        leave_allocation.from_date = current_date
        leave_allocation.to_date = frappe.utils.get_last_day(current_date)  
        leave_allocation.new_leaves_allocated = 2
        leave_allocation.carry_forward = 1  
        leave_allocation.insert(ignore_permissions=True)
        leave_allocation.submit()




# import frappe
# from frappe.utils import getdate
# from calendar import monthrange
# from datetime import datetime

# def add_compensatory_leaves():
#     today = getdate()
    
#     # Always target April of the current year (or adjust year if today is Jan-Mar)
#     current_year = today.year
#     april_month = 4

#     # If today is in Jan/Feb/Mar, allocate for April of the *previous year*
#     if today.month < april_month:
#         current_year -= 1

#     from_date = datetime(current_year, april_month, 1)
#     to_date = datetime(current_year, april_month, monthrange(current_year, april_month)[1])

#     active_employees = frappe.get_all(
#         "Employee",
#         filters={"status": "Active"},
#         fields=["name", "employee_name", "company", "department", "final_confirmation_date"]
#     )

#     for employee in active_employees:
#         # Optional: Check if confirmed before April
#         # if employee.final_confirmation_date and getdate(employee.final_confirmation_date) <= to_date:
#         leave_allocation = frappe.new_doc("Leave Allocation")
#         leave_allocation.employee = employee.name
#         leave_allocation.employee_name = employee.employee_name
#         leave_allocation.department = employee.department
#         leave_allocation.leave_type = "Paid Leave"
#         leave_allocation.company = employee.company
#         leave_allocation.from_date = from_date
#         leave_allocation.to_date = to_date
#         leave_allocation.new_leaves_allocated = 2
#         leave_allocation.carry_forward = 1
#         leave_allocation.insert(ignore_permissions=True)
#         leave_allocation.submit()

