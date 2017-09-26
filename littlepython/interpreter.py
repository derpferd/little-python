from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from copy import copy

from collections import defaultdict

from littlepython.ast import SetArrayItem, GetArrayItem
from littlepython.parser import Assign, Block, ControlBlock, If, BinaryOp, UnaryOp


def defaultdict_to_list(d):
    valid_keys = [x for x in d.keys() if d[x] != 0]
    length = max(valid_keys)+1
    l = [0]*length
    for k, v in d.items():
        if v != 0:
            l[k] = v
    return l


class AlreadyRunningException(Exception):
    pass


class ExecutionCountExceededException(Exception):
    pass


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
    # TODO: allow multithreaded execution.
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
    unaryOps = {"not": lambda a: not a,
                "+": lambda a: a,
                "-": lambda a: -a}

    def __init__(self, ast):
        self.ast = ast
        self.running = False
        self.count_remaining = -1

    def handle_var(self, node, sym_tbl):
        return sym_tbl[node.value]

    def handle_int(self, node, sym_tbl):
        return node.value

    def handle_assign(self, node, sym_tbl):
        assert isinstance(node, Assign)
        sym_tbl[node.left.value] = self.handle(node.right, sym_tbl)

    def handle_block(self, node, sym_tbl):
        assert isinstance(node, Block)
        for child in node.children:
            self.handle(child, sym_tbl)

    def handle_controlblock(self, node, sym_tbl):
        assert isinstance(node, ControlBlock)
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

    def handle_getarrayitem(self, node, sym_tbl):
        assert isinstance(node, GetArrayItem)
        var = self.handle(node.left, sym_tbl)
        return var[self.handle(node.right, sym_tbl)]

    def handle_setarrayitem(self, node, sym_tbl):
        assert isinstance(node, SetArrayItem)
        var = self.handle(node.left, sym_tbl)
        var[self.handle(node.right, sym_tbl)] = self.handle(node.expr, sym_tbl)

    def handle(self, node, sym_tbl):
        self.count_remaining -= 1
        if self.count_remaining == 0:
            raise ExecutionCountExceededException("Running this program would require more operations than allowed.")
        name = 'handle_' + type(node).__name__.lower()
        handler = getattr(self, name, None)
        if handler is None:
            raise NotImplementedError("No {} found.".format(name))
        return handler(node, sym_tbl)

    def run(self, static_vars=None, max_op_count=-1):
        if self.running:
            raise AlreadyRunningException("This program can only be run on one thread. And this one is already running.")
        self.running = True
        self.count_remaining = max_op_count
        state = {}
        if static_vars is not None:
            for key, var in static_vars.items():
                if isinstance(var, list):
                    new_list = defaultdict(int)
                    for i, v in enumerate(var):
                        new_list[i] = v
                    state[key] = new_list
                else:
                    state[key] = copy(var)
        sym_tbl = GlobalSymbolTable(state)
        self.handle(self.ast, sym_tbl)
        end_state = {}
        for key, var in sym_tbl.dump_cur_state().items():
            if isinstance(var, defaultdict):
                end_state[key] = defaultdict_to_list(var)
            else:
                end_state[key] = var

        self.running = False
        return end_state
