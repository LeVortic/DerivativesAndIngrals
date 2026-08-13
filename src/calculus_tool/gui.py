from . import parser as synt
from . import numerical
from . import integration as symbolic
from . import sympy_backend

import tkinter as tk
from tkinter import ttk, messagebox


def symbolic_integral(expr,lower_l, upper_l):
    tree = synt.generate_tree(expr)
    symbolic_integ = symbolic.integrate(tree)
    evaluation = (synt.evaluate(symbolic_integ["symbolic_tree"], upper_l)
                  - synt.evaluate(symbolic_integ["symbolic_tree"], lower_l))
    evaluation_simpsons = numerical.simpson(tree, lower_l, upper_l, 200)
    symbolic_expr = f"∫({synt.turn_to_string(tree)}) dx"
    return symbolic_expr, symbolic_integ["integral"], evaluation, evaluation_simpsons


def compute_integral():
    expr = entry_func.get().strip()
    a_str = entry_a.get().strip()
    b_str = entry_b.get().strip()

    if not expr or not a_str or not b_str:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        a = float(a_str)
        b = float(b_str)
    except:
        messagebox.showerror("Error", "Limits must be numeric.")
        return

    try:

        # Symbolic integral
        original_fn,integral_expr, sym_eval, simpsons_eval = symbolic_integral(expr,a,b)
        sympy_eval=sympy_backend.calculate_integral(expr, a, b)

        # Insert into table
        results_table.delete(*results_table.get_children())
        results_table.insert("", "end",
                             values=[original_fn, integral_expr, f"{sym_eval:.10f}", f"{simpsons_eval:.10f}", sympy_eval[0]])
        results_table.insert("", index="end", value=['','','','', sympy_eval[1]])

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
        pass



# ------------------- UI ----------------------------


def main():
    """Launch the desktop integral calculator."""
    global root, entry_func, entry_a, entry_b, results_table
    root = tk.Tk()
    root.title("Definite Integral Calculator")
    
    frame = ttk.Frame(root, padding=12)
    frame.grid(row=0, column=0, sticky="nsew")
    
    #Row 0: Instructions
    ttk.Label(frame, text="Input f(x) using explicit operators, i.e.: \n3*x*(sin(2*x)) \n ").grid(row=0, column=1)
    
    # Row 1: Function input
    ttk.Label(frame, text="F(x):").grid(row=1, column=0, sticky="e")
    entry_func = ttk.Entry(frame, width=40)
    entry_func.grid(row=1, column=1, columnspan=3, sticky="we")
    
    # Row 2: Limits
    ttk.Label(frame, text="Lower limit (a):").grid(row=2, column=0, sticky="e")
    entry_a = ttk.Entry(frame, width=5)
    entry_a.grid(row=2, column=1, sticky="we")
    
    ttk.Label(frame, text="Upper limit (b):").grid(row=2, column=2, sticky="e")
    entry_b = ttk.Entry(frame, width=5)
    entry_b.grid(row=2, column=3, sticky="we")
    
    # Button
    compute_button = ttk.Button(frame, text="Compute Integral", command=compute_integral)
    compute_button.grid(row=3, column=0, columnspan=4, pady=10)
    
    # Row 4: Table headers + output
    columns = ("original", "symbolic", "eval_symbolic", "simpson","sympy")
    results_table = ttk.Treeview(frame, columns=columns, show="headings", height=4)
    
    results_table.heading("original", text="Original Function")
    results_table.heading("symbolic", text="Symbolic Integral")
    results_table.heading("eval_symbolic", text="Eval (Symbolic)")
    results_table.heading("simpson", text="Eval (Simpson)")
    results_table.heading("sympy", text="Eval (sympy)")
    
    results_table.grid(row=4, column=0, columnspan=5, sticky="nsew")
    
    # Allow resizing
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(3, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()
