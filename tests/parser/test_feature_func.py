import pytest

from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer
from tests import _def, c, v, asg, v, blk, add, getitem, func, sig, call, ret


def test_simple():
    ast = _def(v("t"),
               sig([]),
               blk([asg(v("a"), c(1))]))

    parser = Parser(Tokenizer("func t() {a = 1}"))
    assert parser.statement() == ast


def test_simple_return():
    ast = _def(v("t"),
               sig([]),
               blk([ret(c(1))]))

    parser = Parser(Tokenizer("func t() {return 1}"))
    assert parser.statement() == ast


def test_simple_return_var():
    ast = _def(v("t"),
               sig([]),
               blk([asg(v("a"), c(1)), ret(v("a"))]))

    parser = Parser(Tokenizer("func t() {a = 1\nreturn a}"))
    assert parser.statement() == ast


def test_with_params():
    ast = _def(v("t"),
               sig([v("b"), v("c")]),
               blk([asg(v("a"), c(1))]))

    parser = Parser(Tokenizer("func t(b, c) {a = 1}"))
    assert parser.statement() == ast


def test_call():
    ast = asg(v("a"), call(v("t"), [v("b"), v("c")]))

    parser = Parser(Tokenizer("a = t(b, c)"))
    assert parser.statement() == ast


def test_call_with_add():
    ast = asg(v("a"), call(v("t"), [add(v("b"), c(2)), add(c(1), v("c"))]))

    parser = Parser(Tokenizer("a = t(b+2, 1+c)"))
    assert parser.statement() == ast
