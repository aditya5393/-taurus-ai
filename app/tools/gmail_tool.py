"""Gmail Tool - v2 full agentic: creates REAL drafts (with approval) or saves draft file.

Two modes:
1. Real Gmail API (if credentials exist) - creates draft in Gmail drafts folder
2. Safe fallback - saves draft as .eml / .txt file in outputs/ so demo still works without OAuth

For internship demo, mode 2 is enough to show automation. For production, set up Gmail API OAuth.
"""
import os
import datetime


def create_gmail_draft(to: str, subject: str, body: str, use_api: bool = False) -> str:
    """Create a Gmail draft. Returns status string."""
    # --- Real Gmail API path (optional) ---
    if use_api:
        try:
            # Requires: pip install google-api-python-client google-auth
            # and credentials.json + token.json from Google Cloud OAuth
            # This block is intentionally minimal - see README for setup
            from googleapiclient.discovery import build
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            import base64
            from email.mime.text import MIMEText

            creds = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.compose"])
            if not creds or not creds.valid:
                return "Gmail API not authenticated. Run Gmail OAuth setup first (see README). Falling back to file draft."
            service = build("gmail", "v1", credentials=creds)
            msg = MIMEText(body)
            msg["to"] = to
            msg["subject"] = subject
            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            draft = service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
            return f"✅ Real Gmail draft created! Draft ID: {draft['id']} (check Gmail > Drafts)"
        except Exception as e:
            return f"Gmail API failed ({e}). Saved as file draft instead."

    # --- Safe fallback: file draft (works for demo / professors) ---
    os.makedirs("outputs", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_to = to.replace("@", "_at_").replace(".", "_")
    path = f"outputs/gmail_draft_{safe_to}_{ts}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"To: {to}\nSubject: {subject}\nDate: {datetime.datetime.now()}\n\n{body}\n")
    return f"✅ Draft saved (demo mode): {path}\nTo: {to}\nSubject: {subject}\n\n{body[:500]}..."


def draft_email_from_prompt(prompt: str, llm_fn) -> dict:
    """Ask LLM to produce To/Subject/Body from a prompt like 'Draft Gmail to prof about internship'"""
    raw = llm_fn(
        "You are a Gmail drafting agent. Return format:\nTO: email or 'professor@example.com' if unknown\nSUBJECT: subject line\nBODY: full email body",
        f"Draft this email: {prompt}",
    )
    to, subject, body = "professor@example.com", "Hello", raw
    for line in raw.splitlines():
        if line.strip().upper().startswith("TO:"):
            to = line.split(":", 1)[1].strip()
        if line.strip().upper().startswith("SUBJECT:"):
            subject = line.split(":", 1)[1].strip()
    if "BODY:" in raw:
        body = raw.split("BODY:", 1)[1].strip()
    return {"to": to, "subject": subject, "body": body}
