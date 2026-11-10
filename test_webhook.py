import requests
import hmac
import hashlib

SECRET = "my_webhook_secret_123"

payload = b'{"event": "customer.created", "customer_id": 1}'

signature = hmac.new(
    SECRET.encode(),
    payload,
    hashlib.sha256
).hexdigest()

response = requests.post(
    "http://127.0.0.1:8000/webhooks/customer-events",
    data=payload,
    headers={"X-Signature": signature}
)

print("Status Code:", response.status_code)
print("Response:", response.json())

# Tampered payload test
tampered_payload = b'{"event": "customer.deleted", "customer_id": 1}'

response = requests.post(
    "http://127.0.0.1:8000/webhooks/customer-events",
    data=tampered_payload,
    headers={"X-Signature": signature}
)

print("\nTampered Payload Test")
print("Status Code:", response.status_code)
print("Response:", response.json())