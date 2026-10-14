# Taurus AI v2 — Full Agentic Mode (Not a Chatbot)

## What makes v2 REAL agentic?

| Feature | Chatbot (everyone else) | Taurus AI v2 |
|---|---|---|
| Goal | Answers question | Takes GOAL, makes plan |
| Planning | No | Planner breaks goal into 3-6 steps |
| Tools | None / just text | Gmail draft, Calendar event, File report, Web search, Calculator, Code runner |
| Loop | One answer | Think → Act → Observe → Critic → Retry |
| Critic | No | Critic Agent checks every step |
| Approval | No | Asks before email/calendar (human-in-the-loop) |
| Memory | No | JSON memory + history |
| Trace | No | Full trace log - professors can see thinking |

## Run v2

```bash
pip install -r requirements.txt
cp .env.example .env  # put GROQ_API_KEY
python -m app.main_v2
```

Demo goal to show professors:
```
Find 5 Agentic AI internships, draft Gmail to top one, create calendar reminder, save report
```

## Run v2 UI (for professors)

```bash
streamlit run app/streamlit_app_v2.py
```

Shows: Goal → Plan → Steps → Critic → Approval → Final + Trace

## Gmail - Real vs Demo

- **Demo mode (default):** Saves Gmail draft as file in `outputs/gmail_draft_*.txt` - safe, no OAuth needed, perfect for demo
- **Real mode:** Set `use_api=True` in gmail_tool.py + add `credentials.json` / `token.json` from Google Cloud OAuth (Gmail API scope `gmail.compose`). Then it creates a REAL draft in Gmail > Drafts.

Calendar works the same: demo saves `.ics` file you can import to Google Calendar.

## Files

- `app/planner.py` - breaks goal into steps
- `app/critic.py` - checks every output
- `app/executor.py` - full agentic loop
- `app/tools/gmail_tool.py` - Gmail draft
- `app/tools/calendar_tool.py` - Calendar event (.ics)
- `app/tools/file_tools.py` - save/read reports
- `app/main_v2.py` - CLI
- `app/streamlit_app_v2.py` - UI demo
