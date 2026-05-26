import frappe
from frappe.modules.export_file import export_doc

def execute():
    # 1. ESS Device Registration
    if not frappe.db.exists("DocType", "ESS Device Registration"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "ESS Device Registration",
            "module": "Leapsys Ess Backend",
            "custom": 0,
            "is_submittable": 0,
            "fields": [
                {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "device_id", "label": "Device ID", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "device_name", "label": "Device Name", "fieldtype": "Data"},
                {"fieldname": "is_active", "label": "Is Active", "fieldtype": "Check", "default": "1"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                            {"role": "Employee", "read": 1, "write": 1, "create": 1}]
        })
        doc.insert(ignore_permissions=True)
        
    export_doc(frappe.get_doc("DocType", "ESS Device Registration"))

    # 2. ESS Employee Location Log
    if not frappe.db.exists("DocType", "ESS Employee Location Log"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "ESS Employee Location Log",
            "module": "Leapsys Ess Backend",
            "custom": 0,
            "is_submittable": 0,
            "fields": [
                {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "latitude", "label": "Latitude", "fieldtype": "Float", "reqd": 1},
                {"fieldname": "longitude", "label": "Longitude", "fieldtype": "Float", "reqd": 1},
                {"fieldname": "timestamp", "label": "Timestamp", "fieldtype": "Datetime", "reqd": 1, "in_list_view": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                            {"role": "Employee", "read": 1, "write": 1, "create": 1}]
        })
        doc.insert(ignore_permissions=True)

    export_doc(frappe.get_doc("DocType", "ESS Employee Location Log"))

    frappe.db.commit()
    print("Schemas generated successfully!")
