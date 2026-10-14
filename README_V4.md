# Taurus AI v4 — Self-Learning + Important Data Memory

## What is new in v4?

**Taurus now learns from every task and remembers important data — not just chat history.**

### 1. Important Data Memory (`app/important_memory.py`)
- **Important facts** (importance 9-10): user preferences, names, project details, corrections — never auto-deleted
- **Episodes**: past tasks + what worked / failed + which model was used
- **Lessons**: self-learning insights
- **Preferences**: key-value user preferences
- Storage: `taurus_memory.json` (simple JSON, explainable for internship). Upgrade to ChromaDB/embeddings later.
- Command: `remember this: <fact>` → saves as importance 10

### 2. Self-Learning (`app/self_learning.py`)
Loop after every task:
1. **Before task**: Recall relevant important facts + lessons → inject into prompt
2. **Do task**: existing v3 executor (routing + tools + critic)
3. **After task**: LLM reflects — "What worked? What failed? What to do differently?"
4. **Save**: 1-2 lessons + any important fact → next similar task automatically uses them

This is **memory-based learning, NOT model fine-tuning**. Like a human notebook. Explainable + demo-friendly.

Example:
- Task 1: Taurus solves math without showing steps → user says "show steps"
- Reflection saves lesson: "For math, always show steps, then verify with SymPy"
- Task 2: Same type → lesson recalled → Taurus shows steps automatically

### 3. How to demo for professors (2-min script)
1. `remember this: Aditya prefers short Python answers with comments` → shows memory save
2. Ask a coding question → shows memory recalled + used
3. Give a correction ("show steps") → shows lesson saved
4. Ask similar question again → shows improved answer using lesson
5. `show memory` → shows Important Memory + Lessons lists

This proves learning, not just chatting.

## Run v4

```bash
pip install -r requirements.txt
python -m app.main_v4
# or UI:
streamlit run app/streamlit_app_v4.py
```

## Files
- `app/important_memory.py` - save/recall important, episodes, lessons
- `app/self_learning.py` - build_memory_context + reflect_and_learn
- `app/executor_v4.py` - v4 loop: recall -> route -> act -> critic -> reflect
- `app/main_v4.py` - CLI with "remember this" + "show memory"
- `app/streamlit_app_v4.py` - UI with Memory sidebar + Learned panel
