from __future__ import unicode_literals

from littlepython.feature import Features
from littlepython.tokenizer import TokenTypes


class AST(object):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        possible_attrs = ["token", "left", "right", "children"]
        for attr in possible_attrs:
            if hasattr(self, attr) != hasattr(other, attr):
                return False
            if hasattr(self, attr) and getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        raise NotImplementedError("To be an AST you need to implement this.")


class BinaryOp(AST):
    def __init__(self, op, left, right):
        self.token = self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + str(self.left) + " " + self.token.value + " " + str(self.right) + ")"


class UnaryOp(AST):
    def __init__(self, op, right):
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return self.token.value + "(" + str(self.right) + ")"


class Const(AST):
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


class Block(AST):
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children

    def __str__(self):
        return "{\n" + "".join(map(str, self.children)) + "}"


class Assign(AST):
    def __init__(self, op, left, right):
        assert isinstance(left, Var)
        self.token = self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " " + self.token.value + " " + str(self.right) + "\n"


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


class IfElifElseControl(AST):
    def __init__(self, ifs, else_block):
        # This control must contain at least one if.
        assert len(ifs) > 0
        self.ifs = ifs
        self.else_block = else_block

    def __eq__(self, other):
        if not super(IfElifElseControl, self).__eq__(other):
            return False
        return self.ifs == other.ifs and self.else_block == other.else_block

    def __str__(self):
        s = "if " + str(self.ifs[0].ctrl) + " " + str(self.ifs[0].block)
        for _if in self.ifs[1:]:
            s += " elif " + str(_if.ctrl) + " " + str(_if.block)
        s += " else " + str(self.else_block)
        return s


class Parser(object):
    CONTROL_TYPES = {TokenTypes.IF, TokenTypes.ELIF, TokenTypes.ELSE}

    def __init__(self, tokenizer, features=Features.ALL):
        self.tokenizer = tokenizer
        self.cur_token = next(tokenizer)
        self.features = features

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
        elif self.cur_token.type in self.CONTROL_TYPES:
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
        return IfElifElseControl(ifs, else_block)

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
