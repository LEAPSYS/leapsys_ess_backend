import frappe

def execute():
    # If a corrupted manual version exists, delete it first
    if frappe.db.exists("DocType", "Leapsys ESS App Settings"):
        # We use ignore_missing and force to ensure it gets wiped clean
        frappe.delete_doc("DocType", "Leapsys ESS App Settings", ignore_missing=True, force=True)
    
    # Force Frappe to read our exact JSON file from the module and insert it
    frappe.reload_doc("leapsys_ess_backend", "doctype", "leapsys_ess_app_settings")
