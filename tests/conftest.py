import pytest

from tests.support.harness import make_evaluator, to_string


@pytest.fixture
def evaluator():
    return make_evaluator()


@pytest.fixture
def eval_str():
    from tests.support.harness import eval_string_as_string

    return eval_string_as_string
