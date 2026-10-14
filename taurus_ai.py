"""
Taurus AI v1 - Single-file version
Boss Router + Research + Coding + Math agents
Run: python taurus_ai.py
Needs GROQ_API_KEY in .env (free from console.groq.com)
"""
import os
import re
import io
import contextlib
from dotenv import load_dotenv
from openai import OpenAI
import requests
import sympy as sp

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = "llama-3.3-70b-versatile"


def ask_llm(system, user):
    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    return res.choices[0].message.content


# --- ROUTER (Boss) ---
def route(query):
    q = query.lower()
    if any(w in q for w in ["code", "python", "bug", "function", "program"]):
        return "coding"
    if any(w in q for w in ["solve", "math", "equation", "calculate", "integral", "derivative"]):
        return "math"
    if any(w in q for w in ["research", "search", "summarize", "draft", "message", "email"]):
        return "research"
    try:
        decision = ask_llm(
            "You are a router. Reply with only one word: research, coding, math, or multi.",
            f"Route this: {query}",
        )
        return decision.strip().lower()
    except Exception:
        return "research"


# --- TOOLS ---
def web_search(query):
    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1},
            timeout=10,
        )
        data = r.json()
        return data.get("AbstractText") or (
            data.get("RelatedTopics", [{}])[0].get("Text", "No result found")
            if data.get("RelatedTopics")
            else "No result found"
        )
    except Exception as e:
        return f"Search failed: {e}"


def calculator(expr):
    try:
        expr = expr.replace("^", "**")
        if "=" in expr:
            left, right = expr.split("=", 1)
            x = sp.symbols("x")
            sol = sp.solve(sp.Eq(sp.sympify(left), sp.sympify(right)), x)
            return f"Solution: x = {sol}"
        val = sp.sympify(expr)
        return f"Result: {expr} = {float(val)}"
    except Exception as e:
        return f"Calculator error: {e}"


def run_code(code):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
        return output.getvalue() or "Code ran with no output."
    except Exception as e:
        return f"Error: {e}"


# --- AGENTS ---
def research_agent(query):
    print("[Research Agent] Searching...")
    context = web_search(query)
    return ask_llm(
        "You are a research agent. Summarize with sources and clear bullet points.",
        f"Query: {query}\nSearch result: {context}",
    )


def coding_agent(query):
    print("[Coding Agent] Writing code...")
    code = ask_llm(
        "You are a coding agent. Return ONLY Python code, no explanation, in a code block.",
        query,
    )
    code = re.sub(r"```python|```", "", code).strip()
    print(f"\n--- Generated Code ---\n{code}\n")
    result = run_code(code)
    print(f"--- Execution Result ---\n{result}")
    if "Error" in result:
        fix = ask_llm(
            "You are a coding agent. Fix this code. Return ONLY code.",
            f"Original: {query}\nCode: {code}\nError: {result}",
        )
        fix = re.sub(r"```python|```", "", fix).strip()
        return f"Fixed code:\n{fix}\nRun result: {run_code(fix)}"
    return f"Code worked!\n{code}\nOutput: {result}"


def math_agent(query):
    print("[Math Agent] Solving step-by-step...")
    steps = ask_llm(
        "You are a math agent. Solve step-by-step, show each step clearly, then give final answer.",
        query,
    )
    numbers = re.findall(r"[\d\.\+\-\*/\(\) ]+", query)
    verify = ""
    if numbers and numbers[0].strip():
        verify = f"\n[Calculator check] {calculator(numbers[0])}"
    return steps + verify


# --- MAIN LOOP ---
def main():
    print("=== TAURUS AI v1 ===")
    print("Type 'exit' to quit. Try: research, coding, or math questions.")
    while True:
        try:
            q = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ["exit", "quit"]:
            break
        agent = route(q)
        print(f"[Router] -> {agent} agent")
        if agent == "coding":
            print(coding_agent(q))
        elif agent == "math":
            print(math_agent(q))
        elif agent == "multi":
            print("--- Research part ---")
            print(research_agent(q))
            print("\n--- Math part ---")
            print(math_agent(q))
        else:
            print(research_agent(q))


if __name__ == "__main__":
    main()
