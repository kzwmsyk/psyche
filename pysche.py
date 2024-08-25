#! /usr/bin/env python3
import sys

from scanner import Scanner
from reader import Reader
from printer import Printer
from interpreter import Interpreter
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    interpreter = Interpreter()
    prelude(interpreter)

    scanner = Scanner(stream=sys.stdin)
    reader = Reader(scanner)

    printer = Printer()
    while True:
        try:
            print("pysche> ", end="")
            sys.stdout.flush()
            printer.repr_print(interpreter.eval(reader.read()))
            print()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break
        except EOFError:
            print("\nexit")
            break
        except Exception as e:
            logger.exception("error: %s", e)


def prelude(interpreter: Interpreter):
    with open("prelude.scm", "r") as f:
        reader = Reader(Scanner(stream=f))
        while True:
            sexpr = reader.read()
            if sexpr is None:
                break
            interpreter.eval(sexpr)


if __name__ == "__main__":
    main()
