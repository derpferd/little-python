from __future__ import unicode_literals

from littlepython.error import InvalidSyntaxException
from littlepython.ast import Block, Assign, If, ControlBlock, Var, BinaryOp, UnaryOp, Int, GetArrayItem, SetArrayItem, \
    ForLoop, FunctionSig, Function, FunctionDef, Call, Return, NoOp, Array
from littlepython.feature import Features
from littlepython.tokenizer import TokenTypes


class Parser(object):
    def __init__(self, tokenizer, features=Features.ALL):
        self.tokenizer = tokenizer
        self.cur_token = next(tokenizer)
        self.features = features

    def error(self, msg=""):
        raise InvalidSyntaxException("Invalid syntax: " + msg)

    def eat(self, token_type=None):
        if token_type:
            if self.cur_token.type == token_type:
                self.cur_token = next(self.tokenizer)
            else:
                self.error("Excepted token type {} got {}".format(token_type, self.cur_token.type))
        else:
            self.cur_token = next(self.tokenizer)

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
        statement   : assign_statement
                    | expression
                    | control
                    | empty
        Feature For Loop adds:
                    | loop
        Feature Func adds:
                    | func
                    | return statement
        """
        if self.cur_token.type == TokenTypes.VAR:
            self.tokenizer.start_saving(self.cur_token)
            self.variable()
            peek_var = self.cur_token
            self.tokenizer.replay()
            self.eat()
            if peek_var.type == TokenTypes.ASSIGN:
                return self.assign_statement()
            else:
                return self.expression()
        elif self.cur_token.type in TokenTypes.control(self.features):
            return self.control()
        elif self.cur_token.type in TokenTypes.loop(self.features):
            return self.loop()
        elif self.cur_token.type in TokenTypes.func(self.features):
            if self.cur_token.type == TokenTypes.FUNC:
                return self.func()
            elif self.cur_token.type == TokenTypes.RETURN:
                return self.return_statement()
        self.error("Invalid token or unfinished statement")

    def assign_statement(self):
        """
        assign smt  : variable ASSIGN expression(;)
        Feature Type Array adds:
                    | variable SETITEM expression(;)
        """
        left = self.variable()
        op = self.cur_token
        self.eat(TokenTypes.ASSIGN)
        right = self.expression()
        smt = None
        if Features.TYPE_ARRAY in self.features and isinstance(left, GetArrayItem):
            # Remake this as a setitem.
            smt = SetArrayItem(left.left, left.right, right)
        else:
            smt = Assign(op, left, right)
        if self.cur_token.type == TokenTypes.SEMI_COLON:
            self.eat(TokenTypes.SEMI_COLON)
        return smt

    def return_statement(self):
        """
        return smt  : expression
        """
        self.eat(TokenTypes.RETURN)
        return Return(self.expression())

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

    def loop(self):
        """
        loop       : 'for' init; ctrl; inc block
        """
        self.eat(TokenTypes.FOR_LOOP)
        init = NoOp()
        if self.cur_token.type != TokenTypes.SEMI_COLON:
            init = self.assign_statement()
        else:
            self.eat(TokenTypes.SEMI_COLON)

        ctrl = NoOp()
        if self.cur_token.type != TokenTypes.SEMI_COLON:
            ctrl = self.expression()
        self.eat(TokenTypes.SEMI_COLON)

        inc = NoOp()
        if self.cur_token.type != TokenTypes.LBRACE:
            inc = self.assign_statement()

        block = self.block()
        return ForLoop(init, ctrl, inc, block)

    def func(self):
        """
        func       : func name(paramlist) block
        """
        self.eat(TokenTypes.FUNC)
        name = Var(self.cur_token)
        self.eat(TokenTypes.VAR)
        self.eat(TokenTypes.LPAREN)
        sig = self.param_list()
        self.eat(TokenTypes.RPAREN)
        block = self.block()
        return FunctionDef(name, Function(sig, block))

    def param_list(self):
        """
        paramlist  : var, paramlist
        paramlist  : var
        paramlist  :
        """
        params = []
        while self.cur_token.type == TokenTypes.VAR:
            params.append(Var(self.cur_token))
            self.eat(TokenTypes.VAR)
            if self.cur_token.type == TokenTypes.COMMA:
                self.eat(TokenTypes.COMMA)

        return FunctionSig(params)

    def arg_list(self, ending_char=TokenTypes.RPAREN):
        """
        arglist    : expression, arglist
        arglist    : expression
        arglist    :
        """
        args = []
        while not self.cur_token.type == ending_char:
            args.append(self.expression())
            if self.cur_token.type == TokenTypes.COMMA:
                self.eat(TokenTypes.COMMA)

        return args

    def array_const(self):
        """
        Feature Type Array adds:
        array      : [ arglist ]
        """
        self.eat(TokenTypes.LBRACKET)
        node = Array(self.arg_list(TokenTypes.RBRACKET))
        self.eat(TokenTypes.RBRACKET)
        return node

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
        """
        variable    : variable
        Feature Type Array adds:
        variable    : variable[expression]
        Feature Type Func adds:
        variable    : variable(arg_list)
        """
        var = Var(self.cur_token)
        self.eat(TokenTypes.VAR)
        if Features.TYPE_ARRAY in self.features:
            while self.cur_token.type == TokenTypes.LBRACKET:
                self.eat(TokenTypes.LBRACKET)
                # Start passed the logical ops.
                expr = self.operator_expression(level=2)
                self.eat(TokenTypes.RBRACKET)
                var = GetArrayItem(left=var, right=expr)
        if Features.FUNC in self.features:
            if self.cur_token.type == TokenTypes.LPAREN:
                self.eat(TokenTypes.LPAREN)
                args = self.arg_list()
                self.eat(TokenTypes.RPAREN)
                var = Call(var, args)
        return var

    def expression(self):
        node = self.operator_expression()
        if self.cur_token.type == TokenTypes.NEW_LINE:
            self.eat(TokenTypes.NEW_LINE)
        return node

    def operator_expression(self, level=0):
        levels = ({TokenTypes.OR, TokenTypes.AND},
                  {TokenTypes.NOT},
                  {TokenTypes.EQUAL, TokenTypes.NOT_EQUAL, TokenTypes.GREATER, TokenTypes.GREATER_EQUAL, TokenTypes.LESS, TokenTypes.LESS_EQUAL},
                  {TokenTypes.ADD, TokenTypes.SUB},
                  {TokenTypes.DIV, TokenTypes.MULT, TokenTypes.MOD})

        # If out of level then grab factor instead.
        if level >= len(levels):
            return self.factor()

        if next(iter(levels[level])) in TokenTypes.BINARY_OPS:
            node = self.operator_expression(level+1)
        else:
            node = None

        while self.cur_token.type in levels[level]:
            token = self.cur_token
            self.eat(token.type)

            if token.type in TokenTypes.BINARY_OPS:
                node = BinaryOp(op=token, left=node, right=self.operator_expression(level+1))
            if token.type in TokenTypes.UNARY_OPS:
                node = UnaryOp(op=token, right=self.operator_expression(level+1))

        if node is None:
            node = self.operator_expression(level+1)

        return node

    def factor(self):
        token = self.cur_token
        if token.type == TokenTypes.ADD:
            self.eat(TokenTypes.ADD)
            return UnaryOp(token, self.factor())
        elif token.type == TokenTypes.SUB:
            self.eat(TokenTypes.SUB)
            return UnaryOp(token, self.factor())
        elif token.type == TokenTypes.INT:
            self.eat(TokenTypes.INT)
            return Int(token)
        elif token.type == TokenTypes.LBRACKET:
            return self.array_const()
        elif token.type == TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            node = self.expression()
            self.eat(TokenTypes.RPAREN)
            return node
        elif token.type == TokenTypes.VAR:
            return self.variable()
        else:
            self.error("Excepted a factor type got {}".format(self.cur_token.type))
