import pytest

from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer, TokenTypes


def test_eat_wrong_type_error():
    parser = Parser(Tokenizer("not b+1"))
    with pytest.raises(Exception):
        parser.eat(TokenTypes.CONST)
    parser.eat(TokenTypes.NOT)
    with pytest.raises(Exception):
        parser.eat(TokenTypes.CONST)
    parser.eat(TokenTypes.VAR)
    with pytest.raises(Exception):
        parser.eat(TokenTypes.CONST)
    parser.eat(TokenTypes.ADD)
    with pytest.raises(Exception):
        parser.eat(TokenTypes.VAR)
    parser.eat(TokenTypes.CONST)


def test_error():
    parser = Parser(Tokenizer(""))
    with pytest.raises(Exception) as err:
        parser.error("Bla bla bla")
    assert "Invalid syntax: Bla bla bla" in str(err.value)
