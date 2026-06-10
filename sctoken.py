from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    QUOTE = auto()
    QUASIQUOTE = auto()
    UNQUOTE = auto()
    UNQUOTE_SPLICING = auto()
    DOT = auto()
    NUMBER = auto()
    SYMBOL = auto()
    OTHER = auto()
    EOF = auto()
    T = auto()
    F = auto()
    STRING = auto()
    CHAR = auto()
    VECTOR = auto()
    BYTEVECTOR = auto()


@dataclass
class Token:
    token_type: TokenType
    buffer: str = None
    col: int = None
    line: int = None
    number_exact: bool | None = None
    number_radix: int = 10
