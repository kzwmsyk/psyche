from common import Sexpr, Number, \
    is_nil, NIL, T, is_number, is_symbol, is_atom, cons
from typing import Callable


def export() -> dict[str, Callable]:
    return {
        "+": f_plus,
        "atom": f_atom,
        "eq": f_eq,
        "car": f_car,
        "cdr": f_cdr,
        "cons": f_cons,
    }


def f_plus(args: Sexpr) -> Sexpr:
    def _plus(args: Sexpr) -> int:
        if is_nil(args):
            return 0
        else:
            return args.car.value + _plus(args.cdr)

    return Number(_plus(args))


def f_atom(args: Sexpr) -> Sexpr:

    arg = args.car
    if is_atom(arg) or is_nil(arg):
        return T
    else:
        return NIL


def f_eq(args: Sexpr) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car

    def _eq(car: Sexpr, cadr: Sexpr) -> bool:
        if is_symbol(car):
            return is_symbol(cadr) and car.name == cadr.name
        elif is_number(car):
            return is_number(cadr) and car.value == cadr.value
        else:
            return False

    return T if _eq(car, cadr) else NIL


def f_car(args: Sexpr) -> Sexpr:
    arg = args.car
    return arg.car


def f_cdr(args: Sexpr) -> Sexpr:
    arg = args.car
    return arg.cdr


def f_cons(args: Sexpr) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car
    return cons(car, cadr)
