# Taurus AI v3 — Autonomous Model Routing

## What is new in v3?

**User just gives a prompt. The model itself understands the task and chooses the right specialized LLM.**

No manual selection. No keywords needed.

```
You: "Solve 2x + 5 = 15"
→ Router LLM understands: this is math
→ Activates Math/Reasoning LLM: qwen-qwq-32b
→ Solves step-by-step + SymPy calculator verifies

You: "Write Python code to sort list"
→ Router LLM understands: this is coding
→ Activates Coding LLM: qwen-2.5-coder-32b
→ Writes code + Code Executor runs + fixes if error

You: "Research agentic AI and draft Gmail"
→ Router LLM understands: research + multi-step
→ Activates General LLM: llama-3.3-70b + Planner + Specialists
```

## Model Registry (Groq free tier)

| Task | Model | Why |
|---|---|---|
| Research / Draft | `llama-3.3-70b-versatile` | Best general, drafting |
| Coding | `qwen-2.5-coder-32b` | Trained on code, more accurate |
| Math / Reasoning | `qwen-qwq-32b` | Reasoning model, step-by-step |
| Planner / Critic | `llama-3.3-70b-versatile` | Planning + checking |

If a specialized model is unavailable, it auto-falls back to `llama-3.3-70b-versatile`.

## How it works

1. **Router LLM** (`app/models.py: choose_model_autonomously`) reads your prompt and returns JSON: `{task_type, model, reason, confidence}`
2. **Executor v3** (`app/executor_v3.py`) runs that specialist model + tools
3. **Critic** checks output, **Approval** gate for Gmail/Calendar
4. **Trace** shows: which model was chosen, why, confidence, steps, critic

## Run v3

```bash
pip install -r requirements.txt
cp .env.example .env  # GROQ_API_KEY
python -m app.main_v3
```

UI for professors:
```bash
streamlit run app/streamlit_app_v3.py
```

## Files

- `app/models.py` - Model Registry + autonomous chooser + ask_with_model / ask_for_task
- `app/router_v3.py` - v3 router entry
- `app/executor_v3.py` - v3 full agentic loop with model routing
- `app/main_v3.py` - CLI
- `app/streamlit_app_v3.py` - UI demo showing chosen model + reason
- Agents now use specialized models: research→llama, coding→qwen-coder, math→qwen-qwq
