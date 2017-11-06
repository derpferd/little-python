import pytest

from littlepython import Features
from littlepython.tokenizer import Tokenizer, Tokens, Token
from tests import t


def test_advance():
    tokenizer = Tokenizer("123")
    assert tokenizer.cur_pos == 0
    assert tokenizer.cur_char == '1'
    tokenizer.advance()
    assert tokenizer.cur_pos == 1
    assert tokenizer.cur_char == '2'
    tokenizer.advance()
    assert tokenizer.cur_pos == 2
    assert tokenizer.cur_char == '3'
    tokenizer.advance()
    assert tokenizer.cur_char is None


def test_peek():
    tokenizer = Tokenizer("123")
    assert tokenizer.peek() == '2'
    assert tokenizer.peek(2) == '3'
    assert tokenizer.peek(3) is None
    tokenizer.advance()
    assert tokenizer.peek() == '3'
    assert tokenizer.peek(2) is None
    tokenizer.advance()
    assert tokenizer.peek() is None


def test_skip_comment():
    tokenizer = Tokenizer("#123\nbla")
    tokenizer.skip_comment()
    assert tokenizer.cur_pos == 4
    tokenizer = Tokenizer("213\n#123\nbla")
    for _ in range(4):
        tokenizer.advance()
    tokenizer.skip_comment()
    assert tokenizer.cur_pos == 8
    tokenizer = Tokenizer("213 #123\nbla")
    for _ in range(3):
        tokenizer.advance()
    tokenizer.skip_comment()
    assert tokenizer.cur_pos == 8
    tokenizer = Tokenizer("#123")
    tokenizer.skip_comment()
    assert tokenizer.cur_pos == 4


def test_skip_whitespace():
    tokenizer = Tokenizer(" \t  \nbla")
    tokenizer.skip_comment()
    assert tokenizer.cur_pos == 4


def test_number():
    tokenizer = Tokenizer("123")
    assert tokenizer.number() == t(123)
    tokenizer = Tokenizer("bla 123")
    for _ in range(4):
        tokenizer.advance()
    assert tokenizer.number() == t(123)
    tokenizer = Tokenizer("bla 1 bla")
    for _ in range(4):
        tokenizer.advance()
    assert tokenizer.number() == t(1)
    tokenizer = Tokenizer("bla 42 bla")
    for _ in range(4):
        tokenizer.advance()
    assert tokenizer.number() == t(42)


def test_id():
    tokenizer = Tokenizer("bla")
    assert tokenizer.id() == t("bla")
    tokenizer = Tokenizer("bla foo")
    for _ in range(4):
        tokenizer.advance()
    assert tokenizer.id() == t("foo")
    tokenizer = Tokenizer("bla foo bar")
    for _ in range(4):
        tokenizer.advance()
    assert tokenizer.id() == t("foo")
    tokenizer = Tokenizer("if")
    assert tokenizer.id() == t("if")
    tokenizer = Tokenizer("else")
    assert tokenizer.id() == t("else")
    tokenizer = Tokenizer("_a")
    assert tokenizer.id() == t("_a")


@pytest.mark.parametrize("token_str,token_obj", Tokens.get_multi_word_keywords(Features.ALL).items())
def test_test_for_multi_word_keyword_all(token_str, token_obj):
    tokenizer = Tokenizer(token_str)
    assert tokenizer.test_for_multi_word_keyword() == token_obj


def test_test_for_multi_word_keyword():
    tokenizer = Tokenizer("is not")
    assert tokenizer.test_for_multi_word_keyword() == t("is not")
    tokenizer = Tokenizer("is not bla")
    assert tokenizer.test_for_multi_word_keyword() == t("is not")
    tokenizer = Tokenizer("bla is not foo bar")
    for _ in range(4):
        tokenizer.advance()
    assert tokenizer.test_for_multi_word_keyword() == t("is not")
    tokenizer = Tokenizer("is")
    assert not tokenizer.test_for_multi_word_keyword()
    tokenizer = Tokenizer("is nob")
    assert not tokenizer.test_for_multi_word_keyword()
    tokenizer = Tokenizer("bla is nob foo bar")
    for _ in range(4):
        tokenizer.advance()
    assert not tokenizer.test_for_multi_word_keyword()
    tokenizer = Tokenizer("bla ps not foo bar")
    for _ in range(4):
        tokenizer.advance()
    assert not tokenizer.test_for_multi_word_keyword()


def test_test_for_multi_word_keyword_trailing_alpha_1():
    tokenizer = Tokenizer("is nott")
    assert not tokenizer.test_for_multi_word_keyword()


def test_test_for_multi_word_keyword_trailing_alpha_2():
    tokenizer = Tokenizer("bla is notfoo bar")
    for _ in range(4):
        tokenizer.advance()
    assert not tokenizer.test_for_multi_word_keyword()


def test_test_for_multi_word_keyword_trailing_digit_1():
    tokenizer = Tokenizer("is not3")
    assert not tokenizer.test_for_multi_word_keyword()


def test_test_for_multi_word_keyword_trailing_digit_2():
    tokenizer = Tokenizer("bla is not12 bar")
    for _ in range(4):
        tokenizer.advance()
    assert not tokenizer.test_for_multi_word_keyword()


@pytest.mark.parametrize("token_str,token_obj", Tokens.get_non_alpha(Features.ALL).items())
def test_test_for_non_alpha(token_str, token_obj):
    tokenizer = Tokenizer(token_str)
    assert tokenizer.test_for_non_alpha() == token_obj


@pytest.mark.parametrize("token_str,token_obj", Tokens.get_non_alpha(Features.ALL).items())
def test_test_for_non_alpha_without_spaces(token_str, token_obj):
    tokenizer = Tokenizer("bla2" + token_str + "1")
    for _ in range(4):
        tokenizer.advance()
    assert tokenizer.test_for_non_alpha() == token_obj


@pytest.mark.parametrize("token_str,token_obj", Tokens.get_non_alpha(Features.ALL).items())
def test_test_for_non_alpha_with_spaces(token_str, token_obj):
    tokenizer = Tokenizer("bla2 " + token_str + " 1")
    for _ in range(5):
        tokenizer.advance()
    assert tokenizer.test_for_non_alpha() == token_obj


@pytest.mark.parametrize("token_str,token_obj", Tokens.get_non_alpha(Features.ALL).items())
def test_test_for_non_alpha_with_digits(token_str, token_obj):
    tokenizer = Tokenizer("2" + token_str + "1")
    for _ in range(1):
        tokenizer.advance()
    assert tokenizer.test_for_non_alpha() == token_obj


@pytest.mark.parametrize("token_str,token_obj", Tokens.get_non_alpha(Features.ALL).items())
def test_test_for_non_alpha_with_alpha(token_str, token_obj):
    tokenizer = Tokenizer("a" + token_str + "b")
    for _ in range(1):
        tokenizer.advance()
    assert tokenizer.test_for_non_alpha() == token_obj


def test_get_next_token_1():
    tokenizer = Tokenizer("1 if else 321 not is not < >= <= > ) * +213-432=vfe-elset else-")
    tokens = [t(1), t("if"), t("else"),
              t(321), t("not"), t("is not"),
              t("<"), t(">="), t("<="),
              t(">"), t(")"), t("*"),
              t("+"), t(213), t("-"),
              t(432), t("="), t("vfe"),
              t("-"), t("elset"), t("else"),
              t("-"), t(None)]
    for token in tokens:
        assert tokenizer.get_next_token() == token


def test_get_next_token_2():
    tokenizer = Tokenizer("(1+2)/4 > 1 + 2 and 1 < 3 or 2%5 >= 3 or 3*4 <= 4/2 and not 1 is 2 or 4 is not 5")
    s = t("and")
    tokens = [t("("), t("1"), t("+"), t("2"), t(")"), t("/"), t("4"), t(">"), t("1"), t("+"), t("2"), t("and"), t("1"),
              t("<"), t("3"), t("or"), t("2"), t("%"), t("5"), t(">="), t("3"), t("or"), t("3"), t("*"), t("4"),
              t("<="), t("4"), t("/"), t("2"), t("and"), t("not"), t("1"), t("is"), t("2"), t("or"), t("4"),
              t("is not"), t("5")]
    for token in tokens:
        assert tokenizer.get_next_token() == token


def test_get_next_token_3():
    tokenizer = Tokenizer("if\n{ else } if else elif")
    tokens = [t("if"), t("\n"), t("{"), t("else"), t("}"), t("if"), t("else"), t("elif"), t(None)]
    for token in tokens:
        assert tokenizer.get_next_token() == token


def test_get_next_token_4():
    tokenizer = Tokenizer("bar\n\n\n\nfoo")
    tokens = [t("bar"), t("\n"), t("foo"), t(None)]
    for token in tokens:
        assert tokenizer.get_next_token() == token


def test_get_next_token_5():
    tokenizer = Tokenizer("|")
    with pytest.raises(Exception):
        tokenizer.get_next_token()


def test_get_next_token_6():
    tokenizer = Tokenizer("&")
    with pytest.raises(Exception):
        tokenizer.get_next_token()


def test_get_next_token_7():
    tokenizer = Tokenizer("\r\t &")
    with pytest.raises(Exception):
        tokenizer.get_next_token()


def test_get_next_token_8():
    tokenizer = Tokenizer("123$")
    tokenizer.get_next_token()
    with pytest.raises(Exception):
        tokenizer.get_next_token()


@pytest.mark.parametrize("token_str,token_obj", Tokens.get_all(Features.ALL).items())
def test_token_str_and_repr(token_str, token_obj):
    assert str(token_obj) == token_str
    assert repr(token_obj) == "Token<type:{}, value:{}>".format(token_obj.type, token_str)


def test_token_eq_with_different_type():
    assert t("1") != 1
    assert t("ab") != "ab"


def test_token_from_str_invalid():
    with pytest.raises(ValueError) as err:
        Token.from_str("^")
    assert "Invalid input" in str(err.value)


def test_tokenizer__iter__():
    tokenizer = Tokenizer("adsf")
    assert tokenizer is tokenizer.__iter__()


def test_tokenizer_stop_iter():
    tokenizer = Tokenizer("")
    assert next(tokenizer) == t(None)
    with pytest.raises(StopIteration):
        next(tokenizer)
