from __future__ import division
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
@pytest.mark.parametrize("b", [
    -10,
    -1,
    0,
    1,
    2,
    10,
    2150,
])
@pytest.mark.parametrize("op_str, op_lambda", [
    ("+", lambda a, b: a + b),
    ("-", lambda a, b: a - b),
    ("*", lambda a, b: a * b),
    ("/", lambda a, b: a // b),
    ("%", lambda a, b: a % b),
    ("<", lambda a, b: a < b),
    (">", lambda a, b: a > b),
    ("<=", lambda a, b: a <= b),
    (">=", lambda a, b: a >= b),
])
def test_binary_integer_ops(a, b, op_str, op_lambda):
    code = "c = a {} b".format(op_str)

    if op_str in "/%" and b == 0:
        with pytest.raises(ZeroDivisionError):
            run(code, a=a, b=b)
    else:
        out = run(code, a=a, b=b)
        assert out["c"] == op_lambda(a, b)


@pytest.mark.parametrize("a", [
    (0,),
    (1,),
])
@pytest.mark.parametrize("b", [
    (0,),
    (1,),
])
@pytest.mark.parametrize("op_str, op_lambda", [
    ("and", lambda a, b: a and b),
    ("or", lambda a, b: a or b),
    ("is", lambda a, b: a == b),
    ("is not", lambda a, b: a != b),
])
def test_binary_logical_ops(a, b, op_str, op_lambda):
    code = "c = a {} b".format(op_str)
    out = run(code, a=a, b=b)
    assert out["c"] == op_lambda(a, b)


@pytest.mark.parametrize("a", [
    (0,),
    (1,),
])
def test_op_not(a):
    end = run("b = not a", a=a)
    assert end["b"] == (not a)


@pytest.mark.parametrize("a", [
    (0,),
    (1,),
])
@pytest.mark.parametrize("b", [
    0,
    1,
])
def test_op_not_or(a, b):
    end = run("c = not (a or b)", a=a, b=b)
    assert end["c"] == (not (a or b))
