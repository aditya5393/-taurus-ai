"""Point 5 - Real Users + Real Numbers.
Collect feedback from 10 classmates for 1 week: tasks, time saved, satisfaction.
Use this to get award proof: 'Tested by 10 students, saved X hours'.
"""
import json
import os
import datetime

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "..", "user_feedback.json")


def _load():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE) as f:
            return json.load(f)
    return []


def _save(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_feedback(user: str, task: str, time_saved_min: int, satisfied: bool, comment: str = ""):
    data = _load()
    data.append({
        "user": user, "task": task, "time_saved_min": time_saved_min,
        "satisfied": satisfied, "comment": comment,
        "date": datetime.datetime.now().isoformat(),
    })
    _save(data)
    return data


def summary() -> str:
    data = _load()
    if not data:
        return "No user feedback yet. Get 10 classmates to try Taurus for 1 week."
    total_users = len(set(d["user"] for d in data))
    total_tasks = len(data)
    total_saved = sum(d["time_saved_min"] for d in data)
    sat = sum(1 for d in data if d["satisfied"]) / len(data) * 100
    return f"""Real User Results:
- Users: {total_users}
- Tasks completed: {total_tasks}
- Total time saved: {total_saved} min ({total_saved/60:.1f} hours)
- Satisfaction: {sat:.0f}%
Poster line: "Tested by {total_users} students, saved {total_saved/60:.1f} hours in 1 week."
"""
