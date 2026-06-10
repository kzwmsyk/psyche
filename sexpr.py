
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


@dataclass(eq=False)
class String(Atom):
    value: str


@dataclass
class Number(Atom):
    value: int | float


@dataclass
class Symbol(Atom):
    name: str


@dataclass(eq=False)
class Bytevector(Atom):
    value: bytearray


@dataclass(eq=False)
class Vector(Atom):
    value: list[Sexpr]


@dataclass
class Char(Atom):
    value: str


class Nil(Symbol):
    def __init__(self):
        super().__init__("nil")


NIL = Nil()


@dataclass(eq=False)
class Cell(Sexpr):
    car: Sexpr = None
    cdr: Sexpr = None


class Lambda(Sexpr):
    def __init__(self, params: Sexpr, body: Sexpr, env):
        self.params = params
        self.body = body
        self.env = env


class Macro(Sexpr):
    def __init__(self,
                 name: str,
                 env,
                 *,
                 transformer: "Lambda | None" = None,
                 literals: "list | None" = None,
                 rules: list[tuple[Sexpr, Sexpr]] | None = None):
        self.name = name
        self.env = env
        self.transformer = transformer
        self.literals = literals or []
        self.rules = rules or []


@dataclass
class BuiltinFunction(Sexpr):
    fn: Callable


@dataclass
class BuiltinSpecialForm(Sexpr):
    fn: Callable
