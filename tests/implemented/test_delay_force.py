"""R5RS delay / force."""


def test_delay_force(eval_str):
    assert eval_str("(force (delay (+ 1 2)))") == "3"


def test_delay_evaluates_once(eval_str):
    code = """
    (begin
      (define count 0)
      (define d (delay (begin (set! count (+ count 1)) count)))
      (list (force d) (force d) count))
    """
    assert eval_str(code) == "(1 1 1)"
