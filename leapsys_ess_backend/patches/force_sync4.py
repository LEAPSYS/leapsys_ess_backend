import frappe

def execute():
    try:
        # Force reload the custom doctypes we just created JSONs for
        frappe.reload_doc("leapsys_ess_backend", "doctype", "ess_device_registration")
        frappe.reload_doc("leapsys_ess_backend", "doctype", "ess_employee_location_log")
        
        # Verify they exist
        if not frappe.db.exists("DocType", "ESS Employee Location Log"):
            frappe.log_error("ESS Employee Location Log DocType failed to sync during patch.")
            
    except Exception as e:
        frappe.log_error(title="Failed force_sync4 patch", message=str(e))
