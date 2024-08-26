
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


def caar(sexpr: Sexpr) -> Sexpr:
    return car(car(sexpr))


def cadr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(sexpr))


def cdar(sexpr: Sexpr) -> Sexpr:
    return cdr(car(sexpr))


def cddr(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(sexpr))


def caaar(sexpr: Sexpr) -> Sexpr:
    return car(car(car(sexpr)))


def caadr(sexpr: Sexpr) -> Sexpr:
    return car(car(cdr(sexpr)))


def cadar(sexpr: Sexpr) -> Sexpr:
    return car(cdr(car(sexpr)))


def caddr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(cdr(sexpr)))


def cdaar(sexpr: Sexpr) -> Sexpr:
    return cdr(car(car(sexpr)))


def cdadr(sexpr: Sexpr) -> Sexpr:
    return cdr(car(cdr(sexpr)))


def cddar(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(car(sexpr)))


def cdddr(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(cdr(sexpr)))


def caaaar(sexpr: Sexpr) -> Sexpr:
    return car(car(car(car(sexpr))))


def caaadr(sexpr: Sexpr) -> Sexpr:
    return car(car(car(cdr(sexpr))))


def caadar(sexpr: Sexpr) -> Sexpr:
    return car(cdr(car(sexpr)))


def caaddr(sexpr: Sexpr) -> Sexpr:
    return car(cdr(cdr(sexpr)))


def cadaar(sexpr: Sexpr) -> Sexpr:
    return cdr(car(car(sexpr)))


def cadadr(sexpr: Sexpr) -> Sexpr:
    return cdr(car(cdr(sexpr)))


def caddar(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(car(sexpr)))


def cadddr(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(cdr(sexpr)))


def cdaaar(sexpr: Sexpr) -> Sexpr:
    return cdr(car(car(car(sexpr))))


def cdaadr(sexpr: Sexpr) -> Sexpr:
    return cdr(car(car(cdr(sexpr))))


def cdadar(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(car(sexpr)))


def cdaddr(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(cdr(sexpr)))


def cddaar(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(car(sexpr)))


def cddadr(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(car(cdr(sexpr))))


def cdddar(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(cdr(car(sexpr))))


def cddddr(sexpr: Sexpr) -> Sexpr:
    return cdr(cdr(cdr(cdr(sexpr))))
