"""Taurus AI - Streamlit UI for professors / demo. Run: streamlit run app/streamlit_app.py"""
import streamlit as st
from app.router import route
from app.agents.research_agent import research_agent
from app.agents.coding_agent import coding_agent
from app.agents.math_agent import math_agent

st.set_page_config(page_title="Taurus AI v1", page_icon="♉")
st.title("♉ Taurus AI v1")
st.caption("Boss Router + Research / Coding / Math Agents")

samples = [
    "Research agentic AI and summarize with sources",
    "Write Python code to find fibonacci numbers",
    "Solve 2x + 5 = 15 step by step",
]
cols = st.columns(3)
for i, s in enumerate(samples):
    if cols[i].button(s):
        st.session_state["query"] = s

query = st.text_input("Ask Taurus AI:", value=st.session_state.get("query", ""))

if st.button("Run") and query:
    agent = route(query)
    st.info(f"Router → {agent} agent")
    with st.spinner(f"{agent} agent working..."):
        if agent == "coding":
            ans = coding_agent(query)
        elif agent == "math":
            ans = math_agent(query)
        elif agent == "multi":
            ans = research_agent(query) + "\n\n--- Math part ---\n" + math_agent(query)
        else:
            ans = research_agent(query)
    st.markdown("### Answer")
    st.markdown(ans)
    st.code(ans, language="text")

st.markdown("---")
st.markdown("**How it works:** You ask → Router decides → Specialist agent uses tools (web search, code executor, calculator) → Answer with steps.")
