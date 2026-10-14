"""Taurus AI v3 Router - Autonomous: LLM understands prompt and chooses agent + model.

User flow in v3:
  User: just gives prompt (e.g. "Solve this math problem" / "Write code for...")
  Router LLM: understands task -> picks task_type + specialized model
  Executor: runs that specialist model + tools + critic
"""
from app.models import choose_model_autonomously, ask_with_model, MODEL_REGISTRY


def route_v3(prompt: str) -> dict:
    """Returns routing decision with model info. This is the v3 entry point."""
    decision = choose_model_autonomously(prompt)
    return decision


def ask_llm_v3(task_type: str, system: str, user: str) -> str:
    """Call the specialized model for a task type."""
    info = MODEL_REGISTRY.get(task_type, MODEL_REGISTRY["research"])
    return ask_with_model(info["model"], system, user)
