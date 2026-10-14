"""Taurus AI v4 Executor - Full Agentic + Autonomous Routing + Self-Learning + Important Memory.

Flow:
  1. User gives prompt
  2. Recall relevant Important Memory + Lessons -> inject into task (so it learns)
  3. Router LLM understands task -> chooses specialized model
  4. Planner / Agents execute with tools + Critic
  5. After task: Reflect -> save Lessons + Important facts -> next task gets better
  6. If user says "remember this: ..." -> save as importance 10, never forget
"""
import datetime
from app.models import choose_model_autonomously
from app.planner import make_plan
from app.critic import critique
from app.self_learning import build_memory_context, reflect_and_learn, remember_user_fact
from app.agents.research_agent import research_agent
from app.agents.coding_agent import coding_agent
from app.agents.math_agent import math_agent
from app.tools.gmail_tool import create_gmail_draft, draft_email_from_prompt
from app.tools.calendar_tool import create_calendar_event, parse_event_from_prompt
from app.tools.file_tools import save_report
from app.router import ask_llm


def run_agentic_task_v4(goal: str, auto_approve: bool = False, user_feedback: str = "", log_fn=print) -> dict:
    trace = []
    trace.append(f"[{datetime.datetime.now()}] USER PROMPT: {goal}")

    # --- Special: "remember this" command ---
    low = goal.lower().strip()
    if low.startswith("remember this") or low.startswith("remember:") or "remember this:" in low:
        fact = goal.split(":", 1)[1].strip() if ":" in goal else goal.replace("remember this", "").strip()
        saved = remember_user_fact(fact)
        msg = f"✅ Remembered as important (importance 10, never forget): {fact}"
        log_fn(msg)
        trace.append(f"MEMORY SAVE: {fact}")
        return {"decision": {"task_type": "memory", "model": "-", "reason": "User asked to remember"}, "plan": [], "results": [msg], "final": msg, "trace": trace, "memory_context": ""}

    # --- 1. Recall memory + lessons BEFORE task (self-learning in action) ---
    memory_context = build_memory_context(goal)
    log_fn(f"\n🧠 Memory recalled:\n{memory_context[:800]}")
    trace.append(f"MEMORY RECALL: {memory_context[:500]}")

    # --- 2. Autonomous routing ---
    decision = choose_model_autonomously(goal)
    log_fn(f"\n🧭 Router: {decision['task_type']} -> {decision['model']} | Why: {decision['reason']}")
    trace.append(f"ROUTER: {decision}")

    # --- 3. Execute (single or multi) ---
    if decision["task_type"] != "multi":
        task = decision["task_type"]
        # Inject memory into agent via prompt prefix (agents already use memory-aware prompts in v4 via context)
        enriched = f"{goal}\n\n[MEMORY CONTEXT - use this]:\n{memory_context}"
        if task == "coding":
            out = coding_agent(enriched)
        elif task == "math":
            out = math_agent(enriched)
        else:
            out = research_agent(enriched)
        crit = critique(goal, out)
        trace.append(f"CRITIC: approved={crit['approved']}")
        # --- 4. Self-learning: reflect + save ---
        learned = reflect_and_learn(goal, task, decision["model"], out, success=crit["approved"], user_feedback=user_feedback)
        trace.append(f"SELF-LEARNING: lessons={len(learned['lessons'])} important={len(learned['important_saved'])}")
        log_fn(f"   📚 Self-learning: saved {len(learned['lessons'])} lesson(s)")
        return {"decision": decision, "plan": [], "results": [out], "final": out, "trace": trace, "memory_context": memory_context, "learned": learned}

    # Multi-task
    plan = make_plan(goal)
    trace.append(f"PLAN: {plan}")
    results = []
    for step in plan:
        action = step["action"]
        agent = step["agent"]
        step_decision = choose_model_autonomously(action)
        log_fn(f"\n▶️ Step {step['step']} - {agent} ({step_decision['model']}) : {action}")
        trace.append(f"STEP {step['step']} [{agent}] model={step_decision['model']}")
        try:
            low_a = action.lower()
            if "gmail" in low_a or "email" in low_a or "draft" in low_a:
                draft = draft_email_from_prompt(action, ask_llm)
                out = create_gmail_draft(draft["to"], draft["subject"], draft["body"], use_api=False)
            elif "calendar" in low_a or "reminder" in low_a or "event" in low_a:
                ev = parse_event_from_prompt(action, ask_llm)
                out = create_calendar_event(ev["title"], ev["date_str"], ev["description"])
            elif "save" in low_a or "report" in low_a or "file" in low_a:
                out = save_report(f"Taurus Report - {goal[:40]}", "\n\n".join(results) or action)
            elif agent == "coding":
                out = coding_agent(f"{action}\n\n[MEMORY]:\n{memory_context}")
            elif agent == "math":
                out = math_agent(f"{action}\n\n[MEMORY]:\n{memory_context}")
            else:
                out = research_agent(f"{action}\n\n[MEMORY]:\n{memory_context}")
        except Exception as e:
            out = f"Step failed: {e}"
        crit = critique(action, out)
        trace.append(f"CRITIC Step {step['step']}: approved={crit['approved']}")
        if not crit["approved"]:
            try:
                out = research_agent(f"{action}\nImprove based on feedback: {crit['feedback']}")
            except Exception as e:
                out += f"\nRetry failed: {e}"
        results.append(f"## Step {step['step']} ({agent})\n{out}\n")

    final = "\n".join(results)
    learned = reflect_and_learn(goal, "multi", decision["model"], final, success=True, user_feedback=user_feedback)
    trace.append(f"SELF-LEARNING: lessons={len(learned['lessons'])}")
    return {"decision": decision, "plan": plan, "results": results, "final": final, "trace": trace, "memory_context": memory_context, "learned": learned}
