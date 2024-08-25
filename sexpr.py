
from dataclasses import dataclass
from typing import Callable


class Sexpr:
    pass


@dataclass
class Atom(Sexpr):
    pass


@dataclass
class Number(Atom):
    value: int | float

    def __str__(self):
        return str(self.value)


@dataclass
class Symbol(Atom):
    name: str

    def __str__(self):
        return f"Symbol({self.name})"


class Nil(Symbol):
    def __init__(self):
        super().__init__("nil")

    def __str__(self):
        return "()"


@dataclass
class Cell(Sexpr):
    car: Sexpr = None
    cdr: Sexpr = None

    def __str__(self):
        return f"({self.car} . {self.cdr})"


class Lambda(Sexpr):
    def __init__(self, params: Sexpr, body: Sexpr, env):
        self.params = params
        self.body = body
        self.env = env


@dataclass
class Macro(Sexpr):
    name: str
    params: Sexpr
    body: Sexpr
    env = None


@dataclass
class BuiltinFunction(Sexpr):
    fn: Callable


@dataclass
class BuiltinSpecialForm(Sexpr):
    fn: Callable


NIL = Nil()
T = Symbol("t")
