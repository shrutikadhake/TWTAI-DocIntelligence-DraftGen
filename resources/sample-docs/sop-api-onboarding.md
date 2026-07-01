# Standard Operating Procedure: Onboarding A New API User

## Purpose

This SOP will describe the steps that should be followed by the IT team when a new developer needs to be onboarded to the API platform. The process will ensure that access is granted correctly and that the new user will be able to make their first API call within one business day.

## Scope

This procedure applies to all internal developers and external partners who require API access.

## Prerequisites

Before you begin, make sure the following are ready:

- A verified company email address for the new user
- Manager approval on file
- The onboarding form submitted through the HR portal

## Procedure

### Step 1: Create the user account

Log in to the admin portal at `admin.api.company.com` using your admin credentials.

Navigate to **Users** → **Add New User** and fill in the required fields:

| Field | What to enter |
|---|---|
| Full name | The developer's legal name |
| Email | Their company email address |
| Role | Select API Developer from the dropdown |
| Access level | Standard (can be upgraded later by the manager) |

Click **Save** to create the account.

### Step 2: Generate The API Key

An API key will be generated automatically by the system after the account has been saved. The key will be displayed on screen and it will also be sent to the user's email address by the system.

> **Note:** The API key will only be shown once on screen. Make sure it is copied by you before navigating away from the page.

Copy the key and store it in the team's secure password manager under the developer's name.

### Step 3: Send The Welcome Email

A welcome email template will be used by you to notify the new developer. The template will be found in the shared drive under `Templates/API-Onboarding`.

Open the template and fill in these details:

1. The developer's first name should be added at the top of the email
2. The API key that was generated in Step 2 should be pasted into the designated field
3. The link to the developer documentation will need to be included by you
4. Your name and contact details should be added at the bottom

Send the email to the developer and CC their manager.

### Step 4: Verify Access

After 30 minutes, access will need to be confirmed by you. Call or message the developer and ask them to run this test request:

```
curl -H "Authorization: ApiKey THEIR_KEY" https://api.company.com/v1/ping
```

A successful response will be returned by the system if the setup is correct:

```json
{ "status": "ok", "message": "Connection successful" }
```

If an error is received by the developer, refer to the troubleshooting section below.

## Troubleshooting

| Problem | Likely cause | What should be done |
|---|---|---|
| 401 Unauthorized | Key not activated yet | Wait 10 minutes and try again |
| 404 Not Found | Wrong base URL used by developer | Check the URL in the welcome email |
| 500 Server Error | System issue | The IT helpdesk should be contacted by you |

## Completion

Once access has been confirmed by both parties, the onboarding checklist should be marked as complete by you in the HR portal. The record will be stored automatically by the system.

---

*This SOP was last reviewed in June 2026. Updates will be made by the IT team on a quarterly basis.*
