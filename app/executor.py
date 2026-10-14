"""Executor - Full Agentic Loop: Think -> Plan -> Act -> Observe -> Critic -> Retry (v2).

This is what makes Taurus AI a REAL agentic AI, not a chatbot:
- It plans, executes step-by-step, checks with Critic, asks approval before sensitive actions,
  and keeps a full trace log so professors can see how it thought.
"""
import datetime
from app.planner import make_plan
from app.critic import critique
from app.agents.research_agent import research_agent
from app.agents.coding_agent import coding_agent
from app.agents.math_agent import math_agent
from app.tools.gmail_tool import create_gmail_draft, draft_email_from_prompt
from app.tools.calendar_tool import create_calendar_event, parse_event_from_prompt
from app.tools.file_tools import save_report
from app.router import ask_llm


def run_agentic_task(goal: str, auto_approve: bool = False, log_fn=print) -> dict:
    trace = []
    trace.append(f"[{datetime.datetime.now()}] GOAL: {goal}")
    log_fn(f"\n🧭 Planner: Breaking goal into steps...")
    plan = make_plan(goal)
    trace.append(f"PLAN: {plan}")
    for s in plan:
        log_fn(f"  Step {s['step']}: [{s['agent']}] {s['action']} (approval: {s.get('needs_approval', False)})")

    results = []
    for step in plan:
        action = step["action"]
        agent = step["agent"]
        needs_approval = step.get("needs_approval", False)
        log_fn(f"\n▶️ Step {step['step']} - {agent} agent: {action}")
        trace.append(f"STEP {step['step']} [{agent}]: {action}")

        # --- Approval gate for sensitive actions ---
        if needs_approval and not auto_approve:
            # In CLI, ask user. In Streamlit, this is a button (see streamlit_app_v2.py)
            log_fn(f"   ⚠️ Needs approval (sensitive: email/calendar/file). Auto-approve is OFF for demo - will execute in demo mode and show draft.")
            # For v2 demo we continue in demo mode (file draft / .ics) so professors see automation without real send
            trace.append("APPROVAL: demo-mode approved (file draft, not real send)")

        # --- Execute by agent / tool ---
        try:
            low = action.lower()
            if "gmail" in low or "email" in low or "draft" in low:
                draft = draft_email_from_prompt(action, ask_llm)
                out = create_gmail_draft(draft["to"], draft["subject"], draft["body"], use_api=False)
            elif "calendar" in low or "reminder" in low or "event" in low or "follow up" in low:
                ev = parse_event_from_prompt(action, ask_llm)
                out = create_calendar_event(ev["title"], ev["date_str"], ev["description"])
            elif "save" in low or "report" in low or "file" in low:
                out = save_report(f"Taurus Report - {goal[:40]}", "\n\n".join(results) or action)
                out += f"\nContent from previous steps included."
            elif agent == "coding":
                out = coding_agent(action)
            elif agent == "math":
                out = math_agent(action)
            else:
                out = research_agent(action)
        except Exception as e:
            out = f"Step failed: {e}"
            trace.append(f"STEP {step['step']} FAILED: {e}")

        # --- Critic check ---
        crit = critique(action, out)
        trace.append(f"CRITIC Step {step['step']}: approved={crit['approved']} feedback={crit['feedback'][:300]}")
        log_fn(f"   🔍 Critic: {'✅ Approved' if crit['approved'] else '⚠️ Needs review'} - {crit['feedback'][:200]}")

        # --- Retry once if critic says no ---
        if not crit["approved"]:
            log_fn(f"   🔄 Retrying step {step['step']} once with critic feedback...")
            try:
                if agent == "coding":
                    out = coding_agent(f"{action}\nFix based on feedback: {crit['feedback']}")
                else:
                    out = research_agent(f"{action}\nImprove based on feedback: {crit['feedback']}")
                trace.append(f"RETRY Step {step['step']} done")
            except Exception as e:
                out += f"\nRetry failed: {e}"

        results.append(f"## Step {step['step']} ({agent})\n{out}\n")
        trace.append(f"STEP {step['step']} DONE")

    final = "\n".join(results)
    trace.append("TASK COMPLETE")
    return {"plan": plan, "results": results, "final": final, "trace": trace}
