import logging
from typing import Callable
from sexpr import Sexpr, NIL, BuiltinSpecialForm, Lambda

import sclist as sc

logger = logging.getLogger(__name__)


def export() -> dict[str, Callable]:
    return {
        "if": BuiltinSpecialForm(f_if),
        "setq": BuiltinSpecialForm(f_setq),
        "defun": BuiltinSpecialForm(f_defun),
        "quote": BuiltinSpecialForm(f_quote),
        "lambda": BuiltinSpecialForm(f_lambda),
        "define": BuiltinSpecialForm(f_define),
        "let": BuiltinSpecialForm(f_let),
    }


def f_if(evaluator, args: Sexpr) -> Sexpr:
    cond = sc.car(args)

    if not sc.is_nil(evaluator.eval(cond)):
        then_sexpr = sc.cadr(args)
        return evaluator.eval(then_sexpr)
    else:
        else_sexpr = sc.caddr(args)
        return evaluator.eval(else_sexpr)


def f_setq(evaluator, args: Sexpr) -> Sexpr:
    evaluator.bind(sc.car(args).name, evaluator.eval(sc.cadr(args)))
    return NIL

# (defun name (params...) body)


def f_define(evaluator, args: Sexpr) -> Sexpr:
    evaluator.bind(sc.car(args).name, evaluator.eval(sc.cadr(args)))
    return NIL


def f_defun(evaluator, args: Sexpr) -> Sexpr:
    symbol = sc.car(args)
    params = sc.cadr(args)
    body = sc.cddr(args)
    fn = Lambda(params, body, evaluator.current_scope)
    evaluator.bind(symbol.name, fn)
    return fn


def f_lambda(evaluator, args: Sexpr) -> Sexpr:
    params = sc.car(args)
    body = sc.cdr(args)
    lambda_ = Lambda(params=params,
                     body=body,
                     env=evaluator.current_scope)
    return lambda_


def f_quote(evaluator, args: Sexpr) -> Sexpr:
    return sc.car(args)


def f_let(evaluator, args: Sexpr) -> Sexpr:
    vars = sc.car(args)
    body = sc.cdr(args)
    with evaluator.new_env():

        while not sc.is_nil(vars):
            pair = vars.car
            symbol = pair.car
            value = evaluator.eval(sc.cadr(pair))
            evaluator.bind(symbol.name, value)
            vars = vars.cdr

        while not sc.is_nil(body):
            res = evaluator.eval(body.car)
            body = body.cdr
        return res
