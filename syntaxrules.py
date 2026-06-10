"""R5RS syntax-rules pattern matching and hygienic template expansion."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

from sexpr import Sexpr, Symbol, NIL
import sclist as sl
import scpredicates as sp
from syntaxobject import Gensym, LiteralDescriptor, literal_matches

if TYPE_CHECKING:
    from evaluator import Evaluator


class MacroExpansionError(Exception):
    pass


ELLIPSIS = "..."


def expand_syntax_rules(macro_name: str,
                        literals: list[LiteralDescriptor],
                        rules: list[tuple[Sexpr, Sexpr]],
                        form: Sexpr,
                        evaluator: Evaluator) -> Sexpr:
    literal_desc = {macro_name: None, **{d.name: d for d in literals}}
    literal_names = set(literal_desc.keys())

    for pattern, template in rules:
        bindings: dict[str, Sexpr | list] = {}
        if _match(pattern, form, literal_desc, literal_names, evaluator,
                  bindings):
            pattern_vars = _collect_pattern_vars(pattern, literal_names,
                                                 macro_name)
            return _expand_template(template, bindings, literal_names,
                                    pattern_vars)
    raise MacroExpansionError(f"no matching syntax-rule for: {form}")


def _collect_pattern_vars(pattern: Sexpr,
                          literal_names: set[str],
                          keyword: str,
                          found: set[str] | None = None) -> set[str]:
    if found is None:
        found = set()

    if sp.is_null(pattern):
        return found

    if sp.is_symbol(pattern):
        name = pattern.name
        if name != ELLIPSIS and name not in literal_names and name != keyword:
            found.add(name)
        return found

    if sp.is_pair(pattern):
        _collect_pattern_vars(pattern.car, literal_names, keyword, found)
        if _is_ellipsis_rest(pattern.cdr):
            _collect_pattern_vars(pattern.cdr.car, literal_names, keyword,
                                  found)
            _collect_pattern_vars(pattern.cdr.cdr, literal_names, keyword,
                                  found)
        else:
            _collect_pattern_vars(pattern.cdr, literal_names, keyword, found)
        return found

    return found


def _is_ellipsis_rest(pat_cdr: Sexpr) -> bool:
    return (sp.is_pair(pat_cdr)
            and sp.is_symbol(pat_cdr.car)
            and pat_cdr.car.name == ELLIPSIS)


def _is_improper_tail(pat_cdr: Sexpr) -> bool:
    return sp.is_symbol(pat_cdr) and pat_cdr.name != ELLIPSIS


def _match(pattern: Sexpr,
           expr: Sexpr,
           literal_desc: dict[str, LiteralDescriptor | None],
           literal_names: set[str],
           evaluator: Evaluator,
           bindings: dict[str, Sexpr | list]) -> bool:
    if sp.is_null(pattern):
        return sp.is_null(expr)

    if sp.is_symbol(pattern):
        name = pattern.name
        if name == ELLIPSIS:
            raise MacroExpansionError("invalid ... in pattern")
        if name in literal_names:
            desc = literal_desc.get(name)
            if desc is None:
                return sp.is_symbol(expr) and expr.name == name
            return literal_matches(desc, expr, evaluator)
        bindings[name] = expr
        return True

    if sp.is_pair(pattern):
        if not sp.is_pair(expr):
            return False
        if _is_improper_tail(pattern.cdr):
            trial = deepcopy(bindings)
            if (_match(pattern.car, expr.car, literal_desc, literal_names,
                       evaluator, trial)
                    and _match(pattern.cdr, expr.cdr, literal_desc,
                               literal_names, evaluator, trial)):
                bindings.clear()
                bindings.update(trial)
                return True
            return False
        return _match_pair(pattern.car, pattern.cdr,
                           expr.car, expr.cdr,
                           literal_desc, literal_names, evaluator,
                           bindings)

    return pattern == expr


def _match_pair(pat_car: Sexpr,
                pat_cdr: Sexpr,
                expr_car: Sexpr,
                expr_cdr: Sexpr,
                literal_desc: dict[str, LiteralDescriptor | None],
                literal_names: set[str],
                evaluator: Evaluator,
                bindings: dict[str, Sexpr | list]) -> bool:
    if _is_ellipsis_rest(pat_cdr):
        rest_pat = pat_cdr.cdr
        expr = sl.cons(expr_car, expr_cdr)
        trial = deepcopy(bindings)
        if _match_ellipsis(pat_car, rest_pat, expr, literal_desc,
                           literal_names, evaluator, trial):
            bindings.clear()
            bindings.update(trial)
            return True
        return False

    trial = deepcopy(bindings)
    if not _match(pat_car, expr_car, literal_desc, literal_names,
                  evaluator, trial):
        return False
    if not _match(pat_cdr, expr_cdr, literal_desc, literal_names,
                  evaluator, trial):
        return False
    bindings.clear()
    bindings.update(trial)
    return True


def _merge_repeated_bindings(
        target: dict[str, list],
        item_bindings: dict[str, Sexpr | list]) -> None:
    for key, value in item_bindings.items():
        target.setdefault(key, []).append(value)


def _match_ellipsis(pat_elem: Sexpr,
                    rest_pat: Sexpr,
                    expr: Sexpr,
                    literal_desc: dict[str, LiteralDescriptor | None],
                    literal_names: set[str],
                    evaluator: Evaluator,
                    bindings: dict[str, Sexpr | list]) -> bool:
    items = sl.to_python_list(expr)

    for count in range(len(items) + 1):
        prefix = items[:count]
        suffix = sl.from_python_list(items[count:])
        trial = deepcopy(bindings)

        if sp.is_symbol(pat_elem):
            name = pat_elem.name
            if name in literal_names:
                desc = literal_desc.get(name)
                if desc is None:
                    ok = all(sp.is_symbol(item) and item.name == name
                             for item in prefix)
                else:
                    ok = all(literal_matches(desc, item, evaluator)
                             for item in prefix)
                if not ok:
                    continue
            trial[name] = prefix
        else:
            repeated: dict[str, list] = {}
            ok = True
            for item in prefix:
                item_bindings: dict[str, Sexpr | list] = {}
                if not _match(pat_elem, item, literal_desc, literal_names,
                              evaluator, item_bindings):
                    ok = False
                    break
                _merge_repeated_bindings(repeated, item_bindings)
            if not ok:
                continue
            for key, values in repeated.items():
                trial[key] = values

        if _match(rest_pat, suffix, literal_desc, literal_names,
                  evaluator, trial):
            bindings.clear()
            bindings.update(trial)
            return True

    return False


class _TemplateExpander:
    _LET_FORMS = frozenset({"let", "let*", "letrec"})

    def __init__(self,
                 bindings: dict[str, Sexpr | list],
                 literal_names: set[str],
                 pattern_vars: set[str]):
        self.bindings = bindings
        self.literal_names = literal_names
        self.pattern_vars = pattern_vars
        self._introduced: dict[str, Symbol] = {}

    def expand(self, template: Sexpr) -> Sexpr:
        if sp.is_null(template):
            return NIL

        if sp.is_symbol(template):
            return self._expand_symbol(template, binding_position=False)

        if sp.is_pair(template):
            if _is_ellipsis_rest(template.cdr):
                return self._expand_ellipsis(template.car, template.cdr.cdr)
            if self._is_let_form(template):
                return self._expand_let_form(template)
            if self._is_lambda_form(template):
                return self._expand_lambda_form(template)
            return sl.cons(self.expand(template.car),
                           self.expand(template.cdr))

        return template

    def _is_let_form(self, template: Sexpr) -> bool:
        return (sp.is_pair(template)
                and sp.is_symbol(template.car)
                and template.car.name in self._LET_FORMS
                and sp.is_pair(template.cdr))

    def _is_lambda_form(self, template: Sexpr) -> bool:
        return (sp.is_pair(template)
                and sp.is_symbol(template.car)
                and template.car.name == "lambda"
                and sp.is_pair(template.cdr))

    def _expand_let_form(self, template: Sexpr) -> Sexpr:
        op = self._expand_symbol(template.car, binding_position=False)
        rest = template.cdr
        if sp.is_symbol(rest.car):
            loop_name = self._gensym(rest.car.name)
            bindings = rest.cdr.car
            body = rest.cdr.cdr
            return sl.cons(
                op,
                sl.cons(loop_name,
                        sl.cons(self._expand_let_bindings(bindings),
                                self._expand_sequence(body))))
        bindings = rest.car
        body = rest.cdr
        return sl.cons(op, sl.cons(self._expand_let_bindings(bindings),
                                   self._expand_sequence(body)))

    def _expand_lambda_form(self, template: Sexpr) -> Sexpr:
        op = self._expand_symbol(template.car, binding_position=False)
        params = template.cdr.car
        body = template.cdr.cdr
        return sl.cons(op, sl.cons(self._expand_lambda_params(params),
                                   self._expand_sequence(body)))

    def _expand_let_bindings(self, bindings: Sexpr) -> Sexpr:
        if sp.is_null(bindings):
            return NIL
        pair = bindings.car
        var = pair.car
        init = self.expand(sl.cadr(pair))
        new_var = self._expand_binding_identifier(var)
        rest = self._expand_let_bindings(bindings.cdr)
        return sl.cons(sl.cons(new_var, sl.cons(init, NIL)), rest)

    def _expand_lambda_params(self, params: Sexpr) -> Sexpr:
        if sp.is_null(params):
            return NIL
        if sp.is_symbol(params):
            return self._expand_binding_identifier(params)
        if sp.is_pair(params):
            return sl.cons(self._expand_binding_identifier(params.car),
                           self._expand_lambda_params(params.cdr))
        return params

    def _expand_sequence(self, body: Sexpr) -> Sexpr:
        if sp.is_null(body):
            return NIL
        if sp.is_pair(body.cdr) or not sp.is_null(body.cdr):
            if sp.is_null(body.cdr):
                return sl.cons(self.expand(body.car), NIL)
            return sl.cons(self.expand(body.car),
                           self._expand_sequence(body.cdr))
        return self.expand(body)

    def _expand_binding_identifier(self, var: Sexpr) -> Sexpr:
        if not sp.is_symbol(var):
            return self.expand(var)
        if var.name in self.pattern_vars:
            return self._expand_pattern_var(var)
        return self._gensym(var.name)

    def _expand_symbol(self,
                       template: Symbol,
                       *,
                       binding_position: bool) -> Sexpr:
        name = template.name
        if name in self.literal_names:
            return template
        if name in self.pattern_vars:
            return self._expand_pattern_var(template)
        if name in self._introduced:
            return self._introduced[name]
        if binding_position:
            return self._gensym(name)
        return template

    def _expand_pattern_var(self, template: Symbol) -> Sexpr:
        name = template.name
        if name not in self.bindings:
            raise MacroExpansionError(
                f"unbound pattern variable {name} in template")
        value = self.bindings[name]
        if isinstance(value, list):
            raise MacroExpansionError(
                f"ellipsis variable {name} used outside ellipsis template")
        return value

    def _gensym(self, hint: str) -> Symbol:
        if hint not in self._introduced:
            self._introduced[hint] = Gensym.fresh(hint)
        return self._introduced[hint]

    def _expand_ellipsis(self, pat_elem: Sexpr, rest_template: Sexpr) -> Sexpr:
        expanded_rest = self.expand(rest_template)

        if sp.is_symbol(pat_elem):
            items = self.bindings.get(pat_elem.name, [])
            if not isinstance(items, list):
                items = [items]
            result = expanded_rest
            for item in reversed(items):
                result = sl.cons(item, result)
            return result

        repeated = self._repeated_bindings_for(pat_elem)
        if not repeated:
            return expanded_rest

        length = len(next(iter(repeated.values())))
        result = expanded_rest
        for index in reversed(range(length)):
            local = {
                key: values[index]
                for key, values in repeated.items()
            }
            sub = _TemplateExpander(local, self.literal_names,
                                    self.pattern_vars)
            result = sl.cons(sub.expand(pat_elem), result)
        return result

    def _repeated_bindings_for(self,
                               pat_elem: Sexpr) -> dict[str, list]:
        probe: set[str] = set()
        _collect_pattern_vars(pat_elem, self.literal_names, "", probe)
        repeated: dict[str, list] = {}
        for name in probe:
            value = self.bindings.get(name)
            if isinstance(value, list):
                repeated[name] = value
        return repeated


def _expand_template(template: Sexpr,
                     bindings: dict[str, Sexpr | list],
                     literal_names: set[str],
                     pattern_vars: set[str]) -> Sexpr:
    return _TemplateExpander(bindings, literal_names, pattern_vars).expand(
        template)
