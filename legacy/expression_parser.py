OPERATORS = ['+','-','*','/','^']
def _get_before_char(string, char):
    index = string.find(char)
    if index == -1:
        return string  # character not found
    return string[:index]

def get_outer_expression(expr):
    cont_left = expr.count('(')
    cont_right = expr.count(')')

    if cont_left >0 and cont_left == cont_right:
        return _get_before_char(expr, '(')
    else:
        # print("Problem getting outer expr")
        return None

def parse_complex_expression(expr):
    cont_left = expr.count('(')
    cont_right = expr.count(')')

    if cont_left > 0 and cont_left == cont_right:
        inner_expr = expr[:expr.find('(')]
        outer_expr = expr[expr.find('('):]
        outer_expr = remove_outer_parenthesis(outer_expr)
        return outer_expr,inner_expr
    else:
        # print("Problem getting outer expr")
        return None,None

def get_inner_expression(expr):
    # This may overlap with "handling parenthesis recursively"
    # but is still a simple solution for the intended purpose
    index = expr.find('(')
    return expr[index + 1:-1]

def split_expression_into_pair(expr):
    depth = 0
    operator = None
    operator_index = 1
    for index, char in enumerate(expr):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif depth == 0 and char in OPERATORS:
            operator = char
            operator_index = index
            break
    if operator:
        head_expr= expr[:operator_index]
        tail_expr= expr[operator_index+1:]
    else:
        head_expr= expr
        tail_expr= None
    return head_expr,tail_expr,operator

def split_by_operator(expr, operator):
    depth = 0
    operator = None
    operator_index = 1
    for index, char in enumerate(expr):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif depth == 0 and char in OPERATORS:
            operator = char
            operator_index = index
            break

def simplify_multipliers(expr, var):
    depth = 0
    operator = None
    operator_index = 1
    for index, char in enumerate(expr):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1

def remove_outer_parenthesis(expr):
    if expr[0] !='(':
        return expr
    cont_left = expr.count('(')
    cont_right = expr.count(')')
    if cont_left > 0 :
        valid_parenthesis = cont_left == cont_right
        if valid_parenthesis:
            return remove_outer_parenthesis(expr[1:-1])
        else:
            return None


def simplify_signs(expr):
    expr = expr.replace('+-', '-')
    expr = expr.replace('--', '+')
    expr = expr.replace('(+', '(')
    expr = expr.replace('*1', '')
    expr = expr.replace('1*', '')
    expr = expr.replace('^1', '')
    return expr

# Split expression
# if __name__ == "__main__":
#     func = input("Enter a function to evaluate: ")
#     print("\nParts:")
#     head,tail,operator = split_new(func)
#     print(f"head: {head}, tail: {tail}, op: {operator}")

# Remove outer parenthesis
# if __name__ == "__main__":
#     func = input("Enter a function to evaluate: ")
#     print(f"\nNew expression: {remove_outer_parenthesis(func)}")
