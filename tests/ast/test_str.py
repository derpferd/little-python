import pytest

from littlepython.ast import BinaryOp, Int, UnaryOp, Var, Assign, Block, If, ControlBlock, AST
from tests import t


def test_ast_str():
    node = AST()
    with pytest.raises(NotImplementedError):
        str(node)


def test_int_str():
    node = Int(t("1"))
    s = str(node)
    assert s == "1"
    assert s == repr(node)


def test_var_str():
    node = Var(t("a"))
    assert str(node) == "a"


def test_unaryop_str():
    node = UnaryOp(t("not"), Var(t("a")))
    assert str(node) == "not(a)"


def test_binaryop_str():
    node = BinaryOp(t("+"), Int(t("1")), Var(t("a")))
    assert str(node) == "1 + a"


def test_binaryop_complex_str():
    node = BinaryOp(t("+"), BinaryOp(t("+"), Int(t("1")), Var(t("a"))), Int(t("1")))
    assert str(node) == "(1 + a) + 1"


def test_assign_str():
    node = Assign(t("="), Var(t("a")), Int(t("1")))
    assert str(node) == "a = 1"


def test_block_str():
    node = Block([Assign(t("="), Var(t("a")), Int(t("1")))])
    assert str(node) == "{\na = 1\n}"


def test_if_str():
    node = If(BinaryOp(t("<"), Int(t("1")), Var(t("a"))), Block([Assign(t("="), Var(t("a")), Int(t("1")))]))
    assert str(node) == "if 1 < a {\na = 1\n}"


def test_control_block_str():
    node = ControlBlock([If(BinaryOp(t("<"), Int(t("1")), Var(t("a"))), Block([Assign(t("="), Var(t("a")), Int(t("1")))])),
                         If(BinaryOp(t("<"), Int(t("1")), Var(t("a"))), Block([Assign(t("="), Var(t("a")), Int(t("1")))]))],
                        Block([Assign(t("="), Var(t("a")), Int(t("1")))]))
    assert str(node) == "if 1 < a {\na = 1\n} elif 1 < a {\na = 1\n} else {\na = 1\n}"
