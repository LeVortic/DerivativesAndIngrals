import pytest

from calculus_tool.differentiation import derivative
from calculus_tool.parser import evaluate, generate_tree, simplify_tree


def test_power_rule_includes_chain_rule():
    tree = generate_tree("(2*x)^3")
    result = simplify_tree(derivative(tree))
    assert evaluate(result, 2) == pytest.approx(96)


def test_tangent_derivative():
    tree = generate_tree("tan(x)")
    result = simplify_tree(derivative(tree))
    assert evaluate(result, 0) == pytest.approx(1)
