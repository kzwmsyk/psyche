"""R5RS character procedures."""

from sexpr import Sexpr, NIL, BuiltinFunction, Char, Number
import scpredicates as sp


def export() -> dict[str, BuiltinFunction]:
    return {
        "char=?": BuiltinFunction(f_char_eq_p),
        "char<?": BuiltinFunction(f_char_lt_p),
        "char>?": BuiltinFunction(f_char_gt_p),
        "char<=?": BuiltinFunction(f_char_le_p),
        "char>=?": BuiltinFunction(f_char_ge_p),
        "char-ci=?": BuiltinFunction(f_char_ci_eq_p),
        "char-ci<?": BuiltinFunction(f_char_ci_lt_p),
        "char-ci>?": BuiltinFunction(f_char_ci_gt_p),
        "char-ci<=?": BuiltinFunction(f_char_ci_le_p),
        "char-ci>=?": BuiltinFunction(f_char_ci_ge_p),
        "char-alphabetic?": BuiltinFunction(f_char_alphabetic_p),
        "char-numeric?": BuiltinFunction(f_char_numeric_p),
        "char-whitespace?": BuiltinFunction(f_char_whitespace_p),
        "char-upper-case?": BuiltinFunction(f_char_upper_case_p),
        "char-lower-case?": BuiltinFunction(f_char_lower_case_p),
        "char-upcase": BuiltinFunction(f_char_upcase),
        "char-downcase": BuiltinFunction(f_char_downcase),
        "char->integer": BuiltinFunction(f_char_to_integer),
        "integer->char": BuiltinFunction(f_integer_to_char),
    }


def _to_bool(value: bool) -> Sexpr:
    from sexpr import BOOLEAN_T, BOOLEAN_F
    return BOOLEAN_T if value else BOOLEAN_F


def _chars(args: Sexpr) -> tuple[str, str]:
    left, right = args.car, args.cdr.car
    if not sp.is_char(left) or not sp.is_char(right):
        raise Exception("char required")
    return left.value, right.value


def f_char_eq_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a == b)


def f_char_lt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a < b)


def f_char_gt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a > b)


def f_char_le_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a <= b)


def f_char_ge_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a >= b)


def f_char_ci_eq_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a.lower() == b.lower())


def f_char_ci_lt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a.lower() < b.lower())


def f_char_ci_gt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a.lower() > b.lower())


def f_char_ci_le_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a.lower() <= b.lower())


def f_char_ci_ge_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _chars(args)
    return _to_bool(a.lower() >= b.lower())


def f_char_alphabetic_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        return _to_bool(False)
    return _to_bool(args.car.value.isalpha())


def f_char_numeric_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        return _to_bool(False)
    return _to_bool(args.car.value.isdigit())


def f_char_whitespace_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        return _to_bool(False)
    return _to_bool(args.car.value in " \t\n\r\f\v")


def f_char_upper_case_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        return _to_bool(False)
    ch = args.car.value
    return _to_bool(len(ch) == 1 and ch.isupper())


def f_char_lower_case_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        return _to_bool(False)
    ch = args.car.value
    return _to_bool(len(ch) == 1 and ch.islower())


def f_char_upcase(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        raise Exception("char required")
    return Char(args.car.value.upper())


def f_char_downcase(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        raise Exception("char required")
    return Char(args.car.value.lower())


def f_char_to_integer(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_char(args.car):
        raise Exception("char required")
    return Number(ord(args.car.value))


def f_integer_to_char(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_number(args.car):
        raise Exception("number required")
    return Char(chr(int(args.car.value)))
