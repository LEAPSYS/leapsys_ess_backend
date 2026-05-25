import frappe

@frappe.whitelist()
def get_app_settings():
    """
    Fetches the App Settings for the mobile application.
    Includes White-Labeling configs (colors, logos) and feature toggles.
    """
    try:
        settings = frappe.get_single("Leapsys ESS App Settings")
        
        return {
            "success": True,
            "data": {
                "primary_color": settings.primary_color or "#007BFF",
                "secondary_color": settings.secondary_color or "#6C757D",
                "app_logo_url": settings.app_logo if settings.app_logo else None,
                "company_name": settings.company_name or frappe.defaults.get_user_default("company"),
                "features": {
                    "enable_geofencing": bool(settings.enable_geofencing),
                    "enable_offline_mode": bool(settings.enable_offline_mode),
                    "enable_service_module": bool(settings.enable_service_module),
                    "enable_sales_module": bool(settings.enable_sales_module),
                    "enable_chatbot": bool(settings.enable_chatbot)
                }
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
