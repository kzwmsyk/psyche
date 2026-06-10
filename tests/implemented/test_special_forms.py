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


def test_if_without_else(eval_str):
    assert eval_str("(if #f 1)") == "nil"
    assert eval_str("(if #t 42)") == "42"


def test_cond(eval_str):
    code = """
    (cond ((= 1 2) 0)
          ((= 2 2) 42)
          (else 99))
    """
    assert eval_str(code) == "42"


def test_let_star(eval_str):
    code = """
    (let* ((x 1)
           (y (+ x 1)))
      y)
    """
    assert eval_str(code) == "2"


def test_letrec(eval_str):
    code = """
    (letrec ((even? (lambda (n)
                      (if (= n 0) #t (odd? (- n 1)))))
             (odd? (lambda (n)
                     (if (= n 0) #f (even? (- n 1))))))
      (even? 4))
    """
    assert eval_str(code) == "#t"
