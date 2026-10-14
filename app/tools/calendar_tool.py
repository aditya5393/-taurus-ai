"""Calendar Tool - v2: creates real calendar events (or .ics file in demo mode)."""
import os
import datetime


def create_calendar_event(title: str, date_str: str, description: str = "", duration_min: int = 30) -> str:
    """Create calendar event. Demo mode saves .ics file that can be imported to Google Calendar."""
    os.makedirs("outputs", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() else "_" for c in title)[:40]
    path = f"outputs/calendar_event_{safe}_{ts}.ics"
    # Simple ICS format - Google Calendar can import this
    try:
        dt = datetime.datetime.fromisoformat(date_str.replace("Z", ""))
    except Exception:
        dt = datetime.datetime.now() + datetime.timedelta(days=1)
        dt = dt.replace(hour=10, minute=0, second=0, microsecond=0)
    end = dt + datetime.timedelta(minutes=duration_min)
    fmt = "%Y%m%dT%H%M%S"
    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Taurus AI//EN
BEGIN:VEVENT
UID:taurus-{ts}@taurus.ai
DTSTAMP:{datetime.datetime.now().strftime(fmt)}
DTSTART:{dt.strftime(fmt)}
DTEND:{end.strftime(fmt)}
SUMMARY:{title}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(ics)
    return f"✅ Calendar event saved: {path}\nTitle: {title}\nWhen: {dt} ({duration_min} min)\nImport this .ics into Google Calendar to see it."


def parse_event_from_prompt(prompt: str, llm_fn) -> dict:
    raw = llm_fn(
        "You are a calendar agent. Return format:\nTITLE: title\nDATE: YYYY-MM-DDTHH:MM:SS (guess reasonable date if not given, e.g. tomorrow 10:00)\nDESCRIPTION: short description",
        f"Create calendar event from: {prompt}",
    )
    title, date_str, desc = "Follow up", "", prompt
    for line in raw.splitlines():
        if line.strip().upper().startswith("TITLE:"):
            title = line.split(":", 1)[1].strip()
        if line.strip().upper().startswith("DATE:"):
            date_str = line.split(":", 1)[1].strip()
        if line.strip().upper().startswith("DESCRIPTION:"):
            desc = line.split(":", 1)[1].strip()
    return {"title": title, "date_str": date_str, "description": desc}
