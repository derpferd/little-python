from __future__ import unicode_literals

from enum import Enum

counter = 0


def auto():
    global counter
    counter += 1
    return counter


def alfa_(w):
    """This function returns True if the given string 'w' contains only alphabetic or underscore characters

    Note: It is implemented in a hacky way to increase speed
    """
    return (w + "a").replace('_', '').isalpha()


def alnum_(w):
    """This function returns True if the given string 'w' contains only alphabetic, numeric or underscore characters

    Note: It is implemented in a hacky way to increase speed
    """
    return (w + "a").replace('_', '').isalnum()


class TokenTypes(Enum):
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    MOD = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    CONST = auto()
    VAR = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    ASSIGN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    NEW_LINE = auto()
    EOF = auto()

    @staticmethod
    def from_str(s):
        return {'if': TokenTypes.IF,
                'elif': TokenTypes.ELIF,
                'else': TokenTypes.ELSE,
                'and': TokenTypes.AND,
                'or': TokenTypes.OR,
                'not': TokenTypes.NOT,
                'is': TokenTypes.EQUAL,
                'is not': TokenTypes.NOT_EQUAL,
                '+': TokenTypes.ADD,
                '-': TokenTypes.SUB,
                '*': TokenTypes.MULT,
                '/': TokenTypes.DIV,
                '%': TokenTypes.MOD,
                '<': TokenTypes.LESS,
                '>': TokenTypes.GREATER,
                '{': TokenTypes.LBRACE,
                '}': TokenTypes.RBRACE,
                '(': TokenTypes.LPAREN,
                ')': TokenTypes.RPAREN,
                '=': TokenTypes.ASSIGN,
                '<=': TokenTypes.LESS_EQUAL,
                '>=': TokenTypes.GREATER_EQUAL,
                '\n': TokenTypes.NEW_LINE,
                None: TokenTypes.EOF}.get(s, None)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token<type:{}, value:{}>".format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def from_str(s):
        token_type = TokenTypes.from_str(s)
        if token_type:
            return Token(token_type, s)
        if isinstance(s, str) and s.isdigit() or isinstance(s, int):
            return Token(TokenTypes.CONST, int(s))
        if isinstance(s, str) and len(s) and alfa_(s[0]) and alnum_(s[1:]):
            return Token(TokenTypes.VAR, s)
        raise ValueError("Invalid input")


KEYWORDS = {
    'if': Token(TokenTypes.IF, 'if'),
    'elif': Token(TokenTypes.ELIF, 'elif'),
    'else': Token(TokenTypes.ELSE, 'else'),
    'not': Token(TokenTypes.NOT, 'not'),
    'is': Token(TokenTypes.EQUAL, 'is'),
    'and': Token(TokenTypes.AND, 'and'),
    'or': Token(TokenTypes.OR, 'or'),
    # 'is not': Token(TokenTypes.NOT_EQUAL, 'is not'),
}

NON_ALPHA_1 = {  # non-alphanumeric single char tokens
    '+': Token(TokenTypes.ADD, '+'),
    '-': Token(TokenTypes.SUB, '-'),
    '*': Token(TokenTypes.MULT, '*'),
    '/': Token(TokenTypes.DIV, '/'),
    '%': Token(TokenTypes.MOD, '%'),
    '<': Token(TokenTypes.LESS, '<'),
    '>': Token(TokenTypes.GREATER, '>'),
    '{': Token(TokenTypes.LBRACE, '{'),
    '}': Token(TokenTypes.RBRACE, '}'),
    '(': Token(TokenTypes.LPAREN, '('),
    ')': Token(TokenTypes.RPAREN, ')'),
    '=': Token(TokenTypes.ASSIGN, '='),
}

NON_ALPHA_2 = {  # non-alphanumeric double char tokens
    '<=': Token(TokenTypes.LESS_EQUAL, '<='),
    '>=': Token(TokenTypes.GREATER_EQUAL, '>='),
}


class Tokenizer(object):
    def __init__(self, text):
        self.text = text
        self.cur_pos = -1
        self.cur_char = ""
        self.last_was_new_line = False
        self.last_was_eof = False
        self.advance()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        token = self.get_next_token()
        if self.last_was_eof:
            raise StopIteration()
        if token.type == TokenTypes.EOF:
            self.last_was_eof = True
        return token

    def advance(self):
        self.cur_pos += 1
        if self.cur_pos < len(self.text):
            self.cur_char = self.text[self.cur_pos]
        else:
            self.cur_char = None

    def peek(self, dist=1):
        pos = self.cur_pos + dist
        if pos < len(self.text):
            return self.text[pos]
        else:
            return None

    def skip_comment(self):
        while self.cur_char is not None and self.cur_char != '\n':
            self.advance()

    def skip_whitespace(self):
        while self.cur_char is not None and self.cur_char.isspace() and self.cur_char != "\n":
            self.advance()

    def number(self):
        result = ""
        while self.cur_char is not None and self.cur_char.isdigit():
            result += self.cur_char
            self.advance()

        return Token(TokenTypes.CONST, int(result))

    def id(self):
        result = ""
        while self.cur_char is not None and alnum_(self.cur_char):
            result += self.cur_char
            self.advance()

        return KEYWORDS.get(result, Token(TokenTypes.VAR, result))

    def test_for_is_not(self):
        if self.cur_pos + len("is not") > len(self.text):
            return False
        result = "".join([self.peek(i) for i in range(len("is not"))])
        if result == "is not":
            return True

    def get_next_token(self):
        while self.cur_char is not None:
            if self.cur_char.isspace() and self.cur_char != "\n":
                self.skip_whitespace()
                continue

            if self.cur_char == "#":
                self.advance()
                self.skip_comment()
                continue

            if self.cur_char == "\n":
                if self.last_was_new_line:
                    self.advance()
                    continue
                self.last_was_new_line = True
                self.advance()
                return Token(TokenTypes.NEW_LINE, "\n")
            self.last_was_new_line = False

            if self.test_for_is_not():
                for i in range(len("is not")):
                    self.advance()
                return Token(TokenTypes.NOT_EQUAL, "is not")

            if alfa_(self.cur_char):
                return self.id()

            if self.cur_char.isdigit():
                return self.number()

            if self.peek() is not None and self.cur_char + self.peek() in NON_ALPHA_2:
                result = self.cur_char + self.peek()
                self.advance()
                self.advance()
                return NON_ALPHA_2[result]

            if self.cur_char in NON_ALPHA_1:
                result = self.cur_char
                self.advance()
                return NON_ALPHA_1[result]

            raise Exception("Ran into invalid char '{}' at pos {}".format(self.cur_char, self.cur_pos))

        return Token(TokenTypes.EOF, None)


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
        assert isinstance(op, Token)
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

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.cur_token = tokenizer.next()

    def error(self, msg=""):
        raise Exception("Invalid syntax: " + msg)

    def eat(self, token_type):
        if self.cur_token.type == token_type:
            self.cur_token = self.tokenizer.next()
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
