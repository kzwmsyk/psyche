import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


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


def test_cond(eval_str):
    code = """
    (cond ((eq? 1 2) 0)
          ((eq? 2 2) 42)
          (else 99))
    """
    assert eval_str(code) == "42"
