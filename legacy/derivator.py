# I tried to write my own version of regular expresions
# figured out a much simpler solution later on
# given the usage is specific to a few cases
import expression_parser as parsero
import rules_trigonometric as trigo

def derive(expr, var):
    expr = expr.replace(' ', '')
    print(f"exp: {expr}")
    new_expr = _derive(expr.lower(), var)
    if new_expr:
        return parsero.simplify_signs(new_expr)
    else: return "Send help....Help!"

def _derive(expr, var):
    # Handle parentheses recursively
    if expr.startswith('(') and expr.endswith(')'):
        return _derive(expr[1:-1], var)
#---------- Basic rules
    # Variable rule
    if expr == var:
        return '1'
    # Constant rule:
    if expr.isnumeric() or expr.isdecimal():
        return '0'

    # split expression to simplify it until book rules can be applied
    head, tail, operator= parsero.split_expression_into_pair(expr)
    if operator:
        if operator=='+' or operator=='-':
            return parsero.simplify_signs(
                f"{_derive(head,var)}{operator}{_derive(tail,var)}")
        if operator == '*':
            return(parsero.simplify_signs(
                _apply_rule_product(head,tail,var))
            )
        if operator == '/':
            return(parsero.simplify_signs(
                _apply_rule_division(head,tail,var))
            )
        if operator == '^':
            return (parsero.simplify_signs(
                _apply_rule_power(head,tail,var)
            ))
    #----------Trigonometric and logarithmic--------------------------
    outer_expr, inner_expr = parsero.parse_complex_expression(expr)
    # Unknown method
    if outer_expr == None and inner_expr == None:
        return (f"Unknown method to process d({expr})/d{var} \n"
                f"Try with another equation")
    # logarithmic rule
    if outer_expr == "ln":
        inner_der = _derive(parsero.get_inner_expression(expr), var)
        return f"({inner_der})/({inner_expr})"

    # trigonometric rules
    outer_der = trigo.trigonometric_derivatives(outer_expr, inner_expr)
    inner_der = _derive(parsero.get_inner_expression(expr), var)
    return f"({outer_der})*({inner_der})"


def _apply_rule_power(base, exponent, var):
    if base == var and exponent.isdigit():
        n = int(exponent)
        return f"{n}*{var}^{n - 1}"
    else:
        if base == 'e':
            return f"({base}^{exponent})*({_derive(exponent, var)})"
        else:
            # chain
            der_base = _derive(base, var)
            der_exp = _derive(exponent, var)

            return (f'({exponent})*({base})^({exponent}-1)*({der_base}) + '
                    f'({base})^({exponent})*ln({base})*({der_exp})')


def _apply_rule_product(head,tail, var):
    deriv_head = _derive(head, var)
    deriv_tail = _derive(tail, var)
    result = ''
    if deriv_tail != '0':
        result += _simplify_multiplication(f"{head}*{deriv_tail}", var)
    if deriv_head != '0':
        result += _simplify_multiplication(f"{tail}*{deriv_head}", var)
    return result

def _apply_rule_division(top,bottom, var): #aka quotient
    new_expression = ""
    new_expression += f"({bottom}*{_derive(top, var)}"
    new_expression += f"-{top}*{_derive(bottom, var)})"
    new_expression += f"/({bottom})^2"
    return new_expression

def _simplify_multiplication(expr, var):
    parts = parsero.split_expression_into_pair(expr, '*')
    parts = [p.replace('*','') for p in parts]
    c=1
    exponent = 0
    for p in parts:
        if p.isdigit():
            c *= int(p)
        elif p == var:
            exponent += 1
        elif '^' in p:
            base, power = parsero.split_expression_into_pair(p, '^')
            power = int(power.replace('^', ''))
            if power != 0:
                exponent += power

    new_expr = ""
    if c != 0: new_expr += f'{c}'
    else:  return '0'
    if exponent == 1: new_expr += var
    elif exponent != 0: new_expr += f"{var}^{exponent}"
    return new_expr

if __name__ == "__main__":
    # expresion = "3*x-3*x^3"
    # expresion = "x^3"
    expresion = "4^y"
    # print (expresion)
    # x=_simplify_multiplication(expresion, 'x')
    # x =_apply_rule_power("x^4",'x')
    x = derive(expresion, 'y')
    print(f"from expresion {expresion}, result: {x}")
