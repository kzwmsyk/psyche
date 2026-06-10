"""R5RS vector procedures not in vectorlib yet."""


def test_vector_fill_bang(eval_str):
    code = """
    (begin
      (define v (vector 1 2 3))
      (vector-fill! v 0)
      v)
    """
    assert eval_str(code) == "#(0 0 0)"
