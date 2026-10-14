"""Taurus AI v3 - Autonomous Model Routing CLI. Run: python -m app.main_v3
User just gives prompt. Model itself understands task and chooses right specialized LLM.
"""
from app.executor_v3 import run_agentic_task_v3


def main():
    print("=== ♉ TAURUS AI v3 - AUTONOMOUS MODEL ROUTING ===")
    print("Just give a prompt. Taurus itself understands the task and activates the right model.")
    print("  Math ask  -> Math/Reasoning LLM (qwen-qwq-32b) + SymPy check")
    print("  Coding ask -> Coding LLM (qwen-2.5-coder-32b) + code executor")
    print("  Research ask -> General LLM (llama-3.3-70b)")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            prompt = input("\n🎯 Your Prompt: ")
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in ["exit", "quit"]:
            break
        result = run_agentic_task_v3(prompt, auto_approve=False)
        print("\n" + "="*60)
        print("✅ FINAL RESULT")
        print("="*60)
        print(result["final"])
        print("\n--- TRACE (which model was chosen & why) ---")
        for t in result["trace"]:
            print(t)


if __name__ == "__main__":
    main()
