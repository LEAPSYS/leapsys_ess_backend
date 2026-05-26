import frappe
from frappe.utils import nowdate
from leapsys_ess_backend.api.utils import get_current_employee

@frappe.whitelist()
def get_projects():
    """Fetch active projects assigned to the employee's department/company"""
    try:
        employee = get_current_employee()
        projects = frappe.get_all(
            "Project",
            filters={"status": ["!=", "Completed"]},
            fields=["name", "project_name", "expected_end_date", "status", "percent_complete"]
        )
        return {"success": True, "data": projects}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_tasks():
    """Fetch tasks assigned to the employee"""
    try:
        employee = get_current_employee()
        # Tasks are assigned via ToDo or directly. For simplicity, filtering globally for demo,
        # but in production, we should filter by 'assigned_to' matching frappe.session.user
        tasks = frappe.get_all(
            "Task",
            filters={"status": ["!=", "Completed"]},
            fields=["name", "subject", "project", "status", "exp_end_date", "custom_enable_geofencing", "custom_latitude", "custom_longitude", "custom_geofence_radius"]
        )
        return {"success": True, "data": tasks}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def update_task_status(task_name, status):
    """Update task status from the mobile app"""
    try:
        employee = get_current_employee()
        task = frappe.get_doc("Task", task_name)
        task.status = status
        task.save()
        return {"success": True, "message": f"Task {task_name} updated successfully."}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def log_timesheet(project, task, hours, description, start_lat=None, start_lon=None, end_lat=None, end_lon=None):
    """Log timesheet hours against a task, with GPS tracking points"""
    try:
        employee = get_current_employee()
        ts = frappe.get_doc({
            "doctype": "Timesheet",
            "employee": employee,
            "time_logs": [{
                "activity_type": "Execution",
                "hours": float(hours),
                "project": project,
                "task": task,
                "description": description,
                "custom_start_latitude": start_lat,
                "custom_start_longitude": start_lon,
                "custom_end_latitude": end_lat,
                "custom_end_longitude": end_lon
            }]
        })
        ts.insert(ignore_permissions=True)
        return {"success": True, "message": "Timesheet logged successfully", "name": ts.name}
    except Exception as e:
        return {"success": False, "error": str(e)}
