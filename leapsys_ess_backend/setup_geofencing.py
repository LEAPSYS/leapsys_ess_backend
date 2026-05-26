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
        ],
        "Customer": [
            {"fieldname": "custom_geofencing_section", "label": "Geofencing", "fieldtype": "Section Break"},
            {"fieldname": "custom_latitude", "label": "Latitude", "fieldtype": "Float"},
            {"fieldname": "custom_longitude", "label": "Longitude", "fieldtype": "Float"},
            {"fieldname": "custom_geofence_radius", "label": "Radius (meters)", "fieldtype": "Int", "default": "100"}
        ],
        "Lead": [
            {"fieldname": "custom_geofencing_section", "label": "Geofencing", "fieldtype": "Section Break"},
            {"fieldname": "custom_latitude", "label": "Latitude", "fieldtype": "Float"},
            {"fieldname": "custom_longitude", "label": "Longitude", "fieldtype": "Float"},
            {"fieldname": "custom_geofence_radius", "label": "Radius (meters)", "fieldtype": "Int", "default": "100"}
        ],
        "Maintenance Visit": [
            {"fieldname": "custom_tracking_section", "label": "GPS Tracking Audit", "fieldtype": "Section Break", "insert_after": "maintenance_type"},
            {"fieldname": "custom_enable_geofencing", "label": "Enable Geofence Verification", "fieldtype": "Check", "insert_after": "custom_tracking_section"},
            
            {"fieldname": "custom_travel_start_time", "label": "Travel Start Time", "fieldtype": "Datetime", "insert_after": "custom_enable_geofencing", "read_only": 1},
            {"fieldname": "custom_travel_start_lat", "label": "Travel Start Lat", "fieldtype": "Float", "insert_after": "custom_travel_start_time", "read_only": 1},
            {"fieldname": "custom_travel_start_lon", "label": "Travel Start Lon", "fieldtype": "Float", "insert_after": "custom_travel_start_lat", "read_only": 1},
            
            {"fieldname": "custom_reached_time", "label": "Reached Time", "fieldtype": "Datetime", "insert_after": "custom_travel_start_lon", "read_only": 1},
            {"fieldname": "custom_reached_lat", "label": "Reached Lat", "fieldtype": "Float", "insert_after": "custom_reached_time", "read_only": 1},
            {"fieldname": "custom_reached_lon", "label": "Reached Lon", "fieldtype": "Float", "insert_after": "custom_reached_lat", "read_only": 1},
            
            {"fieldname": "custom_service_start_time", "label": "Service Start Time", "fieldtype": "Datetime", "insert_after": "custom_reached_lon", "read_only": 1},
            {"fieldname": "custom_service_start_lat", "label": "Service Start Lat", "fieldtype": "Float", "insert_after": "custom_service_start_time", "read_only": 1},
            {"fieldname": "custom_service_start_lon", "label": "Service Start Lon", "fieldtype": "Float", "insert_after": "custom_service_start_lat", "read_only": 1},
            
            {"fieldname": "custom_service_end_time", "label": "Service End Time", "fieldtype": "Datetime", "insert_after": "custom_service_start_lon", "read_only": 1},
            {"fieldname": "custom_service_end_lat", "label": "Service End Lat", "fieldtype": "Float", "insert_after": "custom_service_end_time", "read_only": 1},
            {"fieldname": "custom_service_end_lon", "label": "Service End Lon", "fieldtype": "Float", "insert_after": "custom_service_end_lat", "read_only": 1}
        ]
    }

    create_custom_fields(custom_fields, ignore_validate=True)
    frappe.db.commit()
    print("Geofencing custom fields created successfully.")
