import frappe
from frappe import _
from frappe.utils import now_datetime

@frappe.whitelist()
def get_rooms():
    """Fetch all chat rooms the current user is part of."""
    user = frappe.session.user
    
    # Get all rooms where user is a participant
    participant_rooms = frappe.get_all(
        "ESS Chat Room Participant",
        filters={"user": user, "parenttype": "ESS Chat Room"},
        fields=["parent"]
    )
    
    room_names = [p.parent for p in participant_rooms]
    if not room_names:
        return {"success": True, "data": []}
        
    rooms = frappe.get_all(
        "ESS Chat Room",
        filters={"name": ("in", room_names)},
        fields=["name", "room_name", "is_group"]
    )
    
    # Enhance room data with latest message and appropriate name
    result = []
    for room in rooms:
        # Get participants
        parts = frappe.get_all(
            "ESS Chat Room Participant",
            filters={"parent": room.name},
            fields=["user"]
        )
        participants = [p.user for p in parts]
        
        # Determine room name for 1-on-1 chats
        display_name = room.room_name
        if not room.is_group:
            other_users = [u for u in participants if u != user]
            if other_users:
                # Try to get full name
                try:
                    display_name = frappe.db.get_value("User", other_users[0], "full_name") or other_users[0]
                except:
                    display_name = other_users[0]
            else:
                display_name = "Just Me"
                
        # Get latest message
        latest_msg = frappe.get_all(
            "ESS Chat Message",
            filters={"room": room.name},
            fields=["content", "timestamp", "sender"],
            order_by="timestamp desc",
            limit=1
        )
        
        result.append({
            "room_id": room.name,
            "room_name": display_name,
            "is_group": room.is_group,
            "participants": participants,
            "latest_message": latest_msg[0] if latest_msg else None
        })
        
    # Sort by latest message timestamp
    result.sort(key=lambda x: x["latest_message"]["timestamp"] if x["latest_message"] else now_datetime(), reverse=True)
    
    return {"success": True, "data": result}

@frappe.whitelist()
def get_messages(room_id):
    """Fetch messages for a specific room."""
    user = frappe.session.user
    
    # Check permission
    is_participant = frappe.db.exists("ESS Chat Room Participant", {"parent": room_id, "user": user})
    if not is_participant:
        return {"success": False, "error": "Not a participant of this room"}
        
    messages = frappe.get_all(
        "ESS Chat Message",
        filters={"room": room_id},
        fields=["name", "sender", "content", "timestamp"],
        order_by="timestamp asc"
    )
    
    # Enhance with sender name
    for msg in messages:
        msg["sender_name"] = frappe.db.get_value("User", msg.sender, "full_name") or msg.sender
        
    return {"success": True, "data": messages}

@frappe.whitelist()
def send_message(room_id, content):
    """Send a message to a room."""
    user = frappe.session.user
    
    # Check permission
    is_participant = frappe.db.exists("ESS Chat Room Participant", {"parent": room_id, "user": user})
    if not is_participant:
        return {"success": False, "error": "Not a participant of this room"}
        
    doc = frappe.get_doc({
        "doctype": "ESS Chat Message",
        "room": room_id,
        "sender": user,
        "content": content,
        "timestamp": now_datetime()
    })
    doc.insert(ignore_permissions=True)
    
    return {"success": True, "data": {
        "name": doc.name,
        "sender": doc.sender,
        "content": doc.content,
        "timestamp": doc.timestamp
    }}

@frappe.whitelist()
def create_group(name, participants):
    """Create a new group chat."""
    import json
    
    user = frappe.session.user
    try:
        parts = json.loads(participants)
    except:
        return {"success": False, "error": "Invalid participants format"}
        
    if user not in parts:
        parts.append(user)
        
    doc = frappe.get_doc({
        "doctype": "ESS Chat Room",
        "room_name": name,
        "is_group": 1
    })
    
    for p in parts:
        doc.append("participants", {"user": p})
        
    doc.insert(ignore_permissions=True)
    
    return {"success": True, "room_id": doc.name}

@frappe.whitelist()
def start_private_chat(other_user):
    """Start or get an existing 1-on-1 chat."""
    user = frappe.session.user
    
    # Find if a 1-on-1 room already exists between these two
    my_rooms = [r.parent for r in frappe.get_all("ESS Chat Room Participant", filters={"user": user}, fields=["parent"])]
    other_rooms = [r.parent for r in frappe.get_all("ESS Chat Room Participant", filters={"user": other_user}, fields=["parent"])]
    
    common_rooms = list(set(my_rooms).intersection(other_rooms))
    
    for room in common_rooms:
        is_group = frappe.db.get_value("ESS Chat Room", room, "is_group")
        if not is_group:
            # We found the private chat
            return {"success": True, "room_id": room}
            
    # Create new private room
    doc = frappe.get_doc({
        "doctype": "ESS Chat Room",
        "room_name": "",
        "is_group": 0
    })
    doc.append("participants", {"user": user})
    doc.append("participants", {"user": other_user})
    doc.insert(ignore_permissions=True)
    
    return {"success": True, "room_id": doc.name}

@frappe.whitelist()
def get_all_users():
    """Fetch all active users to start chats with."""
    users = frappe.get_all(
        "User", 
        filters={"enabled": 1, "user_type": "System User"},
        fields=["name", "full_name"]
    )
    return {"success": True, "data": users}
