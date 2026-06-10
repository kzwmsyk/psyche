from tests.support.harness import eval_string_as_string


def test_length(eval_str):
    assert eval_str("(length (list 1 2 3))") == "3"


def test_append(eval_str):
    assert eval_str("(append (list 1 2) (list 3))") == "(1 2 3)"


def test_reverse(eval_str):
    assert eval_str("(reverse (list 1 2 3))") == "(3 2 1)"


def test_list_copy(eval_str):
    code = """
    (begin
      (define xs (list 1 2))
      (define ys (list-copy xs))
      (set-car! xs 9)
      ys)
    """
    assert eval_str(code) == "(1 2)"


def test_caddr(eval_str):
    assert eval_str("(caddr (list 1 2 3))") == "3"
