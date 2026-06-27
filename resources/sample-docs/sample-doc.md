# Payment Gateway API

A REST API for processing payments, managing refunds, and tracking transaction history.

---

## Overview

The Payment Gateway API allows developers to integrate payment processing into their applications. It supports multiple payment methods, currencies, and provides real-time transaction status updates.

![Payment Flow Diagram](https://via.placeholder.com/800x300.png?text=Payment+Gateway+Flow)

---

## Key Features

- Accept payments via credit card, debit card, and UPI
- Process refunds within 24 hours
- Real-time webhook notifications
- Multi-currency support (INR, USD, EUR)
- PCI-DSS compliant encryption

---

## Authentication

All API requests require a Bearer token in the Authorization header.

```
Authorization: Bearer YOUR_API_KEY
```

To generate an API key:

1. Log in to your developer dashboard
2. Go to **Settings** → **API Keys**
3. Click **Generate New Key**
4. Copy and store the key securely — it will not be shown again

> **Note:** Never expose your API key in client-side code or public repositories.

---

## Base URL

```
https://api.paymentgateway.com/v2
```

---

## Endpoints

### Create a Payment

Creates a new payment transaction.

**POST** `/payments`

#### Request parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| amount | integer | Yes | Payment amount in smallest currency unit (paise for INR) |
| currency | string | Yes | Three-letter ISO currency code. Example: INR, USD |
| customer_id | string | Yes | Unique ID of the customer making the payment |
| payment_method | string | Yes | Payment method. Accepted values: card, upi, netbanking |
| description | string | No | Short description of the payment. Max 255 characters |
| metadata | object | No | Additional key-value pairs for your internal reference |

#### Request example

```json
POST /payments
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "amount": 49900,
  "currency": "INR",
  "customer_id": "cust_8821",
  "payment_method": "card",
  "description": "Annual subscription renewal",
  "metadata": {
    "order_id": "ORD-2026-441"
  }
}
```

#### Response example

```json
{
  "id": "pay_9f3k21",
  "status": "success",
  "amount": 49900,
  "currency": "INR",
  "customer_id": "cust_8821",
  "payment_method": "card",
  "created_at": "2026-06-24T10:30:00Z"
}
```

---

### Get Payment Status

Retrieves the current status of an existing payment.

**GET** `/payments/{payment_id}`

#### Path parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| payment_id | string | Yes | Unique ID of the payment returned during creation |

#### Response example

```json
{
  "id": "pay_9f3k21",
  "status": "success",
  "amount": 49900,
  "currency": "INR",
  "created_at": "2026-06-24T10:30:00Z",
  "updated_at": "2026-06-24T10:30:05Z"
}
```

---

### Create a Refund

Initiates a full or partial refund for a completed payment.

**POST** `/payments/{payment_id}/refunds`

#### Request parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| amount | integer | No | Amount to refund in smallest currency unit. Defaults to full payment amount if not specified |
| reason | string | No | Reason for the refund. Accepted values: duplicate, requested_by_customer, product_not_received |

---

## Payment status reference

| Status | Meaning |
|---|---|
| pending | Payment initiated but not yet confirmed |
| success | Payment completed successfully |
| failed | Payment could not be processed |
| refunded | Full amount has been refunded |
| partially_refunded | Part of the amount has been refunded |

---

## Error codes

| Code | HTTP status | Meaning | Fix |
|---|---|---|---|
| invalid_key | 401 | API key is missing or incorrect | Check your Authorization header |
| insufficient_funds | 402 | Customer's account has insufficient balance | Ask customer to use a different payment method |
| invalid_currency | 400 | Currency code is not supported | Use a valid ISO currency code |
| payment_not_found | 404 | No payment found with the given ID | Verify the payment_id is correct |
| rate_limit_exceeded | 429 | Too many requests sent in a short period | Wait and retry after 60 seconds |
| server_error | 500 | Unexpected server failure | Retry after 30 seconds; contact support if it persists |

---

## Webhooks

The API sends webhook notifications to your registered URL when a payment status changes.

### Webhook payload example

```json
{
  "event": "payment.success",
  "payment_id": "pay_9f3k21",
  "amount": 49900,
  "currency": "INR",
  "timestamp": "2026-06-24T10:30:05Z"
}
```

### Webhook events

- `payment.success` — Payment completed
- `payment.failed` — Payment failed
- `refund.initiated` — Refund has been started
- `refund.completed` — Refund has been processed

---

## Rate limits

| Plan | Requests per minute | Requests per day |
|---|---|---|
| Starter | 60 | 10,000 |
| Growth | 300 | 100,000 |
| Enterprise | Unlimited | Unlimited |

---

## SDKs and tools

- [Node.js SDK](https://github.com/paymentgateway/node-sdk)
- [Python SDK](https://github.com/paymentgateway/python-sdk)
- [Postman Collection](https://github.com/paymentgateway/postman)

---

## Support

For technical issues, contact the support team:

- **Email:** support@paymentgateway.com
- **Docs:** https://docs.paymentgateway.com
- **Status page:** https://status.paymentgateway.com
