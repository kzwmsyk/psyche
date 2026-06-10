from copy import deepcopy

from sexpr import Sexpr, NIL
import sclist as sl
import scpredicates as sp


class MacroExpansionError(Exception):
    pass


def expand_syntax_rules(literals: list[str],
                        rules: list[tuple[Sexpr, Sexpr]],
                        form: Sexpr) -> Sexpr:
    literal_set = set(literals)
    for pattern, template in rules:
        bindings: dict[str, Sexpr | list[Sexpr]] = {}
        if _match(pattern, form, literal_set, bindings):
            return _expand_template(template, bindings, literal_set)
    raise MacroExpansionError(f"no matching syntax-rule for: {form}")


def _is_ellipsis_rest(pat_cdr: Sexpr) -> bool:
    return (sp.is_pair(pat_cdr)
            and sp.is_symbol(pat_cdr.car)
            and pat_cdr.car.name == "...")


def _match(pattern: Sexpr,
           expr: Sexpr,
           literals: set[str],
           bindings: dict[str, Sexpr | list[Sexpr]]) -> bool:
    if sp.is_null(pattern):
        return sp.is_null(expr)

    if sp.is_symbol(pattern):
        name = pattern.name
        if name == "...":
            raise MacroExpansionError("invalid ... in pattern")
        if name in literals:
            return sp.is_symbol(expr) and expr.name == name
        bindings[name] = expr
        return True

    if sp.is_pair(pattern):
        if not sp.is_pair(expr):
            return False
        return _match_pair(pattern.car, pattern.cdr,
                           expr.car, expr.cdr,
                           literals, bindings)

    return pattern == expr


def _match_pair(pat_car: Sexpr,
                pat_cdr: Sexpr,
                expr_car: Sexpr,
                expr_cdr: Sexpr,
                literals: set[str],
                bindings: dict[str, Sexpr | list[Sexpr]]) -> bool:
    if _is_ellipsis_rest(pat_cdr):
        rest_pat = pat_cdr.cdr
        expr = sl.cons(expr_car, expr_cdr)
        trial = deepcopy(bindings)
        if _match_ellipsis(pat_car, rest_pat, expr, literals, trial):
            bindings.clear()
            bindings.update(trial)
            return True
        return False

    trial = deepcopy(bindings)
    if not _match(pat_car, expr_car, literals, trial):
        return False
    if not _match(pat_cdr, expr_cdr, literals, trial):
        return False
    bindings.clear()
    bindings.update(trial)
    return True


def _match_ellipsis(pat_elem: Sexpr,
                    rest_pat: Sexpr,
                    expr: Sexpr,
                    literals: set[str],
                    bindings: dict[str, Sexpr | list[Sexpr]]) -> bool:
    items = sl.to_python_list(expr)

    for count in range(len(items) + 1):
        prefix = items[:count]
        suffix = sl.from_python_list(items[count:])
        trial = deepcopy(bindings)

        if sp.is_symbol(pat_elem):
            name = pat_elem.name
            if name in literals:
                if not all(sp.is_symbol(item) and item.name == name
                           for item in prefix):
                    continue
            trial[name] = prefix
        else:
            repeated: dict[str, list[Sexpr]] = {}
            ok = True
            for item in prefix:
                item_bindings: dict[str, Sexpr | list[Sexpr]] = {}
                if not _match(pat_elem, item, literals, item_bindings):
                    ok = False
                    break
                for key, value in item_bindings.items():
                    if isinstance(value, list):
                        raise MacroExpansionError(
                            "nested ellipsis in pattern is not supported")
                    repeated.setdefault(key, []).append(value)
            if not ok:
                continue
            for key, values in repeated.items():
                trial[key] = values

        if _match(rest_pat, suffix, literals, trial):
            bindings.clear()
            bindings.update(trial)
            return True

    return False


def _expand_template(template: Sexpr,
                     bindings: dict[str, Sexpr | list[Sexpr]],
                     literals: set[str]) -> Sexpr:
    if sp.is_null(template):
        return NIL

    if sp.is_symbol(template):
        name = template.name
        if name in literals:
            return template
        if name in bindings:
            value = bindings[name]
            if isinstance(value, list):
                raise MacroExpansionError(
                    f"ellipsis variable {name} used outside ellipsis template")
            return value
        return template

    if sp.is_pair(template):
        if _is_ellipsis_rest(template.cdr):
            return _expand_ellipsis_template(template.car,
                                             template.cdr.cdr,
                                             bindings,
                                             literals)
        return sl.cons(_expand_template(template.car, bindings, literals),
                       _expand_template(template.cdr, bindings, literals))

    return template


def _expand_ellipsis_template(pat_elem: Sexpr,
                              rest_template: Sexpr,
                              bindings: dict[str, Sexpr | list[Sexpr]],
                              literals: set[str]) -> Sexpr:
    expanded_rest = _expand_template(rest_template, bindings, literals)

    if not sp.is_symbol(pat_elem):
        raise MacroExpansionError(
            "ellipsis template with compound pattern is not supported")

    items = bindings.get(pat_elem.name, [])
    if not isinstance(items, list):
        items = [items]

    result = expanded_rest
    for item in reversed(items):
        result = sl.cons(item, result)
    return result
