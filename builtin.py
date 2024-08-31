from sexpr import Sexpr, Number, NIL, BOOLEAN_T, BOOLEAN_F, BuiltinFunction, \
    Boolean, String, Symbol, Char, Bytevector, Vector, Nil, Cell
import sclist as sl
import scpredicates as sp
from typing import Callable
from functools import reduce
import logging
logger = logging.getLogger(__name__)


def export() -> dict[str, Callable]:
    return {
        "+": BuiltinFunction(f_plus),
        "-": BuiltinFunction(f_minus),
        "*": BuiltinFunction(f_multi),
        "/": BuiltinFunction(f_div),

        "eq?": BuiltinFunction(f_eq_p),
        "eqv?": BuiltinFunction(f_eqv_p),
        "equal?": BuiltinFunction(f_equal_p),

        "car": BuiltinFunction(f_car),
        "cdr": BuiltinFunction(f_cdr),
        "cons": BuiltinFunction(f_cons),
        "set-car!": BuiltinFunction(f_set_car_bang),
        "set-cdr!": BuiltinFunction(f_set_cdr_bang),

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

        "apply": BuiltinFunction(f_apply),
    }


def _to_values(args: Sexpr) -> list[int]:
    return [x.value for x in sl.to_python_list(args)]


def _to_lisp_boolean(bool: bool) -> Sexpr:
    return BOOLEAN_T if bool else BOOLEAN_F


def f_not(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(not sp.is_truthy(args.car))


def f_plus(args: Sexpr, evaluator=None) -> Sexpr:
    return Number(sum(_to_values(args)))


def f_minus(args: Sexpr, evaluator=None) -> Sexpr:
    lst = _to_values(args)
    if len(lst) == 1:
        return Number(-lst[0])
    else:
        return Number(reduce(lambda x, y: x - y, lst))


def f_multi(args: Sexpr, evaluator=None) -> Sexpr:
    return Number(reduce(lambda x, y: x * y, _to_values(args), 1))


def f_div(args: Sexpr, evaluator=None) -> Sexpr:
    lst = _to_values(args)
    return Number(reduce(lambda x, y: x / y, lst))


def f_eq_p(args: Sexpr, evaluator=None) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car
    # TODO: eqv?との違いをきちんと実装する
    return _to_lisp_boolean(_eqv(car, cadr))


def _eqv(car: Sexpr, cadr: Sexpr) -> bool:
    match car:
        case Boolean():
            return sp.is_boolean(cadr) and car.value == cadr.value
        case Symbol():
            return sp.is_symbol(cadr) and car.name == cadr.name
        case Number():
            # TODO: 不正確な数値の場合を考慮しないといけない
            return sp.is_number(cadr) and car.value == cadr.value
        case Bytevector():
            pass
        case Char():
            pass
        case Nil():
            return sp.is_null(cadr)
        case _:
            return car is cadr


def f_eqv_p(args: Sexpr, evaluator=None) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car
    return _to_lisp_boolean(_eqv(car, cadr))


def f_equal_p(args: Sexpr, evaluator=None) -> Sexpr:
    if f_eqv_p(args):
        return BOOLEAN_T
    (car, cadr) = args.car, args.cdr.car

    def _equal(car: Sexpr, cadr: Sexpr) -> bool:
        if _eqv(car, cadr):
            return True

        match car:
            case String():
                return sp.is_string(cadr) and car.value == cadr.value
            case Bytevector():
                pass
            case Vector():
                pass
            case Cell():
                return (sp.is_pair(cadr)
                        and _equal(car.car, cadr.car)
                        and _equal(car.cdr, cadr.cdr))
    return _to_lisp_boolean(car == cadr)


def f_car(args: Sexpr, evaluator=None) -> Sexpr:
    arg = sl.car(args)
    return arg.car


def f_cdr(args: Sexpr, evaluator=None) -> Sexpr:
    arg = sl.car(args)
    return arg.cdr


def f_cons(args: Sexpr, evaluator=None) -> Sexpr:
    (car, cadr) = args.car, args.cdr.car
    return sl.cons(car, cadr)


def f_set_car_bang(args: Sexpr, evaluator=None) -> Sexpr:
    (pair, obj) = args.car, args.cdr.car
    if not sp.is_pair(pair):
        raise Exception("set-car!: pair required, given: " + str(pair))
    pair.car = obj
    return NIL


def f_set_cdr_bang(args: Sexpr, evaluator=None) -> Sexpr:
    (pair, obj) = args.car, args.cdr.car
    if not sp.is_pair(pair):
        raise Exception("set-car!: pair required, given: " + str(pair))
    pair.cdr = obj
    return NIL


def f_print(args: Sexpr, evaluator=None) -> Sexpr:
    print(args.car)
    return NIL


def f_boolean_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_boolean(args.car))


def f_char_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_char(args.car))


def f_null_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_null(args.car))


def f_pair_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_pair(args.car))


def f_procedure_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_procedure(args.car))


def f_symbol_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_symbol(args.car))


def f_bytevector_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_bytevector(args.car))


def f_eof_object_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_eof_object(args.car))


def f_number_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_number(args.car))


def f_port_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_port(args.car))


def f_string_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_string(args.car))


def f_vector_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_vector(args.car))


def f_apply(args: Sexpr, evaluator=None) -> Sexpr:
    # this supports (apply fn args) [args is a proper list]
    # support (apply fn arg1 arg2 ... . argn) [argn are proper list]

    def helper(args: Sexpr) -> Sexpr:
        if sp.is_null(args.cdr):
            if sp.is_list(args.car):
                return args.car
            else:
                raise Exception("last argument is not a proper list")
        else:
            return sl.cons(args.car, helper(args.cdr))

    proc = args.car
    arg = helper(args.cdr)
    sexp = (sl.cons(proc, arg))
    return evaluator.eval(sexp)


# TODO: (include string1, string2, ...)
# TODO: (include-ci string1, string2, ...)
