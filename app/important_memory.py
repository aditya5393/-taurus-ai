"""Taurus AI v4 - Important Data Memory.
Keeps important data, not just chat history.
- Important facts: user preferences, names, project details, corrections
- Episodic: past tasks + what worked / failed
- Lessons: self-learning insights from reflections

Storage: JSON file (simple, explainable for internship) + optional ChromaDB later.
Important items are never auto-deleted; normal history is capped.
"""
import json
import os
import datetime

STORE_FILE = os.path.join(os.path.dirname(__file__), "..", "taurus_memory.json")


def _load():
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"important": [], "episodes": [], "lessons": [], "preferences": {}}


def _save(data):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data


def save_important(text: str, category: str = "general", importance: int = 9, source: str = "user") -> dict:
    """Save an important fact. importance 1-10, 9-10 = never forget."""
    data = _load()
    item = {
        "id": f"imp_{len(data['important']) + 1}_{int(datetime.datetime.now().timestamp())}",
        "text": text,
        "category": category,
        "importance": importance,
        "source": source,
        "created": datetime.datetime.now().isoformat(),
        "used_count": 0,
    }
    data["important"].append(item)
    _save(data)
    return item


def save_episode(task: str, agent: str, model: str, result_summary: str, success: bool, feedback: str = "") -> dict:
    data = _load()
    ep = {
        "task": task,
        "agent": agent,
        "model": model,
        "result_summary": result_summary[:1000],
        "success": success,
        "feedback": feedback[:500],
        "time": datetime.datetime.now().isoformat(),
    }
    data["episodes"].append(ep)
    data["episodes"] = data["episodes"][-100:]  # keep last 100 episodes
    _save(data)
    return ep


def save_lesson(lesson: str, applies_to: str = "general") -> dict:
    """Self-learning lesson: what Taurus learned and should do differently next time."""
    data = _load()
    item = {
        "lesson": lesson,
        "applies_to": applies_to,
        "created": datetime.datetime.now().isoformat(),
        "used_count": 0,
    }
    data["lessons"].append(item)
    _save(data)
    return item


def recall_relevant(query: str, top_k: int = 5) -> dict:
    """Simple keyword recall: returns important facts + lessons relevant to query.
    In v4 demo this is keyword-based (explainable). Upgrade to embeddings/ChromaDB later.
    """
    data = _load()
    q = query.lower()
    words = [w for w in q.split() if len(w) > 3]

    def score(text: str):
        t = text.lower()
        return sum(1 for w in words if w in t)

    important_sorted = sorted(data["important"], key=lambda x: (x["importance"], score(x["text"])), reverse=True)
    # Filter to relevant, but always keep top important if no match
    relevant_imp = [x for x in important_sorted if score(x["text"]) > 0][:top_k] or important_sorted[:2]
    relevant_lessons = [x for x in data["lessons"] if score(x["lesson"]) > 0 or score(x["applies_to"]) > 0][:top_k]
    # Mark used
    for x in relevant_imp + relevant_lessons:
        x["used_count"] = x.get("used_count", 0) + 1
    if relevant_imp or relevant_lessons:
        _save(data)
    return {"important": relevant_imp, "lessons": relevant_lessons, "preferences": data["preferences"]}


def list_important() -> list:
    return _load()["important"]


def list_lessons() -> list:
    return _load()["lessons"]


def set_preference(key: str, value: str):
    data = _load()
    data["preferences"][key] = value
    _save(data)
    return data["preferences"]
