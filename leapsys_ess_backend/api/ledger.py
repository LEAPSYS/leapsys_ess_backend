import frappe
from leapsys_ess_backend.api.utils import get_current_employee

@frappe.whitelist()
def get_customer_ledger(customer):
    """Fetch general ledger for a specific customer"""
    try:
        employee = get_current_employee()
        
        # General Ledger is stored in GL Entry
        gl_entries = frappe.get_all(
            "GL Entry",
            filters={"party_type": "Customer", "party": customer, "is_cancelled": 0},
            fields=["posting_date", "voucher_type", "voucher_no", "debit", "credit", "remarks"],
            order_by="posting_date desc",
            limit=100
        )
        
        # Calculate balance
        balance = 0
        for entry in gl_entries:
            balance += (entry.debit - entry.credit)
            
        return {
            "success": True, 
            "data": gl_entries,
            "balance": balance
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_employee_ledger():
    """Fetch general ledger for the current employee (advances/claims)"""
    try:
        employee = get_current_employee()
        
        gl_entries = frappe.get_all(
            "GL Entry",
            filters={"party_type": "Employee", "party": employee, "is_cancelled": 0},
            fields=["posting_date", "voucher_type", "voucher_no", "debit", "credit", "remarks"],
            order_by="posting_date desc",
            limit=100
        )
        
        balance = 0
        for entry in gl_entries:
            balance += (entry.debit - entry.credit)
            
        return {
            "success": True, 
            "data": gl_entries,
            "balance": balance
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
