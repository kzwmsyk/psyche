from sexpr import Symbol
from syntaxrules import expand_syntax_rules

from tests.support.harness import read_string, to_string


def test_expand_when_macro():
    pattern = read_string("(when test body ...)")[0]
    template = read_string("(if test (begin body ...))")[0]
    form = read_string("(when #f 99)")[0]
    expanded = expand_syntax_rules(["when"], [(pattern, template)], form)
    assert to_string(expanded) == "(if #f (begin 99))"
