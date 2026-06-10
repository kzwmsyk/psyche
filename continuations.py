"""Non-local control flow for call/cc."""

from __future__ import annotations

from sexpr import Sexpr


class InvokeContinuation(Exception):
    def __init__(self, value: Sexpr):
        self.value = value
