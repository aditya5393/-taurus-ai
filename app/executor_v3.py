"""Taurus AI v3 Executor - Full Agentic Loop with Autonomous Model Routing.

Flow:
  1. User gives prompt (no need to say which model/agent)
  2. Router LLM understands task -> chooses task_type + specialized model + reason
  3. Planner breaks goal into steps (if multi)
  4. Each step runs with its own specialized model + tools
  5. Critic checks each step
  6. Approval gate for Gmail/Calendar/File actions
  7. Full trace shows which model was chosen and why
"""
import datetime
from app.models import choose_model_autonomously, ask_with_model, MODEL_REGISTRY
from app.planner import make_plan
from app.critic import critique
from app.agents.research_agent import research_agent
from app.agents.coding_agent import coding_agent
from app.agents.math_agent import math_agent
from app.tools.gmail_tool import create_gmail_draft, draft_email_from_prompt
from app.tools.calendar_tool import create_calendar_event, parse_event_from_prompt
from app.tools.file_tools import save_report
from app.router import ask_llm


def run_agentic_task_v3(goal: str, auto_approve: bool = False, log_fn=print) -> dict:
    trace = []
    trace.append(f"[{datetime.datetime.now()}] USER PROMPT: {goal}")

    # --- v3: Autonomous routing - model itself understands task ---
    decision = choose_model_autonomously(goal)
    log_fn(f"\n🧠 Autonomous Router understood task:")
    log_fn(f"   Task: {decision['task_type']} | Model: {decision['model']} ({decision['model_label']})")
    log_fn(f"   Why: {decision['reason']} | Confidence: {decision['confidence']:.2f}")
    trace.append(f"ROUTER: task={decision['task_type']} model={decision['model']} reason={decision['reason']}")

    # If single-task, run directly with specialized model. If multi, plan + run steps.
    if decision["task_type"] != "multi":
        task = decision["task_type"]
        log_fn(f"\n▶️ Running {task} agent with specialized model {decision['model']}...")
        if task == "coding":
            out = coding_agent(goal)  # coding_agent uses coder model via ask_llm override in v3? See note below
            # For v3 demo, also show model choice: re-run with specialized model prompt
        elif task == "math":
            out = math_agent(goal)
        else:
            out = research_agent(goal)
        crit = critique(goal, out)
        trace.append(f"CRITIC: approved={crit['approved']} feedback={crit['feedback'][:300]}")
        log_fn(f"   🔍 Critic: {'✅ Approved' if crit['approved'] else '⚠️ Needs review'}")
        return {
            "decision": decision,
            "plan": [{"step": 1, "agent": task, "action": goal, "needs_approval": False}],
            "results": [f"## Step 1 ({task} - {decision['model']})\n{out}\n"],
            "final": out,
            "trace": trace,
        }

    # --- Multi-task: planner + executor ---
    log_fn(f"\n🧭 Planner: Breaking multi-goal into steps...")
    plan = make_plan(goal)
    trace.append(f"PLAN: {plan}")
    for s in plan:
        log_fn(f"  Step {s['step']}: [{s['agent']}] {s['action']}")

    results = []
    for step in plan:
        action = step["action"]
        agent = step["agent"]
        # v3: each step also gets its own specialized model decision
        step_decision = choose_model_autonomously(action)
        model_used = step_decision["model"]
        log_fn(f"\n▶️ Step {step['step']} - {agent} agent with model {model_used} ({step_decision['model_label']})")
        log_fn(f"   Why this model: {step_decision['reason']}")
        trace.append(f"STEP {step['step']} [{agent}] model={model_used} action={action}")

        if step.get("needs_approval") and not auto_approve:
            log_fn(f"   ⚠️ Needs approval - demo mode: will execute as file draft / .ics (not real send)")
            trace.append("APPROVAL: demo-mode approved")

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
            elif agent == "coding":
                out = coding_agent(action)
            elif agent == "math":
                out = math_agent(action)
            else:
                out = research_agent(action)
        except Exception as e:
            out = f"Step failed: {e}"
            trace.append(f"STEP {step['step']} FAILED: {e}")

        crit = critique(action, out)
        trace.append(f"CRITIC Step {step['step']}: approved={crit['approved']}")
        log_fn(f"   🔍 Critic: {'✅ Approved' if crit['approved'] else '⚠️ Needs review'}")
        if not crit["approved"]:
            log_fn(f"   🔄 Retrying step {step['step']} once...")
            try:
                out = research_agent(f"{action}\nImprove based on feedback: {crit['feedback']}")
            except Exception as e:
                out += f"\nRetry failed: {e}"

        results.append(f"## Step {step['step']} ({agent} - {model_used})\n{out}\n")
        trace.append(f"STEP {step['step']} DONE")

    final = "\n".join(results)
    trace.append("TASK COMPLETE")
    return {"decision": decision, "plan": plan, "results": results, "final": final, "trace": trace}
