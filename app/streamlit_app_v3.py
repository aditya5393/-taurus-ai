"""Taurus AI v3 - Autonomous Model Routing Streamlit Demo.
Run: streamlit run app/streamlit_app_v3.py
User just gives prompt -> Router LLM understands task -> picks specialized model -> runs agent -> critic -> result
"""
import streamlit as st
from app.executor_v3 import run_agentic_task_v3

st.set_page_config(page_title="Taurus AI v3 - Autonomous Routing", page_icon="♉")
st.title("♉ Taurus AI v3 — Autonomous Model Routing")
st.caption("Just give a prompt. The model itself understands the task and activates the right specialized LLM.")

st.markdown("**Try (click to fill):**")
examples = [
    "Solve 2x + 5 = 15 step by step",
    "Write Python code to find prime numbers",
    "Research agentic AI and draft Gmail to professor about internship",
    "Find 5 AI internships, draft Gmail to top one, create calendar reminder, save report",
]
cols = st.columns(2)
for i, ex in enumerate(examples):
    if cols[i % 2].button(ex, key=f"v3ex{i}"):
        st.session_state["v3goal"] = ex

goal = st.text_area("🎯 Your Prompt:", value=st.session_state.get("v3goal", ""), height=90)
auto = st.checkbox("Auto-approve sensitive actions (demo uses file drafts, not real send)", value=True)

if st.button("▶️ Run Taurus v3") and goal:
    with st.spinner("Router LLM is understanding your task and choosing the right model..."):
        result = run_agentic_task_v3(goal, auto_approve=auto, log_fn=lambda x: None)
    d = result["decision"]
    st.success(f"🧠 Router chose: **{d['task_type']}** → **{d['model']}** ({d['model_label']})")
    st.info(f"Why: {d['reason']} | Confidence: {d['confidence']:.2f}")

    st.subheader("📋 Plan")
    for s in result["plan"]:
        st.markdown(f"- **Step {s['step']}** [{s['agent']}] {s['action']}")

    st.subheader("✅ Final Result")
    st.markdown(result["final"])

    with st.expander("🔍 See Full Trace (which model, why, critic, approval)"):
        for t in result["trace"]:
            st.text(t)

st.markdown("---")
st.markdown("**v3 Autonomous Routing:** Prompt → Router LLM understands → Picks specialized model (Math / Coding / Research) → Agent + Tools + Critic → Result")
