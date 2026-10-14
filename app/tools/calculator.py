"""Calculator tool - verifies math with SymPy."""
import sympy as sp


def calculator(expr: str) -> str:
    try:
        expr = expr.replace("^", "**")
        if "=" in expr:
            left, right = expr.split("=", 1)
            x = sp.symbols("x")
            sol = sp.solve(sp.Eq(sp.sympify(left), sp.sympify(right)), x)
            return f"Solution: x = {sol}"
        val = sp.sympify(expr)
        return f"Result: {expr} = {float(val)}"
    except Exception as e:
        return f"Calculator error: {e}"
