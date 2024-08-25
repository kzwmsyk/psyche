from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    QUOTE = auto()
    DOT = auto()
    NUMBER = auto()
    SYMBOL = auto()
    OTHER = auto()
    EOF = auto()


@ dataclass
class Token:
    token_type: TokenType
    buffer: str = None
    col: int = None
    line: int = None
