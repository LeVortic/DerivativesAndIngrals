from math import sin as sine
from math import cos as cosine
from math import tan as tangent
from math import exp as expo
from math import log


OP_SYMBOLS = "+-*/^()"
#-------------------------
# TOKENIZER (supports nested functions)
# I had the idea of making the program explain the func and
#  by using the closest to natural language using the tokens
#
def tokenize(expr):
    expr = expr.replace(' ', '')
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]

        if c.isdigit():
            num = c
            i += 1
            dot_seen = (c == '.')
            while i < len(expr) and (expr[i].isdigit() or (expr[i] == '.' and not dot_seen)):
                if expr[i] == '.':
                    dot_seen = True
                num += expr[i]
                i += 1
            tokens.append(("NUMBER", num))
            # here i could check for implicit multiplication if next token begins a variable or '('
            if i < len(expr) and (expr[i].isdigit() or expr[i] == '(' or expr[i].isalpha()):
                tokens.append(("IMPLICIT_TIMES", '*'))
            continue

        if c.isalpha():
            name = c
            i += 1
            while i < len(expr) and expr[i].isalpha():
                name += expr[i]
                i += 1
            tokens.append(("FUNC", name))  # variable or function
            continue

        if c in OP_SYMBOLS:
            map = {
                '+': ('PLUS', '+'),
                '-': ('MINUS', '-'),
                '*': ('TIMES', '*'),
                '/': ('DIV', '/'),
                '^': ('POW', '^'),
                '(': ('LPAREN', '('),
                ')': ('RPAREN', ')')
            }
            tokens.append(map[c])
            i += 1
            if c == ')' and i < len(expr) and (expr[i].isalpha() or expr[i].isdigit() or expr[i] == '('):
                tokens.append(("IMPLICIT_TIMES", '*'))
            continue

        raise Exception(f"Unexpected character: {c} at pos {i}")
    tokens = [("TIMES", '*') if t[0] == 'IMPLICIT_TIMES' else t for t in tokens]
    return tokens

# Turns the tokens into a syntax tree
#
class TreeParser:
    def __init__(self, tokens):
        self.t = tokens
        self.pos = 0

    def peek(self):
        return self.t[self.pos] if self.pos < len(self.t) else ("END","")

    def check(self, kind=None):
        tok= self.peek()
        if kind is None or tok[0] == kind:
            self.pos += 1
            return tok[1]
        raise Exception(f"Expected token {kind}, got {tok}")

    def parse(self):
        node = self.expr()
        if self.peek()[0] != 'END':
            raise Exception(f"Unexpected token after expression: {self.peek()}")
        return node

    def expr(self):
        node = self.term()
        while self.peek()[0] in ("PLUS", "MINUS"):
            op = self.check(self.peek()[0])
            node = ("op", op, node, self.term())
        return node

    def term(self):
        node = self.power()
        while self.peek()[0] in ("TIMES","DIV"):
            op = self.check(self.peek()[0])
            node = ("op", op, node, self.power())
        return node

    def power(self):
        node = self.factor()
        while self.peek()[0] == "POW":
            self.check("POW")
            node = ("op", "^", node, self.factor())
        return node

    def factor(self):
        kind, val = self.peek()

        if kind == "NUMBER":
            self.check("NUMBER")
            return ("num", float(val))

        if kind == "FUNC":
            # Could be variable or function call
            name = self.check("FUNC")
            if self.peek()[0] == "LPAREN":
                self.check("LPAREN")
                arg = self.expr()
                self.check("RPAREN")
                return ("func", name, arg)
            return ("var", name)

        if kind == "LPAREN":
            self.check("LPAREN")
            node = self.expr()
            self.check("RPAREN")
            return node

        if kind == "MINUS":
            self.check("MINUS")
            return ("op", "*", ("num",-1), self.factor())

        raise Exception("Invalid syntax")

def is_num(tree):
    return tree[0] == "num"

def _is_zero(tree):
    return tree[1] == 0 or tree[1] == '0'

def is_one(tree):
    return tree[1] == 1 or tree[1] == '1'
def is_var(tree):
    return tree[0]=="var"

def is_var_mult_or_div(tree):
    if tree[1] == '*' or tree[1] == '/':
        is_ax= is_var(tree[2]) and is_num(tree[3])
        is_xa = is_var(tree[3]) and is_num(tree[2])
        return is_ax or is_xa
    else:
        return False
def simplify_tree(tree):
    t = tree[0]

    if t in ("num", "var"):
        return tree

    if t == "func":
        if tree[1] == 'x':
            return ('op', '*',
                    ('var', 'x'), simplify_tree(tree[2]))
        return ("func", tree[1], simplify_tree(tree[2]))

    if t == "op":
        op = tree[1]
        a = simplify_tree(tree[2])
        b = simplify_tree(tree[3])

        # -------- ADDITION ---------
        if op == "+":
            if _is_zero(a): return simplify_tree(b)
            if _is_zero(b): return simplify_tree(a)
            if is_num(a) and is_num(b):
                result = float(a[1]) + float(b[1])
                return ("num", result)
            return ('op', '+',
                    simplify_tree(a), simplify_tree(b))

        # -------- SUBTRACTION ---------
        if op == "-":
            if _is_zero(b): return a

            if is_num(a) and is_num(b):
                result = float(a[1]) - float(b[1])
                return ("num", result)
            return ('op', '-',
                    simplify_tree(a), simplify_tree(b))

        # -------- MULTIPLICATION ---------
        if op == "*":

            if _is_zero(a) or _is_zero(b): return ("num", '0')
            if is_one(a): return b
            if is_one(b): return a
            if is_num(a) and is_num(b):
                result = float(a[1]) * float(b[1])
                return ("num", result)
            return ('op','*',
                    simplify_tree(a),simplify_tree(b))


        # -------- DIVISION ---------
        if op == "/":
            if _is_zero(a): return ("num", '0')
            if is_one(b): return simplify_tree(a)
            if is_num(a) and is_num(b):
                return ("num", float(a[1]) / float(b[1]))

        # -------- POWER ---------
        if op == "^":
            if _is_zero(b): return ("num", '1')
            if is_one(b): return simplify_tree(a)


    return tree

def turn_to_string(tree):
    # simplified = simplify_tree(tree)
    t = tree[0]

    if t=="num": return str(tree[1])
    if t=="var": return tree[1]
    if t=="func": return f"{tree[1]}({turn_to_string(tree[2])})"

    if t=="op":
        op = tree[1]
        a = turn_to_string(tree[2])
        b = turn_to_string(tree[3])

        # if t in OP_TYPES:
        #     return f"{a} {op} {b}"

        if op == ("+"):
            return f"({a} + {b})"
        if op =='-':
            return f"({a} - {b})"
        if op == '*':
            return f"({a}*{b})"
        if op =='/':
            return f"({a}/{b})"
        if op=="^":
            return f"({a}^{b})"

    return "Syntax error"


def evaluate(tree, value):
    if is_num(tree):
        return float(tree[1])
    if is_var(tree):
        return value

    kind = tree[0]

    if kind == "op":
        op = tree[1]
        left = evaluate(tree[2],value)
        right = evaluate(tree[3],value)

        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        if op == "^":
            return left ** right

    if kind == "func":
        # treat function call as a symbolic variable
        inner_value = evaluate(tree[2],value)
        match(tree[1]):
            case 'sin':
                return  sine(inner_value)
            case 'cos':
                return cosine(inner_value)
            case 'tan':
                return tangent(inner_value)
            case 'cot':
                return 1.0/tangent(inner_value)
            case 'sec':
                return 1.0/ cosine(inner_value)
            case 'csc':
                return  1.0/ sine(inner_value)
            case 'exp':
                return expo(inner_value)
            case 'ln':
                return log(inner_value)
            case 'abs':
                if inner_value<0:
                    return inner_value * (-1)
                else: return inner_value
            case _:
                raise Exception("Syntax error")

    raise Exception("Invalid tree in evaluation")

def generate_tree(expr):
    tokens = tokenize(expr)
    tree = TreeParser(tokens).parse()
    simplified = simplify_tree(tree)
    return simplified

if __name__ == "__main__":
    # expression="(x^2)+sin(2*x)"
    # print(f"expression: {expression}")
    # tokens = tokenize(expression)
    # tree = TreeParser(tokens).parse()
    # simplified = simplify_tree(tree)
    # print(f"simplified: {simplified}")
    # Value=1
    # evaluated = evaluate(simplified,Value)
    # print(f"Evaluated: {evaluated}")

    tree = ('op', '/', ('op', '*', ('num', -1), ('func', 'cos', ('op', '*', ('num', 2.0), ('var', 'x')))), ('op', '+', ('op', '*', ('num', 0), ('var', 'x')), ('op', '*', ('num', 2.0), ('num', 1))))
    tree = ('op', '-', ('op', '*', ('var', 'x'), ('op', '/', ('func', 'sin', ('var', 'x')), ('num', 1))), ('op', '/', ('op', '*', ('num', -1), ('func', 'cos', ('var', 'x'))), ('num', 1)))
    #tree = ('op', '*', ('var', 'x'), ('op', '/', ('func', 'sin', ('var', 'x')), ('num', 1)))
    # tree = (('op', '/', ('func', 'sin', ('var', 'x')), ('num', 1)))
    expr = 'x(sin(x))'
    tree = generate_tree(expr)
    simple = simplify_tree(tree)
    print(turn_to_string(simple))

    print(f"simplified: {simple}")


