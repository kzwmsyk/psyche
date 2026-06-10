"""R5RS call/cc, values, call-with-values, dynamic-wind."""


def test_call_cc_capture(eval_str):
    assert eval_str("(call/cc (lambda (k) 7))") == "7"


def test_call_cc_invoke(eval_str):
    code = """
    (+ 1 (call/cc (lambda (k) (k 5))))
    """
    assert eval_str(code) == "6"


def test_call_with_values(eval_str):
    code = """
    (call-with-values (lambda () (values 10 20)) +)
    """
    assert eval_str(code) == "30"


def test_values(eval_str):
    code = """
    (call-with-values (lambda () (values 1 2 3)) list)
    """
    assert eval_str(code) == "(1 2 3)"


def test_dynamic_wind(eval_str):
    code = """
    (begin
      (define trace '())
      (define (push x) (set! trace (cons x trace)))
      (dynamic-wind
        (lambda () (push 'before))
        (lambda () (push 'body))
        (lambda () (push 'after)))
      trace)
    """
    assert eval_str(code) == "(after body before)"
