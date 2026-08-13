import pytest

from calculus_tool.numerical import simpson
from calculus_tool.parser import generate_tree


def test_simpson_integrates_quadratic():
    assert simpson(generate_tree("x^2"), 0, 1, 100) == pytest.approx(1 / 3)


def test_simpson_preserves_reversed_limit_sign():
    assert simpson(generate_tree("x"), 1, 0, 100) == pytest.approx(-0.5)


def test_simpson_requires_even_interval_count():
    with pytest.raises(ValueError):
        simpson(generate_tree("x"), 0, 1, 3)
