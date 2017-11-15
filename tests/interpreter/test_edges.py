"""This file contains tests to test edge cases relating to the program code text."""
from tests.interpreter import run


def test_empty():
    e = run("")
    assert e == {}


def test_newlines():
    e = run("\n" * 8)
    assert e == {}


def test_trailing_newlines():
    e = run("a=2" + "\n" * 8)
    assert e["a"] == 2
