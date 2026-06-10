from pathlib import Path

import pytest

_UNIMPLEMENTED_DIR = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if _UNIMPLEMENTED_DIR in Path(str(item.fspath)).resolve().parents:
            item.add_marker(
                pytest.mark.xfail(reason="not yet implemented", strict=False)
            )
