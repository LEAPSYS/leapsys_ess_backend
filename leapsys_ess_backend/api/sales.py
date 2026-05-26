import frappe
import json
from leapsys_ess_backend.api.utils import get_current_employee

@frappe.whitelist()
def get_customers():
    """Fetch customers assigned to the logged-in user or all if permitted"""
    try:
        employee = get_current_employee()
        customers = frappe.get_all(
            "Customer",
            fields=["name", "customer_name", "customer_group", "territory"],
            order_by="modified desc",
            limit=50
        )
        return {"success": True, "data": customers}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_leads():
    """Fetch active leads"""
    try:
        employee = get_current_employee()
        leads = frappe.get_all(
            "Lead",
            filters={"status": ["!=", "Converted"]},
            fields=["name", "lead_name", "company_name", "status"],
            order_by="modified desc",
            limit=50
        )
        return {"success": True, "data": leads}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_quotation(customer, items):
    """Create a Quotation on-site"""
    try:
        employee = get_current_employee()
        items_list = json.loads(items) if isinstance(items, str) else items
        
        qt = frappe.get_doc({
            "doctype": "Quotation",
            "party_name": customer,
            "order_type": "Sales",
            "items": items_list
        })
        qt.insert()
        return {"success": True, "message": "Quotation created successfully", "name": qt.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_sales_orders():
    """Fetch recent sales orders"""
    try:
        employee = get_current_employee()
        orders = frappe.get_all(
            "Sales Order",
            fields=["name", "customer", "status", "grand_total", "transaction_date"],
            order_by="transaction_date desc",
            limit=20
        )
        return {"success": True, "data": orders}
    except Exception as e:
        return {"success": False, "error": str(e)}
