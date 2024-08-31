
from dataclasses import dataclass
from typing import Callable


class Sexpr:
    printer = None

    def __str__(self):
        return self.printer.to_string(self)

    def __repr__(self):
        return self.printer.to_string(self)


@dataclass
class Atom(Sexpr):
    pass


@dataclass
class Boolean(Atom):
    value: bool


BOOLEAN_T = Boolean(True)
BOOLEAN_F = Boolean(False)


@dataclass
class String(Atom):
    value: str


@dataclass
class Number(Atom):
    value: int | float


@dataclass
class Symbol(Atom):
    name: str


class Nil(Symbol):
    def __init__(self):
        super().__init__("nil")


NIL = Nil()


@dataclass
class Cell(Sexpr):
    car: Sexpr = None
    cdr: Sexpr = None


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
