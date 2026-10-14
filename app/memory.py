"""Simple JSON memory for Taurus AI - remembers user preferences."""
import json
import os

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "memory.json")


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE) as f:
            return json.load(f)
    return {"preferences": {}, "history": []}


def save_preference(key, value):
    mem = load_memory()
    mem["preferences"][key] = value
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)
    return mem


def add_history(query, agent, answer):
    mem = load_memory()
    mem["history"].append({"query": query, "agent": agent, "answer": answer[:500]})
    mem["history"] = mem["history"][-50:]  # keep last 50
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)
