import sclist as sl
from sexpr import NIL, BOOLEAN_T, BOOLEAN_F
from scanner import Scanner
from sctoken import TokenType
from sexpr import Sexpr, Symbol, Number, String, Char, Vector, Bytevector
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
                return self._read_number(token)
            case TokenType.STRING:
                return String(value=token.buffer)
            case TokenType.CHAR:
                return Char(value=token.buffer)
            case TokenType.VECTOR:
                return Vector(self._read_vector())
            case TokenType.BYTEVECTOR:
                return Bytevector(bytearray(self._read_bytevector()))
            case TokenType.T:
                return BOOLEAN_T
            case TokenType.F:
                return BOOLEAN_F
            case TokenType.QUOTE:
                read = self.read()
                quote = sl.cons(Symbol("quote"),
                                sl.cons(read, NIL))
                return quote
            case TokenType.QUASIQUOTE:
                read = self.read()
                quote = sl.cons(Symbol("quasiquote"),
                                sl.cons(read, NIL))
                return quote
            case TokenType.UNQUOTE:
                read = self.read()
                quote = sl.cons(Symbol("unquote"),
                                sl.cons(read, NIL))
                return quote
            case TokenType.UNQUOTE_SPLICING:
                read = self.read()
                quote = sl.cons(Symbol("unquote-splicing"),
                                sl.cons(read, NIL))
                return quote
            case TokenType.LPAREN:
                return self.readlist()
            case _:
                raise Exception(f"Unexpected token: {token}")

    def _read_number(self, token) -> Number:
        text = token.buffer
        radix = token.number_radix
        exact = token.number_exact
        if radix != 10:
            value = int(text, radix)
            if exact is False:
                return Number(float(value))
            return Number(value)
        if any(marker in text for marker in (".", "e", "E")):
            value = float(text)
            if exact is True and value.is_integer():
                return Number(int(value))
            return Number(value)
        value = int(text)
        if exact is False:
            return Number(float(value))
        return Number(value)

    def _read_vector(self) -> list[Sexpr]:
        items: list[Sexpr] = []
        while True:
            token = self.scanner.get_token()
            if token.token_type == TokenType.RPAREN:
                return items
            self.scanner.pushback_token(token)
            items.append(self.read())

    def _read_bytevector(self) -> list[int]:
        items: list[int] = []
        while True:
            token = self.scanner.get_token()
            if token.token_type == TokenType.RPAREN:
                return items
            self.scanner.pushback_token(token)
            value = self.read()
            if not isinstance(value, Number):
                raise Exception("bytevector element must be a number")
            byte = int(value.value)
            if byte < 0 or byte > 255:
                raise Exception("byte out of range")
            items.append(byte)

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
