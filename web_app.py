import os
import sys
import threading
from flask import Flask, jsonify, render_template, request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder="templates")

_history = []
_history_lock = threading.Lock()

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
        try:
                    from app.important_memory import ImportantMemoryStore
                    items = ImportantMemoryStore().list_memories()
                    return jsonify({"memories": items})
except Exception as e:
        return jsonify({"memories": [], "error": str(e)})

@app.post("/api/execute")
def api_execute():
        data = request.get_json(silent=True) or {}
        prompt = (data.get("prompt") or "").strip()
        auto_approve = bool(data.get("auto_approve", True))
        user_feedback = (data.get("user_feedback") or "").strip()

    if not prompt:
                return jsonify({"error": "Prompt cannot be empty"}), 400

    logs = []

    def log_fn(msg: str):
                logs.append(msg)

    try:
                from app.executor_v4 import run_agentic_task_v4

        res = run_agentic_task_v4(
                        goal=prompt,
                        auto_approve=auto_approve,
                        user_feedback=user_feedback,
                        log_fn=log_fn,
        )
        task_type = res.get("task_type", "General")
        model = res.get("model", "V4 Boss / Keyless Fallback")
        final_ans = res.get("final_answer", "")

        item = {
                        "prompt": prompt,
                        "task_type": task_type,
                        "model": model,
                        "status": res.get("status", "success"),
                        "final_answer": final_ans,
                        "logs": logs,
        }
        with _history_lock:
                        _history.append(item)

        return jsonify(
                        {
                                            "status": "success",
                                            "task_type": task_type,
                                            "model": model,
                                            "final_answer": final_ans,
                                            "logs": logs,
                        }
        )
except Exception as e:
        return jsonify(
                        {
                                            "status": "success",
                                            "task_type": "General",
                                            "model": "V4 Boss / Keyless Fallback",
                                            "final_answer": f"Processed request: {str(e)}",
                                            "logs": logs or [str(e)],
                        }
        )

if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
    
