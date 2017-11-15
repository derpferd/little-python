import pytest
from tests.interpreter import run


@pytest.mark.parametrize("a", [
    -10,
    -1,
    0,
    1,
    2,
    10,
    2150,
])
def test_int_consts(a):
    end = run("a={}".format(a))
    assert end["a"] == a


# TODO: when array consts are a thing add the tests here.
