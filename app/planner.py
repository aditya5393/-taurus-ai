"""Planner Agent - breaks a goal into steps for Taurus AI v2 (full agentic)."""
from app.router import ask_llm
import json


def make_plan(goal: str) -> list:
    """Return list of steps: [{step, agent, action, needs_approval}]"""
    prompt = f"""You are the Planner for Taurus AI, a real agentic AI.
Break this goal into 3-6 concrete steps.
Each step must have: step (number), agent (research/coding/math), action (what to do), needs_approval (true if it sends email / creates calendar event / writes file, else false).
Return ONLY valid JSON list.

Goal: {goal}

Example:
[{{"step": 1, "agent": "research", "action": "Search for 5 Agentic AI internships", "needs_approval": false}},
 {{"step": 2, "agent": "research", "action": "Draft Gmail to top company", "needs_approval": true}}]
"""
    try:
        raw = ask_llm("You are a planner. Return only JSON.", prompt)
        # Extract JSON list
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except Exception:
        pass
    # Fallback simple plan
    return [
        {"step": 1, "agent": "research", "action": f"Research: {goal}", "needs_approval": False},
        {"step": 2, "agent": "coding", "action": f"Prepare code / draft for: {goal}", "needs_approval": False},
        {"step": 3, "agent": "math", "action": f"Verify any math in: {goal}", "needs_approval": False},
    ]
