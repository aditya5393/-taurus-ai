"""Taurus AI v1 - Modular CLI entry point. Run: python -m app.main"""
from app.router import route
from app.agents.research_agent import research_agent
from app.agents.coding_agent import coding_agent
from app.agents.math_agent import math_agent
from app.memory import add_history


def main():
    print("=== TAURUS AI v1 (modular) ===")
    print("Type 'exit' to quit.")
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
            ans = coding_agent(q)
        elif agent == "math":
            ans = math_agent(q)
        elif agent == "multi":
            print("--- Research part ---")
            r = research_agent(q)
            print(r)
            print("\n--- Math part ---")
            ans = math_agent(q)
        else:
            ans = research_agent(q)
        print(ans)
        try:
            add_history(q, agent, ans)
        except Exception:
            pass


if __name__ == "__main__":
    main()
