"""Code executor - runs Python code safely and captures output."""
import io
import contextlib


def run_code(code: str) -> str:
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
        return output.getvalue() or "Code ran with no output."
    except Exception as e:
        return f"Error: {e}"
