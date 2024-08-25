import sclist as sl
from sexpr import NIL, BOOLEAN_T, BOOLEAN_F
from scanner import Scanner
from sctoken import TokenType
from sexpr import Sexpr, Symbol, Number
import scpredicates as sp


from logging import getLogger

logger = getLogger(__name__)


class Reader:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def read(self) -> Sexpr:
        token = self.scanner.get_token()
        logger.debug(f"read token {token}")

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
                logger.debug(f"qread {read}")
                quote = sl.cons(Symbol("quote"),
                                sl.cons(read, NIL))
                logger.debug(f"quote {quote}")
                return quote
            case TokenType.LPAREN:
                return self.readlist()
            case _:
                raise Exception(f"Unexpected token: {token}")

    def readlist(self):
        token = self.scanner.get_token()
        logger.debug(f"read token for list{token}")

        if token.token_type == TokenType.RPAREN:
            return NIL
        elif token.token_type == TokenType.DOT:
            cdr = self.read()
            print(f"cdr {cdr}")
            if sp.is_atom(cdr) or sp.is_null(cdr):
                # Symbol("nil")の場合もここに入る。
                # consume RPAREN
                # has bug
                consume = self.scanner.get_token()
                logger.debug(f"consume {consume}")
            return cdr
        else:
            logger.debug(f"pushback {token}")
            self.scanner.pushback_token(token)
            car = self.read()
            logger.debug(f"car {car}")
            cdr = self.readlist()
            logger.debug(f"cdr {cdr}")
            return sl.cons(car, cdr)
