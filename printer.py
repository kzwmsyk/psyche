from sexpr import Symbol, Cell, Nil, Number, Lambda, \
    BuiltinFunction, BuiltinSpecialForm, Macro
import sclist as sc


class Printer:
    def repr_print(self, sexpr):
        match sexpr:
            case Number():
                print(str(sexpr.value), end="")
            case Symbol():
                print(sexpr.name, end="")
            case Nil():
                print("nil", end="")
            case Lambda():
                print(f"#<lambda ({sexpr.params})>", end="")
            case BuiltinFunction():
                print(f"#<builtin ({sexpr.fn})>", end="")
            case BuiltinSpecialForm():
                print(f"#<builtin ({sexpr.fn})>", end="")
            case Macro():
                print(f"#<macro ({sexpr.params})>", end="")
            case Cell():
                print("(", end="")
                self.repr_print_list(sexpr)

    def repr_print_list(self, sexpr: Cell | Nil):
        if isinstance(sexpr, Nil):
            print(")", end="")
            return
        # sexpr is Cell
        (car, cdr) = (sexpr.car, sexpr.cdr)

        if not sc.is_cell(cdr) and not sc.is_nil(cdr):
            self.repr_print(car)
            print(" . ", end="")
            self.repr_print(cdr)
            print(")", end="")
        else:
            self.repr_print(car)
            if not sc.is_nil(cdr):
                print(" ", end="")
            self.repr_print_list(cdr)
