import frappe
import os
import json

def execute():
    # Force delete the corrupted record if it exists
    if frappe.db.exists("DocType", "Leapsys ESS App Settings"):
        frappe.delete_doc("DocType", "Leapsys ESS App Settings", ignore_missing=True, force=True)
    
    # Get the exact absolute path to the JSON file relative to THIS patch file
    patch_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(patch_dir), "leapsys_ess_backend", "doctype", "leapsys_ess_app_settings", "leapsys_ess_app_settings.json")
    
    with open(json_path, "r") as f:
        doc_dict = json.load(f)
    
    # Manually insert the DocType into the database
    doc = frappe.get_doc(doc_dict)
    doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
    
    # Commit schema so it's queryable for get_single
    frappe.db.commit()
    
    # Seed default values
    settings = frappe.get_single("Leapsys ESS App Settings")
    settings.company_name = "LEAPSYS"
    settings.primary_color = "#0056b3"
    settings.secondary_color = "#e9ecef"
    settings.enable_geofencing = 1
    settings.enable_offline_mode = 0
    settings.enable_service_module = 1
    settings.enable_sales_module = 1
    settings.enable_chatbot = 0
    settings.save(ignore_permissions=True)
