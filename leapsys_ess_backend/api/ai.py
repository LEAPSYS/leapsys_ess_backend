import frappe

@frappe.whitelist()
def chatbot_query(user_query, employee):
    """
    Process natural language queries using a generic AI wrapper.
    Returns parsed intent or direct answers for the mobile app UI.
    """
    try:
        # Here we would integrate with an LLM provider or Dialogflow
        # For boilerplate, returning a mock response
        query = user_query.lower()
        if "leave" in query:
            return {"success": True, "answer": "You have 12 Casual Leaves and 5 Sick Leaves remaining."}
        elif "visit" in query:
            return {"success": True, "answer": "Your next visit is at 2:00 PM for Customer X."}
        
        return {"success": True, "answer": "I can help you with leaves, visits, and expenses. Ask me!"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def process_expense_receipt(file_url):
    """
    Process a receipt image using an OCR service and extract data.
    """
    try:
        # Example pseudo logic to send `file_url` to AWS Textract or Google Cloud Vision
        extracted_data = {
            "amount": 1500.00,
            "date": "2026-05-25",
            "expense_type": "Travel",
            "merchant": "Uber"
        }
        return {"success": True, "data": extracted_data}
    except Exception as e:
        return {"success": False, "error": str(e)}
