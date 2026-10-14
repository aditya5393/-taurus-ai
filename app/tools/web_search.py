"""Web search tool - DuckDuckGo, no API key needed."""
import requests


def web_search(query: str) -> str:
    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1},
            timeout=10,
        )
        data = r.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        topics = data.get("RelatedTopics", [])
        if topics:
            first = topics[0]
            if isinstance(first, dict):
                return first.get("Text", "No result found")
        return "No result found"
    except Exception as e:
        return f"Search failed: {e}"
