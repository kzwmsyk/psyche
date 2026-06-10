import io

import pytest

from scanner import Scanner
from sctoken import TokenType


def tokens(source: str) -> list[TokenType]:
    scanner = Scanner(stream=io.StringIO(source))
    result = []
    while True:
        token = scanner.get_token()
        result.append(token.token_type)
        if token.token_type == TokenType.EOF:
            break
    return result


def token_buffers(source: str) -> list[str | None]:
    scanner = Scanner(stream=io.StringIO(source))
    result = []
    while True:
        token = scanner.get_token()
        result.append(token.buffer)
        if token.token_type == TokenType.EOF:
            break
    return result


def test_integer_literals():
    assert token_buffers("0 42 -7 +9") == ["0", "42", "-7", "+9", None]


def test_boolean_literals():
    assert tokens("#t #f") == [TokenType.T, TokenType.F, TokenType.EOF]


def test_symbols_and_operators():
    assert token_buffers("+ - * / = < >") == ["+", "-", "*", "/", "=", "<", ">", None]


def test_ellipsis_symbol():
    assert token_buffers("...") == ["...", None]


def test_quote_tokens():
    assert tokens("' ` , ,@") == [
        TokenType.QUOTE,
        TokenType.QUASIQUOTE,
        TokenType.UNQUOTE,
        TokenType.UNQUOTE_SPLICING,
        TokenType.EOF,
    ]


def test_string_literal():
    assert token_buffers('"hello\\n"') == ["hello\n", None]


def test_comments_are_skipped():
    assert token_buffers("; comment\n42") == ["42", None]


def test_invalid_sharp_suffix_raises():
    scanner = Scanner(stream=io.StringIO("#q"))
    with pytest.raises(Exception, match="Invalid character after #"):
        scanner.get_token()
