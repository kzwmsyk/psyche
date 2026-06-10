"""R5RS let-syntax / letrec-syntax."""


def test_let_syntax(eval_str):
    code = """
    (let-syntax ((when (syntax-rules ()
                          ((when test body ...)
                           (if test (begin body ...))))))
      (when #t 42))
    """
    assert eval_str(code) == "42"


def test_letrec_syntax_mutual(eval_str):
    code = """
    (letrec-syntax ((even?
                     (syntax-rules ()
                       ((even? x)
                        (or (zero? x)
                            (odd? (- x 1))))))
                    (odd?
                     (syntax-rules ()
                       ((odd? x)
                        (and (not (zero? x))
                             (even? (- x 1)))))))
      (even? 4))
    """
    assert eval_str(code) == "#t"
