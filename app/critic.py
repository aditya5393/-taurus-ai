"""Critic Agent - checks every output before it is accepted (v2)."""
from app.router import ask_llm


def critique(task: str, output: str) -> dict:
    """Return {approved: bool, feedback: str}"""
    verdict = ask_llm(
        "You are a Critic Agent. Check if the output is correct, complete, and safe. "
        "Reply in format: APPROVED: yes/no | FEEDBACK: short reason",
        f"Task: {task}\nOutput: {output[:2000]}",
    )
    approved = "yes" in verdict.lower().split("approved:")[-1][:10] if "approved:" in verdict.lower() else "yes" in verdict.lower()[:20]
    return {"approved": approved, "feedback": verdict, "raw": verdict}


def needs_fix(feedback: str) -> bool:
    return "no" in feedback.lower()[:30]
