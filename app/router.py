"""Boss Router - decides which agent should handle a query."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = "llama-3.3-70b-versatile"


def route(query: str) -> str:
    q = query.lower()
    if any(w in q for w in ["code", "python", "bug", "function", "program"]):
        return "coding"
    if any(w in q for w in ["solve", "math", "equation", "calculate", "integral", "derivative"]):
        return "math"
    if any(w in q for w in ["research", "search", "summarize", "draft", "message", "email"]):
        return "research"
    try:
        res = _client.chat.completions.create(
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
    res = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    return res.choices[0].message.content
