import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


def test_float_literal(eval_str):
    assert eval_str("3.14") == "3.14"


def test_mixed_float_arithmetic(eval_str):
    assert eval_str("(+ 1 2.5)") == "3.5"


def test_numeric_comparison(eval_str):
    assert eval_str("(< 1 2)") == "#t"
    assert eval_str("(> 5 3)") == "#t"
