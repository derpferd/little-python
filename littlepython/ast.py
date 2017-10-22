from __future__ import unicode_literals

from littlepython.tokenizer import Token, TokenTypes


def _var(n):
    return Var(Token(TokenTypes.VAR, n))


class AST(object):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        possible_attrs = ["token", "left", "right", "children", "sig", "block", "ifs", "else_block", "ctrl", "params"]
        for attr in possible_attrs:
            if hasattr(self, attr) != hasattr(other, attr):
                return False
            if hasattr(self, attr) and getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        raise NotImplementedError("To be an AST you need to implement this.")

    def __repr__(self):
        return self.__str__()


class Int(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)


class UnaryOp(AST):
    def __init__(self, op, right):
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return self.token.value + "(" + str(self.right) + ")"


class BinaryOp(AST):
    def __init__(self, op, left, right):
        self.token = self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        # TODO: create better to string.
        s = ""
        if isinstance(self.left, BinaryOp):
            s += "(" + str(self.left) + ")"
        else:
            s += str(self.left)
        s += " " + self.token.value + " "
        if isinstance(self.right, BinaryOp):
            s += "(" + str(self.right) + ")"
        else:
            s += str(self.right)
        # s += ")"
        return s


class FunctionSig(AST):
    # TODO: add return value to this
    def __init__(self, params):
        # Params should be a list of Vars.
        self.params = params

    def __str__(self):
        return "("+", ".join(map(str, self.params))+")"


class Function(AST):
    def __init__(self, sig, block):
        assert isinstance(sig, FunctionSig)
        self.sig = sig
        self.block = block

    def __str__(self):
        return " ".join(map(str, ("func", self.sig, self.block)))


class Assign(AST):
    def __init__(self, op, left, right):
        assert isinstance(left, Var)
        self.token = self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " " + self.token.value + " " + str(self.right)


class Block(AST):
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children

    def __str__(self):
        return "{\n" + "\n".join(map(str, self.children)) + "\n}"


class If(AST):
    def __init__(self, ctrl, block):
        self.ctrl = ctrl
        self.block = block

    def __str__(self):
        return "if " + str(self.ctrl) + " " + str(self.block)


class ControlBlock(AST):
    def __init__(self, ifs, else_block=None):
        # This control must contain at least one if.
        assert len(ifs) > 0
        if else_block is None:
            else_block = Block()
        self.ifs = ifs
        self.else_block = else_block

    def __str__(self):
        s = "if " + str(self.ifs[0].ctrl) + " " + str(self.ifs[0].block)
        for _if in self.ifs[1:]:
            s += " elif " + str(_if.ctrl) + " " + str(_if.block)
        s += " else " + str(self.else_block)
        return s


# Built-in functions
class GetArrayItem(Function):
    def __init__(self, left, right):
        sig = FunctionSig((_var("index"),))
        super(GetArrayItem, self).__init__(sig, Block())
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + "[" + str(self.right) + "]"


class SetArrayItem(Function):
    def __init__(self, left, right, expr):
        sig = FunctionSig((_var("index"), _var("value")))
        super(SetArrayItem, self).__init__(sig, Block())
        self.left = left
        self.right = right
        self.expr = expr

    def __str__(self):
        return str(self.left) + "[" + str(self.right) + "] = " + str(self.expr)
