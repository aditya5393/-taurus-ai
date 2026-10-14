# Taurus AI v1 — Multi-Agent Assistant

One assistant with a Boss Router + 3 Specialist Agents:
- **Research + Messaging Agent** — searches the web, summarizes with sources, drafts messages/emails
- **Coding Agent** — writes Python code, runs it, fixes errors (up to 3 retries)
- **Math Agent** — solves step-by-step and verifies with a calculator (SymPy)

## Quick start (single file)

```bash
cd taurus-ai
pip install -r requirements.txt
cp .env.example .env
# Put your free Groq key in .env
python taurus_ai.py
```

Try:
- `Research agentic AI and summarize with sources`
- `Write Python code to find fibonacci numbers`
- `Solve 2x + 5 = 15 step by step`

## Modular version

```bash
python -m app.main
```

Structure:
```
taurus-ai/
├── taurus_ai.py          # single-file v1 (easiest to run)
├── app/
│   ├── main.py           # CLI for modular version
│   ├── router.py         # Boss router
│   ├── memory.py         # Simple JSON memory
│   ├── agents/
│   │   ├── research_agent.py
│   │   ├── coding_agent.py
│   │   └── math_agent.py
│   └── tools/
│       ├── web_search.py
│       ├── calculator.py
│       └── code_executor.py
├── requirements.txt
└── .env.example
```

## How it works

You ask → Router decides (research / coding / math / multi) → Specialist agent does the work with tools → Boss combines the answer.

Tools:
- Web search via DuckDuckGo (no key needed)
- Calculator via SymPy (verifies math)
- Code executor (runs Python safely and captures output)

## For professors / demo

- Show the 3 sample prompts above — they hit all 3 agents
- Show the agent steps in the terminal (Router -> Agent -> Tool -> Verify)
- Evaluation idea: test 20 math problems, 10 coding tasks, 10 research questions and record scores in your README for internships

## Notes

- This v1 uses Groq's free Llama-3.3-70b model via OpenAI-compatible API.
- Messaging agent drafts messages only — it does not auto-send WhatsApp. You copy and send after approval.
- Keep your real `.env` private. Never commit it to GitHub.
