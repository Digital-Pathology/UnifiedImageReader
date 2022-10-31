
# TODO - add pytest to dev-container
import pytest

# https://docs.pytest.org/en/7.2.x/getting-started.html


@pytest.mark.parametrize(
    "arg1, arg2", [
        (1, 1),
        (2, 2),
        (1, 2)
    ]
)
def test_addition(arg1, arg2):
    assert (arg1+arg2 < 10)
