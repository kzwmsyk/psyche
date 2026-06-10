import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


def test_eq_differs_from_eqv_for_inexact_numbers(eval_str):
    """eq? should distinguish mutable/inexact values per R5RS semantics."""
    code = """
    (begin
      (define a (+ 0.0 0.0))
      (define b (+ 0.0 0.0))
      (list (eq? a b) (eqv? a b)))
    """
    assert eval_str(code) == "(#f #t)"
