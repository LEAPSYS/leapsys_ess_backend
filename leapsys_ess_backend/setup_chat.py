import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_chat():
    frappe.flags.in_install = True
    create_doctypes()
    frappe.db.commit()
    print("Chat DocTypes generated successfully.")

def create_doctypes():
    if not frappe.db.exists("DocType", "ESS Chat Room"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "ESS Chat Room",
            "module": "Leapsys Ess Backend",
            "custom": 1,
            "naming_rule": "Random",
            "autoname": "hash",
            "fields": [
                {"fieldname": "room_name", "fieldtype": "Data", "label": "Room Name", "description": "Blank for 1-on-1 chats"},
                {"fieldname": "is_group", "fieldtype": "Check", "label": "Is Group", "default": 0},
                {"fieldname": "participants_section", "fieldtype": "Section Break"},
                {"fieldname": "participants", "fieldtype": "Table", "label": "Participants", "options": "ESS Chat Room Participant"}
            ],
            "permissions": [
                {"role": "All", "read": 1, "write": 1, "create": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created ESS Chat Room")

    if not frappe.db.exists("DocType", "ESS Chat Room Participant"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "ESS Chat Room Participant",
            "module": "Leapsys Ess Backend",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "user", "fieldtype": "Link", "label": "User", "options": "User", "in_list_view": 1, "reqd": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created ESS Chat Room Participant")

    if not frappe.db.exists("DocType", "ESS Chat Message"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "ESS Chat Message",
            "module": "Leapsys Ess Backend",
            "custom": 1,
            "naming_rule": "Random",
            "autoname": "hash",
            "fields": [
                {"fieldname": "room", "fieldtype": "Link", "label": "Room", "options": "ESS Chat Room", "reqd": 1},
                {"fieldname": "sender", "fieldtype": "Link", "label": "Sender", "options": "User", "reqd": 1},
                {"fieldname": "content", "fieldtype": "Text", "label": "Message Content", "reqd": 1},
                {"fieldname": "timestamp", "fieldtype": "Datetime", "label": "Timestamp", "reqd": 1, "default": "Today"}
            ],
            "permissions": [
                {"role": "All", "read": 1, "write": 1, "create": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created ESS Chat Message")

if __name__ == "__main__":
    setup_chat()
