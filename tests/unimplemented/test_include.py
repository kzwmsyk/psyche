import pytest

from tests.support.harness import eval_string_as_string

pytestmark = pytest.mark.unimplemented


def test_include(eval_str):
    assert eval_str('(include "prelude.scm")') == "nil"
