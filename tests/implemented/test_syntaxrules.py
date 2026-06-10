from syntaxrules import expand_syntax_rules

from tests.support.harness import make_evaluator, read_string, to_string


def test_expand_when_macro():
    evaluator = make_evaluator()
    pattern = read_string("(when test body ...)")[0]
    template = read_string("(if test (begin body ...))")[0]
    form = read_string("(when #f 99)")[0]
    expanded = expand_syntax_rules("when", [], [(pattern, template)], form,
                                   evaluator)
    assert to_string(expanded) == "(if #f (begin 99))"


def test_hygienic_introduced_binding():
    evaluator = make_evaluator()
    code = """
    (begin
      (define x 1)
      (define-syntax shadow
        (syntax-rules ()
          ((shadow body)
           (let ((x 2)) body))))
      (shadow x))
    """
    from tests.support.harness import eval_string_as_string
    assert eval_string_as_string(code, load_prelude=False) == "1"


def test_compound_ellipsis_template():
    evaluator = make_evaluator()
    code = """
    (begin
      (define-syntax pair-list
        (syntax-rules ()
          ((pair-list (x y) ...)
           (list (list x y) ...))))
      (pair-list (1 2) (3 4)))
    """
    from tests.support.harness import eval_string_as_string
    assert eval_string_as_string(code) == "((1 2) (3 4))"


def test_nested_ellipsis_pattern():
    code = """
    (begin
      (define-syntax nest
        (syntax-rules ()
          ((nest (x ...) ...)
           (list (list x ...) ...))))
      (nest (1 2) (3 4)))
    """
    from tests.support.harness import eval_string_as_string
    assert eval_string_as_string(code) == "((1 2) (3 4))"


def test_hygienic_loop_binding():
    code = """
    (begin
      (define loop 99)
      (define-syntax repeat
        (syntax-rules ()
          ((repeat n body ...)
           (let loop ((i n))
             (if (> i 0)
                 (begin body ... (loop (- i 1))))))))
      (repeat 1 loop)
      loop)
    """
    from tests.support.harness import eval_string_as_string
    assert eval_string_as_string(code) == "99"


def test_improper_list_pattern():
    evaluator = make_evaluator()
    code = """
    (begin
      (define-syntax dotted
        (syntax-rules ()
          ((dotted (a . b))
           (cons 'dotted (cons a b)))))
      (dotted (1 . 2)))
    """
    from tests.support.harness import eval_string_as_string
    assert eval_string_as_string(code, load_prelude=False) == "(dotted 1 . 2)"
