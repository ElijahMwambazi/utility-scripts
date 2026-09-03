#!/usr/bin/env python3

import argparse
import csv
import html
import os
import sys
import time
from pathlib import Path

import msal
import requests
from dotenv import load_dotenv

GRAPH_SCOPE = ["Mail.Send"]
GRAPH_SEND_URL = "https://graph.microsoft.com/v1.0/me/sendMail"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send separate personalized Outlook/Microsoft 365 emails via Microsoft Graph."
    )
    parser.add_argument(
        "--recipients",
        default="recipients.csv",
        help="CSV file containing first_name,email columns (default: recipients.csv)",
    )
    parser.add_argument(
        "--template",
        default="email_template.html",
        help="HTML template file (default: email_template.html)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and preview without sending email",
    )
    return parser.parse_args()


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_recipients(path: Path):
    recipients = []
    seen = set()

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"first_name", "email"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Recipient CSV must contain first_name and email columns")

        for row_number, row in enumerate(reader, start=2):
            first_name = (row.get("first_name") or "").strip()
            email_address = (row.get("email") or "").strip().lower()

            if not email_address or "@" not in email_address:
                raise ValueError(f"Invalid email address on CSV row {row_number}")

            if email_address in seen:
                print(f"Skipping duplicate recipient: {email_address}")
                continue

            seen.add(email_address)
            recipients.append({"first_name": first_name, "email": email_address})

    return recipients


def render_template(template: str, first_name: str, apply_url: str) -> str:
    return (
        template.replace("{{first_name}}", html.escape(first_name))
        .replace("{{apply_url}}", html.escape(apply_url, quote=True))
    )


def acquire_token(client_id: str, tenant_id: str) -> str:
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.PublicClientApplication(client_id=client_id, authority=authority)

    accounts = app.get_accounts()
    result = None

    if accounts:
        result = app.acquire_token_silent(GRAPH_SCOPE, account=accounts[0])

    if not result:
        flow = app.initiate_device_flow(scopes=GRAPH_SCOPE)
        if "user_code" not in flow:
            raise RuntimeError(f"Unable to start Microsoft sign-in: {flow}")

        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)

    token = result.get("access_token") if result else None
    if not token:
        description = result.get("error_description", "Unknown authentication error") if result else "Unknown authentication error"
        raise RuntimeError(description)

    return token


def send_message(token: str, subject: str, recipient: dict, body: str):
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body},
            "toRecipients": [
                {"emailAddress": {"address": recipient["email"]}}
            ],
        },
        "saveToSentItems": True,
    }

    response = requests.post(
        GRAPH_SEND_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    if response.status_code != 202:
        raise RuntimeError(
            f"Graph API returned {response.status_code}: {response.text[:500]}"
        )


def main():
    load_dotenv()
    args = parse_args()

    base_dir = Path(__file__).resolve().parent
    recipients_path = (base_dir / args.recipients).resolve()
    template_path = (base_dir / args.template).resolve()

    client_id = require_env("AZURE_CLIENT_ID")
    tenant_id = os.getenv("AZURE_TENANT_ID", "common").strip() or "common"
    subject = require_env("MAIL_SUBJECT")
    apply_url = require_env("APPLY_URL")
    delay_seconds = float(os.getenv("SEND_DELAY_SECONDS", "1"))

    recipients = load_recipients(recipients_path)
    template = template_path.read_text(encoding="utf-8")

    if not recipients:
        print("No recipients found.")
        return 0

    print(f"Loaded {len(recipients)} unique recipient(s).")

    if args.dry_run:
        for recipient in recipients:
            rendered = render_template(template, recipient["first_name"], apply_url)
            print(
                f"DRY RUN -> {recipient['email']} | subject={subject!r} | body_length={len(rendered)}"
            )
        return 0

    token = acquire_token(client_id, tenant_id)

    sent = 0
    failed = 0

    for recipient in recipients:
        try:
            body = render_template(template, recipient["first_name"], apply_url)
            send_message(token, subject, recipient, body)
            sent += 1
            print(f"SENT   {recipient['email']}")
        except Exception as exc:
            failed += 1
            print(f"FAILED {recipient['email']}: {exc}", file=sys.stderr)

        if delay_seconds > 0:
            time.sleep(delay_seconds)

    print(f"Finished. Sent: {sent}. Failed: {failed}.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
