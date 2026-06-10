"""Shared helpers for running psyche in tests."""

from __future__ import annotations

import io
from pathlib import Path

from evaluator import Evaluator
from printer import Printer
from reader import Reader
from scanner import Scanner
from sexpr import NIL, Sexpr, Symbol

ROOT = Path(__file__).resolve().parents[2]
PRELUDE = ROOT / "prelude.scm"
TEST_LIB = Path(__file__).resolve().parent / "test-lib.scm"


def _read_all(reader: Reader) -> list[Sexpr]:
    forms: list[Sexpr] = []
    while True:
        sexpr = reader.read()
        if sexpr is None:
            break
        forms.append(sexpr)
    return forms


def _eval_forms(evaluator: Evaluator, forms: list[Sexpr]) -> list[Sexpr]:
    results: list[Sexpr] = []
    for form in forms:
        results.append(evaluator.eval(form))
    return results


def load_file(evaluator: Evaluator, path: Path) -> None:
    with path.open(encoding="utf-8") as stream:
        forms = _read_all(Reader(Scanner(stream=stream)))
    _eval_forms(evaluator, forms)


def make_evaluator(*, load_prelude: bool = True) -> Evaluator:
    evaluator = Evaluator()
    if load_prelude:
        load_file(evaluator, PRELUDE)
    return evaluator


def read_string(source: str) -> list[Sexpr]:
    return _read_all(Reader(Scanner(stream=io.StringIO(source))))


def eval_string(source: str, *, load_prelude: bool = True) -> Sexpr:
    evaluator = make_evaluator(load_prelude=load_prelude)
    forms = read_string(source)
    if not forms:
        return NIL
    return _eval_forms(evaluator, forms)[-1]


def eval_all(source: str, *, load_prelude: bool = True) -> list[Sexpr]:
    evaluator = make_evaluator(load_prelude=load_prelude)
    return _eval_forms(evaluator, read_string(source))


def to_string(sexpr: Sexpr) -> str:
    return Printer().to_string(sexpr)


def eval_string_as_string(source: str, *, load_prelude: bool = True) -> str:
    return to_string(eval_string(source, load_prelude=load_prelude))


def run_scheme_test_file(path: Path) -> int:
    """Load test-lib.scm and a Scheme test file; return failure count."""
    evaluator = make_evaluator()
    load_file(evaluator, TEST_LIB)
    load_file(evaluator, path)
    failures = evaluator.find_symbol(Symbol("*test-failures*"))
    return failures.value
