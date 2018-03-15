from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
from copy import copy

from collections import defaultdict

from multiprocessing import Lock

from littlepython.ast import SetArrayItem, GetArrayItem, ForLoop, FunctionDef, Call, Function
from littlepython.error import ExecutionCountExceededException, DivisionByZeroException
from littlepython.parser import Assign, Block, ControlBlock, If, BinaryOp, UnaryOp
from littlepython.feature import Features


class Array(defaultdict):
    def __init__(self, *args):
        super(Array, self).__init__(int)
        if len(args) == 1:
            try:
                for i, arg in enumerate(args[0]):
                    self[i] = arg
            except TypeError:
                for i, arg in enumerate(args):
                    self[i] = arg


def convert_python_type_to_lp_type(var):
    if isinstance(var, int):
        return var
    if isinstance(var, list) or isinstance(var, tuple):
        new_list = defaultdict(int)
        for i, v in enumerate(var):
            new_list[i] = convert_python_type_to_lp_type(v)
        return new_list
    raise TypeError("Little Python doesn't support this type as input.")


def convert_lp_type_to_python_type(var):
    if isinstance(var, int):
        return var
    if isinstance(var, defaultdict):
        valid_keys = [x for x in var.keys() if var[x] != 0]
        if not valid_keys:
            return []
        length = max(valid_keys) + 1
        new_list = [0] * length
        for k, v in var.items():
            if v != 0:
                new_list[k] = convert_lp_type_to_python_type(v)
        return new_list
    return copy(var)


class StopFunc(Exception):
    pass


class SymbolTable(object):
    def resolve(self, name):
        raise NotImplementedError("Must be implemented")

    def set(self, name, value):
        raise NotImplementedError("Must be implemented")

    def enter_scope(self, name="NA"):
        raise NotImplementedError("Must be implemented")

    def exit_scope(self):
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

    def enter_scope(self, name="NA"):
        pass

    def exit_scope(self):
        pass

    def dump_cur_state(self):
        return copy(self.global_state)


class ScopedSymbolTable(SymbolTable):
    # TODO: write tests for this.
    def __init__(self, global_state):
        assert isinstance(global_state, dict)
        self.global_state = global_state
        self.scopes = []
        self.scope_names = []

    def resolve(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return self.global_state.get(name, 0)

    def set(self, name, value):
        if name in self.global_state:
            self.global_state[name] = value
            return
        if self.scopes:
            self.scopes[-1][name] = value
        else:
            self.global_state[name] = value

    def enter_scope(self, name="NA"):
        self.scopes += [{}]
        self.scope_names += [name]

    def exit_scope(self):
        self.scopes.pop(-1)
        self.scope_names.pop(-1)

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

    def __init__(self, ast, features):
        self.ast = ast
        self.features = features
        self.running_lock = Lock()
        self.count_remaining = -1
        self.random = random

    def handle_noop(self, *args, **kwargs):
        pass

    def handle_var(self, node, sym_tbl):
        if node.value == "rand" and Features.RANDOM_VAR in self.features:
            return self.random.randint(-2147483647, 2147483647)
        return sym_tbl[node.value]

    def handle_int(self, node, sym_tbl):
        return node.value

    def handle_array(self, node, sym_tbl):
        # array =
        # for i, val in enumerate(node.vals):
        #     array[i] = self.handle(node, sym_tbl)
        return Array(self.handle(val, sym_tbl) for val in node.vals)

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

    def handle_forloop(self, node, sym_tbl):
        assert isinstance(node, ForLoop)
        self.handle(node.init, sym_tbl)
        while self.handle(node.ctrl, sym_tbl):
            self.handle(node.block, sym_tbl)
            self.handle(node.inc, sym_tbl)

    def handle_binaryop(self, node, sym_tbl):
        assert isinstance(node, BinaryOp)
        try:
            return self.binaryOps[node.op.value](self.handle(node.left, sym_tbl), self.handle(node.right, sym_tbl))
        except ZeroDivisionError:
            raise DivisionByZeroException()

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

    def handle_functiondef(self, node, sym_tbl):
        assert isinstance(node, FunctionDef)
        sym_tbl[node.name.value] = node.function

    def handle_call(self, node, sym_tbl):
        assert isinstance(node, Call)
        # Look up variable that contains the function.
        func = sym_tbl[node.func.value]
        # make sure that the arglist length matches the func signature
        assert len(func.sig.params) == len(node.arglist)
        args_copy = []
        for var in node.arglist:
            args_copy += [self.handle(var, sym_tbl)]

        sym_tbl.enter_scope()

        for arg, param in zip(args_copy, func.sig.params):
            sym_tbl[param.value] = arg

        # Now run the function
        try:
            self.handle(func.block, sym_tbl)
        except StopFunc:
            pass  # This means we hit a return statement
        rtn = sym_tbl["return"]
        sym_tbl.exit_scope()
        return rtn

    def handle_return(self, node, sym_tbl):
        sym_tbl["return"] = self.handle(node.expr, sym_tbl)
        raise StopFunc()

    def handle(self, node, sym_tbl):
        self.count_remaining -= 1
        if self.count_remaining == 0:
            raise ExecutionCountExceededException("Running this program would require more operations than allowed.")
        name = 'handle_' + type(node).__name__.lower()
        handler = getattr(self, name, None)
        if handler is None:
            raise NotImplementedError("No {} found.".format(name))
        return handler(node, sym_tbl)

    def run(self, static_vars=None, max_op_count=-1, random=None):
        with self.running_lock:
            self.count_remaining = max_op_count
            if random is not None:
                self.random = random
            state = {}
            if static_vars is not None:
                for key, var in static_vars.items():
                    state[key] = convert_python_type_to_lp_type(var)
            sym_tbl = ScopedSymbolTable(state)
            self.handle(self.ast, sym_tbl)
            end_state = {}
            for key, var in sym_tbl.dump_cur_state().items():
                if isinstance(var, Function):
                    continue
                else:
                    end_state[key] = convert_lp_type_to_python_type(var)

            return end_state
