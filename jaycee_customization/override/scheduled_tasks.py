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

