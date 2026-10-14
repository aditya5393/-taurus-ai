"""Boss Router - decides which agent should handle a query."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_client = None
MODEL = "llama-3.3-70b-versatile"


def _get_client():
    global _client
    if _client is not None:
        return _client
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            import streamlit as st
            if "GROQ_API_KEY" in st.secrets:
                key = str(st.secrets["GROQ_API_KEY"])
                os.environ["GROQ_API_KEY"] = key
        except Exception:
            pass
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. On Streamlit Cloud: Manage app > Settings > Secrets > "
            'add GROQ_API_KEY = "gsk_..." then Reboot. Locally: put it in .env'
        )
    _client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
    return _client


def route(query: str) -> str:
    q = query.lower()
    if any(w in q for w in ["code", "python", "bug", "function", "program"]):
        return "coding"
    if any(w in q for w in ["solve", "math", "equation", "calculate", "integral", "derivative"]):
        return "math"
    if any(w in q for w in ["research", "search", "summarize", "draft", "message", "email"]):
        return "research"
    try:
        client = _get_client()
        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a router. Reply with only one word: research, coding, math, or multi."},
                {"role": "user", "content": f"Route this: {query}"},
            ],
            temperature=0.3,
        )
        return res.choices[0].message.content.strip().lower()
    except Exception:
        return "research"


def ask_llm(system: str, user: str) -> str:
    client = _get_client()
    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    return res.choices[0].message.content
