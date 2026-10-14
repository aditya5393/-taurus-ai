"""Point 2 - Measurable Self-Learning: Evaluation + Learning Curve.
Run same 20 tasks on Day 1 vs Day 7 after corrections, show improvement.
This is the award-winning proof: Taurus improves by learning, not just claims it.
"""
import json
import os
import datetime

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "evaluation_results.json")

# 20-task test set: 7 math, 7 coding, 6 research
TEST_SET = [
    {"id": 1, "type": "math", "prompt": "Solve 2x + 5 = 15 step by step", "expected_contains": "5"},
    {"id": 2, "type": "math", "prompt": "What is 15% of 240?", "expected_contains": "36"},
    {"id": 3, "type": "math", "prompt": "Solve x^2 - 5x + 6 = 0", "expected_contains": "2"},
    {"id": 4, "type": "math", "prompt": "Calculate derivative of x^2 + 3x", "expected_contains": "2x"},
    {"id": 5, "type": "math", "prompt": "If a train travels 120 km in 2 hours, what is speed?", "expected_contains": "60"},
    {"id": 6, "type": "math", "prompt": "Solve 3x - 7 = 8", "expected_contains": "5"},
    {"id": 7, "type": "math", "prompt": "What is factorial of 5?", "expected_contains": "120"},
    {"id": 8, "type": "coding", "prompt": "Write Python code to find fibonacci numbers", "expected_contains": "def"},
    {"id": 9, "type": "coding", "prompt": "Write Python code to sort a list", "expected_contains": "sort"},
    {"id": 10, "type": "coding", "prompt": "Write Python function to check prime number", "expected_contains": "def"},
    {"id": 11, "type": "coding", "prompt": "Write Python code to reverse a string", "expected_contains": "reverse"},
    {"id": 12, "type": "coding", "prompt": "Write Python code to find max in list", "expected_contains": "max"},
    {"id": 13, "type": "coding", "prompt": "Write Python code to count vowels in string", "expected_contains": "vowel"},
    {"id": 14, "type": "coding", "prompt": "Fix this bug: for i in range(5) print(i) - missing colon", "expected_contains": ":"},
    {"id": 15, "type": "research", "prompt": "Research agentic AI and summarize with sources", "expected_contains": "agent"},
    {"id": 16, "type": "research", "prompt": "Research LangGraph and summarize", "expected_contains": "LangGraph"},
    {"id": 17, "type": "research", "prompt": "Draft Gmail to professor about internship", "expected_contains": "Dear"},
    {"id": 18, "type": "research", "prompt": "Summarize what is RAG in AI", "expected_contains": "retrieval"},
    {"id": 19, "type": "research", "prompt": "Research Python vs Java for AI", "expected_contains": "Python"},
    {"id": 20, "type": "research", "prompt": "Draft a professional email asking for project feedback", "expected_contains": "Subject"},
]


def score_result(expected_contains: str, result: str) -> bool:
    return expected_contains.lower() in result.lower()


def run_evaluation(run_fn, label: str = "Day 1") -> dict:
    """run_fn(prompt) -> result string. Returns scores + saves to file."""
    results = []
    correct = 0
    for t in TEST_SET:
        try:
            out = run_fn(t["prompt"])
            ok = score_result(t["expected_contains"], out)
        except Exception as e:
            out, ok = f"Error: {e}", False
        if ok:
            correct += 1
        results.append({"id": t["id"], "type": t["type"], "prompt": t["prompt"], "correct": ok})
    score = {"label": label, "date": datetime.datetime.now().isoformat(), "correct": correct, "total": len(TEST_SET), "accuracy": correct / len(TEST_SET), "details": results}
    # Append to file
    data = []
    if os.path.exists(EVAL_FILE):
        with open(EVAL_FILE) as f:
            data = json.load(f)
    data.append(score)
    with open(EVAL_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return score


def learning_curve() -> str:
    """Return text chart of improvement over runs."""
    if not os.path.exists(EVAL_FILE):
        return "No evaluation runs yet. Run run_evaluation() on Day 1 and Day 7."
    with open(EVAL_FILE) as f:
        data = json.load(f)
    lines = ["Taurus Learning Curve (Accuracy over time):"]
    for d in data:
        bar = "█" * int(d["accuracy"] * 20)
        lines.append(f"{d['label']} ({d['date'][:10]}): {d['correct']}/{d['total']} = {d['accuracy']*100:.0f}% {bar}")
    if len(data) >= 2:
        imp = (data[-1]["accuracy"] - data[0]["accuracy"]) * 100
        lines.append(f"\nImprovement: {imp:+.0f} points - This is your award proof!")
    return "\n".join(lines)
