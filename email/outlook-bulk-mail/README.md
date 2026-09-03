# Outlook Bulk Personalized Email

Send a separate Microsoft 365 / Outlook email to each recipient using Microsoft Graph.

## Why use this

Unlike CC or BCC bulk sending, every recipient receives an individual message addressed only to them. This is useful for invitations, application notices, internal announcements, outreach, and other personalized bulk communication.

## Features

- one message per recipient
- no visible CC/BCC recipient list
- CSV recipient input
- first-name personalization
- HTML email support
- optional application/action URL
- dry-run mode
- duplicate recipient detection
- send/failure logging
- configurable delay between messages

## Requirements

- Python 3.10+
- a Microsoft Entra ID application registration
- Microsoft Graph `Mail.Send` permission
- an Outlook / Microsoft 365 account permitted to send mail

## Setup

1. Copy `.env.example` to `.env`.
2. Fill in your Microsoft Entra tenant, client, and sender details.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `recipients.example.csv` to `recipients.csv` and add recipients.
5. Edit `email_template.html` and the subject in `.env`.
6. Start with a dry run:

```bash
python send_bulk_email.py --dry-run
```

7. Send:

```bash
python send_bulk_email.py
```

## Recipient CSV

```csv
first_name,email
Jane,jane@example.com
John,john@example.com
```

Do not commit real recipient lists to this repository.

## Authentication

This utility uses Microsoft Graph. For a personal/internal script, use an Entra application configured for the appropriate Graph authentication flow and grant only the permissions required for sending mail.

Never commit client secrets, access tokens, passwords, or `.env` files.

## Responsible sending

Use this utility only for recipients you are authorized to contact. Respect organizational policies, Microsoft sending limits, applicable anti-spam requirements, and unsubscribe/opt-out obligations where applicable.
