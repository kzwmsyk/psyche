from tests.support.harness import eval_string_as_string


def test_arithmetic(eval_str):
    assert eval_str("(+ 1 2 3)") == "6"
    assert eval_str("(- 10 3)") == "7"
    assert eval_str("(- 5)") == "-5"
    assert eval_str("(* 2 3 4)") == "24"
    assert eval_str("(/ 8 2)") == "4.0"


def test_not(eval_str):
    assert eval_str("(not #f)") == "#t"
    assert eval_str("(not 0)") == "#f"


def test_list_operations(eval_str):
    assert eval_str("(car (cons 1 2))") == "1"
    assert eval_str("(cdr (cons 1 2))") == "2"
    assert eval_str("(cons 1 (cons 2 nil))") == "(1 2)"


def test_set_car_and_set_cdr(eval_str):
    code = """
    (begin
      (define p (cons 1 2))
      (set-car! p 9)
      (set-cdr! p 8)
      p)
    """
    assert eval_str(code) == "(9 . 8)"


def test_type_predicates(eval_str):
    assert eval_str("(boolean? #t)") == "#t"
    assert eval_str("(null? nil)") == "#t"
    assert eval_str("(pair? (cons 1 2))") == "#t"
    assert eval_str("(symbol? 'x)") == "#t"
    assert eval_str("(number? 1)") == "#t"
    assert eval_str("(string? \"a\")") == "#t"


def test_eqv(eval_str):
    assert eval_str("(eqv? 'a 'a)") == "#t"
    assert eval_str("(eqv? 1 1)") == "#t"
    assert eval_str("(eqv? 'a 'b)") == "#f"


def test_apply(eval_str):
    assert eval_str("(apply + (list 1 2 3))") == "6"
    assert eval_str("(apply + 1 2 (list 3 4))") == "10"


def test_numeric_comparison(eval_str):
    assert eval_str("(= 1 1)") == "#t"
    assert eval_str("(< 1 2)") == "#t"
    assert eval_str("(> 5 3)") == "#t"
    assert eval_str("(<= 2 2)") == "#t"
    assert eval_str("(>= 3 2)") == "#t"


def test_procedure_p(eval_str):
    assert eval_str("(procedure? (lambda (x) x))") == "#t"
    assert eval_str("(procedure? +)") == "#t"
    assert eval_str("(procedure? 1)") == "#f"


def test_eq_and_eqv(eval_str):
    assert eval_str("(eqv? 2 2)") == "#t"
    assert eval_str("(eq? 2 2)") == "#f"
    assert eval_str("(eq? 'a 'a)") == "#t"
    code = """
    (begin
      (define p (cons 1 2))
      (eq? p p))
    """
    assert eval_str(code) == "#t"
    assert eval_str("(eq? (cons 1 2) (cons 1 2))") == "#f"
