import pytest

from littlepython import Features
from littlepython.tokenizer import Tokenizer
from tests import t


def test_elif_disabled():
    tokenizer = Tokenizer("elif", Features.NONE)
    tokens = [t("elif")]
    for token in tokens:
        assert tokenizer.get_next_token() != token


def test_elif_enabled():
    tokenizer = Tokenizer("elif", Features.ELIF)
    tokens = [t("elif")]
    for token in tokens:
        assert tokenizer.get_next_token() == token


def test_if_disabled():
    tokenizer = Tokenizer("if else", Features.NONE)
    tokens = [t("if"), t("else")]
    for token in tokens:
        assert tokenizer.get_next_token() != token


def test_if_enabled():
    tokenizer = Tokenizer("if else", Features.IF)
    tokens = [t("if"), t("else")]
    for token in tokens:
        assert tokenizer.get_next_token() == token


def test_array_disabled():
    tokenizer = Tokenizer("[", Features.NONE)
    with pytest.raises(Exception):
        tokenizer.get_next_token()
    tokenizer = Tokenizer("]", Features.NONE)
    with pytest.raises(Exception):
        tokenizer.get_next_token()


def test_array_enabled():
    tokenizer = Tokenizer("[ ] []", Features.TYPE_ARRAY)
    tokens = [t("["), t("]"), t("["), t("]")]
    for token in tokens:
        assert tokenizer.get_next_token() == token
