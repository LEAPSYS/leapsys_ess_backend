import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    """
    Custom wrapper around standard login to return additional metadata
    useful for the mobile app (like API key/secret, user roles).
    """
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success": False,
            "message": _("Incorrect User or Password")
        }
        return

    # Generate or get API secrets
    user = frappe.get_doc("User", usr)
    api_secret = frappe.generate_hash(length=15)
    
    # Check if api keys are generated, if not generate them
    if not user.api_key:
        api_key = frappe.generate_hash(length=15)
        user.api_key = api_key
    
    user.api_secret = api_secret
    user.save(ignore_permissions=True)
    frappe.db.commit()

    frappe.local.response["message"] = {
        "success": True,
        "message": _("Logged In Successfully"),
        "api_key": user.api_key,
        "api_secret": api_secret,
        "full_name": user.full_name,
        "email": user.email,
        "roles": frappe.get_roles(usr)
    }

@frappe.whitelist()
def logout():
    """
    Custom logout endpoint.
    """
    frappe.local.login_manager.logout()
    frappe.db.commit()
    frappe.local.response["message"] = {
        "success": True,
        "message": _("Logged Out Successfully")
    }

@frappe.whitelist()
def check_auth():
    if frappe.session.user == 'Guest':
        frappe.throw(_("Not logged in"), frappe.AuthenticationError)
        
    employee = frappe.get_all("Employee", filters={"user_id": frappe.session.user}, fields=["name", "employee_name", "image"])
    
    frappe.local.response["message"] = {
        "success": True,
        "employee": employee[0] if employee else None
    }
