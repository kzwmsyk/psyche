"""R5RS port I/O."""

from __future__ import annotations

import sys
from typing import IO, TYPE_CHECKING

from reader import Reader
from scanner import Scanner, EOL
from sexpr import Sexpr, NIL, BuiltinFunction, String, Char, Symbol
from printer import Printer
import scpredicates as sp
import sclist as sl

if TYPE_CHECKING:
    from evaluator import Evaluator


class EofObject(Sexpr):
    pass


EOF_OBJECT = EofObject()


class Port(Sexpr):
    def __init__(self,
                 stream: IO[str],
                 name: str,
                 *,
                 input_port: bool = True,
                 output_port: bool = False):
        self.stream = stream
        self.name = name
        self.input_port = input_port
        self.output_port = output_port
        self.closed = False
        self._peeked: str | None = None
        self._reader: Reader | None = None

    def read_char(self) -> str:
        if self.closed:
            raise Exception(f"port is closed: {self.name}")
        if self._peeked is not None:
            ch = self._peeked
            self._peeked = None
            return ch
        ch = self.stream.read(1)
        return ch

    def peek_char(self) -> str:
        if self.closed:
            raise Exception(f"port is closed: {self.name}")
        if self._peeked is None:
            self._peeked = self.stream.read(1)
        return self._peeked

    def write(self, text: str) -> None:
        if self.closed:
            raise Exception(f"port is closed: {self.name}")
        self.stream.write(text)
        self.stream.flush()

    def scheme_reader(self) -> Reader:
        if self._reader is None:
            self._reader = Reader(PortScanner(self))
        return self._reader


class PortScanner(Scanner):
    """Scanner that reads through a Port (respects peek-char buffer)."""

    def __init__(self, port: Port):
        super().__init__(stream=port.stream)
        self.port = port

    def _get_char(self) -> str:
        if self.pushback_chars:
            c = self.pushback_chars.pop()
        else:
            c = self.port.read_char()

        if c == EOL:
            if len(self.line_ends) == self.line - 1:
                self.line_ends.append(self.col)
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return c


def init_ports(evaluator: Evaluator) -> None:
    evaluator.current_input_port = Port(sys.stdin, "stdin")
    evaluator.current_output_port = Port(sys.stdout, "stdout", output_port=True)


def export() -> dict[str, BuiltinFunction]:
    return {
        "eof-object?": BuiltinFunction(f_eof_object_p),
        "port?": BuiltinFunction(f_port_p),
        "current-input-port": BuiltinFunction(f_current_input_port),
        "current-output-port": BuiltinFunction(f_current_output_port),
        "open-input-file": BuiltinFunction(f_open_input_file),
        "open-output-file": BuiltinFunction(f_open_output_file),
        "close-input-port": BuiltinFunction(f_close_input_port),
        "close-output-port": BuiltinFunction(f_close_output_port),
        "read": BuiltinFunction(f_read),
        "read-char": BuiltinFunction(f_read_char),
        "peek-char": BuiltinFunction(f_peek_char),
        "write-char": BuiltinFunction(f_write_char),
        "display": BuiltinFunction(f_display),
        "write": BuiltinFunction(f_write),
        "newline": BuiltinFunction(f_newline),
        "load": BuiltinFunction(f_load),
        "input-port?": BuiltinFunction(f_input_port_p),
        "output-port?": BuiltinFunction(f_output_port_p),
        "with-input-from-file": BuiltinFunction(f_with_input_from_file),
        "with-output-to-file": BuiltinFunction(f_with_output_to_file),
        "call-with-input-file": BuiltinFunction(f_call_with_input_file),
        "call-with-output-file": BuiltinFunction(f_call_with_output_file),
    }


def _to_lisp_boolean(value: bool) -> Sexpr:
    from sexpr import BOOLEAN_T, BOOLEAN_F
    return BOOLEAN_T if value else BOOLEAN_F


def _require_port(obj: Sexpr, *, input_ok: bool = False,
                  output_ok: bool = False) -> Port:
    if not isinstance(obj, Port):
        raise Exception("port required")
    if input_ok and not obj.input_port:
        raise Exception("input port required")
    if output_ok and not obj.output_port:
        raise Exception("output port required")
    if obj.closed:
        raise Exception("port is closed")
    return obj


def f_eof_object_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(isinstance(args.car, EofObject))


def f_port_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(isinstance(args.car, Port))


def f_current_input_port(args: Sexpr, evaluator=None) -> Sexpr:
    return evaluator.current_input_port


def f_current_output_port(args: Sexpr, evaluator=None) -> Sexpr:
    return evaluator.current_output_port


def f_open_input_file(args: Sexpr, evaluator=None) -> Sexpr:
    path = _string_value(args.car)
    stream = open(path, encoding="utf-8")
    return Port(stream, path, input_port=True, output_port=False)


def f_open_output_file(args: Sexpr, evaluator=None) -> Sexpr:
    path = _string_value(args.car)
    stream = open(path, "w", encoding="utf-8")
    return Port(stream, path, input_port=False, output_port=True)


def f_close_input_port(args: Sexpr, evaluator=None) -> Sexpr:
    port = _require_port(args.car, input_ok=True)
    port.stream.close()
    port.closed = True
    return NIL


def f_close_output_port(args: Sexpr, evaluator=None) -> Sexpr:
    port = _require_port(args.car, output_ok=True)
    port.stream.close()
    port.closed = True
    return NIL


def f_read(args: Sexpr, evaluator=None) -> Sexpr:
    port = _input_port_arg(args, evaluator)
    result = port.scheme_reader().read()
    if result is None:
        return EOF_OBJECT
    return result


def f_read_char(args: Sexpr, evaluator=None) -> Sexpr:
    port = _input_port_arg(args, evaluator)
    ch = port.read_char()
    if ch == "":
        return EOF_OBJECT
    return Char(ch)


def f_peek_char(args: Sexpr, evaluator=None) -> Sexpr:
    port = _input_port_arg(args, evaluator)
    ch = port.peek_char()
    if ch == "":
        return EOF_OBJECT
    return Char(ch)


def f_write_char(args: Sexpr, evaluator=None) -> Sexpr:
    if sp.is_null(args):
        raise Exception("write-char: missing argument")
    if not sp.is_char(args.car):
        raise Exception("write-char: character required")
    port = (_require_port(args.cadr, output_ok=True)
            if not sp.is_null(args.cdr)
            else evaluator.current_output_port)
    port.write(args.car.value)
    return NIL


def f_display(args: Sexpr, evaluator=None) -> Sexpr:
    if sp.is_null(args):
        raise Exception("display: missing argument")
    port = (_require_port(args.cadr, output_ok=True)
            if not sp.is_null(args.cdr)
            else evaluator.current_output_port)
    port.write(Printer().display_to_string(args.car))
    return NIL


def f_write(args: Sexpr, evaluator=None) -> Sexpr:
    if sp.is_null(args):
        raise Exception("write: missing argument")
    port = (_require_port(args.cadr, output_ok=True)
            if not sp.is_null(args.cdr)
            else evaluator.current_output_port)
    port.write(Printer().to_string(args.car))
    return NIL


def f_newline(args: Sexpr, evaluator=None) -> Sexpr:
    port = (_require_port(args.car, output_ok=True)
            if not sp.is_null(args)
            else evaluator.current_output_port)
    port.write("\n")
    return NIL


def f_input_port_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(isinstance(args.car, Port) and args.car.input_port)


def f_output_port_p(args: Sexpr, evaluator=None) -> Sexpr:
    return _to_lisp_boolean(isinstance(args.car, Port) and args.car.output_port)


def f_with_input_from_file(args: Sexpr, evaluator=None) -> Sexpr:
    path = _string_value(args.car)
    proc = args.cdr.car
    previous = evaluator.current_input_port
    port = Port(open(path, encoding="utf-8"), path,
                input_port=True, output_port=False)
    try:
        evaluator.current_input_port = port
        return evaluator.apply(proc, NIL)
    finally:
        evaluator.current_input_port = previous
        port.stream.close()
        port.closed = True


def f_with_output_to_file(args: Sexpr, evaluator=None) -> Sexpr:
    path = _string_value(args.car)
    proc = args.cdr.car
    previous = evaluator.current_output_port
    port = Port(open(path, "w", encoding="utf-8"), path,
                input_port=False, output_port=True)
    try:
        evaluator.current_output_port = port
        return evaluator.apply(proc, NIL)
    finally:
        evaluator.current_output_port = previous
        port.stream.close()
        port.closed = True


def f_call_with_input_file(args: Sexpr, evaluator=None) -> Sexpr:
    path = _string_value(args.car)
    proc = args.cdr.car
    port = Port(open(path, encoding="utf-8"), path,
                input_port=True, output_port=False)
    try:
        return evaluator.apply(proc, sl.cons(port, NIL))
    finally:
        port.stream.close()
        port.closed = True


def f_call_with_output_file(args: Sexpr, evaluator=None) -> Sexpr:
    path = _string_value(args.car)
    proc = args.cdr.car
    port = Port(open(path, "w", encoding="utf-8"), path,
                input_port=False, output_port=True)
    try:
        return evaluator.apply(proc, sl.cons(port, NIL))
    finally:
        port.stream.close()
        port.closed = True


def f_load(args: Sexpr, evaluator=None) -> Sexpr:
    path = _string_value(args.car)
    with open(path, encoding="utf-8") as stream:
        reader = Reader(Scanner(stream=stream))
        result = NIL
        while True:
            sexpr = reader.read()
            if sexpr is None:
                break
            result = evaluator.eval(sexpr)
    return result


def _input_port_arg(args: Sexpr, evaluator: Evaluator) -> Port:
    if sp.is_null(args):
        return evaluator.current_input_port
    return _require_port(args.car, input_ok=True)


def _string_value(sexpr: Sexpr) -> str:
    if not sp.is_string(sexpr):
        raise Exception("string required")
    return sexpr.value
