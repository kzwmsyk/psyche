"""Multiple return values (R5RS values / call-with-values)."""

from __future__ import annotations

from sexpr import Sexpr


class MultipleValues(Sexpr):
    def __init__(self, values: list[Sexpr]):
        self.values = values
