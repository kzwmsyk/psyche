"""R5RS number procedures beyond basic arithmetic."""


def test_abs(eval_str):
    assert eval_str("(abs -5)") == "5"


def test_max_min(eval_str):
    assert eval_str("(max 1 5 3)") == "5"
    assert eval_str("(min 1 5 3)") == "1"


def test_quotient_remainder_modulo(eval_str):
    assert eval_str("(quotient 10 3)") == "3"
    assert eval_str("(remainder 10 3)") == "1"
    assert eval_str("(modulo 10 3)") == "1"
    assert eval_str("(modulo -10 3)") == "2"


def test_gcd_lcm(eval_str):
    assert eval_str("(gcd 12 8)") == "4"
    assert eval_str("(lcm 12 8)") == "24"


def test_floor_ceiling_truncate_round(eval_str):
    assert eval_str("(floor 3.7)") == "3"
    assert eval_str("(ceiling 3.2)") == "4"
    assert eval_str("(truncate 3.7)") == "3"
    assert eval_str("(round 3.5)") == "4"


def test_exact_inexact_conversion(eval_str):
    assert eval_str("(inexact? (exact->inexact 1))") == "#t"
    assert eval_str("(exact? (inexact->exact 2.0))") == "#t"


def test_expt_sqrt(eval_str):
    assert eval_str("(expt 2 3)") == "8"
    assert eval_str("(sqrt 9)") == "3.0"


def test_number_predicates(eval_str):
    assert eval_str("(complex? 1)") == "#t"
    assert eval_str("(real? 1)") == "#t"
    assert eval_str("(rational? 1)") == "#t"
