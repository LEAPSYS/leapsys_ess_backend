import frappe
from leapsys_ess_backend.api.utils import get_current_employee

@frappe.whitelist()
def get_activity_feed():
    """Fetch company announcements / activity feed"""
    try:
        employee = get_current_employee()
        
        # In ERPNext, company-wide announcements often use 'Communication' with subject 'Announcement'
        # or a custom 'Activity Post' doctype. We will check Communication for now, or ToDo if nothing else fits.
        # A proper implementation might use a custom Doctype 'Activity Post'
        
        # We will query 'Communication' where communication_type = 'Communication' and sent_or_received = 'Sent'
        # Or just standard Energy Point Log
        
        communications = frappe.get_all(
            "Communication",
            filters={"communication_type": "Communication"},
            fields=["name", "subject", "content", "sender_full_name", "creation"],
            order_by="creation desc",
            limit=20
        )
        
        return {"success": True, "data": communications}
    except Exception as e:
        return {"success": False, "error": str(e)}
