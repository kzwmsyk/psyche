from typing import IO
import sclist as sc
from sexpr import NIL
from scanner import Scanner
from enum import Enum, auto
from dataclasses import dataclass
from sctoken import Token, TokenType
from sexpr import Sexpr, Symbol, Number


class Reader:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def read(self) -> Sexpr:
        token = self.scanner.get_token()
        match token.token_type:
            case TokenType.EOF:
                return None
            case TokenType.SYMBOL:
                return Symbol(name=token.buffer)
            case TokenType.NUMBER:
                return Number(value=int(token.buffer))
            case TokenType.QUOTE:
                return sc.cons(Symbol("quote"),
                               sc.cons(self.read(), NIL))
            case TokenType.LPAREN:
                return self.readlist()
            case _:
                raise Exception(f"Unexpected token: {token}")

    def readlist(self):
        token = self.scanner.get_token()
        if token.token_type == TokenType.RPAREN:
            return NIL
        elif token.token_type == TokenType.DOT:
            cdr = self.read()
            if sc.is_atom(cdr):
                self.scanner.get_token()  # consume RPAREN...?
            return cdr
        else:
            self.scanner.pushback_token(token)
            car = self.read()
            cdr = self.readlist()
            return sc.cons(car, cdr)
