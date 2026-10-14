"""Point 6 - Multimodal / RAG: Personal Knowledge Base.
Upload your notes (txt/md/pdf text) -> Taurus answers FROM YOUR NOTES using retrieval.
This makes Taurus more than a text chatbot. Uses simple keyword retrieval (explainable).
Upgrade later to ChromaDB + embeddings for true vector RAG.
"""
import os
import re

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
os.makedirs(KB_DIR, exist_ok=True)


def add_note(filename: str, content: str) -> str:
    path = os.path.join(KB_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"✅ Note saved: {path}"


def list_notes() -> list:
    return os.listdir(KB_DIR) if os.path.exists(KB_DIR) else []


def answer_from_notes(query: str, llm_fn) -> str:
    """Retrieve relevant notes, then ask LLM to answer ONLY from those notes (RAG)."""
    files = list_notes()
    if not files:
        return "No notes in Knowledge Base yet. Upload your notes first (knowledge_base/ folder)."
    words = [w.lower() for w in query.split() if len(w) > 3]
    scored = []
    for fn in files:
        with open(os.path.join(KB_DIR, fn), encoding="utf-8") as f:
            text = f.read()
        score = sum(1 for w in words if w in text.lower())
        if score > 0:
            scored.append((score, fn, text[:2000]))
    scored.sort(reverse=True)
    if not scored:
        return "No relevant notes found for this query."
    context = "\n\n".join([f"[{fn}]: {t}" for _, fn, t in scored[:3]])
    return llm_fn(
        "You are Taurus RAG agent. Answer ONLY from the provided notes. If answer not in notes, say 'Not in your notes'. Cite which note you used.",
        f"Question: {query}\n\nYour Notes:\n{context}",
    )


def extract_text_from_pdf_hint() -> str:
    return "For PDF: pip install PyPDF2, then use PyPDF2.PdfReader to extract text and save via add_note(). For images: use pytesseract OCR, then add_note(). See README_AWARD.md for setup."
