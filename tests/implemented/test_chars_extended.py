"""R5RS character procedures not in charlib yet."""


def test_char_ci_comparison(eval_str):
    assert eval_str("(char-ci=? #\\a #\\A)") == "#t"
    assert eval_str("(char-ci<? #\\a #\\B)") == "#t"
    assert eval_str("(char-ci>? #\\Z #\\a)") == "#t"


def test_char_predicates(eval_str):
    assert eval_str("(char-alphabetic? #\\a)") == "#t"
    assert eval_str("(char-numeric? #\\0)") == "#t"
    assert eval_str("(char-whitespace? #\\space)") == "#t"
    assert eval_str("(char-upper-case? #\\A)") == "#t"
    assert eval_str("(char-lower-case? #\\a)") == "#t"


def test_char_case_conversion(eval_str):
    assert eval_str("(char-upcase #\\a)") == "#\\A"
    assert eval_str("(char-downcase #\\Z)") == "#\\z"
