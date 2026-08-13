from .parser import evaluate

PI= 3.14159

def simpson(tree, lower_limit, upper_limit, n_elements=10000):
    """Approximate a definite integral using Simpson's rule."""
    if n_elements <= 0 or n_elements % 2:
        raise ValueError("n_elements must be a positive even integer")
    if lower_limit == upper_limit:
        return 0.0

    direction = 1
    if lower_limit > upper_limit:
        lower_limit, upper_limit = upper_limit, lower_limit
        direction = -1

    h = (upper_limit - lower_limit) / n_elements
    interval = evenly_spaced_list(lower_limit, upper_limit, n_elements + 1)

    # evaluate from the list using
    # the syntax tree operator
    y = [evaluate(tree,value) for value in interval]

    # gettting 2 lists of even number of elements
    # sum of odd elements get multiplied by 4
    # sum of even elements get multiplied by 2

    S = y[0] + y[-1] + 4 * sum(y[1:-1:2]) + 2 * sum(y[2:-1:2])

    return direction * S * h / 3

def evenly_spaced_list(min_value, max_value, size=100):
    if min_value > max_value:
        n = max_value
        max_value = min_value
        min_value = n
    step = (max_value - min_value) / (size-1)
    array = []
    array.append(min_value)
    for i in range(1,size):
        array.append(min_value + (i * step))
    return array


# if __name__ == "__main__":
#     expression="cos(x)"
#     tree=synt.generate_tree(expression)
#     result = simpson(tree, 0, PI,100)  # avoid division by zero
#     print("Simpson approximation:", result)
