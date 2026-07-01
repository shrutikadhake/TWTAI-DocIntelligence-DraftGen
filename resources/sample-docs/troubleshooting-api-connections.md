# Troubleshooting Guide: API Connection Issues

This guide will help you resolve the most common API connection problems. Work through each section in order until your issue is resolved.

---

## Before You Begin

Make sure you have the following information ready:

- Your API key
- The endpoint URL you are trying to reach
- The error message or status code you are seeing
- The name of the application or tool making the request

---

## Error 401: Unauthorized

This error means your API key was not accepted by the server.

### Common causes

- The API key has expired or been revoked
- The key is being passed in the wrong header
- Extra spaces or characters have been accidentally included in the key by you

### How to fix it

**Check your header format.** The Authorization header must be formatted exactly like this:

```
Authorization: Bearer YOUR_API_KEY
```

Not like this:

```
Authorization: YOUR_API_KEY
Authorization: ApiKey YOUR_API_KEY
```

**Verify your key is active.** Log in to your dashboard and go to **Settings** → **API Keys**. Confirm your key shows a status of **Active**.

**Generate a new key if needed.** If the key has been revoked or you are unsure of its status, generate a new one and update your application.

---

## Error 403: Forbidden

A 403 error means your key is valid but access to the requested resource has been denied by the system.

### Common causes

- Your account plan does not include access to the endpoint you are trying to reach
- The resource belongs to a different workspace than the one your key is scoped to
- IP allowlisting has been enabled and your IP address has not been added

### How to fix it

1. Check your plan permissions in **Settings** → **Plan and Billing**
2. Confirm the workspace your key is associated with
3. If IP allowlisting is enabled, your IP address will need to be added by your admin

> **Note:** If you believe access should be granted but is being blocked by the system, contact your account administrator before raising a support ticket.

---

## Error 429: Too Many Requests

This error means your application has exceeded the rate limit for your plan.

### Rate limits by plan

| Plan | Requests per minute | Requests per day |
|---|---|---|
| Starter | 60 | 10,000 |
| Growth | 300 | 100,000 |
| Enterprise | Custom | Custom |

### How to fix it

**Add retry logic to your application.** When a 429 is received, your application should wait before retrying. The recommended approach is exponential backoff:

```
1st retry: wait 1 second
2nd retry: wait 2 seconds
3rd retry: wait 4 seconds
4th retry: wait 8 seconds
```

**Check the Retry-After header.** The server will include a `Retry-After` header in 429 responses. This header will tell you exactly how many seconds to wait before retrying.

**Consider upgrading your plan** if you regularly hit rate limits. Contact the sales team at sales@company.com.

---

## Error 500: Internal Server Error

A 500 error means something went wrong on the server side. This is not caused by your request.

### What to do

1. Wait 30 seconds and retry your request
2. Check the status page at `status.api.company.com` for any ongoing incidents
3. If the error persists for more than 10 minutes, a support ticket should be submitted by you at `support.api.company.com`

When submitting a ticket, include:

- The full request you made (URL, headers, body)
- The exact error response received by you
- The timestamp of when the error first occurred
- Your API key ID (not the key itself)

---

## Connection Timeouts

If your requests are timing out without receiving a response, the following should be checked by you:

### Check your network

Run a basic connectivity test from your server:

```bash
curl -I https://api.company.com/v1/ping
```

If this command also times out, the issue is likely network-related and not specific to your API requests.

### Check your timeout settings

Most HTTP clients will have a default timeout of 30 seconds. For endpoints that process large amounts of data, this may not be enough. Consider increasing your timeout to 60 or 90 seconds.

### Contact support

If connectivity tests pass but API requests still time out, the support team should be contacted by you with the details of the affected endpoint and your server's IP address.

---

## Still Not Working?

If you have worked through this guide and the issue has not been resolved, contact the support team:

- **Email:** support@company.com
- **Live chat:** Available Monday to Friday, 9am to 6pm IST
- **Status page:** status.api.company.com

When you contact support, please include your API key ID, the error you are seeing, and the steps you have already tried. This will help the support team resolve your issue faster.
