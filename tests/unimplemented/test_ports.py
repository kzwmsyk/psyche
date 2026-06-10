import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


def test_display(eval_str):
    assert eval_str("(begin (display 42) nil)") == "nil"


def test_read_from_port(eval_str):
    assert eval_str("(read)") is not None
