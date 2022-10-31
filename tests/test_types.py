
import pytest
from typing import Any

from unified_image_reader import types


@pytest.mark.parametrize("obj, should_be_region_index", [
    (10, True),
    (10.0, True),
    (10.1, False)
])
def test_is_region_index(obj: Any, should_be_region_index: bool):
    assert types.is_region_index(obj) == should_be_region_index
