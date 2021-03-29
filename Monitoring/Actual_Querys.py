import requests
import json



alias_db = ["rexmas_prod", "manager_mas_prod"]
url = "https://351baqjau5.execute-api.us-east-1.amazonaws.com/DEVKERNEL"

payload = json.dumps({
  "api_id": "get_current_queries",
  "environment": "manager_prodkernel",
  "customer_domain": "prodkernel",
  "domain": "manager",
  "session_id": "023590ad51d6a2ea77bc20aebdfbfca2",
  "alias_db": alias_db[1]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)