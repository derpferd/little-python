import pytest

from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer
from tests.parser import EOF, v, c, add, _not, div, _and, sub, _or, gt, lt, mod, ge, le, mult, _is_not, _is


@pytest.mark.parametrize("op, op_str", [
    (add, "+"),
    (sub, "-"),
    (_not, "not"),
])
@pytest.mark.parametrize("operand, operand_str", [
    (c(1), "1"),
    (v("a"), "a"),
])
def test_uniary_ops(op, operand, op_str, operand_str):
    ast = op(operand)
    s = op_str+" "+operand_str
    parser = Parser(Tokenizer(s))
    assert parser.expression() == ast


@pytest.mark.parametrize("op, op_str", [
    (div, "/"),
    (mod, "%"),
    (mult, "*"),
    (add, "+"),
    (sub, "-"),
    (_is, "is"),
    (_is_not, "is not"),
    (gt, ">"),
    (lt, "<"),
    (ge, ">="),
    (le, "<="),
    (_or, "or"),
    (_and, "and"),
])
@pytest.mark.parametrize("left, left_str", [
    (c(1), "1"),
    (sub(c(1)), "-1"),
    (v("a"), "a"),
])
@pytest.mark.parametrize("right, right_str", [
    (c(2), "2"),
    (sub(c(2)), "-2"),
    (v("b"), "b"),
])
def test_binary_ops_all_levels(op, left, right, op_str, left_str, right_str):
    ast = op(left, right)
    s = " ".join((left_str, op_str, right_str))
    parser = Parser(Tokenizer(s))
    assert parser.expression() == ast


@pytest.mark.parametrize("op, op_str", [
    (div, "/"),
    (mod, "%"),
    (mult, "*"),
])
@pytest.mark.parametrize("left, left_str", [
    (c(1), "1"),
    (sub(c(1)), "-1"),
    (v("a"), "a"),
])
@pytest.mark.parametrize("right, right_str", [
    (c(2), "2"),
    (sub(c(2)), "-2"),
    (v("b"), "b"),
])
def test_binary_ops_level_5_and_below(op, left, right, op_str, left_str, right_str):
    ast = op(left, right)
    s = left_str+op_str+right_str
    parser = Parser(Tokenizer(s))
    assert parser.expression() == ast


@pytest.mark.parametrize("op, op_str", [
    (add, "+"),
    (sub, "-"),
])
@pytest.mark.parametrize("left, left_str", [
    (c(1), "1"),
    (div(c(1), c(3)), "1/3"),
    (sub(c(1)), "-1"),
    (v("a"), "a"),
])
@pytest.mark.parametrize("right, right_str", [
    (c(2), "2"),
    (div(c(2), c(4)), "2/4"),
    (sub(c(2)), "-2"),
    (v("b"), "b"),
])
def test_binary_ops_level_4_and_below(op, left, right, op_str, left_str, right_str):
    ast = op(left, right)
    s = left_str+op_str+right_str
    parser = Parser(Tokenizer(s))
    assert parser.expression() == ast


# TODO: add tests for levels 3-1 including lower levels in the tests.


def test_unary_var():
    ast = _not(v("b"))
    parser = Parser(Tokenizer("not b"))
    assert parser.expression() == ast


def test_var_bin_var():
    ast = add(v("a"), v("b"))
    parser = Parser(Tokenizer("a+b"))
    assert parser.expression() == ast


def test_const_bin_var():
    ast = add(c(1), v("b"))
    parser = Parser(Tokenizer("1+b"))
    assert parser.expression() == ast


def test_multiple_same_priority_bins_1():
    ast1 = add(c(1), add(v("b"), c(4)))
    ast2 = add(add(c(1), v("b")), c(4))
    parser = Parser(Tokenizer("1+b+4"))
    expr = parser.expression()
    assert expr == ast1 or expr == ast2


def test_multiple_same_priority_bins_2():
    ast1 = add(c(1), add(v("b"), add(c(4), v("a"))))
    ast2 = add(add(add(c(1), v("b")), c(4)), v("a"))
    parser = Parser(Tokenizer("1+b+4+a"))
    expr = parser.expression()
    assert expr == ast1 or expr == ast2


def test_multiple_same_priority_bins_3():
    ast1 = sub(c(1), add(v("b"), c(4)))
    ast2 = add(sub(c(1), v("b")), c(4))
    parser = Parser(Tokenizer("1-b+4"))
    expr = parser.expression()
    assert expr == ast1 or expr == ast2


def test_multiple_same_priority_bins_4():
    ast1 = sub(c(1), add(v("b"), sub(c(4), v("a"))))
    ast2 = sub(add(sub(c(1), v("b")), c(4)), v("a"))
    parser = Parser(Tokenizer("1-b+4-a"))
    expr = parser.expression()
    assert expr == ast1 or expr == ast2


def test_differing_priority_bins_1():
    ast = add(c(1), div(v("b"), c(4)))
    parser = Parser(Tokenizer("1+b/4"))
    assert parser.expression() == ast


def test_differing_priority_bins_2():
    ast = add(div(c(1), v("b")), c(4))
    parser = Parser(Tokenizer("1/b+4"))
    assert parser.expression() == ast


def test_parens():
    ast = div(add(c(1), v("b")), c(4))
    parser = Parser(Tokenizer("(1+b)/4"))
    assert parser.expression() == ast


def test_tailing_new_line():
    ast = add(v("a"), v("b"))
    parser = Parser(Tokenizer("a+b\n"))
    assert parser.expression() == ast
    assert parser.cur_token == EOF


def test_lt_1():
    ast = lt(div(add(c(1), c(2)), c(3)), add(c(4), c(5)))
    parser = Parser(Tokenizer("(1+2)/3 < 4 + 5"))
    assert parser.expression() == ast


def test_lt_2():
    ast = lt(div(add(c(1), c(2)), c(3)), add(c(1), c(2)))
    parser = Parser(Tokenizer("(1+2)/3 < 1 + 2"))
    assert parser.expression() == ast


def test_gt_1():
    ast = gt(div(add(c(1), c(2)), c(3)), add(c(4), c(5)))
    parser = Parser(Tokenizer("(1+2)/3 > 4 + 5"))
    assert parser.expression() == ast


def test_gt_2():
    ast = gt(div(add(c(1), c(2)), c(3)), add(c(1), c(2)))
    parser = Parser(Tokenizer("(1+2)/3 > 1 + 2"))
    assert parser.expression() == ast


# TODO: rewrite this.
# def test_all_ops():
#     ast = _and(gt(div(add(c(1), c(2)), c(4)), add(c(1), c(2))), _or(lt(c(1), c(3)), _or(ge(mod(c(2), c(5)), c(3)), _and(le(mult(c(3), c(4)), div(c(4), c(2))), _or(_not(_is(c(1), c(2))), _is_not(c(4), c(5)))))))
#     parser = Parser(Tokenizer("(1+2)/4 > 1 + 2 and 1 < 3 or 2%5 >= 3 or 3*4 <= 4/2 and not 1 is 2 or 4 is not 5"))
#     assert parser.expression() == ast
