import pytest

from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer
from tests import getitem, v, c, blk, asg, _is, _if, ctrl, setitem, add


@pytest.mark.parametrize("var, var_str", [
    (v("a"), "a"),
    (getitem(v("a"), c(1)), "a[1]"),
])
@pytest.mark.parametrize("expr, expr_str", [
    (c(0), "0"),
    (v("b"), "b"),
    (add(v("b"), c(1)), "b+1"),
])
def test_getitem(var, expr, var_str, expr_str):
    ast = getitem(var, expr)
    parser = Parser(Tokenizer(var_str+"["+expr_str+"]"))
    assert parser.variable() == ast


@pytest.mark.parametrize("var, var_str", [
    (v("a"), "a"),
    (getitem(v("a"), c(1)), "a[1]"),
])
@pytest.mark.parametrize("expr, expr_str", [
    (c(0), "0"),
    (add(v("b"), c(1)), "b+1"),
    (v("b"), "b"),
])
@pytest.mark.parametrize("val, val_str", [
    (c(0), "0"),
    (v("c"), "c"),
    (getitem(v("c"), c(1)), "c[1]"),
])
def test_setitem(var, expr, val, var_str, expr_str, val_str):
    ast = setitem(var, expr, val)
    parser = Parser(Tokenizer(var_str+"["+expr_str+"]"+"="+val_str))
    assert parser.statement() == ast


def test_if():
    ast = ctrl([_if(_is(getitem(v("a"), c(0)), c(8)), blk([asg(v("b"), c(3))]))], blk())
    parser = Parser(Tokenizer("if a[0] is 8 { b = 3 }"))
    assert parser.statement() == ast
