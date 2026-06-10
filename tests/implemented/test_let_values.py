"""R5RS let-values family (specialform.py TODO)."""


def test_let_values(eval_str):
    code = """
    (let-values (((a b) (values 1 2)))
      (+ a b))
    """
    assert eval_str(code) == "3"


def test_let_star_values(eval_str):
    code = """
    (let*-values (((a) (values 1))
                  ((b) (values (+ a 2))))
      b)
    """
    assert eval_str(code) == "3"


def test_letrec_values(eval_str):
    code = """
    (letrec-values (((f) (values (lambda (x) (+ x 1)))))
      (f 41))
    """
    assert eval_str(code) == "42"
