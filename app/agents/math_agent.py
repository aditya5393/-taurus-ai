"""Math Agent - solves step-by-step and verifies with calculator.
v3: uses specialized Math/Reasoning LLM (qwen-qwq-32b) via autonomous routing."""
import re
from app.models import ask_for_task
from app.tools.calculator import calculator


def math_agent(query: str) -> str:
    print("[Math Agent] Solving step-by-step... (Math Reasoning LLM)")
    steps = ask_for_task("math",
        "You are a math agent. Solve step-by-step, show each step clearly, then give final answer.",
        query,
    )
    numbers = re.findall(r"[\d\.\+\-\*/\(\) ]+", query)
    verify = ""
    if numbers and numbers[0].strip():
        verify = f"\n[Calculator check] {calculator(numbers[0])}"
    return steps + verify
