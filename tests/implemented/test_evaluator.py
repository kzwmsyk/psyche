import pytest

from tests.support.harness import eval_string_as_string


def test_self_evaluating_atoms(eval_str):
    assert eval_str("42") == "42"
    assert eval_str("#t") == "#t"
    assert eval_str("#f") == "#f"
    assert eval_str('"hello"') == '"hello"'


def test_quote(eval_str):
    assert eval_str("(quote (1 2))") == "(1 2)"


def test_if_truthy_branch(eval_str):
    assert eval_str("(if #t 1 2)") == "1"


def test_if_falsy_branch(eval_str):
    assert eval_str("(if #f 1 2)") == "2"


def test_define_and_lookup(eval_str):
    assert eval_str("(begin (define x 10) x)") == "10"


def test_lambda_and_application(eval_str):
    code = "(begin (define square (lambda (x) (* x x))) (square 4))"
    assert eval_str(code) == "16"


def test_lexical_closure(eval_str):
    code = """
    (begin
      (define make-adder (lambda (n) (lambda (x) (+ n x))))
      (define add3 (make-adder 3))
      (add3 5))
    """
    assert eval_str(code) == "8"


def test_rest_arguments(eval_str):
    code = "(begin (define f (lambda args args)) (f 1 2 3))"
    assert eval_str(code) == "(1 2 3)"


def test_let(eval_str):
    code = "(let ((x 2) (y 3)) (+ x y))"
    assert eval_str(code) == "5"


def test_and_short_circuit(eval_str):
    assert eval_str("(and #f 99)") == "#f"
    assert eval_str("(and 1 2 3)") == "#t"


def test_or_short_circuit(eval_str):
    assert eval_str("(or #f 0 42)") == "#t"
    assert eval_str("(or #f #f)") == "#f"


def test_begin_returns_last(eval_str):
    assert eval_str("(begin 1 2 3)") == "3"


def test_set_bang(eval_str):
    code = "(begin (define x 1) (set! x 2) x)"
    assert eval_str(code) == "2"


def test_unknown_symbol_raises():
    from tests.support.harness import eval_string

    with pytest.raises(Exception, match="Unknown symbol"):
        eval_string("(unknown)", load_prelude=False)
