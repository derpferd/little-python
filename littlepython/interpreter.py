from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from copy import copy

from littlepython.parser import Assign, Block, IfElifElseControl, If, BinaryOp, UnaryOp


class SymbolTable(object):
    def resolve(self, name):
        raise NotImplementedError("Must be implemented")

    def set(self, name, value):
        raise NotImplementedError("Must be implemented")

    def __getitem__(self, item):
        return self.resolve(item)

    def __setitem__(self, key, value):
        return self.set(key, value)


class GlobalSymbolTable(SymbolTable):
    def __init__(self, global_state):
        assert isinstance(global_state, dict)
        self.global_state = global_state

    def resolve(self, name):
        return self.global_state.get(name, 0)

    def set(self, name, value):
        self.global_state[name] = value

    def dump_cur_state(self):
        return copy(self.global_state)


class LPProg(object):
    binaryOps = {"+": lambda a, b: a + b,
                 "-": lambda a, b: a - b,
                 "*": lambda a, b: a * b,
                 # This might become a problem in future versions this works for integers only
                 "/": lambda a, b: a // b,
                 "%": lambda a, b: a % b,
                 "or": lambda a, b: a or b,
                 "and": lambda a, b: a and b,
                 "is": lambda a, b: a == b,
                 "is not": lambda a, b: a != b,
                 "<": lambda a, b: a < b,
                 ">": lambda a, b: a > b,
                 "<=": lambda a, b: a <= b,
                 ">=": lambda a, b: a >= b}
    unaryOps = {"not": lambda a: not a}

    def __init__(self, ast):
        self.ast = ast

    def handle_var(self, node, sym_tbl):
        return sym_tbl[node.value]

    def handle_const(self, node, sym_tbl):
        return node.value

    def handle_assign(self, node, sym_tbl):
        assert isinstance(node, Assign)
        sym_tbl[node.left.value] = self.handle(node.right, sym_tbl)

    def handle_block(self, node, sym_tbl):
        assert isinstance(node, Block)
        for child in node.children:
            self.handle(child, sym_tbl)

    def handle_ifelifelsecontrol(self, node, sym_tbl):
        assert isinstance(node, IfElifElseControl)
        for _if in node.ifs:
            assert isinstance(_if, If)
            if self.handle(_if.ctrl, sym_tbl):
                self.handle(_if.block, sym_tbl)
                return
        self.handle(node.else_block, sym_tbl)

    def handle_binaryop(self, node, sym_tbl):
        assert isinstance(node, BinaryOp)
        return self.binaryOps[node.op.value](self.handle(node.left, sym_tbl), self.handle(node.right, sym_tbl))

    def handle_unaryop(self, node, sym_tbl):
        assert isinstance(node, UnaryOp)
        return self.unaryOps[node.op.value](self.handle(node.right, sym_tbl))

    def handle(self, node, sym_tbl):
        name = 'handle_' + type(node).__name__.lower()
        handler = getattr(self, name, None)
        if handler is None:
            raise NotImplementedError("No {} found.".format(name))
        return handler(node, sym_tbl)

    def run(self, static_vars=None):
        state = {}
        if static_vars is not None:
            state = copy(static_vars)
        sym_tbl = GlobalSymbolTable(state)
        self.handle(self.ast, sym_tbl)
        return sym_tbl.dump_cur_state()
