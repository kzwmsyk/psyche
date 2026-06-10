from tests.support.harness import eval_string_as_string


def test_define_function_sugar(eval_str):
    code = "(begin (define (double x) (+ x x)) (double 6))"
    assert eval_str(code) == "12"


def test_quasiquote(eval_str):
    code = "(let ((x 2)) `(+ 1 ,x))"
    assert eval_str(code) == "(+ 1 2)"


def test_quasiquote_splicing(eval_str):
    code = "(let ((xs (list 2 3))) `(1 ,@xs 4))"
    assert eval_str(code) == "(1 2 3 4)"


def test_define_function_with_rest(eval_str):
    code = "(begin (define (f x . rest) rest) (f 1 2 3))"
    assert eval_str(code) == "(2 3)"
