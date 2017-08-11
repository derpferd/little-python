from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer
from tests.parser import v, c, asg, add


def test_simple():
    ast = asg(v("b"), c(1))
    parser = Parser(Tokenizer("b = 1"))
    assert parser.statement() == ast


def test_var_to_var():
    ast = asg(v("a"), v("b"))
    parser = Parser(Tokenizer("a=b"))
    assert parser.statement() == ast


def test_var_to_expr():
    ast = asg(v("a"), add(v("b"), c(1)))
    parser = Parser(Tokenizer("a=b+1"))
    assert parser.statement() == ast
