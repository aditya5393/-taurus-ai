"""Taurus AI v2 - Full Agentic Streamlit Demo for Professors.
Run: streamlit run app/streamlit_app_v2.py
Shows: Goal -> Plan -> Steps -> Critic -> Approval -> Final + Trace
"""
import streamlit as st
from app.executor import run_agentic_task

st.set_page_config(page_title="Taurus AI v2 - Full Agentic", page_icon="♉")
st.title("♉ Taurus AI v2 — Full Agentic Mode")
st.caption("Give a GOAL. Taurus plans, acts with tools, checks with Critic, asks approval, and automates.")

st.markdown("**Try one goal (click to fill):**")
examples = [
    "Find 5 Agentic AI internships, draft Gmail to top one, create calendar reminder, save report",
    "Research LangGraph, write Python code demo, solve a math problem from it, save report",
]
cols = st.columns(2)
for i, ex in enumerate(examples):
    if cols[i].button(ex, key=f"ex{i}"):
        st.session_state["goal"] = ex

goal = st.text_area("🎯 Your Goal:", value=st.session_state.get("goal", ""), height=80)
auto = st.checkbox("Auto-approve sensitive actions (demo mode uses file drafts, not real send)", value=True)

if st.button("▶️ Run Agentic Task") and goal:
    logs = []
    def log_fn(msg):
        logs.append(msg)
    with st.spinner("Taurus is planning + acting + checking..."):
        result = run_agentic_task(goal, auto_approve=auto, log_fn=lambda x: None)

    st.subheader("📋 Plan")
    for s in result["plan"]:
        st.markdown(f"- **Step {s['step']}** [{s['agent']}] {s['action']} — approval: {s.get('needs_approval', False)}")

    st.subheader("✅ Final Result")
    st.markdown(result["final"])

    with st.expander("🔍 See Full Trace (how Taurus thought)"):
        for t in result["trace"]:
            st.text(t)

    st.success("Done! Check outputs/ folder for Gmail draft file, calendar .ics, and report.")

st.markdown("---")
st.markdown("**Agentic features in v2:** Planner • Think-Act-Observe-Retry • Critic • Human approval • Gmail/Calendar/File tools • Memory • Full trace")
