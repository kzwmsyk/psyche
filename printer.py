from common import Sexpr, Symbol, Cell, Atom, Nil, Number, is_cell, is_nil


class Printer:
    def repr_print(self, sexpr):
        match sexpr:
            case Number():
                print(str(sexpr.value), end="")
            case Symbol():
                print(sexpr.name, end="")
            case Nil():
                print("nil", end="")
            case Cell():
                print("(", end="")
                self.repr_print_list(sexpr)

    def repr_print_list(self, sexpr: Cell | Nil):
        if isinstance(sexpr, Nil):
            print(")", end="")
            return
        # sexpr is Cell
        (car, cdr) = (sexpr.car, sexpr.cdr)

        if not is_cell(cdr) and not is_nil(cdr):
            self.repr_print(car)
            print(" . ", end="")
            self.repr_print(cdr)
            print(")", end="")
        else:
            self.repr_print(car)
            if not is_nil(cdr):
                print(" ", end="")
            self.repr_print_list(cdr)
