"""Taurus AI v4 - Self-Learning + Important Memory CLI. Run: python -m app.main_v4
Commands:
  - Just type a prompt -> Taurus does task + learns from it
  - "remember this: <fact>" -> saves as importance 10, never forget
  - "show memory" -> lists important facts + lessons
"""
from app.executor_v4 import run_agentic_task_v4
from app.important_memory import list_important, list_lessons


def main():
    print("=== ♉ TAURUS AI v4 - SELF-LEARNING + IMPORTANT MEMORY ===")
    print("Taurus learns from every task and remembers important data.")
    print("Try: 'remember this: Aditya prefers short Python answers'")
    print("Then: 'show memory' to see what it remembers.")
    print("Type 'exit' to quit.\n")
    last_goal = ""
    while True:
        try:
            prompt = input("\n🎯 Your Prompt: ")
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in ["exit", "quit"]:
            break
        if prompt.lower().strip() == "show memory":
            print("\n--- IMPORTANT MEMORY ---")
            for it in list_important():
                print(f"- [{it['category']} | imp {it['importance']}] {it['text']} (used {it.get('used_count',0)}x)")
            print("\n--- LESSONS LEARNED ---")
            for ls in list_lessons():
                print(f"- [{ls['applies_to']}] {ls['lesson']}")
            continue
        # Ask for feedback to learn from (optional, press Enter to skip)
        feedback = ""
        if last_goal:
            feedback = input("Any feedback / correction on last answer? (Enter to skip): ").strip()
        result = run_agentic_task_v4(prompt, auto_approve=False, user_feedback=feedback)
        print("\n" + "="*60)
        print("✅ FINAL RESULT")
        print("="*60)
        print(result["final"])
        print("\n--- TRACE ---")
        for t in result["trace"]:
            print(t)
        last_goal = prompt


if __name__ == "__main__":
    main()
