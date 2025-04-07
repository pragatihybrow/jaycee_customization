import frappe
from frappe.utils import today, get_first_day, add_months

def add_compensatory_leaves():
    leave_type = "Paid Leave"  # Corrected Leave Type
    first_day_of_month = get_first_day(today())

    # Check if Leave Type exists
    if not frappe.db.exists("Leave Type", leave_type):
        frappe.throw(f"Leave Type '{leave_type}' does not exist. Please create it manually.")

    # Fetch all active employees
    employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])

    for emp in employees:
        # Check if leave allocation already exists for this month
        existing_allocation = frappe.get_all("Leave Allocation", 
            filters={
                "employee": emp.name,
                "leave_type": leave_type,
                "from_date": first_day_of_month,
                "docstatus": 1  # Only check submitted records
            }
        )

        if not existing_allocation:
            leave_allocation = frappe.get_doc({
                "doctype": "Leave Allocation",
                "employee": emp.name,
                "leave_type": leave_type,
                "from_date": first_day_of_month,
                "to_date": add_months(first_day_of_month, 1),
                "new_leaves_allocated": 2,
                "docstatus": 1  # Auto-submit
            })
            leave_allocation.insert(ignore_permissions=True)
            frappe.db.commit()

            frappe.msgprint(f"Added 2 compensatory off leaves for {emp.name}")
