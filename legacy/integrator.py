import re
import expression_parser as emt

INTEGRAL_SIGN = '∫'

def integrate(expr, var ='x'):
    expr = expr.replace(' ', '')
    return emt.simplify_signs(_integrate(expr)) + " + C"

# ------------ CORE INTEGRATOR ------------
def _integrate(expr, var='x'):
    # Parentheses wrapper
    if expr.startswith('(') and expr.endswith(')'):
        return _integrate(expr[1:-1])

    # SUM RULE ------------------------------------------------------------
    parts = _split(expr, '+-')
    if len(parts) > 1:
        acc = ''
        for p in parts:
            sign = '+' if not p.startswith('-') else '-'
            term = p.lstrip('+-')
            acc += f'{sign}({_integrate(term)})'
        return acc

    # PRODUCT RULE (constant × function) ------------------------------------
    parts = _split(expr, '*')
    if len(parts) > 1:
        for i, p in enumerate(parts):
            if _is_num(p):
                const = p
                rest = '*'.join(parts[:i] + parts[i + 1:])
                return f'{const}*({_integrate(rest)})'
        return f'∫({expr})d{var}'  # unsupported general product

    # POWER RULE ------------------------------------------------------------
    parts = _split(expr, '^')
    if len(parts) > 1:
        base, exp = parts
        if base == var and _is_num(exp):
            n = float(exp)
            if n == -1:
                return f'ln|{var}|'
            else:
                return f'{var}^{n + 1}/({n + 1})'
        return f'∫({expr})d{var}'

    # TRIG FUNCTIONS --------------------------------------------------------
    t = _match_trig(expr)
    if t:
        func, inner = t
        d_inner = _derive_simple(inner)

        # If reverse chain rule fails → leave symbolic
        if d_inner == "?":
            return f'∫({expr})d{var}'

        # Compute outer integral * chain rule factor
        if func == "sin":
            return f'-cos({inner})/({d_inner})'
        if func == "cos":
            return f'sin({inner})/({d_inner})'
        if func == "tan":
            return f'-ln|cos({inner})|/({d_inner})'
        if func == "sec":
            return f'sec({inner})*sin({inner})/({d_inner})'
        if func == "csc":
            return f'-csc({inner})*cot({inner})/({d_inner})'
        if func == "cot":
            return f'ln|sin({inner})|/({d_inner})'

    # SPECIAL TRIG STRUCTURES ----------------------------------------------
    if expr.startswith("sec(") and expr.replace(" ", "").endswith(")*tan(" + expr[4:]):
        return f'sec({expr[4:-1]})'

    # EXPONENTIAL -----------------------------------------------------------
    if expr.startswith("exp(") and expr.endswith(")"):
        inner = expr[4:-1]
        d_inner = _derive_simple(inner)
        if d_inner != "?":
            return f'exp({inner})/({d_inner})'

    # NATURAL LOG -----------------------------------------------------------
    if expr == f"ln({var})" or expr == f"log({var})":
        return f'{var}*ln({var}) - {var}'

    # VARIABLE --------------------------------------------------------------
    if expr == var:
        return f'{var}^2/2'

    # CONSTANT --------------------------------------------------------------
    if _is_num(expr):
        return f'{expr}*{var}'

    # DEFAULT / UNSUPPORTED -------------------------------------------------
    return f'∫({expr})d{var}'


# ------------ SUPPORT UTILITIES ------------

def _match_trig( expr):
    m = re.match(r'(sin|cos|tan|sec|csc|cot)\((.+)\)', expr)
    if m:
        return m.group(1), m.group(2)
    return None


def _is_num( s):
    return re.fullmatch(r'-?\d+(\.\d+)?', s) is not None


def _split( expr, ops):
    parts, depth, current = [], 0, ''
    for c in expr:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c in ops and depth == 0:
            parts.append(current)
            current = c
            continue
        current += c
    parts.append(current)
    return [p for p in parts if p]


# Very simple derivative used for reverse chain rule
def _derive_simple(expr, var='x'):
    expr = expr.strip()
    if expr == var:
        return "1"
    if _is_num(expr):
        return "0"
    # constant * x
    if "*" in expr:
        parts = expr.split("*")
        nums = [p for p in parts if _is_num(p)]
        vars = [p for p in parts if p == var]
        if len(vars) == 1 and len(nums) == 1:
            return nums[0]
    return "?"  # unsupported inner


# ------------------------- TESTER -------------------------
if __name__ == "__main__":
    func = input("Enter a function to integrate: ")
    print("\nIntegral:")
    print(integrate(func))
