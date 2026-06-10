from tests.support.harness import eval_string_as_string


def test_set_bang_updates_global(eval_str):
    code = "(begin (define x 1) (set! x 3) x)"
    assert eval_str(code) == "3"


def test_set_bang_updates_outer_binding_from_let(eval_str):
    code = """
    (begin
      (define a 1)
      (define b 2)
      (let ((tmp a))
        (set! a b)
        (set! b tmp))
      (list a b))
    """
    assert eval_str(code) == "(2 1)"
