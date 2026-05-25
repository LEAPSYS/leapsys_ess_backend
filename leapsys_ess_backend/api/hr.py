import frappe
from frappe import _

@frappe.whitelist()
def get_leave_balances(employee):
    """Fetch leave balances for an employee"""
    try:
        balances = frappe.get_all(
            "Leave Allocation",
            filters={"employee": employee, "docstatus": 1},
            fields=["leave_type", "total_leaves_allocated", "new_leaves_allocated"]
        )
        return {"success": True, "data": balances}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def submit_expense_claim(employee, expense_type, amount, date, description):
    """Submit a new expense claim"""
    try:
        expense = frappe.get_doc({
            "doctype": "Expense Claim",
            "employee": employee,
            "posting_date": date,
            "expenses": [{
                "expense_type": expense_type,
                "amount": amount,
                "description": description
            }]
        })
        expense.insert()
        return {"success": True, "message": "Expense Claim submitted successfully.", "name": expense.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_salary_slips(employee):
    """Fetch salary slips for the employee"""
    try:
        slips = frappe.get_all(
            "Salary Slip",
            filters={"employee": employee, "docstatus": 1},
            fields=["name", "start_date", "end_date", "gross_pay", "net_pay"],
            order_by="start_date desc"
        )
        return {"success": True, "data": slips}
    except Exception as e:
        return {"success": False, "error": str(e)}
