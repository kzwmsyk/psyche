"""R5RS port procedures beyond current ports.py."""

import tempfile
from pathlib import Path


def test_input_output_port_p(eval_str):
    assert eval_str("(input-port? (current-input-port))") == "#t"
    assert eval_str("(output-port? (current-output-port))") == "#t"


def test_with_input_from_file(eval_str):
    with tempfile.NamedTemporaryFile("w", suffix=".scm", delete=False) as tmp:
        tmp.write("99\n")
        path = tmp.name
    try:
        code = f"""
        (with-input-from-file "{path}"
          (lambda () (read)))
        """
        assert eval_str(code) == "99"
    finally:
        Path(path).unlink(missing_ok=True)


def test_call_with_input_file(eval_str):
    with tempfile.NamedTemporaryFile("w", suffix=".scm", delete=False) as tmp:
        tmp.write("11\n")
        path = tmp.name
    try:
        code = f"""
        (call-with-input-file "{path}"
          (lambda (port) (read port)))
        """
        assert eval_str(code) == "11"
    finally:
        Path(path).unlink(missing_ok=True)


def test_with_output_to_file(eval_str):
    with tempfile.NamedTemporaryFile("w", suffix=".scm", delete=False) as tmp:
        path = tmp.name
    try:
        code = f"""
        (begin
          (with-output-to-file "{path}"
            (lambda () (display "hi")))
          (with-input-from-file "{path}"
            (lambda () (read-char))))
        """
        assert eval_str(code) == "#\\h"
    finally:
        Path(path).unlink(missing_ok=True)
