from contextlib import contextmanager
from common import Sexpr, Symbol, Cell, Nil, \
    is_cell, is_nil, NIL, T, is_number, is_symbol, is_atom, cons
import builtin
import specialform
from typing import Callable, Self
from dataclasses import dataclass
from enum import Enum, auto


class ScopeEntryType(Enum):
    SEXPR = auto()
    BUILTIN_FUNCTION = auto()
    BUILTIN_SPECIAL_FORM = auto()
    FUNCTION = auto()
    MACRO = auto()


@dataclass
class EnvEntry:
    env: 'Env'
    type: ScopeEntryType
    sexpr: Sexpr | None = None
    fn: Callable | None = None


class Env:
    def __init__(self, parent: Self | None,
                 variables: dict[str, Sexpr] | None = None):
        self.parent = parent
        self.env: dict[str, EnvEntry] = {}
        if variables is not None:
            for name, sexpr in variables.items():
                self.bind_sexpr(name, sexpr)

    def bind_sexpr(self, name: str, sexpr: Sexpr | Callable):
        self.env[name] = EnvEntry(self,
                                  ScopeEntryType.SEXPR,
                                  sexpr=sexpr)

    def bind_builtin_function(self, name: str, fn: Callable):
        self.env[name] = EnvEntry(self,
                                  ScopeEntryType.BUILTIN_FUNCTION,
                                  fn=fn)

    def bind_builtin_special_form(self, name: str, fn: Callable):
        self.env[name] = EnvEntry(self,
                                  ScopeEntryType.BUILTIN_SPECIAL_FORM,
                                  fn=fn)

    def bind_function(self, name: str, sexpr: Sexpr):
        self.env[name] = EnvEntry(self,
                                  ScopeEntryType.FUNCTION,
                                  sexpr=sexpr)

    def bind_macro(self, name: str, sexpr: Sexpr):
        self.env[name] = EnvEntry(self,
                                  ScopeEntryType.MACRO,
                                  sexpr=sexpr)


class Interpreter:
    def __init__(self):
        self.global_env = Env(None, {
            "nil": NIL,
            "t": T,
        })
        self.current_env = self.global_env

        for name, builtin_function in builtin.export().items():
            self.global_env.bind_builtin_function(name, builtin_function)

        for name, special_form in specialform.export().items():
            self.global_env.bind_builtin_special_form(name, special_form)

    @contextmanager
    def new_env(self, env: Env = None):
        orig_env = self.current_env
        if env is None:
            new_env = Env(self.current_env)
            new_env.parent = self.current_env
            self.current_env = new_env
        else:
            new_env = env
            self.current_env = env
        yield
        self.current_env = orig_env

    def eval(self, sexpr: Sexpr) -> Sexpr:

        if is_atom(sexpr):
            if is_number(sexpr):
                return sexpr
            elif is_symbol(sexpr) and self.has_symbol(sexpr):
                return self.find_symbol(sexpr).sexpr
        elif is_cell(sexpr):
            if is_number(sexpr.car):
                raise Exception(f"eval error: {sexpr.car}")

            return self.apply(sexpr.car, sexpr.cdr)

    def eval_list(self, args: Cell | Nil) -> Sexpr:
        if is_nil(args):
            return NIL
        else:
            return cons(self.eval(args.car),
                        self.eval_list(args.cdr))

    def apply(self, func: Sexpr, args: Sexpr) -> Sexpr:
        env_entry = self.find_symbol(func)

        match env_entry.type:
            case ScopeEntryType.BUILTIN_SPECIAL_FORM:
                return env_entry.fn(self, args)
            case ScopeEntryType.BUILTIN_FUNCTION:
                return env_entry.fn(self.eval_list(args))
            case ScopeEntryType.FUNCTION:
                params = env_entry.sexpr.car
                body = env_entry.sexpr.cdr
                evaled_args = self.eval_list(args)
                with self.new_env(env_entry.env):
                    with self.new_env():
                        self.bind_arg(params, evaled_args)
                        while not is_nil(body):
                            res = self.eval(body.car)
                            body = body.cdr
                        return res

            case ScopeEntryType.MACRO:
                raise Exception(
                    f"Macro application is not supported: {func}")
            case _:
                raise Exception(f"Unknown function: {func}")

    def bind_arg(self, params: Cell, args: Sexpr):
        while not is_nil(params):
            param = params.car
            arg = args.car
            self.bind_sexpr(param, arg)
            params = params.cdr
            args = args.cdr

    def bind_sexpr(self, symbol: Symbol, sexpr: Sexpr):
        self.current_env.bind_sexpr(symbol.name, sexpr)

    def bind_function(self, symbol: Symbol, sexpr: Sexpr):
        self.current_env.bind_function(symbol.name, sexpr)

    def find_symbol(self, symbol: Symbol) -> Env:
        scope = self.current_env
        while scope is not None:
            if symbol.name in scope.env:
                return scope.env[symbol.name]
            scope = scope.parent

        raise Exception(f"Unknown symbol: {symbol.name}")

    def has_symbol(self, symbol: Symbol) -> bool:
        scope = self.current_env
        while scope is not None:
            if symbol.name in scope.env:
                return True
            scope = scope.parent

        return False
