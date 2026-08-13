from . import parser as synt
from . import differentiation as derivator

MAX_RECURSION = 20

def derivate(tree, var='x'):
    return synt.simplify_tree(derivator.derivative(tree, var))

# this wasnt necessary, but when i pictured "simp of u"  simp(u)
# i laughed... so i had to do it
# it made testing and debugging subjectively better
def simp(tree):
    return synt.simplify_tree(tree)

def _integrate(tree, var="x",recursion=1):
    recursion +=1
    if recursion > MAX_RECURSION:
        raise Exception("Max recursion reached")
    tree = simp(tree)

    t = tree[0]

    # CONSTANT
    if t == "num":
        return ("op","*", tree, ("var", var))

    # VARIABLE, this was also a quick fix for typo errors
    if t == "var":
        if tree[1] == var:
            return ("op","/", ("op","^",("var",var),("num",2)), ("num",2))
        return ("op","*", tree, ("var", var))

    # FUNCTION
    if t == "func":
        name, u = tree[1], tree[2]
        d_u = simp(derivate(u, var))
        outer = ()
        # Trigonometrics
        match name:
            case 'sin':
                outer = ("op","*",
                        ("num", -1), ("func","cos",u)
                        )
            case 'cos':
                outer = ("func", "sin", u)
            case 'tan':
                cosu = ("func", "cos", u)
                ln_of_cos = ("func", "ln", cosu)
                outer = ("op","*",
                        ("num", -1), ln_of_cos)
            case 'cot':
                sinu = ("func", "sin", u)
                absin = ("func", "abs", sinu)
                ln_of_sin = ("func", "ln", absin)
                outer = ln_of_sin
            case 'sec':
                secu = ("func", "sec", u)
                tanu = ("func", "tan", u)
                outer = ("func", "ln", ("func", "abs", ("op", "+", secu, tanu)))
            case 'csc':
                cotu = ("func", "cot", u)
                minus_csc = ("op","*",
                        ("num", -1), tree)
                outer = ("op","*",
                         minus_csc, cotu)
            case 'exp':
                outer = tree
            case 'ln':
                ln_minus_one = ("op", "-",
                                tree, ("num", "1"))
                return ("op", "*",
                            ("var", "x"), ln_minus_one)
            case _:
                raise Exception(f"Integration of '{name}' not implemented.")


        return ('op', '/',
                outer, d_u
                )

    # OPERATORS
    if t == "op":
        op = tree[1]
        a = tree[2]
        b = tree[3]

        # sum rule
        if op == "+":
            return ("op","+",
                    _integrate(a, var,recursion),
                    _integrate(b, var,recursion)
            )

        if op == "-":
            return ("op","-",
                    _integrate(a, var,recursion),
                    _integrate(b, var,recursion)
            )

        # product rule -> integration by parts: ∫ u dv = uv - ∫ v du
        if op =='*':
            if synt.is_num(a):
                return simp(
                    ("op", "*", a, _integrate(b, var, recursion))
                )

            if synt.is_num(b):
                return simp(
                    ("op", "*", b, _integrate(a, var, recursion))
                )
            # print("using integration by parts")
            try:

                u = a
                du = simp(derivate(u, var))
                dv = b
                v = _integrate(dv, var, recursion)

                return ("op", "-",
                     ("op","*",u,v),
                     _integrate(("op", "*", v, du), var,recursion)

                )
            except Exception as e:
                if recursion <2:
                    try:
                        u = b
                        du = simp(derivate(u, var))
                        dv = a
                        v = _integrate(dv, var, recursion)
                        return ("op", "-",
                                ("op", "*", u, v),
                                _integrate(("op", "*", v, du), var,recursion)

                                )
                    except Exception as e:
                        return ("var", "max recursion")


        # division : substitution if numerator matches derivative of denominator
        if op == '/':
            top, bottom = a, b

            if derivate(bottom,var) == top:
                return ("func","ln",bottom)
            return ("op","/",
                    _integrate(top, var, recursion), bottom)

        # powers: x^n
        if op == "^":
            base, exp = a, b
            if synt.is_var(base) and synt.is_num(exp):
                n = exp[1]
                return ("op","/",
                        ("op","^",
                         base,("num",n+1)),
                         ("num",n+1))

            if synt.is_num(base) and synt.is_var(exp):
                return ("op","/",
                        tree, ("func", "ln", base))

            #try sustitution u^n
            if synt.is_num(exp):
                n = exp[1]
                du = derivate(base,var)
                n_plus_1 = ("num", n + 1)
                divisor = simp(("op","*",
                           n_plus_1, du))
                return ("op", "/",
                        ("op", "^",
                         base, ("num", n + 1)),
                        divisor
                        )

    raise Exception(f"Cannot integrate:  {synt.turn_to_string(tree)}")

def integrate(tree):
    try:
        integral=_integrate(tree, "x")
        simp_integral = simp(integral)
        string_result = synt.turn_to_string(simp_integral) + ' + c'
        string_result = string_result.replace('1*', '')
    except Exception:
        string_result = "not implemented solution"
        simp_integral = tree
    finally:
        pass
    return {
        "integral": string_result,
        "symbolic_tree": simp_integral

    }


def parse_and_integrate(expr):
    tokens = synt.tokenize(expr)
    tree = synt.TreeParser(tokens).parse()
    simplified = simp(tree)
    integral = _integrate(simplified, "x")
    simp_integral = simp(integral)
    # print(integral)
    # print(simp_integral)
    # print(synt.turn_to_string( simp_integral))

    string_result = synt.turn_to_string(simp_integral) + ' + c'
    string_result = string_result.replace('1*','')
    return {
        "integral": string_result,
        "integral_tree": integral

    }

if __name__ == "__main__":
    fx= "x*cos(2*x)"

    # fx= "cos((2*x))"
    dict = parse_and_integrate(fx)

    print ("\n")
    print (dict["integral"])
    # print (dict)
    # lower = synt.evaluate(dict.get("integral"),2)
    # upper = synt.evaluate(dict.get("integral"),4)
    # print (upper)
    # print (lower)