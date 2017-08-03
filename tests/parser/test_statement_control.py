from littlepython.parser import Tokenizer, Parser
from tests.parser import _if, ctrl, blk, _is, v, c, asg


def test_if():
    ast = ctrl([_if(_is(v("a"), c(8)), blk([asg(v("b"), c(3))]))], blk())
    parser = Parser(Tokenizer("if a is 8 { b = 3 }"))
    assert parser.statement() == ast


def test_if_with_new_lines():
    ast = ctrl([_if(_is(v("a"), c(8)), blk([asg(v("b"), c(3))]))], blk())
    parser = Parser(Tokenizer("if a is 8 {\nb = 3\n}"))
    assert parser.statement() == ast


def test_empty_if():
    ast = ctrl([_if(_is(v("a"), c(8)), blk())], blk())
    parser = Parser(Tokenizer("if a is 8 { }"))
    assert parser.statement() == ast


def test_empty_if_with_new_line():
    ast = ctrl([_if(_is(v("a"), c(8)), blk())], blk())
    parser = Parser(Tokenizer("if a is 8 { \n }"))
    assert parser.statement() == ast


def test_if_else():
    ast = ctrl([_if(_is(v("a"), c(8)), blk([asg(v("b"), c(3))]))], blk([asg(v("b"), c(2))]))
    parser = Parser(Tokenizer("if a is 8 { b = 3 } else { b = 2 }"))
    assert parser.statement() == ast


def test_if_elif():
    ast = ctrl([_if(_is(v("a"), c(8)), blk([asg(v("b"), c(3))])),
                _if(_is(v("a"), c(4)), blk([asg(v("b"), c(2))]))], blk())
    parser = Parser(Tokenizer("if a is 8 { b = 3 } elif a is 4 { b = 2 }"))
    assert parser.statement() == ast


def test_if_elif_else():
    ast = ctrl([_if(_is(v("a"), c(8)), blk([asg(v("b"), c(3))])),
                _if(_is(v("a"), c(4)), blk([asg(v("b"), c(2))]))], blk([asg(v("b"), c(2))]))
    parser = Parser(Tokenizer("if a is 8 { b = 3 } elif a is 4 { b = 2 } else { b = 2 }"))
    assert parser.statement() == ast


def test_if_elif_elif_else():
    ast = ctrl([_if(_is(v("a"), c(8)), blk([asg(v("b"), c(3))])),
                _if(_is(v("a"), c(4)), blk([asg(v("b"), c(2))])),
                _if(_is(v("a"), c(7)), blk([asg(v("b"), c(6))]))], blk([asg(v("b"), c(2))]))
    parser = Parser(Tokenizer("if a is 8 { b = 3 } elif a is 4 { b = 2 } elif a is 7 { b = 6 } else { b = 2 }"))
    assert parser.statement() == ast
