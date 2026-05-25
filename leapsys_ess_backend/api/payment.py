import frappe

@frappe.whitelist(allow_guest=True)
def razorpay_webhook():
    """
    Webhook to receive Razorpay/UPI payment status.
    Auto-generates a Sales Invoice upon successful payment.
    """
    try:
        payload = frappe.request.get_data(as_text=True)
        # Parse webhook payload and verify signature here
        # Example pseudo-logic:
        # if payment_successful:
        #   create_sales_invoice(order_id)
        
        return {"status": "ok"}
    except Exception as e:
        frappe.log_error(message=str(e), title="Payment Webhook Error")
        return {"status": "error"}

def create_sales_invoice(sales_order_id):
    """Helper to auto-generate an invoice"""
    so = frappe.get_doc("Sales Order", sales_order_id)
    si = frappe.model.mapper.get_mapped_doc("Sales Order", sales_order_id, {
        "Sales Order": {
            "doctype": "Sales Invoice"
        }
    })
    si.insert()
    si.submit()
    # Trigger email to customer
    return si.name
