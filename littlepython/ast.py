from __future__ import unicode_literals


class AST(object):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        standard_attrs = ["token", "left", "right", "children"]
        for attr in standard_attrs:
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


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)


class Int(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)


class Var(AST):
    # TODO: implement type
    def __init__(self, token, type=None):
        self.token = token
        self.value = token.value
        self.type = type

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
        return "(" + str(self.left) + " " + self.token.value + " " + str(self.right) + ")"


class Assign(AST):
    def __init__(self, op, left, right):
        assert isinstance(left, Var)
        self.token = self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " " + self.token.value + " " + str(self.right) + "\n"


class Block(AST):
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children

    def __str__(self):
        return "{\n" + "".join(map(str, self.children)) + "}"


class If(AST):
    def __init__(self, ctrl, block):
        self.ctrl = ctrl
        self.block = block

    def __eq__(self, other):
        if not super(If, self).__eq__(other):
            return False
        return self.ctrl == other.ctrl and self.block == other.block

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

    def __eq__(self, other):
        if not super(ControlBlock, self).__eq__(other):
            return False
        return self.ifs == other.ifs and self.else_block == other.else_block

    def __str__(self):
        s = "if " + str(self.ifs[0].ctrl) + " " + str(self.ifs[0].block)
        for _if in self.ifs[1:]:
            s += " elif " + str(_if.ctrl) + " " + str(_if.block)
        s += " else " + str(self.else_block)
        return s
