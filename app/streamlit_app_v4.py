"""Taurus AI v4 - Premium Black-and-Gold ChatGPT-style UI + Real Agentic Backend.
Run: streamlit run app/streamlit_app_v4.py
Chat-first: "Ask anything and do anything" + Bull calm/angry states + Chat History + Task History + Memory
Backend: executor_v4 (Recall Memory -> Route -> Act -> Critic -> Reflect -> Save Lesson)
"""
import os
import datetime
import streamlit as st

# Load GROQ_API_KEY from Streamlit Secrets into env BEFORE importing executor
try:
    if "GROQ_API_KEY" in st.secrets and st.secrets["GROQ_API_KEY"]:
        os.environ["GROQ_API_KEY"] = str(st.secrets["GROQ_API_KEY"])
except Exception:
    pass

from app.executor_v4 import run_agentic_task_v4
from app.important_memory import list_important, list_lessons, save_important

st.set_page_config(
    page_title="Taurus AI — Ask anything and do anything",
    page_icon="♉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Premium Black-and-Gold CSS ---
st.markdown(
    """
<style>
/* App background */
.stApp { background-color: #0A0A0A; color: #F5F5F5; }
[data-testid="stAppViewContainer"] { background-color: #0A0A0A; }
[data-testid="stHeader"] { background-color: rgba(10,10,10,0.9); }
[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #2A2118; }
[data-testid="stSidebar"] * { color: #E8E8E8; }
h1, h2, h3, h4 { color: #F5F5F5 !important; }
p, li, span, div { color: #E8E8E8; }
a { color: #D4AF37 !important; }

/* Gold buttons */
.stButton > button {
    background-color: #111111 !important;
    color: #D4AF37 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}
.stButton > button:hover { background-color: #D4AF37 !important; color: #0A0A0A !important; }

/* Chat input */
[data-testid="stChatInput"] { background-color: #0A0A0A; }
[data-testid="stChatInput"] textarea { background-color: #1A1A1A !important; color: #FFFFFF !important; border: 1px solid #D4AF37 !important; border-radius: 16px !important; }
[data-testid="stChatInput"] button { background-color: #D4AF37 !important; color: #0A0A0A !important; }

/* Chat messages */
[data-testid="stChatMessage"] { background-color: #161616 !important; border: 1px solid #2A2118 !important; border-radius: 16px !important; margin-bottom: 12px; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { color: #F5F5F5; }

/* Text inputs / text area */
.stTextInput input, .stTextArea textarea {
    background-color: #1A1A1A !important; color: #FFFFFF !important;
    border: 1px solid #3A3A3A !important; border-radius: 12px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #D4AF37 !important; }

/* Expander */
[data-testid="stExpander"] { background-color: #141414 !important; border: 1px solid #2A2118 !important; border-radius: 12px !important; }

/* Bull states */
.bull-wrap { text-align: center; margin: 6px 0 2px 0; }
.bull-calm { font-size: 72px; line-height: 1; color: #D4AF37; text-shadow: 0 0 28px rgba(212,175,55,0.55); }
.bull-angry {
    font-size: 72px; line-height: 1; color: #FF2D2D;
    text-shadow: 0 0 32px rgba(255,45,45,0.8);
    animation: taurus-shake 0.35s infinite;
    transform: translateY(4px) scale(1.04);
}
@keyframes taurus-shake {
    0% { transform: translate(0px, 4px) rotate(0deg); }
    25% { transform: translate(-2px, 5px) rotate(-1.5deg); }
    50% { transform: translate(2px, 4px) rotate(1.5deg); }
    75% { transform: translate(-1px, 6px) rotate(-1deg); }
    100% { transform: translate(0px, 4px) rotate(0deg); }
}
.bull-label-calm { color: #D4AF37; font-weight: 700; letter-spacing: 2px; font-size: 12px; margin-top: 4px; }
.bull-label-angry { color: #FF2D2D; font-weight: 800; letter-spacing: 2px; font-size: 12px; margin-top: 4px; }
.bull-face { color: #AAAAAA; font-size: 13px; margin-top: 2px; }
.hero-title { text-align: center; font-size: 34px; font-weight: 700; color: #FFFFFF; margin: 10px 0 4px 0; }
.hero-sub { text-align: center; color: #AAAAAA; font-size: 15px; margin-bottom: 18px; }
.gold { color: #D4AF37; }
.router-badge {
    display: inline-block; background: #1A1A1A; border: 1px solid #D4AF37; color: #D4AF37;
    padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; margin: 4px 0 10px 0;
}
.task-row { background: #161616; border: 1px solid #2A2118; border-radius: 10px; padding: 8px 10px; margin-bottom: 8px; font-size: 13px; }
</style>
""",
    unsafe_allow_html=True,
)

# --- Missing key: premium error card, not a crash ---
if not os.getenv("GROQ_API_KEY"):
    st.markdown(
        """
        <div style="text-align:center; padding: 40px 20px;">
            <div style="font-size:64px;">♉</div>
            <h2 style="color:#D4AF37;">Taurus AI needs its key</h2>
            <p style="color:#CCCCCC;">GROQ_API_KEY is not set. In Streamlit Cloud: Manage app (bottom-right) &gt; Settings &gt; Secrets &gt; add one line:<br>
            <code style="color:#D4AF37;">GROQ_API_KEY = "gsk_..."</code> (free key from console.groq.com) &gt; Save &gt; Reboot.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# --- Session state: chat + task history ---
if "taurus_chats" not in st.session_state:
    st.session_state.taurus_chats = []  # list of {id, title, messages: [{role, content, meta}]}
if "taurus_current" not in st.session_state:
    st.session_state.taurus_current = None
if "taurus_tasks" not in st.session_state:
    st.session_state.taurus_tasks = []  # list of {goal, task_type, model, time}
if "taurus_bull" not in st.session_state:
    st.session_state.taurus_bull = "calm"  # calm | working
if "taurus_pending" not in st.session_state:
    st.session_state.taurus_pending = None


def _new_chat():
    chat_id = f"chat-{len(st.session_state.taurus_chats)+1}-{datetime.datetime.now().strftime('%H%M%S')}"
    st.session_state.taurus_chats.insert(0, {"id": chat_id, "title": "New chat", "messages": []})
    st.session_state.taurus_current = chat_id
    st.session_state.taurus_bull = "calm"


def _current_chat():
    cid = st.session_state.taurus_current
    for c in st.session_state.taurus_chats:
        if c["id"] == cid:
            return c
    if not st.session_state.taurus_chats:
        _new_chat()
        return st.session_state.taurus_chats[0]
    st.session_state.taurus_current = st.session_state.taurus_chats[0]["id"]
    return st.session_state.taurus_chats[0]


def _bull_header():
    if st.session_state.taurus_bull == "working":
        st.markdown(
            """
            <div class="bull-wrap">
                <div class="bull-angry">♉</div>
                <div class="bull-label-angry">⚡ CHARGING • WORKING</div>
                <div class="bull-face">Brows furrowed • Eyes narrowed • Nostrils flared • Jaw tense • Lowered, ready to charge</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="bull-wrap">
                <div class="bull-calm">♉</div>
                <div class="bull-label-calm">CALM • WATCHING</div>
                <div class="bull-face">Relaxed • Watching • Ready</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ================= SIDEBAR: History + Memory =================
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;"><div style="font-size:44px; color:#D4AF37;">♉</div>'
        '<div style="font-size:20px; font-weight:800; letter-spacing:2px;">TAURUS <span style="color:#D4AF37;">AI</span></div>'
        '<div style="color:#AAAAAA; font-size:12px;">Agentic AI • Self-Learning</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    if st.button("＋ New Chat", use_container_width=True):
        _new_chat()
        st.rerun()

    st.markdown("### 💬 Chat History")
    if not st.session_state.taurus_chats:
        st.caption("No chats yet. Ask something to start.")
    for c in st.session_state.taurus_chats[:20]:
        label = (c["title"][:42] + "…") if len(c["title"]) > 42 else c["title"]
        if st.button(label, key=f"hist-{c['id']}", use_container_width=True):
            st.session_state.taurus_current = c["id"]
            st.session_state.taurus_bull = "calm"
            st.rerun()

    st.markdown("### 📋 Task History")
    if not st.session_state.taurus_tasks:
        st.caption("No tasks yet.")
    for t in st.session_state.taurus_tasks[-10:][::-1]:
        st.markdown(
            f'<div class="task-row">✅ <b>{t["task_type"]}</b> → {t["model"]}<br>'
            f'<span style="color:#AAAAAA;">{t["goal"][:70]}</span><br>'
            f'<span style="color:#777777; font-size:11px;">{t["time"]}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### 🧠 Important Memory")
    try:
        for it in list_important()[-8:]:
            st.markdown(f"- **{it['category']}** (imp {it['importance']}): {it['text']}")
    except Exception:
        st.caption("Memory unavailable.")
    st.markdown("### 📚 Lessons Learned")
    try:
        for ls in list_lessons()[-8:]:
            st.markdown(f"- [{ls['applies_to']}] {ls['lesson']}")
    except Exception:
        st.caption("No lessons yet.")
    st.markdown("---")
    st.markdown("**Remember this:**")
    fact = st.text_input("Save important fact", placeholder="e.g. Aditya prefers short answers")
    if st.button("💾 Save as Important") and fact:
        try:
            save_important(fact, category="user", importance=10, source="sidebar")
            st.success("Saved! It will be recalled next time.")
            st.rerun()
        except Exception as e:
            st.error(f"Could not save: {e}")

# ================= MAIN =================
chat = _current_chat()
_bull_header()

# Hero when empty
if not chat["messages"]:
    st.markdown('<div class="hero-title">Ask anything and do anything</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Research • Coding • Math • Drafting • Planning — Taurus understands, plans, acts, verifies, and learns.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("**Try:**")
    examples = [
        "Solve 2x + 5 = 15 step by step",
        "Write Python code to find prime numbers",
        "Research agentic AI and draft Gmail to professor",
        "remember this: Aditya prefers short Python answers with comments",
    ]
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        if cols[i % 2].button(ex, key=f"ex{i}", use_container_width=True):
            st.session_state.taurus_pending = ex
            st.rerun()
else:
    # Render chat history
    for m in chat["messages"]:
        with st.chat_message(m["role"]):
            if m.get("meta"):
                st.markdown(f'<span class="router-badge">{m["meta"]}</span>', unsafe_allow_html=True)
            st.markdown(m["content"])
            if m.get("learned"):
                with st.expander("📚 What Taurus Learned"):
                    st.markdown(m["learned"])
            if m.get("trace"):
                with st.expander("🔍 Full Trace"):
                    for t in m["trace"]:
                        st.text(t)

# Feedback (optional, helps learning)
feedback = st.text_input(
    "Feedback / correction on last answer? (optional — helps Taurus learn)",
    placeholder="e.g. Make it shorter, add comments...",
    key="taurus_feedback",
)

# Chat input — ChatGPT-style, at bottom
prompt = st.chat_input("Ask anything and do anything")
if st.session_state.taurus_pending:
    prompt = st.session_state.taurus_pending
    st.session_state.taurus_pending = None

if prompt:
    # Title from first prompt
    if chat["title"] == "New chat":
        chat["title"] = prompt[:48]
    chat["messages"].append({"role": "user", "content": prompt})
    st.session_state.taurus_bull = "working"
    # Show user message immediately + working bull on rerun is handled by state; run now
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.status("Taurus is working: Recalling memory → Routing → Acting → Verifying → Learning…", expanded=False) as status:
            try:
                result = run_agentic_task_v4(
                    prompt, auto_approve=True, user_feedback=feedback, log_fn=lambda x: None
                )
                d = result.get("decision", {})
                meta = f"🧠 {d.get('task_type','?')} → {d.get('model','?')} • {d.get('reason','')[:90]}"
                st.markdown(f'<span class="router-badge">{meta}</span>', unsafe_allow_html=True)
                st.markdown(result.get("final", ""))
                learned_md = ""
                learned = result.get("learned", {})
                if learned:
                    parts = []
                    for ls in learned.get("lessons", []):
                        parts.append(f"- {ls['lesson']}")
                    for imp in learned.get("important_saved", []):
                        parts.append(f"- 💾 Saved important: {imp['text']}")
                    if parts:
                        learned_md = "\n".join(parts)
                        with st.expander("📚 What Taurus Learned"):
                            st.markdown(learned_md)
                trace = result.get("trace", [])
                if trace:
                    with st.expander("🔍 Full Trace"):
                        for t in trace:
                            st.text(t)
                status.update(label="Done — Taurus learned from this task.", state="complete")
                # Save to history
                chat["messages"].append(
                    {
                        "role": "assistant",
                        "content": result.get("final", ""),
                        "meta": meta,
                        "learned": learned_md,
                        "trace": trace,
                    }
                )
                st.session_state.taurus_tasks.append(
                    {
                        "goal": prompt,
                        "task_type": d.get("task_type", "?"),
                        "model": d.get("model", "?"),
                        "time": datetime.datetime.now().strftime("%d %b %H:%M"),
                    }
                )
            except Exception as e:
                status.update(label="Taurus hit an error.", state="error")
                err = f"Sorry — Taurus hit an error: {e}"
                st.error(err)
                chat["messages"].append({"role": "assistant", "content": err})
    st.session_state.taurus_bull = "calm"
    st.rerun()

st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#777777; font-size:12px;">Taurus v4 Self-Learning Loop: Recall Memory → Route → Act → Critic → Reflect → Save Lesson → Next task gets better</div>',
    unsafe_allow_html=True,
)
