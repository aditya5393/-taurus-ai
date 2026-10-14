"""File Tools - v2: save reports, read files, list outputs (real automation)."""
import os
import datetime


def save_report(title: str, content: str) -> str:
    os.makedirs("outputs", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() else "_" for c in title)[:40]
    path = f"outputs/report_{safe}_{ts}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\nGenerated: {datetime.datetime.now()}\n\n{content}\n")
    return f"✅ Report saved: {path}"


def read_file(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()[:5000]
    except Exception as e:
        return f"Read failed: {e}"


def list_outputs() -> str:
    if not os.path.exists("outputs"):
        return "No outputs yet."
    files = os.listdir("outputs")
    return "Outputs:\n" + "\n".join(f"- {f}" for f in files) if files else "Outputs folder is empty."
