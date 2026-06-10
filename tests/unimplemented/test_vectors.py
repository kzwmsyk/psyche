import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


def test_vector_literal(eval_str):
    assert eval_str("#(1 2 3)") == "#(1 2 3)"


def test_vector_ref(eval_str):
    assert eval_str("(vector-ref #(10 20) 1)") == "20"
