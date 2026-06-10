"""R5RS delay promises."""

from __future__ import annotations

from typing import Callable

from sexpr import Sexpr


class Promise(Sexpr):
    def __init__(self, thunk: Callable[[], Sexpr]):
        self.thunk = thunk
        self.evaluated = False
        self.value: Sexpr | None = None
