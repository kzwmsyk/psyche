import logging
from typing import Callable
from sexpr import Sexpr, NIL, BuiltinSpecialForm, Lambda, \
    BOOLEAN_T, BOOLEAN_F, Symbol

import sclist as sl
import scpredicates as sp

logger = logging.getLogger(__name__)


def export() -> dict[str, Callable]:
    return {
        "if": BuiltinSpecialForm(f_if),
        "set!": BuiltinSpecialForm(f_set_bang),
        "quote": BuiltinSpecialForm(f_quote),
        "quasiquote": BuiltinSpecialForm(f_quasiquote),
        "lambda": BuiltinSpecialForm(f_lambda),
        "define": BuiltinSpecialForm(f_define),
        "let": BuiltinSpecialForm(f_let),
        "and": BuiltinSpecialForm(f_and),
        "or": BuiltinSpecialForm(f_or),
        "begin": BuiltinSpecialForm(f_begin),
    }


def f_and(evaluator, args: Sexpr) -> Sexpr:
    while not sp.is_null(args):
        if sp.is_falsy(evaluator.eval(sl.car(args))):
            return BOOLEAN_F
        args = sl.cdr(args)
    return BOOLEAN_T


def f_or(evaluator, args: Sexpr) -> Sexpr:
    while not sp.is_null(args):
        if sp.is_truthy(evaluator.eval(sl.car(args))):
            return BOOLEAN_T
        args = sl.cdr(args)
    return BOOLEAN_F


def f_if(evaluator, args: Sexpr) -> Sexpr:
    cond = sl.car(args)

    if sp.is_truthy(evaluator.eval(cond)):
        then_sexpr = sl.cadr(args)
        return evaluator.eval(then_sexpr)
    else:
        else_sexpr = sl.caddr(args)
        return evaluator.eval(else_sexpr)


def f_set_bang(evaluator, args: Sexpr) -> Sexpr:
    evaluator.bind(sl.car(args).name, evaluator.eval(sl.cadr(args)))
    return NIL


def f_define(evaluator, args: Sexpr) -> Sexpr:

    car = sl.car(args)

    if sp.is_symbol(car):
        # (define var expr)
        evaluator.bind(car.name, evaluator.eval(sl.cadr(args)))
        return NIL

    elif sp.is_pair(car):
        # (define (fn x y z ...) body)
        # (define (fn x y z ... . rest) body)
        # (define (fn . rest) body)

        fn = sl.car(car)
        params = sl.cdr(car)
        body = sl.cdr(args)

        lambda_ = Lambda(params=params,
                         body=body,
                         env=evaluator.current_scope)
        evaluator.bind(fn.name, lambda_)
        return NIL

    else:
        raise Exception("Invalid define syntax")


def f_lambda(evaluator, args: Sexpr) -> Sexpr:
    params = sl.car(args)
    body = sl.cdr(args)
    lambda_ = Lambda(params=params,
                     body=body,
                     env=evaluator.current_scope)
    return lambda_


def f_quote(evaluator, args: Sexpr) -> Sexpr:
    return sl.car(args)


def f_quasiquote(evaluator, args: Sexpr) -> Sexpr:
    sexpr = sl.car(args)
    return _expand_quasiquote(evaluator, sexpr)


def _expand_quasiquote(evaluator, sexpr: Sexpr) -> Sexpr:
    if not sp.is_pair(sexpr):
        return sexpr

    elif sp.is_pair(sexpr) and sl.car(sexpr) == Symbol("unquote"):
        # ,expr => (unquote expr) => eval(expr)
        return evaluator.eval(sl.cadr(sexpr))

    elif sp.is_pair(sexpr):
        # (not-unquote ... ,@expr ...)
        # => (not-unquote... (unquote-splicing expr) ...)
        # or
        # (,@expr ...)
        # => ((unquote-splicing expr) ...)
        # by recursion.

        car = sl.car(sexpr)
        cdr = sl.cdr(sexpr)

        if sp.is_pair(car) and car.car == Symbol("unquote-splicing"):
            ls = evaluator.eval(sl.cadr(car))
            if not sp.is_list(ls):
                raise Exception("Unquote-splicing must be a list")

            return _append(ls, _expand_quasiquote(evaluator, cdr))
        else:
            return sl.cons(_expand_quasiquote(evaluator, car),
                           _expand_quasiquote(evaluator, cdr))


def _append(ls: Sexpr, elem: Sexpr) -> Sexpr:
    assert sp.is_list(ls)

    if sp.is_null(ls):
        if sp.is_list(elem):
            return elem
        else:
            return sl.cons(elem, NIL)
    else:
        return sl.cons(ls.car, _append(ls.cdr, elem))


def f_let(evaluator, args: Sexpr) -> Sexpr:
    vars = sl.car(args)
    body = sl.cdr(args)
    with evaluator.new_env():

        while not sp.is_null(vars):
            pair = vars.car
            symbol = pair.car
            value = evaluator.eval(sl.cadr(pair))
            evaluator.bind(symbol.name, value)
            vars = vars.cdr

        while not sp.is_null(body):
            res = evaluator.eval(body.car)
            body = body.cdr
        return res

# TODO: (let* ...)
# TODO: (letrec ...)
# TODO: (let-values ...)
# TODO: (let*-values ...)
# TODO: (letrec-values ...)
# TODO: (letrec*-values ...)


def f_begin(evaluator, args: Sexpr) -> Sexpr:
    ret = NIL
    while not sp.is_null(args):
        ret = evaluator.eval(args.car)
        args = args.cdr
    return ret


def f_define_syntax(evaluator, args: Sexpr) -> Sexpr:

    pass
