"""R5RS string procedures not in stringlib yet."""


def test_string_ci_comparison(eval_str):
    assert eval_str('(string-ci=? "abc" "ABC")') == "#t"
    assert eval_str('(string-ci<? "abc" "BCD")') == "#t"
    assert eval_str('(string-ci>? "zzz" "aaa")') == "#t"


def test_string_fill_bang(eval_str):
    code = """
    (begin
      (define s (make-string 3 #\\x))
      (string-set! s 0 #\\a)
      (string-fill! s #\\o)
      s)
    """
    assert eval_str(code) == '"ooo"'
