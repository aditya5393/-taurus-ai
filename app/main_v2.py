"""Taurus AI v2 - Full Agentic CLI. Run: python -m app.main_v2"""
from app.executor import run_agentic_task


def main():
    print("=== ♉ TAURUS AI v2 - FULL AGENTIC MODE ===")
    print("Give me a GOAL, not just a question. I will plan, act, check, and automate.")
    print("Example: Find 5 Agentic AI internships, draft Gmail to top one, create calendar reminder, save report")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            goal = input("\n🎯 Your Goal: ")
        except (EOFError, KeyboardInterrupt):
            break
        if goal.lower() in ["exit", "quit"]:
            break
        result = run_agentic_task(goal, auto_approve=False)
        print("\n" + "="*60)
        print("✅ FINAL RESULT")
        print("="*60)
        print(result["final"])
        print("\n--- TRACE (how Taurus thought) ---")
        for t in result["trace"]:
            print(t)


if __name__ == "__main__":
    main()
