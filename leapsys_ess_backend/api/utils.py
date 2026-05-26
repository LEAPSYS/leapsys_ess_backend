import frappe
from frappe import _

def get_current_employee():
    """
    Fetches the Employee record associated with the currently authenticated ERPNext user.
    Throws an error if the user is not linked to an employee.
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)
        
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    if not employee:
        frappe.throw(_("No Employee profile found for the logged-in user {0}.").format(frappe.session.user))
        
    return employee
