from contextlib import contextmanager
from sexpr import Sexpr, Symbol, Cell, Nil, NIL, \
    BuiltinFunction, BuiltinSpecialForm, Lambda, Macro, \
    Number, Boolean
import sclist as sl
import scpredicates as sp
import builtin
import specialform
from typing import Self

from logging import getLogger

logger = getLogger(__name__)


class Env:
    def __init__(self, parent: Self | None):
        self.parent = parent
        self.env: dict[str, Sexpr] = {}

    def bind(self, name: str, sexpr: Sexpr):
        self.env[name] = sexpr

    def bind_dict(self, dict: dict[str, Sexpr]):
        for name, sexpr in dict.items():
            self.env[name] = sexpr


class Evaluator:
    def __init__(self):
        self.global_scope = Env(None)
        self.current_scope = self.global_scope

        self.global_scope.bind_dict({
            "nil": NIL,
        })

        self.global_scope.bind_dict(builtin.export())
        self.global_scope.bind_dict(specialform.export())

    @contextmanager
    def new_env(self, scope: Env = None):
        orig_scope = self.current_scope
        if scope is None:
            new_scope = Env(parent=self.current_scope)
            self.current_scope = new_scope
        else:
            new_scope = scope
            self.current_scope = scope
        yield
        self.current_scope = orig_scope

    def eval(self, sexpr: Sexpr) -> Sexpr:
        match sexpr:
            case Boolean():
                return sexpr
            case Number():
                return sexpr
            case Symbol():
                return self.find_symbol(sexpr)
            case Lambda():
                return sexpr
            case Cell():
                return self.apply(self.eval(sexpr.car),
                                  sexpr.cdr)
            case _:
                return sexpr

    def eval_list(self, args: Cell | Nil) -> Sexpr:
        if sp.is_null(args):
            return NIL
        else:
            return sl.cons(self.eval(args.car),
                           self.eval_list(args.cdr))

    def apply(self, func: Sexpr, args: Sexpr) -> Sexpr:

        match func:
            case BuiltinSpecialForm():
                return func.fn(self, args)
            case BuiltinFunction():
                return func.fn(self.eval_list(args), evaluator=self)
            case Lambda():
                body = func.body
                params = func.params
                fixed_params = []
                rest_param = None

                if sp.is_symbol(params):
                    # (lambda x body)
                    rest_param = params
                elif sp.is_list(params):
                    # (lambda (x y ...) body)
                    fixed_params = [p for p in sl.to_python_list(params)]
                elif sp.is_pair(params):
                    # (lambda (x y z ... . rest) body)
                    car = params.car
                    cdr = params.cdr
                    while sp.is_pair(cdr):
                        logger.debug(f"car:{car} cdr:{cdr}")
                        fixed_params.append(car)
                        car = cdr.car
                        cdr = cdr.cdr

                    fixed_params.append(car)
                    rest_param = cdr

                evaled_args = self.eval_list(args)

                with self.new_env(func.env):
                    with self.new_env():
                        self._bind_arg(fixed_params, rest_param, evaled_args)
                        while not sp.is_null(body):
                            res = self.eval(body.car)
                            body = body.cdr
                        return res
            case Macro():
                raise Exception(
                    f"Macro application is not supported: {func}")
            case _:
                raise Exception(f"Unknown function: {func}")

    def _bind_arg(self,
                  fixed_params: list[Symbol] = [],
                  rest_param: Symbol | None = None,
                  args: Sexpr = NIL):

        for fixed_param in fixed_params:
            self.bind(fixed_param.name, args.car)
            args = args.cdr

        if rest_param is not None:
            self.bind(rest_param.name, args)

    def find_symbol(self, symbol: Symbol) -> Sexpr:
        scope = self.current_scope
        while scope is not None:
            if symbol.name in scope.env:
                return scope.env[symbol.name]
            scope = scope.parent

        raise Exception(f"Unknown symbol: {symbol.name}")

    def has_symbol(self, symbol: Symbol) -> bool:
        scope = self.current_scope
        while scope is not None:
            if symbol.name in scope.env:
                return True
            scope = scope.parent

        return False

    def bind(self, name: str, sexpr: Sexpr):
        self.current_scope.bind(name, sexpr)
