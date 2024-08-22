from common import Sexpr,  is_nil, NIL, car, cadr, caddr, cdr
from typing import Callable


def export() -> dict[str, Callable]:
    return {
        "if": f_if,
        "setq": f_setq,
        "defun": f_defun,
        "quote": f_quote,
    }


def f_if(evaluator, args: Sexpr) -> Sexpr:
    cond = car(args)

    if not is_nil(evaluator.eval(cond)):
        then_sexpr = cadr(args)
        return evaluator.eval(then_sexpr)
    else:
        else_sexpr = caddr(args)
        return evaluator.eval(else_sexpr)


def f_setq(evaluator, args: Sexpr) -> Sexpr:
    evaluator.bind_sexpr(car(args), evaluator.eval(cadr(args)))
    return NIL


def f_defun(evaluator, args: Sexpr) -> Sexpr:
    evaluator.bind_function(car(args), cdr(args))


def f_quote(evaluator, args: Sexpr) -> Sexpr:
    return car(args)
