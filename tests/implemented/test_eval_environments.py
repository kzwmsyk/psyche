"""R5RS eval environment specifiers."""


def test_scheme_report_environment(eval_str):
    code = """
    (eval '(+ 2 3) (scheme-report-environment 5))
    """
    assert eval_str(code) == "5"


def test_null_environment(eval_str):
    """null-environment has syntax keywords only, not library bindings."""
    code = """
    (eval '(if #t 3 4) (null-environment 5))
    """
    assert eval_str(code) == "3"
