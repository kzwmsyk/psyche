import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


def test_procedure_p_on_lambda(eval_str):
    assert eval_str("(procedure? (lambda (x) x))") == "#t"


def test_char_p(eval_str):
    assert eval_str("(char? #\\a)") == "#t"


def test_vector_p(eval_str):
    assert eval_str("(vector? #(1 2 3))") == "#t"


def test_port_p(eval_str):
    assert eval_str("(port? (current-input-port))") == "#t"
