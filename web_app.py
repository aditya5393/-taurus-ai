"""Taurus AI — Real deployable web app (Flask) serving the EXACT decided UI.

Frontend: templates/index.html — the decided artifact UI preserved verbatim
(black-and-gold premium identity, real bull calm/angry images, "Ask anything
and do anything", chat history + task history, Demo / Memory / Proof / System tabs).
Only the simulated JS chat was replaced with real fetch POST /api/chat calls.

Backend: app/executor_v4.py run_agentic_task_v4 (Recall -> Route -> Act -> Verify -> Learn).
GROQ_API_KEY comes from the environment (Render dashboard -> Environment).
The app never crashes on a missing key: /api/chat returns a clear JSON error.

Run locally:
    GROQ_API_KEY=... python web_app.py
    # or: gunicorn web_app:app -b 0.0.0.0:$PORT

Render: see render.yaml / Dockerfile.web (start: gunicorn web_app:app).
"""
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="templates")

# Server-side task history (the UI also keeps session history client-side).
_history_lock = threading.Lock()
_history = []  # list of {prompt, task_type, model, status}


def _groq_configured() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))


@app.get("/health")
def health():
    return jsonify({"status": "ok", "groq_configured": _groq_configured()})


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/history")
def api_history():
    with _history_lock:
        items = list(reversed(_history[-50:]))
    return jsonify({"history": items})


@app.get("/api/memory")
def api_memory():
    """Real approved memory + lessons for the Memory view. Never crashes the UI."""
    try:
        from app.important_memory import list_important, list_lessons

        return jsonify(
            {"important": list_important()[-20:], "lessons": list_lessons()[-20:]}
        )
    except Exception as e:  # pragma: no cover - defensive
        return jsonify({"important": [], "lessons": [], "error": str(e)})


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "") or "").strip()
    feedback = str(data.get("feedback", "") or "").strip()
    if not prompt:
        return jsonify({"error": "Prompt is empty. Write a task first."}), 400
    if not _groq_configured():
        return (
            jsonify(
                {
                    "error": (
                        "GROQ_API_KEY is not set on the server. "
                        "On Render: Dashboard > your service > Environment > add "
                        "GROQ_API_KEY (free key from console.groq.com) > save, then redeploy. "
                        "Locally: set GROQ_API_KEY in your environment and restart."
                    )
                }
            ),
            503,
        )
    # Import here (lazy) so a missing key / import problem becomes a JSON error,
    # never a crashed process. models.py already lazy-loads the Groq client.
    try:
        from app.executor_v4 import run_agentic_task_v4
    except Exception as e:
        return jsonify({"error": f"Backend failed to load: {e}"}), 500

    with _history_lock:
        _history.append(
            {"prompt": prompt[:200], "task_type": "…", "model": "…", "status": "RUNNING"}
        )
    try:
        result = run_agentic_task_v4(
            prompt, auto_approve=True, user_feedback=feedback, log_fn=lambda x: None
        )
    except Exception as e:
        with _history_lock:
            if _history:
                _history[-1]["status"] = "FAILED"
        return jsonify({"error": f"Taurus hit an error: {e}"}), 500

    decision = result.get("decision", {}) or {}
    with _history_lock:
        if _history:
            _history[-1].update(
                {
                    "task_type": decision.get("task_type", "?"),
                    "model": decision.get("model", "?"),
                    "status": "DONE",
                }
            )
    return jsonify(
        {
            "final": result.get("final", ""),
            "decision": decision,
            "memory_context": result.get("memory_context", ""),
            "learned": result.get("learned", {}),
            "trace": result.get("trace", []),
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
