from sexpr import Symbol, Cell, Nil, Number, Lambda, \
    BuiltinFunction, BuiltinSpecialForm, Macro, \
    Boolean
import scpredicates as sp


class Printer:
    def repr_print(self, sexpr):
        match sexpr:
            case Number():
                print(str(sexpr.value), end="")
            case Symbol():
                print(sexpr.name, end="")
            case Nil():
                print("nil", end="")
            case Boolean():
                if sp.is_truthy(sexpr):
                    print("#t", end="")
                else:
                    print("#f", end="")
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
        if sp.is_null(sexpr):
            print(")", end="")
            return

        # sexpr is Cell
        (car, cdr) = (sexpr.car, sexpr.cdr)

        if not sp.is_pair(cdr) and not sp.is_null(cdr):
            self.repr_print(car)
            print(" . ", end="")
            self.repr_print(cdr)
            print(")", end="")
        else:
            self.repr_print(car)
            if not sp.is_null(cdr):
                print(" ", end="")
            self.repr_print_list(cdr)
