# API Changelog

This document lists all changes to the REST API across versions. Changes are listed from newest to oldest.

![API Version History](https://via.placeholder.com/800x150.png?text=API+Version+History)

---

## Version 3.2.0 — June 2026

> **Release theme:** Performance improvements and expanded webhook support.

### What's new

#### Webhook retry mechanism

Webhooks now automatically retry on failure. If your endpoint returns a non-2xx status code, the system retries up to **five times** with exponential backoff.

Retry schedule:

| Attempt | Delay |
|---|---|
| 1st retry | 30 seconds |
| 2nd retry | 2 minutes |
| 3rd retry | 10 minutes |
| 4th retry | 1 hour |
| 5th retry | 6 hours |

After five failed attempts, the webhook event is marked as `failed` and no further retries occur.

#### New endpoint: Batch operations

You can now process up to **50 records in a single request** using the new batch endpoint.

**POST** `/v3/batch`

Request body:

```json
{
  "operations": [
    { "method": "POST", "path": "/users", "body": { "name": "Alice" } },
    { "method": "DELETE", "path": "/users/42" },
    { "method": "PATCH", "path": "/users/17", "body": { "status": "active" } }
  ]
}
```

Response:

```json
{
  "results": [
    { "status": 201, "body": { "id": "usr_991", "name": "Alice" } },
    { "status": 200, "body": { "deleted": true } },
    { "status": 200, "body": { "id": "17", "status": "active" } }
  ]
}
```

### Improvements

- Response time for `GET /users` reduced by **40%** through query optimization
- Pagination now supports `cursor` in addition to `offset` for more consistent results on large datasets
- Rate limit headers now included on all responses, not just rate-limited ones

### Bug fixes

- Fixed: `created_at` timestamp returned in local time instead of UTC
- Fixed: Filtering by `status=inactive` returned active users in some edge cases
- Fixed: `PATCH /orders/{id}` returned `404` when order existed but belonged to a different workspace

---

## Version 3.1.0 — April 2026

> **Release theme:** Authentication overhaul and new user management endpoints.

### What's new

#### OAuth 2.0 support

The API now supports OAuth 2.0 authorization code flow in addition to API key authentication.

Supported grant types:

- `authorization_code` — for server-side applications
- `client_credentials` — for machine-to-machine integrations
- `refresh_token` — for long-lived sessions

#### New endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v3/users/{id}/sessions` | List all active sessions for a user |
| `DELETE` | `/v3/users/{id}/sessions/{session_id}` | Revoke a specific session |
| `POST` | `/v3/auth/token/refresh` | Refresh an expired access token |
| `GET` | `/v3/audit-log` | Retrieve audit log entries |

### Breaking changes

> **Action required:** The following changes require updates to your integration before upgrading.

- The `user.role` field now returns an object instead of a string. Update your parsers accordingly.

  **Before:**
  ```json
  { "role": "admin" }
  ```

  **After:**
  ```json
  { "role": { "id": "rol_1", "name": "admin", "permissions": ["read", "write", "delete"] } }
  ```

- The `/v2/auth/login` endpoint is now deprecated and will be removed in version 4.0.0. Migrate to `/v3/auth/token`.

### Bug fixes

- Fixed: Pagination `next_cursor` was null on the second-to-last page
- Fixed: `DELETE /workspaces/{id}` did not cascade-delete associated resources
- Fixed: API key creation returned `500` when the key name contained special characters

---

## Version 3.0.0 — January 2026

> **Release theme:** Major version upgrade. Full backward compatibility break from v2.

### Summary of breaking changes

This version introduces breaking changes across the entire API surface. Key changes:

1. All endpoints moved from `/v2/` to `/v3/`
2. Authentication header changed from `X-API-Key` to `Authorization: Bearer`
3. All timestamps now return in ISO 8601 UTC format (`2026-01-15T10:30:00Z`)
4. Error response format standardized across all endpoints
5. Pagination changed from page-based to cursor-based

### New error format

All errors now follow a consistent structure:

```json
{
  "error": {
    "code": "invalid_token",
    "message": "The provided token has expired.",
    "docs": "https://docs.api.com/errors/invalid_token",
    "request_id": "req_8fk2j91"
  }
}
```

### Migration guide

Follow these steps to migrate from v2 to v3:

1. Update your base URL from `https://api.example.com/v2` to `https://api.example.com/v3`
2. Replace `X-API-Key: your_key` header with `Authorization: Bearer your_key`
3. Update timestamp parsing to handle ISO 8601 UTC format
4. Update error handling to use the new `error.code` field instead of HTTP status codes alone
5. Replace page-based pagination (`?page=2`) with cursor-based (`?after=cursor_value`)

---

## Version 2.8.0 — October 2025

### What's new

- Added `GET /v2/reports/summary` endpoint for generating usage reports
- Added `include_deleted` query parameter to list endpoints
- Added support for filtering by date ranges using `created_after` and `created_before`

### Bug fixes

- Fixed: Webhook signature verification failed for payloads larger than 10KB
- Fixed: `GET /v2/search` ignored the `limit` parameter and always returned 20 results

---

## Deprecation schedule

| Feature | Deprecated in | Removed in | Alternative |
|---|---|---|---|
| `/v2/auth/login` | v3.1.0 | v4.0.0 | `/v3/auth/token` |
| `X-API-Key` header | v3.0.0 | v4.0.0 | `Authorization: Bearer` |
| Page-based pagination | v3.0.0 | v4.0.0 | Cursor-based pagination |
| `user.role` as string | v3.1.0 | v4.0.0 | `user.role` as object |

---

## Support

- **Documentation:** [https://docs.api.com](https://docs.api.com)
- **Status page:** [https://status.api.com](https://status.api.com)
- **Developer forum:** [https://community.api.com](https://community.api.com)
- **Email support:** [api-support@company.com](mailto:api-support@company.com)
