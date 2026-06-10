"""R5RS number procedures."""

from __future__ import annotations

import math

from sexpr import Sexpr, BuiltinFunction, Number, String
import scpredicates as sp
import sclist as sl


def export() -> dict[str, BuiltinFunction]:
    return {
        "exact?": BuiltinFunction(f_exact_p),
        "inexact?": BuiltinFunction(f_inexact_p),
        "integer?": BuiltinFunction(f_integer_p),
        "complex?": BuiltinFunction(f_complex_p),
        "real?": BuiltinFunction(f_real_p),
        "rational?": BuiltinFunction(f_rational_p),
        "number->string": BuiltinFunction(f_number_to_string),
        "string->number": BuiltinFunction(f_string_to_number),
        "abs": BuiltinFunction(f_abs),
        "max": BuiltinFunction(f_max),
        "min": BuiltinFunction(f_min),
        "quotient": BuiltinFunction(f_quotient),
        "remainder": BuiltinFunction(f_remainder),
        "modulo": BuiltinFunction(f_modulo),
        "gcd": BuiltinFunction(f_gcd),
        "lcm": BuiltinFunction(f_lcm),
        "floor": BuiltinFunction(f_floor),
        "ceiling": BuiltinFunction(f_ceiling),
        "truncate": BuiltinFunction(f_truncate),
        "round": BuiltinFunction(f_round),
        "exact->inexact": BuiltinFunction(f_exact_to_inexact),
        "inexact->exact": BuiltinFunction(f_inexact_to_exact),
        "expt": BuiltinFunction(f_expt),
        "sqrt": BuiltinFunction(f_sqrt),
    }


def _to_bool(value: bool) -> Sexpr:
    from sexpr import BOOLEAN_T, BOOLEAN_F
    return BOOLEAN_T if value else BOOLEAN_F


def _num_values(args: Sexpr) -> list[int | float]:
    return [item.value for item in sl.to_python_list(args)]


def _as_number(value: int | float, *, exact: bool | None = None) -> Number:
    if exact is False or isinstance(value, float):
        return Number(float(value))
    if isinstance(value, float) and value.is_integer():
        return Number(int(value))
    return Number(value)


def f_exact_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_number(args.car):
        return _to_bool(False)
    return _to_bool(isinstance(args.car.value, int) and not isinstance(args.car.value, bool))


def f_inexact_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_number(args.car):
        return _to_bool(False)
    return _to_bool(isinstance(args.car.value, float))


def f_integer_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_number(args.car):
        return _to_bool(False)
    value = args.car.value
    if isinstance(value, float):
        return _to_bool(value.is_integer())
    return _to_bool(True)


def f_complex_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_bool(sp.is_number(args.car))


def f_real_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_bool(sp.is_number(args.car))


def f_rational_p(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_number(args.car):
        return _to_bool(False)
    value = args.car.value
    if isinstance(value, float):
        return _to_bool(value.is_integer())
    return _to_bool(True)


def f_number_to_string(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_number(args.car):
        raise Exception("number required")
    return String(str(args.car.value))


def f_string_to_number(args: Sexpr, evaluator=None) -> Sexpr:
    from sexpr import BOOLEAN_F
    if not sp.is_string(args.car):
        raise Exception("string required")
    text = args.car.value.strip()
    if text == "":
        return BOOLEAN_F
    try:
        if any(marker in text for marker in (".", "e", "E")):
            return Number(float(text))
        return Number(int(text))
    except ValueError:
        return BOOLEAN_F


def f_abs(args: Sexpr, evaluator=None) -> Sexpr:
    value = args.car.value
    if isinstance(value, int):
        return Number(abs(value))
    return Number(abs(float(value)))


def f_max(args: Sexpr, evaluator=None) -> Sexpr:
    values = _num_values(args)
    return _as_number(max(values))


def f_min(args: Sexpr, evaluator=None) -> Sexpr:
    values = _num_values(args)
    return _as_number(min(values))


def f_quotient(args: Sexpr, evaluator=None) -> Sexpr:
    n, d = args.car.value, args.cdr.car.value
    return Number(math.trunc(n / d))


def f_remainder(args: Sexpr, evaluator=None) -> Sexpr:
    n, d = args.car.value, args.cdr.car.value
    return Number(n - d * math.trunc(n / d))


def f_modulo(args: Sexpr, evaluator=None) -> Sexpr:
    n, d = args.car.value, args.cdr.car.value
    return Number(n - d * math.floor(n / d))


def f_gcd(args: Sexpr, evaluator=None) -> Sexpr:
    values = [int(v) for v in _num_values(args)]
    return Number(math.gcd(*values))


def f_lcm(args: Sexpr, evaluator=None) -> Sexpr:
    values = [int(v) for v in _num_values(args)]
    result = 1
    for value in values:
        result = math.lcm(result, value)
    return Number(result)


def _int_result(value: float) -> Number:
    if float(value).is_integer():
        return Number(int(value))
    return Number(value)


def f_floor(args: Sexpr, evaluator=None) -> Sexpr:
    return _int_result(math.floor(args.car.value))


def f_ceiling(args: Sexpr, evaluator=None) -> Sexpr:
    return _int_result(math.ceil(args.car.value))


def f_truncate(args: Sexpr, evaluator=None) -> Sexpr:
    return _int_result(math.trunc(args.car.value))


def f_round(args: Sexpr, evaluator=None) -> Sexpr:
    return _int_result(round(args.car.value))


def f_exact_to_inexact(args: Sexpr, evaluator=None) -> Sexpr:
    return Number(float(args.car.value))


def f_inexact_to_exact(args: Sexpr, evaluator=None) -> Sexpr:
    value = args.car.value
    if isinstance(value, float) and value.is_integer():
        return Number(int(value))
    return Number(value)


def f_expt(args: Sexpr, evaluator=None) -> Sexpr:
    base, exp = args.car.value, args.cdr.car.value
    result = base ** exp
    if isinstance(result, float) and result.is_integer():
        return Number(int(result))
    return Number(result)


def f_sqrt(args: Sexpr, evaluator=None) -> Sexpr:
    return Number(math.sqrt(args.car.value))
