from tests.support.harness import read_string, to_string


def test_reads_atoms():
    assert to_string(read_string("42")[0]) == "42"
    assert to_string(read_string("#t")[0]) == "#t"
    assert to_string(read_string("foo")[0]) == "foo"
    assert to_string(read_string('"hi"')[0]) == '"hi"'


def test_reads_proper_list():
    assert to_string(read_string("(1 2 3)")[0]) == "(1 2 3)"


def test_reads_empty_list():
    assert to_string(read_string("()")[0]) == "nil"


def test_reads_dotted_pair():
    assert to_string(read_string("(a . b)")[0]) == "(a . b)"


def test_quote_sugar():
    assert to_string(read_string("'x")[0]) == "(quote x)"


def test_quasiquote_sugar():
    assert to_string(read_string("`(a ,b)")[0]) == "(quasiquote (a (unquote b)))"


def test_unquote_splicing_sugar():
    assert to_string(read_string("`(,@xs)")[0]) == "(quasiquote ((unquote-splicing xs)))"
