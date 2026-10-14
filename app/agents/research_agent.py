"""Research + Messaging Agent - searches web, summarizes, drafts messages.
v3: uses specialized Research LLM (llama-3.3-70b) via autonomous routing."""
from app.models import ask_for_task
from app.tools.web_search import web_search


def research_agent(query: str) -> str:
    print("[Research Agent] Searching... (Research LLM)")
    context = web_search(query)
    return ask_for_task("research",
        "You are a research agent. Summarize with sources and clear bullet points. "
        "If the user asks to draft a message/email, draft it and ask for approval before sending.",
        f"Query: {query}\nSearch result: {context}",
    )
