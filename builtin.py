from sexpr import Sexpr, Cell, Nil, Symbol, Number, NIL, T, BuiltinFunction
from sctoken import Token, TokenType
import sclist as sc
from typing import Callable
from functools import reduce


def export() -> dict[str, Callable]:
    return {
        "+": BuiltinFunction(f_plus),
        "-": BuiltinFunction(f_minus),
        "*": BuiltinFunction(f_multi),
        "/": BuiltinFunction(f_div),
        "atom": BuiltinFunction(f_atom),
        "eq": BuiltinFunction(f_eq),
        "car": BuiltinFunction(f_car),
        "cdr": BuiltinFunction(f_cdr),
        "cons": BuiltinFunction(f_cons),
        "print": BuiltinFunction(f_print),
    }


def _to_list(args: Sexpr) -> list[int]:
    if sc.is_nil(args):
        return []
    else:
        return [args.car.value] + _to_list(args.cdr)


def f_plus(args: Sexpr) -> Sexpr:
    return Number(sum(_to_list(args)))


def f_minus(args: Sexpr) -> Sexpr:
    lst = _to_list(args)
    print(lst)
    return Number(reduce(lambda x, y: x - y, lst))


def f_multi(args: Sexpr) -> Sexpr:
    return Number(reduce(lambda x, y: x * y, _to_list(args), 1))


def f_div(args: Sexpr) -> Sexpr:
    lst = _to_list(args)
    return Number(reduce(lambda x, y: x / y, lst))


def f_atom(args: Sexpr) -> Sexpr:

    arg = args.car
    if sc.is_atom(arg) or sc.is_nil(arg):
        return T
    else:
        return NIL


def f_eq(args: Sexpr) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car

    def _eq(car: Sexpr, cadr: Sexpr) -> bool:
        if sc.is_symbol(car):
            return sc.is_symbol(cadr) and car.name == cadr.name
        elif sc.is_number(car):
            return sc.is_number(cadr) and car.value == cadr.value
        else:
            return False

    return T if _eq(car, cadr) else NIL


def f_car(args: Sexpr) -> Sexpr:
    arg = sc.car(args)
    return arg.car


def f_cdr(args: Sexpr) -> Sexpr:
    arg = sc.car(args)
    return arg.cdr


def f_cons(args: Sexpr) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car
    return sc.cons(car, cadr)


def f_print(args: Sexpr) -> Sexpr:
    print(args.car)
    return NIL
