from typing import IO
from common import Token, TokenType, Sexpr, Atom, Number, \
    Symbol, NIL, cons, is_atom
from scanner import Scanner


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
                return cons(Symbol("quote"),
                            cons(self.read(), NIL))
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
            if is_atom(cdr):
                self.scanner.get_token()  # consume RPAREN...?
            return cdr
        else:
            self.scanner.pushback_token(token)
            car = self.read()
            cdr = self.readlist()
            return cons(car, cdr)
