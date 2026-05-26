import frappe
import json
from leapsys_ess_backend.api.utils import get_current_employee

@frappe.whitelist()
def get_maintenance_visits(date):
    """Fetch assigned maintenance visits for the service engineer for a specific date"""
    try:
        employee = get_current_employee()
        visits = frappe.get_all(
            "Maintenance Visit",
            filters={"mntc_date": date, "docstatus": 1},
            fields=["name", "customer", "status", "maintenance_type", "completion_status"]
        )
        return {"success": True, "data": visits}
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
