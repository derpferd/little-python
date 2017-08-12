from __future__ import unicode_literals

from littlepython.ast import Block, Assign, If, ControlBlock, Var, BinaryOp, UnaryOp, Const
from littlepython.feature import Features
from littlepython.tokenizer import TokenTypes


class Parser(object):
    @staticmethod
    def get_control_types(features):
        return {TokenTypes.IF, TokenTypes.ELIF, TokenTypes.ELSE}

    def __init__(self, tokenizer, features=Features.ALL):
        self.tokenizer = tokenizer
        self.cur_token = next(tokenizer)
        self.features = features
        self.control_type = self.get_control_types(features)

    def error(self, msg=""):
        raise Exception("Invalid syntax: " + msg)

    def eat(self, token_type):
        if self.cur_token.type == token_type:
            self.cur_token = next(self.tokenizer)
        else:
            self.error("Excepted token type {} got {}".format(token_type, self.cur_token.type))

    def program(self):
        """program : (newline) statement
                   | program statement
        """
        statements = []
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        while self.cur_token.type != TokenTypes.EOF:
            statements += [self.statement()]
        return Block(statements)

    def statement(self):
        """
        statement   : variable ASSIGN expression
                    | control
                    | empty
        """
        if self.cur_token.type == TokenTypes.VAR:
            left = self.variable()
            op = self.cur_token
            self.eat(TokenTypes.ASSIGN)
            right = self.expression()
            return Assign(op, left, right)
        elif self.cur_token.type in self.control_type:
            return self.control()

    def control(self):
        """
        control    : 'if' ctrl_exp block ('elif' ctrl_exp block)* ('else' block)
        """
        self.eat(TokenTypes.IF)
        ctrl = self.expression()
        block = self.block()
        ifs = [If(ctrl, block)]
        else_block = Block()
        while self.cur_token.type == TokenTypes.ELIF:
            self.eat(TokenTypes.ELIF)
            ctrl = self.expression()
            block = self.block()
            ifs.append(If(ctrl, block))
        if self.cur_token.type == TokenTypes.ELSE:
            self.eat(TokenTypes.ELSE)
            else_block = self.block()
        return ControlBlock(ifs, else_block)

    def block(self):
        """
        block      : { (newline) statements } (newline)
        """
        statements = []
        self.eat(TokenTypes.LBRACE)
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        while self.cur_token.type != TokenTypes.RBRACE:
            statements.append(self.statement())
        self.eat(TokenTypes.RBRACE)
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        return Block(statements)

    def variable(self):
        var = Var(self.cur_token)
        self.eat(TokenTypes.VAR)
        return var

    def expression(self):
        """This expression parser is in a different format for simplicity
        expression : expression (newline)

        """

        # TODO: convert these to types instead of strings
        binary_ops = ["+", "-", "*", "/", "%", "or", "and", "is", "is not", ">", "<", "<=", ">="]
        unary_ops = ["not"]
        operand_types = {TokenTypes.VAR: Var, TokenTypes.CONST: Const}
        parens = (TokenTypes.LPAREN, TokenTypes.RPAREN)

        operator_stack = []
        operand_stack = []

        # TODO: convert these to types instead of strings
        def get_op_priority(op):
            # Ref: https://docs.python.org/2/reference/expressions.html
            if op in ('or', 'and'):
                return 1
            if op in ('not',):
                return 2
            if op in ('is', 'is not', '>', '<', '<=', '>='):
                return 3
            if op in ('+', '-'):
                return 4
            if op in ('/', '*', "%"):
                return 5
            return -1

        def build_last_tree(operands, operators):
            op = operators.pop()
            b = None
            if op.value in binary_ops:
                b = operands.pop()
            a = operands.pop()
            if b is not None:
                return BinaryOp(op, a, b)
            else:
                return UnaryOp(op, a)

        # TODO: handle negative numbers
        while self.cur_token.value in binary_ops or self.cur_token.value in unary_ops or self.cur_token.type in operand_types or self.cur_token.type in parens:
            if self.cur_token.type in operand_types:
                operand = operand_types[self.cur_token.type](self.cur_token)
                operand_stack.append(operand)
                self.eat(self.cur_token.type)
            elif self.cur_token.value in binary_ops or self.cur_token.value in unary_ops:
                while operator_stack and get_op_priority(operator_stack[-1].value) > get_op_priority(
                        self.cur_token.value):
                    operand_stack.append(build_last_tree(operand_stack, operator_stack))
                operator_stack.append(self.cur_token)
                self.eat(self.cur_token.type)
            elif self.cur_token.type == TokenTypes.LPAREN:
                operator_stack.append(self.cur_token)
                self.eat(TokenTypes.LPAREN)
            elif self.cur_token.type == TokenTypes.RPAREN:
                op = self.cur_token
                while op.type != TokenTypes.LPAREN:
                    ast = build_last_tree(operand_stack, operator_stack)
                    op = operator_stack[-1]
                    operand_stack.append(ast)
                operator_stack.pop()  # remove the LPAREN we ran into.
                self.eat(TokenTypes.RPAREN)
        while operator_stack:
            operand_stack.append(build_last_tree(operand_stack, operator_stack))
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        return operand_stack[0]
