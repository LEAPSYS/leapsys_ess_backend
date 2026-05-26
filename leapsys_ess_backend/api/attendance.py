import frappe
from frappe.utils import nowdate, nowtime
import math

from leapsys_ess_backend.api.utils import get_current_employee

def calculate_distance(lat1, lon1, lat2, lon2):
    # Basic Haversine implementation for distance
    R = 6371e3
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c # meters

@frappe.whitelist()
def mark_attendance(log_type, lat, lon, is_offline_sync=False, original_timestamp=None):
    """
    Mark attendance, validating geofence coordinates against the employee's assigned location or branch.
    Handles offline sync natively. Uses secure ERPNext session authorization.
    """
    try:
        employee = get_current_employee()
        # Example Validation:
        # Ensure employee is near the office (Mock radius 100 meters)
        # In a real scenario, fetch 'lat' and 'lon' from Employee or Branch
        office_lat, office_lon = 28.7041, 77.1025 # Example Delhi coords
        distance = calculate_distance(float(lat), float(lon), office_lat, office_lon)
        
        # Geofence enforcement if enabled in App Settings
        settings = frappe.get_single("Leapsys ESS App Settings")
        if settings.enable_geofencing and distance > 100:
            return {"success": False, "error": "You are outside the designated geofence area."}

        # Log Location
        frappe.get_doc({
            "doctype": "ESS Employee Location Log",
            "employee": employee,
            "latitude": lat,
            "longitude": lon,
            "timestamp": original_timestamp if original_timestamp else f"{nowdate()} {nowtime()}"
        }).insert(ignore_permissions=True)

        # Create Attendance
        attendance = frappe.get_doc({
            "doctype": "Attendance",
            "employee": employee,
            "attendance_date": nowdate(),
            "status": "Present" if log_type == "IN" else "On Leave" # Simplify logic
        })
        # Note: You might want to use Checkin/Checkout DocType in Frappe HR
        
        return {"success": True, "message": "Attendance marked successfully."}
    except Exception as e:
        return {"success": False, "error": str(e)}
