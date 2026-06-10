from sexpr import Sexpr, Number, NIL, BOOLEAN_T, BOOLEAN_F, BuiltinFunction, \
    Boolean, String, Symbol, Char, Bytevector, Vector, Nil, Cell
import sclist as sl
import scpredicates as sp
from typing import Callable
from functools import reduce
import charlib
import stringlib
import vectorlib
import numberlib
import bytevectorlib
import ports
from continuations import InvokeContinuation
from values import MultipleValues
from promise import Promise
import logging
logger = logging.getLogger(__name__)


def export() -> dict[str, Callable]:
    result = {
        "+": BuiltinFunction(f_plus),
        "-": BuiltinFunction(f_minus),
        "*": BuiltinFunction(f_multi),
        "/": BuiltinFunction(f_div),

        "=": BuiltinFunction(f_num_eq),
        "<": BuiltinFunction(f_lt),
        ">": BuiltinFunction(f_gt),
        "<=": BuiltinFunction(f_le),
        ">=": BuiltinFunction(f_ge),

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
        "number?": BuiltinFunction(f_number_p),
        "string?": BuiltinFunction(f_string_p),
        "vector?": BuiltinFunction(f_vector_p),

        "apply": BuiltinFunction(f_apply),
        "map": BuiltinFunction(f_map),
        "for-each": BuiltinFunction(f_for_each),
        "force": BuiltinFunction(f_force),
        "values": BuiltinFunction(f_values),
        "call-with-values": BuiltinFunction(f_call_with_values),
        "call-with-current-continuation": BuiltinFunction(f_call_cc),
        "call/cc": BuiltinFunction(f_call_cc),
        "dynamic-wind": BuiltinFunction(f_dynamic_wind),
        "scheme-report-environment": BuiltinFunction(f_scheme_report_environment),
        "null-environment": BuiltinFunction(f_null_environment),
    }
    result.update(charlib.export())
    result.update(stringlib.export())
    result.update(vectorlib.export())
    result.update(numberlib.export())
    result.update(bytevectorlib.export())
    result.update(ports.export())
    result["eof-object"] = ports.EOF_OBJECT
    return result


def _to_values(args: Sexpr) -> list[int | float]:
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


def _compare_args(args: Sexpr) -> tuple[Sexpr, Sexpr]:
    return args.car, args.cdr.car


def _as_numbers(car: Sexpr, cadr: Sexpr) -> tuple[int | float, int | float]:
    if not sp.is_number(car) or not sp.is_number(cadr):
        raise Exception("number required")
    return car.value, cadr.value


def f_num_eq(args: Sexpr, evaluator=None) -> Sexpr:
    car, cadr = _compare_args(args)
    left, right = _as_numbers(car, cadr)
    return _to_lisp_boolean(left == right)


def f_lt(args: Sexpr, evaluator=None) -> Sexpr:
    car, cadr = _compare_args(args)
    left, right = _as_numbers(car, cadr)
    return _to_lisp_boolean(left < right)


def f_gt(args: Sexpr, evaluator=None) -> Sexpr:
    car, cadr = _compare_args(args)
    left, right = _as_numbers(car, cadr)
    return _to_lisp_boolean(left > right)


def f_le(args: Sexpr, evaluator=None) -> Sexpr:
    car, cadr = _compare_args(args)
    left, right = _as_numbers(car, cadr)
    return _to_lisp_boolean(left <= right)


def f_ge(args: Sexpr, evaluator=None) -> Sexpr:
    car, cadr = _compare_args(args)
    left, right = _as_numbers(car, cadr)
    return _to_lisp_boolean(left >= right)


def f_eq_p(args: Sexpr, evaluator=None) -> Sexpr:
    car, cadr = _compare_args(args)
    return _to_lisp_boolean(_eq(car, cadr))


def _eq(car: Sexpr, cadr: Sexpr) -> bool:
    if car is cadr:
        return True

    match car:
        case Boolean():
            return sp.is_boolean(cadr) and car.value == cadr.value
        case Symbol():
            return sp.is_symbol(cadr) and car.name == cadr.name
        case Nil():
            return sp.is_null(cadr)
        case Cell() | String() | Vector() | Bytevector():
            return False
        case Number() | Char():
            return False
        case _:
            return False


def _eqv(car: Sexpr, cadr: Sexpr) -> bool:
    if car is cadr:
        return True

    match car:
        case Boolean():
            return sp.is_boolean(cadr) and car.value == cadr.value
        case Symbol():
            return sp.is_symbol(cadr) and car.name == cadr.name
        case Number():
            return sp.is_number(cadr) and car.value == cadr.value
        case Char():
            return sp.is_char(cadr) and car.value == cadr.value
        case Nil():
            return sp.is_null(cadr)
        case _:
            return False


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
            case Vector():
                return (sp.is_vector(cadr)
                        and len(car.value) == len(cadr.value)
                        and all(_equal(a, b)
                                for a, b in zip(car.value, cadr.value)))
            case Bytevector():
                return (sp.is_bytevector(cadr)
                        and car.value == cadr.value)
            case Cell():
                return (sp.is_pair(cadr)
                        and _equal(car.car, cadr.car)
                        and _equal(car.cdr, cadr.cdr))
            case _:
                return False
    return _to_lisp_boolean(_equal(car, cadr))


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


def f_number_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_number(args.car))


def f_string_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_string(args.car))


def f_vector_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(sp.is_vector(args.car))


def f_map(args: Sexpr, evaluator=None) -> Sexpr:
    proc = args.car
    lists = sl.to_python_list(args.cdr)
    if not lists:
        raise Exception("map: at least one list required")

    py_lists: list[list[Sexpr]] = []
    for lst in lists:
        if not sp.is_list(lst):
            raise Exception("map: list required")
        py_lists.append(sl.to_python_list(lst))

    if not py_lists[0]:
        return NIL

    length = len(py_lists[0])
    if any(len(items) != length for items in py_lists):
        raise Exception("map: lists differ in length")

    results: list[Sexpr] = []
    for i in range(length):
        call_args = sl.from_python_list([items[i] for items in py_lists])
        results.append(evaluator.apply(proc, call_args))
    return sl.from_python_list(results)


def f_for_each(args: Sexpr, evaluator=None) -> Sexpr:
    proc = args.car
    lists = sl.to_python_list(args.cdr)
    if not lists:
        raise Exception("for-each: at least one list required")

    py_lists: list[list[Sexpr]] = []
    for lst in lists:
        if not sp.is_list(lst):
            raise Exception("for-each: list required")
        py_lists.append(sl.to_python_list(lst))

    if not py_lists[0]:
        return NIL

    length = len(py_lists[0])
    if any(len(items) != length for items in py_lists):
        raise Exception("for-each: lists differ in length")

    for i in range(length):
        call_args = sl.from_python_list([items[i] for items in py_lists])
        evaluator.apply(proc, call_args)
    return NIL


def f_force(args: Sexpr, evaluator=None) -> Sexpr:
    promise = args.car
    if not isinstance(promise, Promise):
        return promise
    if not promise.evaluated:
        promise.value = promise.thunk()
        promise.evaluated = True
    return promise.value


def f_values(args: Sexpr, evaluator=None) -> MultipleValues:
    return MultipleValues(sl.to_python_list(args))


def f_call_with_values(args: Sexpr, evaluator=None) -> Sexpr:
    producer = args.car
    consumer = args.cdr.car
    produced = evaluator.apply_for_values(producer, NIL)
    if isinstance(produced, MultipleValues):
        call_args = sl.from_python_list(produced.values)
    else:
        call_args = sl.cons(produced, NIL)
    return evaluator.apply(consumer, call_args)


def f_call_cc(args: Sexpr, evaluator=None) -> Sexpr:
    proc = args.car

    def invoke_k(k_args: Sexpr, evaluator=None) -> Sexpr:
        raise InvokeContinuation(k_args.car)

    continuation = BuiltinFunction(invoke_k)
    try:
        return evaluator.apply(proc, sl.cons(continuation, NIL))
    except InvokeContinuation as exc:
        return exc.value


def f_dynamic_wind(args: Sexpr, evaluator=None) -> Sexpr:
    before = args.car
    thunk = args.cdr.car
    after = args.cdr.cdr.car
    evaluator.apply(before, NIL)
    try:
        return evaluator.apply(thunk, NIL)
    finally:
        evaluator.apply(after, NIL)


def f_scheme_report_environment(args: Sexpr, evaluator=None) -> Sexpr:
    import specialform as sf
    version = int(args.car.value)
    return sf.SchemeReportEnvironment(version)


def f_null_environment(args: Sexpr, evaluator=None) -> Sexpr:
    import specialform as sf
    version = int(args.car.value)
    return sf.NullEnvironment(version)


def f_apply(args: Sexpr, evaluator=None) -> Sexpr:
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
