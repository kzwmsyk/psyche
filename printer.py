from sexpr import Sexpr, Symbol, Cell, Nil, Number, Lambda, \
    BuiltinFunction, BuiltinSpecialForm, Macro, \
    Boolean, String, Char, Vector, Bytevector
import scpredicates as sp


class Printer:

    def repr_print(self, sexpr):
        print(self.to_string(sexpr))

    def to_string(self, sexpr):
        match sexpr:
            case Number():
                return self._number_to_string(sexpr)
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
                return self._string_to_string(sexpr.value)
            case Char():
                return self._char_to_string(sexpr.value)
            case Vector():
                return self._vector_to_string(sexpr)
            case Bytevector():
                return self._bytevector_to_string(sexpr)
            case Lambda():
                return f"#<lambda ({sexpr.params})>"
            case BuiltinFunction():
                return f"#<builtin ({sexpr.fn})>"
            case BuiltinSpecialForm():
                return f"#<builtin ({sexpr.fn})>"
            case Macro():
                return f"#<macro {sexpr.name}>"
            case Cell():
                return "(" + self.to_string_list(sexpr)

    def display_to_string(self, sexpr):
        if sp.is_string(sexpr):
            return sexpr.value
        if sp.is_char(sexpr):
            return sexpr.value
        return self.to_string(sexpr)

    def _number_to_string(self, number: Number) -> str:
        value = number.value
        if isinstance(value, float) and value.is_integer():
            return f"{value:.1f}"
        return str(value)

    def _string_to_string(self, value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    def _char_to_string(self, value: str) -> str:
        for name, ch in {
            "nul": "\0",
            "space": " ",
            "tab": "\t",
            "newline": "\n",
            "return": "\r",
        }.items():
            if value == ch:
                return f"#\\{name}"
        if len(value) == 1 and value not in (" ", "\n", "\t"):
            return f"#\\{value}"
        return f"#\\?"

    def _vector_to_string(self, vector: Vector) -> str:
        items = " ".join(self.to_string(item) for item in vector.value)
        return f"#({items})"

    def _bytevector_to_string(self, bytevector: Bytevector) -> str:
        items = " ".join(str(byte) for byte in bytevector.value)
        return f"#u8({items})"

    def to_string_list(self, sexpr: Cell | Nil):
        if sp.is_null(sexpr):
            return ")"

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
