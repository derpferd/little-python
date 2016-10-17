# Copyright (C) Jonathan Beaulieu (beau0307@d.umn.edu)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
import sys
import random
from copy import deepcopy as copy


class Var(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<LP Var: '" + self.name + "'>"


class LPProg(object):
    binaryOps = {"+": lambda a, b: a + b,
                 "-": lambda a, b: a - b,
                 "*": lambda a, b: a * b,
                 # This might become a problem in future versions this works for integers only
                 "/": lambda a, b: a // b,
                 "%": lambda a, b: a % b,
                 "or": lambda a, b: a or b,
                 "and": lambda a, b: a and b,
                 "is": lambda a, b: a is b,
                 "is not": lambda a, b: a is not b}
    unaryOps = {"not": lambda a: not a,
                 "int": lambda a: int(a)}

    def __init__(self, program_ASTs):
        self.program_ASTs = program_ASTs

    @staticmethod
    def resolve_var(var, state):
        if str(var) not in state:
            if str(var) == "rand":
                return random.randint(-2147483647, 2147483647)
            else:
                return 0
        else:
            return state[str(var)]

    @staticmethod
    def eval_expression(expression, state):
        if isinstance(expression, Var):
            return LPProg.resolve_var(expression, state)
        operands = {"a": expression.get("a"), "b": expression.get("b")}
        # print ("B:",expression)
        for operand in ["a", "b"]:
            if operand in expression and isinstance(expression[operand], Var):
                operands[operand] = LPProg.resolve_var(expression[operand], state)
            elif operand in expression and isinstance(expression[operand], dict):
                operands[operand] = LPProg.eval_expression(expression[operand], state)
        # print ("A:",expression)
        if expression["op"] in LPProg.unaryOps:
            return LPProg.unaryOps[expression["op"]](operands["a"])
        elif expression["op"] in LPProg.binaryOps:
            return LPProg.binaryOps[expression["op"]](operands["a"], operands["b"])
        raise Exception("Unknown op")

    @staticmethod
    def eval_statement(statement, state):
        # print ("ST:", statement)
        if statement["op"] == "if":
            if LPProg.eval_expression(statement["ctrl"], state):
                for stm in statement["if"]:
                    LPProg.eval_statement(stm, state)
            elif "else" in statement:
                for stm in statement["else"]:
                    LPProg.eval_statement(stm, state)
        elif statement["op"] == "=":
            state[statement["var"]] = LPProg.eval_expression(statement["exp"], state)


    # static_vars are varibles that the program will be able to access and change
    # the return value is the varibles at the end of the program
    # both take the form of a dictionary with the variable name as the key and the value as the value
    def run(self, static_vars={}):
        state = copy(static_vars)
        for ast in self.program_ASTs:
            self.eval_statement(ast, state)
        return state


def peek(iterable):
    if len(iterable) == 0:
        return None
    else:
        first = iterable.pop(0)
        return first, [first] + iterable


def safe_get(iterable):
    if len(iterable) == 0:
        return None
    else:
        first = iterable.pop()
        return first


class TokenStreamer(object):
    def __init__(self, lines):
        self.lines = lines
        self.cur_line = 0

    @staticmethod
    def tokenize(line):
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/(){}=%#]|[A-Za-z_][A-Za-z0-9_]*|\d+', line))
        return list(token_iter)

    def has_nxt_line(self):
        return self.cur_line < len(self.lines)

    def nxt_line(self):
        line = self.lines[self.cur_line]
        self.cur_line += 1
        return line

    def peek_nxt_tokens(self):
        if not self.has_nxt_line():
            return []
        tks = self.nxt_tokens()
        self.cur_line -= 1
        return tks

    def nxt_tokens(self):
        return TokenStreamer.tokenize(self.nxt_line())


class Compiler(object):
    NONE = 0
    IF = 1

    binaryOps = ["+", "-", "*", "/", "%", "or", "and", "is", "is not"]
    unaryOps = ["not"]

    def __init__(self):
        self.controls = ["if"]
        self.var_ptrn = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    @staticmethod
    def build_last_tree(operands, operators):
        op = operators.pop()
        if op in Compiler.binaryOps:
            b = operands.pop()
        a = operands.pop()
        tree = {"op": op, "a": a}
        if op in Compiler.binaryOps:
            tree["b"] = b
        return tree

    @staticmethod
    def get_op_priority(op):
        if op in ('(', ')'):
            return 0
        if op in ('and', 'or'):
            return 1
        if op in ('not'):
            return 2
        if op in ('is', 'is not'):
            return 3
        if op in ('+', '-'):
            return 4
        if op in ('/', '*', "%"):
            return 5

    def parse_exp(self, tokens):
        token_pos = 0
        operators_stack = []
        operands_stack = []
        while token_pos < len(tokens):
            token = tokens[token_pos]
            # Handle "is not" op
            if token == "is" and token_pos + 1 < len(tokens) and tokens[token_pos + 1] == "not":
                token = "is not"
                token_pos += 1
            if token in self.binaryOps:
                while operators_stack and self.get_op_priority(operators_stack[-1]) >= self.get_op_priority(token):
                    operands_stack.append(self.build_last_tree(operands_stack, operators_stack))
                operators_stack.append(token)
            elif token in self.unaryOps:
                while operators_stack and self.get_op_priority(operators_stack[-1]) >= self.get_op_priority(token):
                    operands_stack.append(self.build_last_tree(operands_stack, operators_stack))
                operators_stack.append(token)
            elif token == '(':
                operators_stack.append(token)
            elif token == ')':
                while token != '(':
                    tree = self.build_last_tree(operands_stack, operators_stack)
                    token = operators_stack[-1]
                    operands_stack.append(tree)
                operators_stack.pop()
            elif token.isdigit():
                operands_stack.append({"op": "int", "a": int(token)})
            elif token and token[0] == "#":
                token_pos = len(tokens)
            else:
                # At this point it should only be a variable.
                # TODO: check if the variable is valid or not.
                operands_stack.append(Var(token))
            token_pos += 1
        while operators_stack:
            operands_stack.append(self.build_last_tree(operands_stack, operators_stack))
        return operands_stack[0]

    # This pass is the simply parse the program into an AST
    def pass1(self, lines):
        # for now assume:
        #  - program has correct syntax
        #  - program has only single nested controls
        if not lines:
            return []
        tk_stream = TokenStreamer(lines)
        program = []
        levels = []
        level_stms = []
        level_ctrls = []
        state = self.NONE
        line = None
        while tk_stream.has_nxt_line():
            tokens = list(tk_stream.nxt_tokens())

            if not len(tokens) or "#" == tokens[0][0]:
                continue

            if tokens[0] == '}':
                assert len(levels) >= 1
                ctrl = level_ctrls.pop()
                stms = level_stms.pop()
                level = levels.pop()

                level[ctrl] = stms

                # if "op" in levels[-1][-1] and levels[-1][-1]["op"] in self.controls:
                #     levels[-1][-1][ctrl] = stms
                # else:
                #     levels[-1] += stms

                if ctrl == "if" and ("else" in tokens or "else" in tk_stream.peek_nxt_tokens()):
                    # we need to continue
                    level_ctrls.append("else")
                    levels.append(level)
                    level_stms.append([])
                elif len(levels) == 0:
                    program += [level]
                    state = self.NONE
                else:
                    level_stms[-1].append(level)
            elif tokens[0] in self.controls: # or first_token == "else":
                # parse for control
                statement = {}
                statement["op"] = tokens[0]
                statement["ctrl"] = self.parse_exp(tokens[1:-1])  # -1 to remove to '{' at the end

                level_ctrls.append(statement["op"])
                levels.append(statement)
                level_stms.append([])
                state = self.IF
            else:
                statement = {}
                assert len(tokens) >= 3
                # parse for variable setting
                assert self.var_ptrn.match(tokens[0]) is not None
                statement["var"] = tokens[0]
                assert tokens[1] == "="
                statement["op"] = "="
                statement["exp"] = self.parse_exp(tokens[2:])
                if state == self.IF:
                    level_stms[-1] += [statement]
                else:
                    program += [statement]

        return program

    # This is the optimization pass
    # It takes an array of statements and returns a LPProg
    def pass2(self, program):
        # TODO: implement
        return LPProg(program)

    # compiles lp program passed as an array of lines of text
    # returns a LPProg
    def compile(self, lines):
        return self.pass2(self.pass1(lines))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("How to run:")
        print("python lp.py file_to_be_run.lp")
    else:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print("Could not find that file sorry :(")
        lines = open(filename, 'r').readlines()
        c = Compiler()
        prog = c.compile(lines)
        state = prog.run()
        print("Ending variable Values:")
        print("Name".center(14, "-")+"|"+"Value".center(11, "-"))
        for var in sorted(state):
            print(var.center(14)+"|"+str(state[var]).center(11))
