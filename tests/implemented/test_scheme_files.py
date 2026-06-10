from pathlib import Path

import pytest

from tests.support.harness import run_scheme_test_file

SCHEME_TESTS = sorted(Path(__file__).parent.joinpath("scheme").glob("test_*.scm"))


@pytest.mark.parametrize("path", SCHEME_TESTS, ids=lambda p: p.name)
def test_scheme_file(path: Path):
    failures = run_scheme_test_file(path)
    assert failures == 0
