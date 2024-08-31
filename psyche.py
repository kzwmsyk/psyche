#! /usr/bin/env python3
import sys

from scanner import Scanner
from reader import Reader
from printer import Printer
from evaluator import Evaluator
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    evaluator = Evaluator()
    prelude(evaluator)

    scanner = Scanner(stream=sys.stdin)
    reader = Reader(scanner)

    printer = Printer()
    while True:
        try:
            print("psyche> ", end="")
            sys.stdout.flush()
            printer.repr_print(evaluator.eval(reader.read()))
            print()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break
        except EOFError:
            print("\nexit")
            break
        except Exception as e:
            logger.exception("error: %s", e)
            pass


def prelude(envaluator: Evaluator):
    with open("prelude.scm", "r") as f:
        reader = Reader(Scanner(stream=f))
        while True:
            sexpr = reader.read()
            if sexpr is None:
                break
            envaluator.eval(sexpr)


if __name__ == "__main__":
    main()
