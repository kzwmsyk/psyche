"""Syntax objects for hygienic macro expansion (R5RS syntax-rules)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sexpr import Sexpr, Symbol

if TYPE_CHECKING:
    from evaluator import Env, Evaluator


@dataclass
class SyntaxObject(Sexpr):
    """S-expression with the expansion-site environment for identifier tests."""

    datum: Sexpr
    use_env: "Env | None" = None


@dataclass
class LiteralDescriptor:
    """Identifier literal from (syntax-rules (lit ...) ...) at define time."""

    name: str
    binding: Sexpr | None


class Gensym:
    _counter = 0

    @classmethod
    def fresh(cls, hint: str) -> Symbol:
        cls._counter += 1
        return Symbol(f"{hint}${cls._counter}")


def syntax_datum(obj: SyntaxObject | Sexpr) -> Sexpr:
    if isinstance(obj, SyntaxObject):
        return obj.datum
    return obj


def datum_to_syntax(datum: Sexpr, use_env: "Env | None" = None) -> SyntaxObject:
    return SyntaxObject(datum=datum, use_env=use_env)


def resolve_literal_descriptor(evaluator: "Evaluator",
                             symbol: Symbol) -> LiteralDescriptor:
    return LiteralDescriptor(
        name=symbol.name,
        binding=evaluator.lookup_symbol(symbol),
    )


def literal_matches(descriptor: LiteralDescriptor,
                    expr: Sexpr,
                    evaluator: "Evaluator") -> bool:
    from scpredicates import is_symbol

    if not is_symbol(expr):
        return False
    if expr.name != descriptor.name:
        return False
    current = evaluator.lookup_symbol(expr)
    if descriptor.binding is None:
        return current is None
    return current is descriptor.binding
