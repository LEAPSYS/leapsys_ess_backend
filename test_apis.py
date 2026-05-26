import urllib.request
import urllib.parse
import json

BASE_URL = "https://erp.leapsys.in/api/method"
HEADERS = {
    "Authorization": "token 7e4685703cdfbdf:bd8797cbe416fb7",
    "Content-Type": "application/json"
}

endpoints = [
    {"name": "Settings (get_app_settings)", "url": "/leapsys_ess_backend.api.settings.get_app_settings", "method": "GET"},
    {"name": "AI (chatbot_query)", "url": "/leapsys_ess_backend.api.ai.chatbot_query", "method": "POST", "data": {"user_query": "leave", "employee": "EMP-001"}},
    {"name": "AI (process_expense_receipt)", "url": "/leapsys_ess_backend.api.ai.process_expense_receipt", "method": "POST", "data": {"file_url": "/private/files/test.png"}},
    {"name": "Attendance (mark_attendance)", "url": "/leapsys_ess_backend.api.attendance.mark_attendance", "method": "POST", "data": {"employee": "EMP-001", "log_type": "IN", "lat": 28.7042, "lon": 77.1026}},
    {"name": "HR (get_leave_balances)", "url": "/leapsys_ess_backend.api.hr.get_leave_balances", "method": "GET", "params": {"employee": "EMP-001"}},
    {"name": "HR (get_salary_slips)", "url": "/leapsys_ess_backend.api.hr.get_salary_slips", "method": "GET", "params": {"employee": "EMP-001"}},
    {"name": "Service (get_maintenance_visits)", "url": "/leapsys_ess_backend.api.service.get_maintenance_visits", "method": "GET", "params": {"employee": "EMP-001", "date": "2026-05-26"}},
    {"name": "Service (get_bag_inventory)", "url": "/leapsys_ess_backend.api.service.get_bag_inventory", "method": "GET", "params": {"employee": "EMP-001"}},
    {"name": "Payment (razorpay_webhook)", "url": "/leapsys_ess_backend.api.payment.razorpay_webhook", "method": "POST", "data": {"status": "ok"}}
]

print("Starting API Tests...\n")
for ep in endpoints:
    print(f"Testing {ep['name']}...")
    url = BASE_URL + ep['url']
    try:
        if ep['method'] == 'GET':
            if 'params' in ep:
                url += '?' + urllib.parse.urlencode(ep['params'])
            req = urllib.request.Request(url, headers=HEADERS, method='GET')
        else:
            data = json.dumps(ep.get('data', {})).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=HEADERS, method='POST')
        
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            text = response.read().decode('utf-8')
            print(f"Status Code: {status}")
            print(f"Response: {text[:200]}")
    except urllib.error.HTTPError as e:
        text = e.read().decode('utf-8')
        print(f"HTTPError: {e.code}")
        print(f"Response: {text[:200]}")
    except Exception as e:
        print(f"Error: {str(e)}")
    print("-" * 40)
