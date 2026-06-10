"""R5RS bytevectors (type stub only)."""

from tests.support.harness import read_string, to_string


def test_bytevector_literal():
    forms = read_string("#u8(1 2 3)")
    assert to_string(forms[0]) == "#u8(1 2 3)"


def test_bytevector_p(eval_str):
    assert eval_str("(bytevector? #u8(1))") == "#t"


def test_make_bytevector(eval_str):
    code = """
    (begin
      (define bv (make-bytevector 2 0))
      (bytevector-set! bv 1 5)
      (bytevector-ref bv 1))
    """
    assert eval_str(code) == "5"
