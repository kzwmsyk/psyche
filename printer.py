from sexpr import Sexpr, Symbol, Cell, Nil, Number, Lambda, \
    BuiltinFunction, BuiltinSpecialForm, Macro, \
    Boolean, String
import scpredicates as sp


class Printer:

    def repr_print(self, sexpr):
        print(self.to_string(sexpr))

    def to_string(self, sexpr):
        match sexpr:
            case Number():
                return str(sexpr.value)
            case Symbol():
                return sexpr.name
            case Nil():
                return "nil"
            case Boolean():
                if sp.is_truthy(sexpr):
                    return "#t"
                else:
                    return "#f"
            case String():
                return f'"{sexpr.value}"'
            case Lambda():
                return f"#<lambda ({sexpr.params})>"
            case BuiltinFunction():
                return f"#<builtin ({sexpr.fn})>"
            case BuiltinSpecialForm():
                return f"#<builtin ({sexpr.fn})>"
            case Macro():
                return f"#<macro ({sexpr.params})>"
            case Cell():
                return "(" + self.to_string_list(sexpr)

    def to_string_list(self, sexpr: Cell | Nil):
        if sp.is_null(sexpr):
            return ")"

        # sexpr is Cell
        (car, cdr) = (sexpr.car, sexpr.cdr)

        if not sp.is_pair(cdr) and not sp.is_null(cdr):
            return f"{self.to_string(car)} . {self.to_string(cdr)})"
        else:
            buf = self.to_string(car)
            if not sp.is_null(cdr):
                buf += " "
            buf += self.to_string_list(cdr)
            return buf


DEBUG_PRINTER = Printer()
Sexpr.printer = DEBUG_PRINTER
