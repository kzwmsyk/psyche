import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


def test_char_literal(eval_str):
    assert eval_str("#\\a") == "#\\a"


def test_char_to_integer(eval_str):
    assert eval_str("(char->integer #\\a)") == "97"
