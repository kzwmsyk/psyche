import sclist as sl
from sexpr import NIL, BOOLEAN_T, BOOLEAN_F
from scanner import Scanner
from sctoken import TokenType
from sexpr import Sexpr, Symbol, Number
from logging import getLogger

logger = getLogger(__name__)


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
            case TokenType.T:
                return BOOLEAN_T
            case TokenType.F:
                return BOOLEAN_F
            case TokenType.QUOTE:
                read = self.read()
                quote = sl.cons(Symbol("quote"),
                                sl.cons(read, NIL))
                return quote
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
            # consume RPAREN
            self.scanner.get_token()
            return cdr
        else:
            self.scanner.pushback_token(token)
            car = self.read()
            cdr = self.readlist()
            return sl.cons(car, cdr)
