import pytest

from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer
from tests import _for, c, v, asg, lt, blk, add, getitem


def test_simple():
    ast = _for(asg(v("i"), c(0)),
               lt(v("i"), c(10)),
               asg(v("i"), add(v("i"), c(1))),
               blk([asg(v("a"), c(1))]))
    parser = Parser(Tokenizer("for i = 0; i < 10; i = i + 1 {a = 1}"))
    assert parser.statement() == ast


def test_array():
    ast = _for(asg(v("i"), c(0)),
               lt(v("i"), c(10)),
               asg(v("i"), add(v("i"), c(1))),
               blk([asg(v("a"), getitem(v("b"), v("i")))]))
    parser = Parser(Tokenizer("for i = 0; i < 10; i = i + 1 {a = b[i]}"))
    assert parser.statement() == ast
