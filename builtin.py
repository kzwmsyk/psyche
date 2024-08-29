from sexpr import Sexpr, Number, NIL, BOOLEAN_T, BOOLEAN_F, BuiltinFunction
import sclist as sl
import scpredicates as sp
from typing import Callable
from functools import reduce


def export() -> dict[str, Callable]:
    return {
        "+": BuiltinFunction(f_plus),
        "-": BuiltinFunction(f_minus),
        "*": BuiltinFunction(f_multi),
        "/": BuiltinFunction(f_div),

        "eq": BuiltinFunction(f_eq),
        "car": BuiltinFunction(f_car),
        "cdr": BuiltinFunction(f_cdr),
        "cons": BuiltinFunction(f_cons),
        "print": BuiltinFunction(f_print),

        "not": BuiltinFunction(f_not),

        "boolean?": BuiltinFunction(f_boolean_p),
        "char?": BuiltinFunction(f_char_p),
        "null?": BuiltinFunction(f_null_p),
        "pair?": BuiltinFunction(f_pair_p),
        "procedure?": BuiltinFunction(f_procedure_p),
        "symbol?": BuiltinFunction(f_symbol_p),
        "bytevector?": BuiltinFunction(f_bytevector_p),
        "eof-object?": BuiltinFunction(f_eof_object_p),
        "number?": BuiltinFunction(f_number_p),
        "port?": BuiltinFunction(f_port_p),
        "string?": BuiltinFunction(f_string_p),
        "vector?": BuiltinFunction(f_vector_p),
    }


def _to_values(args: Sexpr) -> list[int]:
    return [x.value for x in sl.to_python_list(args)]


def _to_lisp_boolean(bool: bool) -> Sexpr:
    return BOOLEAN_T if bool else BOOLEAN_F


def f_not(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(not sp.is_truthy(args.car))


def f_plus(args: Sexpr) -> Sexpr:
    return Number(sum(_to_values(args)))


def f_minus(args: Sexpr) -> Sexpr:
    lst = _to_values(args)
    if len(lst) == 1:
        return Number(-lst[0])
    else:
        return Number(reduce(lambda x, y: x - y, lst))


def f_multi(args: Sexpr) -> Sexpr:
    return Number(reduce(lambda x, y: x * y, _to_values(args), 1))


def f_div(args: Sexpr) -> Sexpr:
    lst = _to_values(args)
    return Number(reduce(lambda x, y: x / y, lst))


def f_eq(args: Sexpr) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car

    def _eq(car: Sexpr, cadr: Sexpr) -> bool:
        if sp.is_symbol(car):
            return sp.is_symbol(cadr) and car.name == cadr.name
        elif sp.is_number(car):
            return sp.is_number(cadr) and car.value == cadr.value
        else:
            return car == cadr

    return _to_lisp_boolean(_eq(car, cadr))


def f_car(args: Sexpr) -> Sexpr:
    arg = sl.car(args)
    return arg.car


def f_cdr(args: Sexpr) -> Sexpr:
    arg = sl.car(args)
    return arg.cdr


def f_cons(args: Sexpr) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car
    return sl.cons(car, cadr)


def f_print(args: Sexpr) -> Sexpr:
    print(args.car)
    return NIL


def f_boolean_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_boolean(args.car))


def f_char_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_char(args.car))


def f_null_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_null(args.car))


def f_pair_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_pair(args.car))


def f_procedure_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_procedure(args.car))


def f_symbol_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_symbol(args.car))


def f_bytevector_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_bytevector(args.car))


def f_eof_object_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_eof_object(args.car))


def f_number_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_number(args.car))


def f_port_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_port(args.car))


def f_string_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_string(args.car))


def f_vector_p(args: Sexpr) -> Sexpr:
    return _to_lisp_boolean(sp.is_vector(args.car))
