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

@frappe.whitelist()
def get_quotations():
    """Fetch recent quotations"""
    try:
        employee = get_current_employee()
        quotations = frappe.get_all(
            "Quotation",
            fields=["name", "customer_name", "status", "grand_total", "transaction_date"],
            order_by="transaction_date desc",
            limit=50
        )
        return {"success": True, "data": quotations}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_quotation_detail(name):
    """Fetch quotation detail with items"""
    try:
        employee = get_current_employee()
        quotation = frappe.get_doc("Quotation", name)
        
        # Prepare items data
        items = []
        for item in quotation.items:
            items.append({
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.amount
            })
            
        return {
            "success": True, 
            "data": {
                "name": quotation.name,
                "customer_name": quotation.customer_name,
                "transaction_date": quotation.transaction_date,
                "status": quotation.status,
                "grand_total": quotation.grand_total,
                "items": items
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_sales_order_detail(name):
    """Fetch sales order detail with items"""
    try:
        employee = get_current_employee()
        so = frappe.get_doc("Sales Order", name)
        
        items = []
        for item in so.items:
            items.append({
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.amount,
                "delivered_qty": item.delivered_qty
            })
            
        return {
            "success": True,
            "data": {
                "name": so.name,
                "customer_name": so.customer_name,
                "transaction_date": so.transaction_date,
                "delivery_date": so.delivery_date,
                "status": so.status,
                "grand_total": so.grand_total,
                "per_delivered": so.per_delivered,
                "items": items
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_sales_order(customer, items, delivery_date):
    """Create a Sales Order on-site"""
    try:
        employee = get_current_employee()
        items_list = json.loads(items) if isinstance(items, str) else items
        
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": customer,
            "delivery_date": delivery_date,
            "items": items_list
        })
        so.insert()
        return {"success": True, "message": "Sales Order created successfully", "name": so.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_items():
    """Fetch items for selection"""
    try:
        items = frappe.get_all(
            "Item",
            filters={"disabled": 0, "is_sales_item": 1},
            fields=["name", "item_name", "item_group", "stock_uom", "standard_rate"],
            limit=100
        )
        return {"success": True, "data": items}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_item_stock(item_code):
    """Fetch stock balance for an item"""
    try:
        # Sum of actual_qty in all warehouses
        stock = frappe.db.sql('''
            SELECT sum(actual_qty) as total_qty 
            FROM `tabBin` 
            WHERE item_code = %s
        ''', (item_code,), as_dict=True)
        
        total_qty = stock[0].total_qty if stock and stock[0].total_qty else 0
        return {"success": True, "item_code": item_code, "actual_qty": total_qty}
    except Exception as e:
        return {"success": False, "error": str(e)}
