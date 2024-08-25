
from sexpr import Sexpr, Cell, Nil, Symbol, Number, Atom, NIL


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


def cddr(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(sexpr))


def caddr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(cdr(sexpr)))


def cadddr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(cdr(cdr(sexpr))))
