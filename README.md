# Webhook Receiver API

## Overview
A FastAPI webhook receiver that validates incoming customer events
using HMAC-SHA256 signatures.

## Technologies
- Python
- FastAPI
- HMAC-SHA256
- BackgroundTasks
- Pytest

## Setup

Install dependencies:

    py -m pip install -e ".[dev]"

## Environment Variables

Create a `.env` file:

    WEBHOOK_SECRET=my_webhook_secret_123

## Run Application

    py -m uvicorn src.main:app --reload

Open Swagger:

http://127.0.0.1:8000/docs

## Endpoint

POST /webhooks/customer-events

Header:
X-Signature

## Expected Responses

- Valid signature: 200 Accepted
- Invalid signature: 401 Invalid signature
- Missing signature: 401 Missing signature

## Run Tests

    py -m pytest -v