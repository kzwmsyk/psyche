from syntaxobject import (
    SyntaxObject,
    datum_to_syntax,
    resolve_literal_descriptor,
    syntax_datum,
)

from tests.support.harness import make_evaluator, read_string


def test_syntax_datum_roundtrip():
    datum = read_string("(a 1)")[0]
    stx = datum_to_syntax(datum)
    assert isinstance(stx, SyntaxObject)
    assert syntax_datum(stx) is datum


def test_literal_descriptor_captures_binding():
    evaluator = make_evaluator()
    evaluator.bind("x", read_string("42")[0])
    desc = resolve_literal_descriptor(evaluator, read_string("x")[0])
    assert desc.name == "x"
    assert desc.binding is not None
