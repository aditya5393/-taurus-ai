"""Coding Agent - writes code, runs it, fixes errors.
v3: uses specialized Coding LLM (qwen-2.5-coder-32b) via autonomous routing."""
import re
from app.models import ask_for_task
from app.tools.code_executor import run_code


def coding_agent(query: str) -> str:
    print("[Coding Agent] Writing code... (Coding LLM)")
    code = ask_for_task("coding",
        "You are a coding agent. Return ONLY Python code, no explanation, in a code block.",
        query,
    )
    code = re.sub(r"```python|```", "", code).strip()
    print(f"\n--- Generated Code ---\n{code}\n")
    result = run_code(code)
    print(f"--- Execution Result ---\n{result}")
    if "Error" in result:
        fix = ask_for_task("coding",
            "You are a coding agent. Fix this code. Return ONLY code.",
            f"Original: {query}\nCode: {code}\nError: {result}",
        )
        fix = re.sub(r"```python|```", "", fix).strip()
        return f"Fixed code:\n{fix}\nRun result: {run_code(fix)}"
    return f"Code worked!\n{code}\nOutput: {result}"
