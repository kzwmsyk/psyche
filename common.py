
from enum import Enum, auto
from dataclasses import dataclass


class Sexpr:
    pass


@dataclass
class Atom(Sexpr):
    pass


@dataclass
class Number(Atom):
    value: int | float

    def __str__(self):
        return str(self.value)


@dataclass
class Symbol(Atom):
    name: str

    def __str__(self):
        return f"Symbol({self.name})"


class Nil(Symbol):
    def __init__(self):
        super().__init__("nil")

    def __str__(self):
        return "()"


NIL = Nil()
T = Symbol("t")


@ dataclass
class Cell:
    car: Sexpr = None
    cdr: Sexpr = None

    def __str__(self):
        return f"({self.car} . {self.cdr})"


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


class ErrorCode(Enum):
    CANT_FIND_ERR = 1
    ARG_SYM_ERR = 2
    ARG_NUM_ERR = 3
    ARG_LIS_ERR = 4
    ARG_LEN0_ERR = 5
    ARG_LEN1_ERR = 6
    ARG_LEN2_ERR = 7
    ARG_LEN3_ERR = 8
    MALFORM_ERR = 9
    CANT_READ_ERR = 10
    ILLEGAL_OBJ_ERR = 11


def cons(car: Sexpr, cdr: Sexpr) -> Sexpr:
    return Cell(car, cdr)


def is_atom(expr: Sexpr) -> bool:
    return isinstance(expr, Atom)


def is_number(expr: Sexpr) -> bool:
    return isinstance(expr, Number)


def is_symbol(expr: Sexpr) -> bool:
    return isinstance(expr, Symbol)


def is_cell(expr: Sexpr) -> bool:
    return isinstance(expr, Cell)


def is_nil(expr: Sexpr) -> bool:
    return isinstance(expr, Nil)


def is_subr(expr: Sexpr) -> bool:
    pass


def car(expr: Sexpr) -> Sexpr:
    if is_cell(expr):
        return expr.car
    else:
        return NIL


def cdr(sexpr: Sexpr) -> Sexpr:
    if is_cell(sexpr):
        return sexpr.cdr
    else:
        return NIL


def cadr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(sexpr))


def caddr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(cdr(sexpr)))


def cadddr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(cdr(cdr(sexpr))))
