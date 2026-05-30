"""Send an email via Gmail SMTP using an app password.

Reads GMAIL_USER and GMAIL_APP_PASSWORD from the environment. Caller is
expected to source the env file (e.g. remote_workstation/.env) before
invoking.

Prints the Message-ID on success; exits 2 if env is missing, 3 on SMTP
failure. Used by /weekly-brief step 8 as the primary delivery path; the
Gmail MCP create_draft is a fallback when env is unset.
"""
from __future__ import annotations

import argparse
import os
import smtplib
import ssl
import sys
import uuid
from email.message import EmailMessage
from pathlib import Path


def send(
    to_addr: str,
    subject: str,
    body: str,
    from_addr: str,
    app_password: str,
    html_body: str | None = None,
) -> str:
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Message-ID"] = f"<{uuid.uuid4()}@{from_addr.split('@', 1)[1]}>"
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.starttls(context=ctx)
        server.login(from_addr, app_password)
        server.send_message(msg)

    return msg["Message-ID"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True)
    parser.add_argument(
        "--body-file",
        required=True,
        type=Path,
        help="Path to a UTF-8 plain-text file containing the email body",
    )
    parser.add_argument(
        "--html-body-file",
        type=Path,
        default=None,
        help="Optional HTML alternative body",
    )
    parser.add_argument(
        "--from-addr",
        default=None,
        help="Override sender; defaults to $GMAIL_USER",
    )
    args = parser.parse_args()

    from_addr = args.from_addr or os.environ.get("GMAIL_USER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not from_addr or not app_password:
        print(
            "error: GMAIL_USER and GMAIL_APP_PASSWORD must be set in the "
            "environment (source remote_workstation/.env first)",
            file=sys.stderr,
        )
        return 2

    body = args.body_file.read_text(encoding="utf-8")
    html_body = args.html_body_file.read_text(encoding="utf-8") if args.html_body_file else None

    try:
        message_id = send(
            to_addr=args.to,
            subject=args.subject,
            body=body,
            from_addr=from_addr,
            app_password=app_password,
            html_body=html_body,
        )
    except smtplib.SMTPException as exc:
        print(f"error: SMTP send failed: {exc}", file=sys.stderr)
        return 3

    print(message_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
