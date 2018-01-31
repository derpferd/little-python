from tests.interpreter import run


def test_func_call_without_assign():
    b = {}
    e = run("x=0 func test() { x = 2} test()")
    assert e == {"x": 2}


def test_func_accessing_global_scope():
    b = {}
    e = run("x=0 func test() { return x + 2} a = test()")
    assert e == {"x": 0, "a": 2}


def test_func_scope_overlapping_global():
    b = {}
    e = run("x=0 func test(x) { x = x + 1} test(2)")
    assert e == {"x": 3}
