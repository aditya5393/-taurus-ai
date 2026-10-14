"""Point 1 - Killer Story Runner: ONE goal -> full automation demo.
Run: python -m app.killer_story
Story: Research Agentic AI internships, draft Gmail to top one, create reminder, save report.
"""
from app.executor_v4 import run_agentic_task_v4


def main():
    goal = "Find 5 Agentic AI internships, draft Gmail to top one, create calendar reminder to follow up, save report"
    print("=== ♉ TAURUS AI - KILLER STORY DEMO ===")
    print(f"ONE Goal: {goal}\n")
    result = run_agentic_task_v4(goal, auto_approve=True)
    print("\n=== FINAL RESULT ===")
    print(result["final"])
    print("\n=== TRACE ===")
    for t in result["trace"]:
        print(t)


if __name__ == "__main__":
    main()
