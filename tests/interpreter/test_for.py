import pytest

from littlepython.interpreter import ExecutionCountExceededException
from tests.interpreter import run


def test_normal_for():
    e = run("x = 0 for i = 0; i < 10; i = i + 1 {x = x + 1}")
    assert e == {"x": 10, "i": 10}


def test_for_with_empty_statements():
    e = run("x = 0 for ;x < 10; {x = x + 1}")
    assert e == {"x": 10}


def test_infinite_for_loop():
    with pytest.raises(ExecutionCountExceededException):
        run("x = 0 for ;1; {x = x + 1}", max_op_count=1000)
