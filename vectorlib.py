"""R5RS vector procedures."""

from sexpr import Sexpr, NIL, BuiltinFunction, Vector, Number
import scpredicates as sp
import sclist as sl


def export() -> dict[str, BuiltinFunction]:
    return {
        "make-vector": BuiltinFunction(f_make_vector),
        "vector": BuiltinFunction(f_vector),
        "vector-length": BuiltinFunction(f_vector_length),
        "vector-ref": BuiltinFunction(f_vector_ref),
        "vector-set!": BuiltinFunction(f_vector_set_bang),
        "vector->list": BuiltinFunction(f_vector_to_list),
        "list->vector": BuiltinFunction(f_list_to_vector),
        "vector-fill!": BuiltinFunction(f_vector_fill_bang),
    }


def _vector_arg(sexpr: Sexpr) -> Vector:
    if not sp.is_vector(sexpr):
        raise Exception("vector required")
    return sexpr


def f_make_vector(args: Sexpr, evaluator=None) -> Sexpr:
    length = int(args.car.value)
    fill = NIL if sp.is_null(args.cdr) else args.cdr.car
    return Vector([fill] * length)


def f_vector(args: Sexpr, evaluator=None) -> Sexpr:
    return Vector(sl.to_python_list(args))


def f_vector_length(args: Sexpr, evaluator=None) -> Sexpr:
    return Number(len(_vector_arg(args.car).value))


def f_vector_ref(args: Sexpr, evaluator=None) -> Sexpr:
    vec = _vector_arg(args.car)
    index = int(args.cdr.car.value)
    return vec.value[index]


def f_vector_set_bang(args: Sexpr, evaluator=None) -> Sexpr:
    vec = _vector_arg(args.car)
    index = int(args.cdr.car.value)
    vec.value[index] = args.cdr.cdr.car
    return NIL


def f_vector_to_list(args: Sexpr, evaluator=None) -> Sexpr:
    items = _vector_arg(args.car).value
    result = NIL
    for item in reversed(items):
        result = sl.cons(item, result)
    return result


def f_list_to_vector(args: Sexpr, evaluator=None) -> Sexpr:
    return Vector(sl.to_python_list(args.car))


def f_vector_fill_bang(args: Sexpr, evaluator=None) -> Sexpr:
    vector = _vector_arg(args.car)
    fill = args.cdr.car
    vector.value[:] = [fill] * len(vector.value)
    return NIL
