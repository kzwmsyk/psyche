"""R5RS lexical syntax not yet supported by scanner/reader."""

from tests.support.harness import read_string, to_string


def test_binary_radix(eval_str):
    assert eval_str("#b101") == "5"


def test_octal_radix(eval_str):
    assert eval_str("#o17") == "15"


def test_hex_radix(eval_str):
    assert eval_str("#x10") == "16"


def test_exactness_prefix(eval_str):
    assert eval_str("(exact? #e1.0)") == "#t"
    assert eval_str("(inexact? #i1)") == "#t"


def test_block_comment(eval_str):
    assert eval_str("(+ 1 #| block |# 2)") == "3"


def test_string_hex_escape():
    forms = read_string('"\\x41"')
    assert to_string(forms[0]) == '"A"'
