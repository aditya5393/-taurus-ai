"""Taurus AI v4 - Self-Learning.
After every task, Taurus reflects: What worked? What failed? What should I do differently next time?
That reflection becomes a Lesson saved in Important Memory and reused on future tasks.

Loop:
  1. Before task: recall relevant important facts + lessons -> include in prompt (so it learns)
  2. Do task (existing executor)
  3. After task: LLM reflects -> saves 1-2 lessons + important facts (if user said "remember this" or correction)
  4. Next similar task: lessons are recalled automatically -> better result without retraining

This is NOT model fine-tuning. It is memory-based learning (like a human notebook) - explainable and perfect for internship demo.
"""
from app.router import ask_llm
from app.important_memory import save_lesson, save_important, recall_relevant, save_episode


def build_memory_context(query: str) -> str:
    """Build context string from recalled memory to inject into agent prompt."""
    rec = recall_relevant(query)
    parts = []
    if rec["important"]:
        parts.append("IMPORTANT FACTS TO REMEMBER:")
        for it in rec["important"]:
            parts.append(f"- [{it['category']} | importance {it['importance']}] {it['text']}")
    if rec["lessons"]:
        parts.append("\nLESSONS LEARNED FROM PAST TASKS (apply these):")
        for ls in rec["lessons"]:
            parts.append(f"- [{ls['applies_to']}] {ls['lesson']}")
    if rec["preferences"]:
        parts.append("\nUSER PREFERENCES:")
        for k, v in rec["preferences"].items():
            parts.append(f"- {k}: {v}")
    return "\n".join(parts) if parts else "No relevant memory yet."


def reflect_and_learn(task: str, agent: str, model: str, result: str, success: bool, user_feedback: str = "") -> dict:
    """Call LLM to reflect and save lessons. Returns {lessons, important_saved}."""
    prompt = f"""You are Taurus AI's Self-Learning module.
Task: {task}
Agent: {agent} | Model: {model} | Success: {success}
Result (first 1500 chars): {result[:1500]}
User feedback / correction (if any): {user_feedback or 'none'}

Return ONLY:
LESSON 1: <one concrete lesson to do better next time, or 'none' if nothing to learn>
LESSON 2: <second lesson or 'none'>
IMPORTANT: <one important fact to remember long-term, or 'none'>

Rules: Be specific, not generic. Example good lesson: "For math word problems, always extract numbers first, then solve with SymPy before answering."
"""
    try:
        raw = ask_llm("You are a self-learning reflection agent. Be specific and concise.", prompt)
    except Exception as e:
        return {"lessons": [], "important_saved": [], "raw": f"Reflection failed: {e}"}

    lessons, important_saved = [], []
    for line in raw.splitlines():
        line = line.strip()
        if line.upper().startswith("LESSON") and "none" not in line.lower():
            lesson_text = line.split(":", 1)[1].strip() if ":" in line else line
            if len(lesson_text) > 10:
                saved = save_lesson(lesson_text, applies_to=agent)
                lessons.append(saved)
        if line.upper().startswith("IMPORTANT") and "none" not in line.lower():
            fact = line.split(":", 1)[1].strip() if ":" in line else line
            if len(fact) > 10:
                saved = save_important(fact, category="learned", importance=8, source="self-learning")
                important_saved.append(saved)

    # Always save episode
    save_episode(task, agent, model, result, success, user_feedback)
    return {"lessons": lessons, "important_saved": important_saved, "raw": raw}


def remember_user_fact(text: str, category: str = "user"):
    """User says 'remember this' -> save as high-importance."""
    return save_important(text, category=category, importance=10, source="user: remember this")
