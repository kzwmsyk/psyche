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
    scanner = Scanner(stream=sys.stdin)
    reader = Reader(scanner)
    interpreter = Interpreter()
    printer = Printer()
    try:
        while True:
            print("pysche> ", end="")
            sys.stdout.flush()
            printer.repr_print(interpreter.eval(reader.read()))
            print()

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
    except EOFError:
        print("\nexit")
    except Exception as e:
        logger.exception("error: %s", e)


if __name__ == "__main__":
    main()
