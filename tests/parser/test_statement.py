from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer
from tests import v


def test_var():
    ast = v("a")
    parser = Parser(Tokenizer("a"))
    assert parser.statement() == ast
