"""Point 7 - Safety + Privacy as Feature (Responsible AI - awards love this).
- Approval-gated: Never auto-send email / create calendar without approval
- Local-first: Important memory stored locally in taurus_memory.json, user can see/delete it
- Trace: Every decision logged, explainable
- Deletable memory: User can delete any important fact
"""
import os
import json
from app.important_memory import _load as load_mem, _save as save_mem


def needs_approval(action: str) -> bool:
    """True if action is sensitive and needs human approval."""
    sensitive = ["send email", "gmail", "calendar", "create event", "delete", "pay", "send"]
    return any(s in action.lower() for s in sensitive)


def approval_gate(action: str, auto_approve: bool = False) -> tuple:
    """Return (approved, message). In demo, auto_approve=False means show draft first."""
    if not needs_approval(action):
        return True, "No approval needed (read-only / safe action)"
    if auto_approve:
        return True, "Auto-approved in demo mode (file draft, not real send)"
    return False, f"⚠️ Approval needed for: {action}\nTaurus will show draft first. Say 'approve' to proceed, or it stays as draft."


def delete_important_fact(fact_id_or_text: str) -> str:
    data = load_mem()
    before = len(data["important"])
    data["important"] = [x for x in data["important"] if x["id"] != fact_id_or_text and fact_id_or_text.lower() not in x["text"].lower()]
    save_mem(data)
    removed = before - len(data["important"])
    return f"Deleted {removed} important fact(s). You control your memory."


def privacy_summary() -> str:
    return """Taurus Safety & Privacy:
- ✅ Approval-gated: Never auto-sends email / creates calendar without your approval
- ✅ Local-first: Memory stored locally in taurus_memory.json, not sent to third parties
- ✅ Deletable: Say 'delete memory: <fact>' to remove any saved fact
- ✅ Traceable: Every step logged (Plan -> Act -> Critic -> Result)
- ✅ Explainable: Router shows which model was chosen and why
"""
