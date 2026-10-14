"""Taurus AI v4 - Self-Learning + Important Memory Streamlit Demo.
Run: streamlit run app/streamlit_app_v4.py
Shows: Memory recalled -> Router -> Plan -> Result -> What Taurus Learned -> Memory panel
"""
import streamlit as st
from app.executor_v4 import run_agentic_task_v4
from app.important_memory import list_important, list_lessons, save_important

st.set_page_config(page_title="Taurus AI v4 - Self-Learning", page_icon="♉")
st.title("♉ Taurus AI v4 — Self-Learning + Memory")
st.caption("Taurus learns from every task and remembers important data. Try it, correct it, watch it improve.")

with st.sidebar:
    st.subheader("🧠 Important Memory")
    for it in list_important()[-10:]:
        st.markdown(f"- **{it['category']}** (imp {it['importance']}): {it['text']}")
    st.subheader("📚 Lessons Learned")
    for ls in list_lessons()[-10:]:
        st.markdown(f"- [{ls['applies_to']}] {ls['lesson']}")
    st.markdown("---")
    st.markdown("**Remember this:**")
    fact = st.text_input("Save important fact (e.g. Aditya prefers short answers)")
    if st.button("💾 Save as Important") and fact:
        save_important(fact, category="user", importance=10, source="sidebar")
        st.success("Saved! It will be recalled next time.")
        st.rerun()

st.markdown("**Try:**")
examples = [
    "Solve 2x + 5 = 15 step by step",
    "Write Python code to find prime numbers",
    "remember this: Aditya prefers short Python answers with comments",
    "Research agentic AI and draft Gmail to professor",
]
cols = st.columns(2)
for i, ex in enumerate(examples):
    if cols[i % 2].button(ex, key=f"v4ex{i}"):
        st.session_state["v4goal"] = ex

goal = st.text_area("🎯 Your Prompt:", value=st.session_state.get("v4goal", ""), height=90)
feedback = st.text_input("Feedback / correction on last answer? (optional, helps Taurus learn)")
if st.button("▶️ Run Taurus v4") and goal:
    with st.spinner("Recalling memory → Routing → Acting → Learning..."):
        result = run_agentic_task_v4(goal, auto_approve=True, user_feedback=feedback, log_fn=lambda x: None)
    d = result["decision"]
    st.success(f"🧠 Router chose: **{d.get('task_type')}** → **{d.get('model')}**")
    st.info(f"**Memory used:**\n{result.get('memory_context','')[:800]}")
    st.subheader("✅ Final Result")
    st.markdown(result["final"])
    learned = result.get("learned", {})
    if learned:
        st.subheader("📚 What Taurus Learned This Time")
        for ls in learned.get("lessons", []):
            st.markdown(f"- {ls['lesson']}")
        for imp in learned.get("important_saved", []):
            st.markdown(f"- 💾 Saved important: {imp['text']}")
    with st.expander("🔍 Full Trace"):
        for t in result["trace"]:
            st.text(t)

st.markdown("---")
st.markdown("**v4 Self-Learning Loop:** Recall Memory → Route → Act → Critic → Reflect → Save Lesson → Next task gets better")
