TRIGO_DERIV = {
    "sin": "cos(x)",
    "cos": "-sin(x)",
    "tan": "sec^2(x)",
    "csc": "-csc(x)*cot(x)",
    "sec": "sec(x)*tan(x)",
    "cot": "-(csc^2(x))"
}
TRIGO_H_DERIV = {
    "sinh": "cosh(x)",
    "cosh": "sinh(x)",
    "tanh": "sech^2(x)",
    "csch": "-csch(x)*coth(x)",
    "sech": "-sech(x)*tanh(x)",
    "coth": "-(csch(x))"
}
TRIGO_INTEGRAL = {
    "sin": "-cos(x)",
    "cos": "sin(x)",
    "tan": "-ln(cos(x))",
    "sec": "sec(x)*sin(x)",
    "csc": "-csc(x)*cot(x)",
    "cot": "ln|sin(x)|"
}

def trigonometric_derivatives(outer_expr, inner_expr):
    if outer_expr in TRIGO_DERIV:
        return  TRIGO_DERIV.get(outer_expr).replace('x',inner_expr)
    elif outer_expr in TRIGO_H_DERIV:
        return TRIGO_H_DERIV.get(outer_expr).replace('x', inner_expr)
    else:
        print("Expression in trigo not found")
        return None

def trigonometric_integrals(outer_expr, inner_expr):
    if outer_expr in TRIGO_DERIV:
        return  TRIGO_DERIV.get(outer_expr).replace('x',inner_expr)
    else:
        print("Expression in trigo not found")
        return None