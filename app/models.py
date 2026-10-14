"""Taurus AI v3 - Autonomous Model Routing.
User just gives a prompt. The model itself understands the task and chooses the right specialized LLM.

This is the key v3 upgrade: no manual model selection, no keywords.
The Router LLM reads the prompt, understands intent, and picks agent + model.
"""
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# --- Model Registry: specialized LLMs per task (Groq free tier) ---
# If a model name is not available on your Groq account, it auto-falls back to llama-3.3-70b.
MODEL_REGISTRY = {
    "research": {
        "model": "llama-3.3-70b-versatile",
        "label": "General / Research LLM",
        "why": "Best for research, summarising, drafting messages/emails",
    },
    "coding": {
        "model": "qwen-2.5-coder-32b",
        "label": "Coding LLM",
        "why": "Trained on code - more accurate for writing / fixing Python",
        "fallback": "llama-3.3-70b-versatile",
    },
    "math": {
        "model": "qwen-qwq-32b",
        "label": "Math / Reasoning LLM",
        "why": "Reasoning model - better step-by-step math, then verified by SymPy calculator",
        "fallback": "llama-3.3-70b-versatile",
    },
    "planner": {
        "model": "llama-3.3-70b-versatile",
        "label": "Planner LLM",
        "why": "Plans tasks into steps",
    },
    "critic": {
        "model": "llama-3.3-70b-versatile",
        "label": "Critic LLM",
        "why": "Checks outputs for correctness",
    },
    "multi": {
        "model": "llama-3.3-70b-versatile",
        "label": "Orchestrator LLM",
        "why": "Multi-part goal - will use multiple specialist models",
    },
}

ROUTER_MODEL = "llama-3.3-70b-versatile"


def ask_with_model(model: str, system: str, user: str, temperature: float = 0.3) -> str:
    """Call a specific model. Falls back to router model if the specialized model fails."""
    try:
        res = _client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
        )
        return res.choices[0].message.content
    except Exception as e:
        if model != ROUTER_MODEL:
            # Fallback: specialized model not available -> use general model
            res = _client.chat.completions.create(
                model=ROUTER_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
            )
            return res.choices[0].message.content + f"\n\n[Note: {model} unavailable ({e}), used fallback {ROUTER_MODEL}]"
        raise


def choose_model_autonomously(prompt: str) -> dict:
    """
    v3 core: User just gives prompt. LLM itself understands task and chooses model.
    Returns: {task_type, agent, model, model_label, reason, confidence}
    """
    system = """You are the Model Router for Taurus AI, a real agentic AI.
User just gives a prompt. YOU must understand the task and choose the RIGHT specialized model.

Task types and models:
- research: for research, search, summarise, draft messages/emails, general questions -> model: llama-3.3-70b-versatile
- coding: for writing code, fixing bugs, Python, functions, programs -> model: qwen-2.5-coder-32b
- math: for math, equations, calculations, reasoning, proofs -> model: qwen-qwq-32b
- multi: for goals needing 2+ types (e.g. research + code + math + email + calendar) -> model: llama-3.3-70b-versatile (orchestrator will use specialists)

Return ONLY valid JSON:
{"task_type": "research| coding|math|multi", "agent": "same as task_type", "model": "exact model name", "reason": "1 line why this model fits", "confidence": 0.0-1.0}

Examples:
- "Write Python code to sort list" -> coding, qwen-2.5-coder-32b
- "Solve 2x+5=15" -> math, qwen-qwq-32b
- "Research agentic AI" -> research, llama-3.3-70b-versatile
- "Find internships, draft Gmail, create reminder, save report" -> multi
"""
    try:
        raw = ask_with_model(ROUTER_MODEL, system, f"User prompt: {prompt}")
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])
        task = data.get("task_type", "research").strip().lower()
        if task not in MODEL_REGISTRY:
            task = "research"
        info = MODEL_REGISTRY[task]
        return {
            "task_type": task,
            "agent": task,
            "model": info["model"],
            "model_label": info["label"],
            "reason": data.get("reason", info["why"]),
            "confidence": float(data.get("confidence", 0.9)),
            "raw": raw,
        }
    except Exception:
        # Keyword fallback if router LLM fails
        q = prompt.lower()
        if any(w in q for w in ["code", "python", "bug", "function"]):
            task = "coding"
        elif any(w in q for w in ["solve", "math", "equation", "calculate"]):
            task = "math"
        elif any(w in q for w in ["draft", "gmail", "calendar", "report", "research", "find"]):
            task = "multi" if "and" in q or "," in q else "research"
        else:
            task = "research"
        info = MODEL_REGISTRY[task]
        return {
            "task_type": task,
            "agent": task,
            "model": info["model"],
            "model_label": info["label"],
            "reason": f"Fallback routing: {info['why']}",
            "confidence": 0.6,
            "raw": "fallback",
        }


def ask_for_task(task_type: str, system: str, user: str) -> str:
    """Helper: agents call this - it auto-picks the right specialized model for their task type."""
    info = MODEL_REGISTRY.get(task_type, MODEL_REGISTRY["research"])
    return ask_with_model(info["model"], system, user)
