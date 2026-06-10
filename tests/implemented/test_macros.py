from tests.support.harness import eval_string_as_string


def test_syntax_rules_when(eval_str):
    code = """
    (begin
      (define-syntax when
        (syntax-rules ()
          ((when test body ...)
           (if test (begin body ...)))))
      (when #t 42))
    """
    assert eval_str(code) == "42"


def test_syntax_rules_unless(eval_str):
    code = """
    (begin
      (define-syntax unless
        (syntax-rules ()
          ((unless test body ...)
           (if (not test) (begin body ...)))))
      (unless #f 100))
    """
    assert eval_str(code) == "100"


def test_lambda_transformer_macro(eval_str):
    code = """
    (begin
      (define-syntax double
        (lambda (form)
          (list '+ (cadr form) (cadr form))))
      (double 5))
    """
    assert eval_str(code) == "10"


def test_syntax_rules_swap(eval_str):
    code = """
    (begin
      (define-syntax swap!
        (syntax-rules ()
          ((swap! x y)
           (let ((tmp x))
             (set! x y)
             (set! y tmp)))))
      (define a 1)
      (define b 2)
      (swap! a b)
      (list a b))
    """
    assert eval_str(code) == "(1 2)"
