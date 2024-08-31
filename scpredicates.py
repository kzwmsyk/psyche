
from sexpr import Sexpr, Cell, Nil, Symbol, Number, String, \
    BOOLEAN_T, BOOLEAN_F


def is_boolean(expr: Sexpr) -> bool:
    "boolean?"
    return expr == BOOLEAN_T or expr == BOOLEAN_F


def is_char(expr: Sexpr) -> bool:
    "char?"
    pass


def is_null(expr: Sexpr) -> bool:
    "null?"
    return isinstance(expr, Nil)


def is_pair(expr: Sexpr) -> bool:
    "pair?"
    return isinstance(expr, Cell)


def is_procedure(expr: Sexpr) -> bool:
    "procedure?"
    pass


def is_symbol(expr: Sexpr) -> bool:
    "symbol?"
    return isinstance(expr, Symbol)


def is_bytevector(expr: Sexpr) -> bool:
    "bytevector?"
    pass


def is_eof_object(expr: Sexpr) -> bool:
    "eof-object?"
    pass


def is_number(expr: Sexpr) -> bool:
    "number?"
    return isinstance(expr, Number)


def is_port(expr: Sexpr) -> bool:
    "port?"
    pass


def is_string(expr: Sexpr) -> bool:
    "string?"
    return isinstance(expr, String)


def is_vector(expr: Sexpr) -> bool:
    "vector?"
    pass


def is_truthy(expr: Sexpr) -> bool:
    return not (is_boolean(expr) and expr == BOOLEAN_F)


def is_falsy(expr: Sexpr) -> bool:
    return is_boolean(expr) and expr == BOOLEAN_F


def is_atom(expr: Sexpr) -> bool:
    return not is_pair(expr) and not is_null(expr)


def is_list(expr: Sexpr) -> bool:
    if is_null(expr):
        return True
    elif is_pair(expr):
        return is_list(expr.cdr)
    else:
        return False
