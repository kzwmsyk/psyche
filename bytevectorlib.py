"""R5RS bytevector procedures."""

from sexpr import Sexpr, NIL, BuiltinFunction, Bytevector, Number
import scpredicates as sp
import sclist as sl


def export() -> dict[str, BuiltinFunction]:
    return {
        "make-bytevector": BuiltinFunction(f_make_bytevector),
        "bytevector?": BuiltinFunction(f_bytevector_p),
        "bytevector-length": BuiltinFunction(f_bytevector_length),
        "bytevector-ref": BuiltinFunction(f_bytevector_ref),
        "bytevector-set!": BuiltinFunction(f_bytevector_set_bang),
        "bytevector": BuiltinFunction(f_bytevector),
        "list->bytevector": BuiltinFunction(f_list_to_bytevector),
        "bytevector->list": BuiltinFunction(f_bytevector_to_list),
    }


def _bv_arg(sexpr: Sexpr) -> Bytevector:
    if not sp.is_bytevector(sexpr):
        raise Exception("bytevector required")
    return sexpr


def _byte_arg(sexpr: Sexpr) -> int:
    if not sp.is_number(sexpr):
        raise Exception("number required")
    value = int(sexpr.value)
    if value < 0 or value > 255:
        raise Exception("byte out of range")
    return value


def f_make_bytevector(args: Sexpr, evaluator=None) -> Sexpr:
    length = int(args.car.value)
    fill = 0 if sp.is_null(args.cdr) else _byte_arg(args.cdr.car)
    return Bytevector(bytearray([fill] * length))


def f_bytevector_p(args: Sexpr, evaluator=None) -> Sexpr:
    from sexpr import BOOLEAN_T, BOOLEAN_F
    return BOOLEAN_T if sp.is_bytevector(args.car) else BOOLEAN_F


def f_bytevector_length(args: Sexpr, evaluator=None) -> Sexpr:
    return Number(len(_bv_arg(args.car).value))


def f_bytevector_ref(args: Sexpr, evaluator=None) -> Sexpr:
    bv = _bv_arg(args.car)
    index = int(args.cdr.car.value)
    return Number(bv.value[index])


def f_bytevector_set_bang(args: Sexpr, evaluator=None) -> Sexpr:
    bv = _bv_arg(args.car)
    index = int(args.cdr.car.value)
    bv.value[index] = _byte_arg(args.cdr.cdr.car)
    return NIL


def f_bytevector(args: Sexpr, evaluator=None) -> Sexpr:
    return Bytevector(bytearray(_byte_arg(item) for item in sl.to_python_list(args)))


def f_list_to_bytevector(args: Sexpr, evaluator=None) -> Sexpr:
    return Bytevector(bytearray(_byte_arg(item) for item in sl.to_python_list(args.car)))


def f_bytevector_to_list(args: Sexpr, evaluator=None) -> Sexpr:
    result = NIL
    for byte in reversed(_bv_arg(args.car).value):
        result = sl.cons(Number(byte), result)
    return result
