import frappe
import json
from leapsys_ess_backend.api.utils import get_current_employee

from frappe.utils import now_datetime

@frappe.whitelist()
def get_maintenance_visits(date):
    """Fetch assigned maintenance visits for the service engineer for a specific date"""
    try:
        employee = get_current_employee()
        visits = frappe.get_all(
            "Maintenance Visit",
            filters={"mntc_date": date, "docstatus": ["<", 2]},
            fields=[
                "name", "customer", "status", "maintenance_type", "completion_status",
                "custom_enable_geofencing",
                "custom_travel_start_time", "custom_reached_time", 
                "custom_service_start_time", "custom_service_end_time"
            ]
        )
        
        # Attach customer coordinates
        for visit in visits:
            if visit.customer:
                cust = frappe.get_value("Customer", visit.customer, ["custom_latitude", "custom_longitude", "custom_geofence_radius"], as_dict=True)
                if cust:
                    visit.update(cust)
                    
        return {"success": True, "data": visits}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_maintenance_visit(customer, date, purpose):
    try:
        employee = get_current_employee()
        visit = frappe.get_doc({
            "doctype": "Maintenance Visit",
            "customer": customer,
            "mntc_date": date,
            "purposes": [{"item_code": purpose, "description": "Created from ESS App"}]
        })
        visit.insert(ignore_permissions=True)
        return {"success": True, "message": "Visit created successfully", "name": visit.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_issue(customer, subject, description):
    try:
        issue = frappe.get_doc({
            "doctype": "Issue",
            "customer": customer,
            "subject": subject,
            "description": description,
            "status": "Open",
            "raised_by": frappe.session.user
        })
        issue.insert(ignore_permissions=True)
        return {"success": True, "message": "Service Call created successfully", "name": issue.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def update_visit_tracking_status(visit_name, step, lat, lon):
    try:
        visit = frappe.get_doc("Maintenance Visit", visit_name)
        now = now_datetime()
        
        if step == 'travel_start':
            visit.custom_travel_start_lat = lat
            visit.custom_travel_start_lon = lon
            visit.custom_travel_start_time = now
            visit.status = "Draft" # Example status progression
        elif step == 'reached':
            visit.custom_reached_lat = lat
            visit.custom_reached_lon = lon
            visit.custom_reached_time = now
        elif step == 'service_start':
            visit.custom_service_start_lat = lat
            visit.custom_service_start_lon = lon
            visit.custom_service_start_time = now
        elif step == 'service_end':
            visit.custom_service_end_lat = lat
            visit.custom_service_end_lon = lon
            visit.custom_service_end_time = now
            visit.completion_status = "Fully Completed"
            
        visit.save(ignore_permissions=True)
        return {"success": True, "message": f"Updated tracking: {step}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_sales_order(customer, items):
    """Create a Sales Order on-site"""
    try:
        items_list = json.loads(items) if isinstance(items, str) else items
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": customer,
            "order_type": "Sales",
            "items": items_list
        })
        so.insert()
        return {"success": True, "message": "Sales Order created successfully", "name": so.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_bag_inventory():
    """Get the inventory in the engineer's assigned warehouse/bag"""
    try:
        employee = get_current_employee()
        # Assuming the employee is linked to a specific Warehouse (e.g. via a custom field or naming convention)
        warehouse = f"Bag - {employee}"
        inventory = frappe.get_all(
            "Bin",
            filters={"warehouse": warehouse, "actual_qty": [">", 0]},
            fields=["item_code", "actual_qty"]
        )
        return {"success": True, "data": inventory}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def update_maintenance_visit(visit_name, status, completion_status):
    """Update maintenance visit status"""
    try:
        employee = get_current_employee()
        visit = frappe.get_doc("Maintenance Visit", visit_name)
        visit.status = status
        visit.completion_status = completion_status
        visit.save()
        return {"success": True, "message": f"Visit {visit_name} updated successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_issues():
    """Fetch assigned issues/tickets"""
    try:
        employee = get_current_employee()
        issues = frappe.get_all(
            "Issue",
            filters={"status": ["!=", "Closed"]},
            fields=["name", "subject", "status", "priority", "customer"]
        )
        return {"success": True, "data": issues}
    except Exception as e:
        return {"success": False, "error": str(e)}
