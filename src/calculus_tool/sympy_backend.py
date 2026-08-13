from sympy import Integral, integrate, symbols, sympify

def calculate_integral(expr_str: str, lower_limit = 0, upper_limit= 1.0, var='x'):
    # Return the symbolic integral expression and its evaluated result.

    try:
        x = symbols(var)
        expr = sympify(expr_str)
        symbolic_result = integrate(expr, x)
        numeric_result = Integral(expr, (x, lower_limit, upper_limit))
        return [f"Symbolic_result: {symbolic_result}", f"numeric result: {numeric_result.evalf()}"]
    except Exception as e:
        return f"Rewrite {expr_str}. Exception: {e}"
