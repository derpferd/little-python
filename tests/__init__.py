from littlepython.ast import Int, Var, BinaryOp, UnaryOp, Assign, ControlBlock, If, Block, GetArrayItem, SetArrayItem, \
    ForLoop, Function, FunctionDef, FunctionSig, Call, Return
from littlepython.tokenizer import Token, TokenTypes


def t(s):
    return Token.from_str(s)


# def iterator_to_generator(iterator):
#     return (i for i in iterator)


ADD = Token(TokenTypes.ADD, "+")
SUB = Token(TokenTypes.SUB, "-")
DIV = Token(TokenTypes.DIV, "/")
NOT = Token(TokenTypes.NOT, "not")
EOF = Token(TokenTypes.EOF, None)


def add(l, r=None):
    if r:
        return BinaryOp(ADD, l, r)
    return UnaryOp(ADD, l)


def sub(l, r=None):
    if r:
        return BinaryOp(SUB, l, r)
    return UnaryOp(SUB, l)


def mult(l, r):
    return BinaryOp(Token(TokenTypes.MULT, "*"), l, r)


def div(l, r):
    return BinaryOp(DIV, l, r)


def mod(l, r):
    return BinaryOp(Token(TokenTypes.MOD, "%"), l, r)


def _is(l, r):
    return BinaryOp(Token(TokenTypes.EQUAL, "is"), l, r)


def _is_not(l, r):
    return BinaryOp(Token(TokenTypes.NOT_EQUAL, "is not"), l, r)


def _not(e):
    return UnaryOp(NOT, e)


def _and(l, r):
    return BinaryOp(Token(TokenTypes.AND, "and"), l, r)


def _or(l, r):
    return BinaryOp(Token(TokenTypes.OR, "or"), l, r)


def lt(l, r):
    return BinaryOp(Token(TokenTypes.LESS, "<"), l, r)


def gt(l, r):
    return BinaryOp(Token(TokenTypes.GREATER, ">"), l, r)


def le(l, r):
    return BinaryOp(Token(TokenTypes.LESS_EQUAL, "<="), l, r)


def ge(l, r):
    return BinaryOp(Token(TokenTypes.GREATER_EQUAL, ">="), l, r)


def asg(l, r):
    return Assign(t("="), l, r)


def blk(stms=None):
    if stms is None:
        stms = []
    return Block(stms)


def _if(expr, block):
    return If(expr, block)


def ctrl(ifs, els):
    return ControlBlock(ifs, els)


def _for(init, ctrl, inc, block):
    return ForLoop(init, ctrl, inc, block)


def func(sig, block):
    return Function(sig, block)


def _def(name, sig, block):
    return FunctionDef(name, Function(sig, block))


def sig(params):
    return FunctionSig(params)


def ret(expr):
    return Return(expr)


def call(func, args):
    return Call(func, args)


def getitem(l, r):
    return GetArrayItem(l, r)


def setitem(l, r, e):
    return SetArrayItem(l, r, e)


def c(v):
    return Int(Token(TokenTypes.INT, v))


def v(n):
    return Var(Token(TokenTypes.VAR, n))

