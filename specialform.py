import logging
from typing import Callable
from sexpr import Sexpr, NIL, BuiltinSpecialForm, Lambda, Macro, \
    BOOLEAN_T, BOOLEAN_F, Symbol
from syntaxobject import resolve_literal_descriptor

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
        "let*": BuiltinSpecialForm(f_let_star),
        "letrec": BuiltinSpecialForm(f_letrec),
        "cond": BuiltinSpecialForm(f_cond),
        "and": BuiltinSpecialForm(f_and),
        "or": BuiltinSpecialForm(f_or),
        "begin": BuiltinSpecialForm(f_begin),
        "define-syntax": BuiltinSpecialForm(f_define_syntax),
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
        if sp.is_null(sl.cddr(args)):
            return NIL
        else_sexpr = sl.caddr(args)
        return evaluator.eval(else_sexpr)


def f_set_bang(evaluator, args: Sexpr) -> Sexpr:
    name = sl.car(args).name
    value = evaluator.eval(sl.cadr(args))
    evaluator.assign(name, value)
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
    if sp.is_symbol(sl.car(args)):
        return _named_let(evaluator, args)

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


def _named_let(evaluator, args: Sexpr) -> Sexpr:
    name = sl.car(args)
    vars = sl.cadr(args)
    body = sl.cddr(args)

    param_list: list[Symbol] = []
    init_exprs: list[Sexpr] = []
    while not sp.is_null(vars):
        pair = vars.car
        param_list.append(pair.car)
        init_exprs.append(sl.cadr(pair))
        vars = vars.cdr

    params = sl.from_python_list(param_list)
    lambda_ = Lambda(params=params, body=body, env=evaluator.current_scope)
    evaled_inits = [evaluator.eval(init) for init in init_exprs]

    with evaluator.new_env():
        evaluator.bind(name.name, lambda_)
        with evaluator.new_env():
            for param, value in zip(param_list, evaled_inits):
                evaluator.bind(param.name, value)
            while not sp.is_null(body):
                res = evaluator.eval(body.car)
                body = body.cdr
            return res


def f_let_star(evaluator, args: Sexpr) -> Sexpr:
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


def f_letrec(evaluator, args: Sexpr) -> Sexpr:
    vars = sl.car(args)
    body = sl.cdr(args)
    inits: list[tuple[Symbol, Sexpr]] = []

    with evaluator.new_env():
        while not sp.is_null(vars):
            pair = vars.car
            symbol = pair.car
            evaluator.bind(symbol.name, NIL)
            inits.append((symbol, sl.cadr(pair)))
            vars = vars.cdr

        for symbol, init in inits:
            evaluator.assign(symbol.name, evaluator.eval(init))

        while not sp.is_null(body):
            res = evaluator.eval(body.car)
            body = body.cdr
        return res


def f_cond(evaluator, args: Sexpr) -> Sexpr:
    while not sp.is_null(args):
        clause = args.car
        if not sp.is_pair(clause):
            raise Exception("cond: invalid clause")

        if sp.is_symbol(clause.car) and clause.car.name == "else":
            body = clause.cdr
            while not sp.is_null(body):
                res = evaluator.eval(body.car)
                body = body.cdr
            return res

        test_result = evaluator.eval(clause.car)
        if sp.is_truthy(test_result):
            rest = clause.cdr
            if sp.is_null(rest):
                return test_result
            if sp.is_symbol(rest.car) and rest.car.name == "=>":
                proc = evaluator.eval(sl.cadr(rest))
                return evaluator.apply(proc, sl.cons(test_result, NIL))
            while not sp.is_null(rest):
                res = evaluator.eval(rest.car)
                rest = rest.cdr
            return res

        args = args.cdr
    return NIL

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
    name = sl.car(args)
    if not sp.is_symbol(name):
        raise Exception("define-syntax: name must be a symbol")

    spec = sl.cadr(args)
    if not sp.is_pair(spec):
        raise Exception("define-syntax: invalid transformer spec")

    if sl.car(spec) == Symbol("syntax-rules"):
        literals = [
            resolve_literal_descriptor(evaluator, lit)
            for lit in sl.to_python_list(sl.cadr(spec))
        ]
        rules_expr = sl.cddr(spec)
        rules = []
        while not sp.is_null(rules_expr):
            rule = rules_expr.car
            rules.append((sl.car(rule), sl.cadr(rule)))
            rules_expr = rules_expr.cdr

        macro = Macro(name=name.name,
                      env=evaluator.current_scope,
                      literals=literals,
                      rules=rules)
    else:
        transformer = evaluator.eval(spec)
        if not isinstance(transformer, Lambda):
            raise Exception("define-syntax: transformer must be a procedure")
        macro = Macro(name=name.name,
                      env=evaluator.current_scope,
                      transformer=transformer)

    evaluator.bind(name.name, macro)
    return NIL
