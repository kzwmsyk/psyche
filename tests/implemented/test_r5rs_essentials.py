import tempfile
from pathlib import Path

from tests.support.harness import ROOT, eval_string_as_string, read_string, to_string


def test_float_literal_and_arithmetic(eval_str):
    assert eval_str("3.14") == "3.14"
    assert eval_str("(+ 1 2.5)") == "3.5"
    assert eval_str("(exact? 1)") == "#t"
    assert eval_str("(inexact? 1.0)") == "#t"


def test_characters(eval_str):
    assert eval_str("#\\a") == "#\\a"
    assert eval_str("(char->integer #\\a)") == "97"
    assert eval_str("(integer->char 65)") == "#\\A"
    assert eval_str("(char? #\\a)") == "#t"


def test_vectors(eval_str):
    assert eval_str("#(1 2 3)") == "#(1 2 3)"
    assert eval_str("(vector-ref #(10 20) 1)") == "20"
    assert eval_str("(vector-length #(1 2))") == "2"


def test_string_procedures(eval_str):
    assert eval_str('(string-length "abc")') == "3"
    assert eval_str('(string-ref "abc" 1)') == "#\\b"
    assert eval_str('(string-append "ab" "cd")') == '"abcd"'
    assert eval_str("(symbol->string 'x)") == '"x"'


def test_case(eval_str):
    code = """
    (case 2
      ((1) 10)
      ((2 3) 20)
      (else 99))
    """
    assert eval_str(code) == "20"


def test_do(eval_str):
    code = """
    (do ((i 0 (+ i 1)))
        ((= i 3) i)
      i)
    """
    assert eval_str(code) == "3"


def test_eval(eval_str):
    code = """
    (eval '(+ 2 3) (interaction-environment))
    """
    assert eval_str(code) == "5"


def test_display_and_write(capsys, eval_str):
    eval_str('(begin (display "hi") (newline) nil)')
    captured = capsys.readouterr()
    assert captured.out == "hi\n"


def test_load(eval_str):
    with tempfile.NamedTemporaryFile("w", suffix=".scm", delete=False) as tmp:
        tmp.write("(define loaded-value 42)\n")
        path = tmp.name
    try:
        code = f'(begin (load "{path}") loaded-value)'
        assert eval_str(code) == "42"
    finally:
        Path(path).unlink(missing_ok=True)


def test_eq_inexact_numbers(eval_str):
    code = """
    (begin
      (define a (+ 0.0 0.0))
      (define b (+ 0.0 0.0))
      (list (eq? a b) (eqv? a b)))
    """
    assert eval_str(code) == "(#f #t)"


def test_port_p(eval_str):
    assert eval_str("(port? (current-input-port))") == "#t"


def test_include(eval_str):
    path = ROOT / "prelude.scm"
    assert eval_str(f'(include "{path}")') == "nil"


def test_read_from_port(eval_str):
    with tempfile.NamedTemporaryFile("w", suffix=".scm", delete=False) as tmp:
        tmp.write("42\n")
        path = tmp.name
    try:
        code = f"""
        (let ((p (open-input-file "{path}")))
          (begin (define v (read p))
                 (close-input-port p)
                 v))
        """
        assert eval_str(code) == "42"
    finally:
        Path(path).unlink(missing_ok=True)


def test_map_and_for_each(eval_str):
    assert eval_str("(map (lambda (x) (* x 2)) (list 1 2 3))") == "(2 4 6)"
    assert eval_str("(begin (for-each (lambda (x) x) (list 1 2)) nil)") == "nil"
