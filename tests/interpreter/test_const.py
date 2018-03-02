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


@pytest.mark.parametrize("a", [
    [],
    [1, 2, 3, 4],
    [[1, 2], [3, 4]],
    [[[[[1]]]], [2, 2, 3, [3]]],
])
def test_array_consts(a):
    end = run("a={}".format(a))
    assert end["a"] == a

