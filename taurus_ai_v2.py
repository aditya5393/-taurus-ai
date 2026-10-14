"""Taurus AI v2 - Full Agentic Single-File Demo (for quick testing).
For the full modular version, use: python -m app.main_v2
This file shows the full loop in one place: Plan -> Act -> Critic -> Approve -> Execute.
"""
print("Taurus AI v2 - Full Agentic Mode")
print("Use the modular version for real use: python -m app.main_v2")
print("This file is a pointer - the real v2 code lives in app/ (planner, critic, executor, tools).")
print("")
print("v2 features:")
print(" 1. Planner - breaks goal into steps")
print(" 2. Executor - Think -> Act -> Observe -> Retry loop")
print(" 3. Critic - checks every output")
print(" 4. Tools - Gmail draft (file + real API), Calendar (.ics), File reports, Web search, Calculator, Code runner")
print(" 5. Approval - asks before sensitive actions (email/calendar)")
print(" 6. Trace - full log of how it thought")
print("")
print("Run: python -m app.main_v2")
