from .parser import is_num, turn_to_string

def derivative(tree, var='x'):
    t = tree[0]

    if t == "num":
        return ("num",0)

    if t == "var":
        return ("num",1 if tree[1] == var else 0)

    if t == "func":
        name, arg = tree[1], tree[2]
        da = derivative(arg,var)
        outer = tree
        match name:
            case 'sin':
                outer= ("func","cos",arg)
            case "cos": outer= ("op","*",
                                ("num",-1), ("func","sin",arg))
            case "tan":
                secx = ("func", "sec", arg)
                outer = ("op", "^", secx, ("num", 2))

            case 'cot':
                cscx = ("func","csc",arg)
                csc_sq = ("op", "^", cscx, ("num", 2))
                outer = ("op","*",
                               ("num",-1), csc_sq)
            case  'sec':
                tanx = ("func","tan",arg)
                outer = ("op","*",tree, tanx)
            case 'csc':
                cotx = ("func","cot",arg)
                minus_cscx = ("op","*",  ("num",-1), tree)
                outer = ("op","*",  minus_cscx, cotx)

            case "exp": return ("op","*", ("func","exp",arg), da)
            case "ln":  return ("op","/", da, arg)

        return ("op","*", outer, da)

    if t=="op":
        op = tree[1]
        a,b = tree[2],tree[3]
        da,db = derivative(a,var), derivative(b,var)

        if op=="+":
            return ("op","+",da,db)
        if op=="-":
            return ("op","-",da,db)
        if op=="*":
            return ("op","+", ("op","*",da,b), ("op","*",a,db))
        if op=="/":
            return ("op","/", ("op","-", ("op","*",da,b), ("op","*",a,db)), ("op","^",b,("num",2)))
        if op=="^":
            if is_num(b):  # power rule
                n = b[1]
                return ("op", "*", ("op", "*", ("num", n), ("op", "^", a, ("num", n-1))), da)

    raise Exception("Cannot differentiate: " + turn_to_string(tree))