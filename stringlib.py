"""R5RS string procedures."""

from sexpr import Sexpr, NIL, BuiltinFunction, String, Symbol, Number
import scpredicates as sp
import sclist as sl


def export() -> dict[str, BuiltinFunction]:
    return {
        "make-string": BuiltinFunction(f_make_string),
        "string": BuiltinFunction(f_string),
        "string-length": BuiltinFunction(f_string_length),
        "string-ref": BuiltinFunction(f_string_ref),
        "string-set!": BuiltinFunction(f_string_set_bang),
        "substring": BuiltinFunction(f_substring),
        "string-copy": BuiltinFunction(f_string_copy),
        "string-append": BuiltinFunction(f_string_append),
        "string=?": BuiltinFunction(f_string_eq_p),
        "string<?": BuiltinFunction(f_string_lt_p),
        "string>?": BuiltinFunction(f_string_gt_p),
        "string<=?": BuiltinFunction(f_string_le_p),
        "string>=?": BuiltinFunction(f_string_ge_p),
        "string-ci=?": BuiltinFunction(f_string_ci_eq_p),
        "string-ci<?": BuiltinFunction(f_string_ci_lt_p),
        "string-ci>?": BuiltinFunction(f_string_ci_gt_p),
        "string-ci<=?": BuiltinFunction(f_string_ci_le_p),
        "string-ci>=?": BuiltinFunction(f_string_ci_ge_p),
        "string-fill!": BuiltinFunction(f_string_fill_bang),
        "string->list": BuiltinFunction(f_string_to_list),
        "list->string": BuiltinFunction(f_list_to_string),
        "string->symbol": BuiltinFunction(f_string_to_symbol),
        "symbol->string": BuiltinFunction(f_symbol_to_string),
    }


def _to_bool(value: bool) -> Sexpr:
    from sexpr import BOOLEAN_T, BOOLEAN_F
    return BOOLEAN_T if value else BOOLEAN_F


def _str_arg(sexpr: Sexpr) -> str:
    if not sp.is_string(sexpr):
        raise Exception("string required")
    return sexpr.value


def _strings(args: Sexpr) -> tuple[str, str]:
    return _str_arg(args.car), _str_arg(args.cdr.car)


def f_make_string(args: Sexpr, evaluator=None) -> Sexpr:
    length = int(args.car.value)
    if sp.is_null(args.cdr):
        fill = " "
    elif sp.is_char(args.cdr.car):
        fill = args.cdr.car.value
    else:
        raise Exception("char required")
    return String(fill * length)


def f_string(args: Sexpr, evaluator=None) -> Sexpr:
    values = []
    for item in sl.to_python_list(args):
        if sp.is_char(item):
            values.append(item.value)
        else:
            raise Exception("char required")
    return String("".join(values))


def f_string_length(args: Sexpr, evaluator=None) -> Sexpr:
    return Number(len(_str_arg(args.car)))


def f_string_ref(args: Sexpr, evaluator=None) -> Sexpr:
    from sexpr import Char
    text = _str_arg(args.car)
    index = int(args.cdr.car.value)
    return Char(text[index])


def f_string_set_bang(args: Sexpr, evaluator=None) -> Sexpr:
    text = _str_arg(args.car)
    index = int(args.cdr.car.value)
    ch = args.cdr.cdr.car.value
    if not sp.is_char(args.cdr.cdr.car):
        raise Exception("char required")
    chars = list(text)
    chars[index] = ch
    args.car.value = "".join(chars)
    return NIL


def f_substring(args: Sexpr, evaluator=None) -> Sexpr:
    text = _str_arg(args.car)
    start = int(args.cdr.car.value)
    end = int(args.cdr.cdr.car.value)
    return String(text[start:end])


def f_string_copy(args: Sexpr, evaluator=None) -> Sexpr:
    return String(_str_arg(args.car))


def f_string_append(args: Sexpr, evaluator=None) -> Sexpr:
    parts = [_str_arg(item) for item in sl.to_python_list(args)]
    return String("".join(parts))


def f_string_eq_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a == b)


def f_string_lt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a < b)


def f_string_gt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a > b)


def f_string_le_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a <= b)


def f_string_ge_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a >= b)


def f_string_ci_eq_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a.lower() == b.lower())


def f_string_ci_lt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a.lower() < b.lower())


def f_string_ci_gt_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a.lower() > b.lower())


def f_string_ci_le_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a.lower() <= b.lower())


def f_string_ci_ge_p(args: Sexpr, evaluator=None) -> Sexpr:
    a, b = _strings(args)
    return _to_bool(a.lower() >= b.lower())


def f_string_fill_bang(args: Sexpr, evaluator=None) -> Sexpr:
    from sexpr import Char
    text = _str_arg(args.car)
    if sp.is_null(args.cdr):
        raise Exception("string-fill!: fill character required")
    if not sp.is_char(args.cdr.car):
        raise Exception("char required")
    fill = args.cdr.car.value
    args.car.value = fill * len(text)
    return NIL


def f_string_to_list(args: Sexpr, evaluator=None) -> Sexpr:
    from sexpr import Char
    text = _str_arg(args.car)
    result = NIL
    for ch in reversed(text):
        result = sl.cons(Char(ch), result)
    return result


def f_list_to_string(args: Sexpr, evaluator=None) -> Sexpr:
    chars = []
    for item in sl.to_python_list(args.car):
        if not sp.is_char(item):
            raise Exception("char required")
        chars.append(item.value)
    return String("".join(chars))


def f_string_to_symbol(args: Sexpr, evaluator=None) -> Sexpr:
    return Symbol(_str_arg(args.car))


def f_symbol_to_string(args: Sexpr, evaluator=None) -> Sexpr:
    if not sp.is_symbol(args.car):
        raise Exception("symbol required")
    return String(args.car.name)
