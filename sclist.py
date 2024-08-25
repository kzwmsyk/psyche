
from sexpr import Sexpr, Cell, NIL
import scpredicates as sp


def cons(car: Sexpr, cdr: Sexpr) -> Sexpr:
    return Cell(car, cdr)


def car(expr: Sexpr) -> Sexpr:
    if sp.is_pair(expr):
        return expr.car
    else:
        return NIL


def cdr(sexpr: Sexpr) -> Sexpr:
    if sp.is_pair(sexpr):
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
