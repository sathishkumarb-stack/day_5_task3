import hmac
import hashlib

from fastapi.testclient import TestClient
from src.main import app
from src.security import WEBHOOK_SECRET

client = TestClient(app)


def create_signature(payload: bytes):
    return hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()


def test_valid_signature():
    payload = b'{"event": "customer.created", "customer_id": 1}'
    signature = create_signature(payload)

    response = client.post(
        "/webhooks/customer-events",
        content=payload,
        headers={"X-Signature": signature}
    )

    assert response.status_code == 200
    assert response.json() == {"status": "accepted"}


def test_tampered_payload():
    original_payload = b'{"event": "customer.created"}'
    signature = create_signature(original_payload)

    tampered_payload = b'{"event": "customer.deleted"}'

    response = client.post(
        "/webhooks/customer-events",
        content=tampered_payload,
        headers={"X-Signature": signature}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid signature"}


def test_missing_signature():
    response = client.post(
        "/webhooks/customer-events",
        content=b'{"event": "customer.created"}'
    )

    assert response.status_code == 401