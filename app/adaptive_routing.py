"""Point 3 - Adaptive Routing That Learns YOU (Unique Twist).
Normal routing: Math -> Math model, Coding -> Coding model.
Adaptive: Taurus tracks which model actually succeeded for THIS user, and prefers it next time.

Example: For Aditya's math, QwQ worked 90% vs Llama 70% -> Taurus now prefers QwQ for him.
This is personalised routing - no one else has it.
"""
import json
import os

ADAPT_FILE = os.path.join(os.path.dirname(__file__), "..", "adaptive_routing.json")


def _load():
    if os.path.exists(ADAPT_FILE):
        with open(ADAPT_FILE) as f:
            return json.load(f)
    return {}  # {task_type: {model: {success, total}}}


def _save(data):
    with open(ADAPT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def record_result(task_type: str, model: str, success: bool):
    data = _load()
    data.setdefault(task_type, {}).setdefault(model, {"success": 0, "total": 0})
    data[task_type][model]["total"] += 1
    if success:
        data[task_type][model]["success"] += 1
    _save(data)


def best_model_for(task_type: str, default_model: str) -> tuple:
    """Return (best_model, reason). Uses past success rates for this user."""
    data = _load()
    if task_type not in data:
        return default_model, "No history yet - using default specialized model"
    best, best_rate, best_total = default_model, -1, 0
    for model, stats in data[task_type].items():
        if stats["total"] >= 2:  # need at least 2 samples
            rate = stats["success"] / stats["total"]
            if rate > best_rate:
                best, best_rate, best_total = model, rate, stats["total"]
    if best_rate >= 0:
        return best, f"Learned: {best} worked {best_rate*100:.0f}% ({best_total} tasks) for you - preferred over default"
    return default_model, "Not enough history - using default"


def adaptive_summary() -> str:
    data = _load()
    if not data:
        return "No adaptive history yet. Complete tasks to learn your best models."
    lines = ["Adaptive Routing - What Taurus learned about YOU:"]
    for task, models in data.items():
        for model, s in models.items():
            rate = s["success"] / s["total"] * 100 if s["total"] else 0
            lines.append(f"- {task} | {model}: {s['success']}/{s['total']} = {rate:.0f}% success")
    return "\n".join(lines)
