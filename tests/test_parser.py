import math

import pytest

from calculus_tool.parser import evaluate, generate_tree


def test_parse_and_evaluate_polynomial():
    tree = generate_tree("x^2 + 2*x + 1")
    assert evaluate(tree, 3) == pytest.approx(16)


def test_parse_and_evaluate_trigonometric_function():
    tree = generate_tree("sin(x)")
    assert evaluate(tree, math.pi / 2) == pytest.approx(1)
