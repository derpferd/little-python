import pytest

from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer
from tests.parser import getitem, v, c, blk, asg, _is, _if, ctrl, setitem


@pytest.mark.parametrize("var, var_str", [
    (v("a"), "a"),
    (getitem(v("a"), c(1)), "a[1]"),
])
@pytest.mark.parametrize("expr, expr_str", [
    (c(0), "0"),
    (v("b"), "b"),
])
def test_getitem(var, expr, var_str, expr_str):
    ast = getitem(var, expr)
    parser = Parser(Tokenizer(var_str+"["+expr_str+"]"))
    assert parser.variable() == ast


def test_setitem():
    ast = setitem(v("a"), c(0), c(1))
    parser = Parser(Tokenizer("a[0] = 1"))
    assert parser.statement() == ast


def test_if():
    ast = ctrl([_if(_is(getitem(v("a"), c(0)), c(8)), blk([asg(v("b"), c(3))]))], blk())
    parser = Parser(Tokenizer("if a[0] is 8 { b = 3 }"))
    assert parser.statement() == ast
