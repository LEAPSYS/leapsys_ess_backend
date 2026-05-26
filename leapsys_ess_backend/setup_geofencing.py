import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup():
    custom_fields = {
        "Task": [
            {
                "fieldname": "custom_geofencing_section",
                "label": "Geofencing",
                "fieldtype": "Section Break",
                "insert_after": "description"
            },
            {
                "fieldname": "custom_enable_geofencing",
                "label": "Enable Geofencing for Timesheets",
                "fieldtype": "Check",
                "insert_after": "custom_geofencing_section"
            },
            {
                "fieldname": "custom_latitude",
                "label": "Latitude",
                "fieldtype": "Float",
                "depends_on": "custom_enable_geofencing",
                "insert_after": "custom_enable_geofencing"
            },
            {
                "fieldname": "custom_longitude",
                "label": "Longitude",
                "fieldtype": "Float",
                "depends_on": "custom_enable_geofencing",
                "insert_after": "custom_latitude"
            },
            {
                "fieldname": "custom_geofence_radius",
                "label": "Radius (meters)",
                "fieldtype": "Int",
                "default": "100",
                "depends_on": "custom_enable_geofencing",
                "insert_after": "custom_longitude"
            }
        ],
        "Timesheet Detail": [
            {
                "fieldname": "custom_location_section",
                "label": "Location Tracking",
                "fieldtype": "Section Break",
                "insert_after": "description"
            },
            {
                "fieldname": "custom_start_latitude",
                "label": "Start Latitude",
                "fieldtype": "Float",
                "insert_after": "custom_location_section"
            },
            {
                "fieldname": "custom_start_longitude",
                "label": "Start Longitude",
                "fieldtype": "Float",
                "insert_after": "custom_start_latitude"
            },
            {
                "fieldname": "custom_end_latitude",
                "label": "End Latitude",
                "fieldtype": "Float",
                "insert_after": "custom_start_longitude"
            },
            {
                "fieldname": "custom_end_longitude",
                "label": "End Longitude",
                "fieldtype": "Float",
                "insert_after": "custom_end_latitude"
            }
        ]
    }

    create_custom_fields(custom_fields, ignore_validate=True)
    frappe.db.commit()
    print("Geofencing custom fields created successfully.")
