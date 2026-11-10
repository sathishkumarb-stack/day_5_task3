import hmac
import hashlib
import logging

from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks

from src.security import WEBHOOK_SECRET

app = FastAPI(title="Webhook Receiver API")

logging.basicConfig(level=logging.INFO)


def process_event(payload: bytes):
    """Process webhook event in the background."""
    logging.info("Webhook event received: %s", payload.decode("utf-8"))


@app.post("/webhooks/customer-events")
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_signature: str = Header(default=None)
):
    if not x_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing signature"
        )

    if not WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Webhook secret is not configured"
        )

    raw_body = await request.body()

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_signature):
        raise HTTPException(
            status_code=401,
            detail="Invalid signature"
        )

    background_tasks.add_task(process_event, raw_body)

    return {"status": "accepted"}