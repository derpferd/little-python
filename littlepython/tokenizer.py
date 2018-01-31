from __future__ import unicode_literals

import inspect
from collections import defaultdict, OrderedDict
from enum import Enum
from littlepython.feature import Features

counters = defaultdict(lambda: -1)


def auto():
    global counters
    caller = inspect.stack()[1][3]
    counters[caller] += 1
    return counters[caller]


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


class classproperty(object):
    """ @classmethod+@property """
    def __init__(self, f):
        self.f = classmethod(f)

    def __get__(self, *a):
        return self.f.__get__(*a)()


class TokenTypes(Enum):
    # Basic Ops
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    MOD = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()

    # types
    INT = auto()
    ARRAY = auto()

    # Grouping tokens
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()

    # control
    ASSIGN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR_LOOP = auto()
    FUNC = auto()
    RETURN = auto()

    # Whitespace
    NEW_LINE = auto()
    SEMI_COLON = auto()
    EOF = auto()

    # Other
    VAR = auto()

    @classproperty
    def BINARY_OPS(cls):
        return {cls.ADD, cls.SUB, cls.MULT, cls.DIV, cls.MOD, cls.AND, cls.OR, cls.GREATER, cls.GREATER_EQUAL, cls.LESS,
                cls.LESS_EQUAL, cls.EQUAL, cls.NOT_EQUAL}

    @classproperty
    def UNARY_OPS(cls):
        return {cls.NOT}

    @classproperty
    def OPERANDS(cls):
        return {cls.VAR, cls.INT}

    @classproperty
    def PARENS(cls):
        return {cls.LPAREN, cls.RPAREN}

    @classmethod
    def control(cls, features):
        types = set()
        if Features.IF in features:
            types |= {TokenTypes.IF, TokenTypes.ELSE}
        if Features.ELIF in features:
            types |= {TokenTypes.ELIF}
        return types

    @classmethod
    def loop(cls, features):
        types = set()
        if Features.FOR_LOOP in features:
            types |= {TokenTypes.FOR_LOOP}
        return types

    @classmethod
    def func(cls, features):
        if Features.FUNC in features:
            return {TokenTypes.FUNC, TokenTypes.RETURN}
        return {}

    @staticmethod
    def from_str(s):
        return {'if': TokenTypes.IF,
                'elif': TokenTypes.ELIF,
                'else': TokenTypes.ELSE,
                'for': TokenTypes.FOR_LOOP,
                'func': TokenTypes.FUNC,
                'and': TokenTypes.AND,
                'or': TokenTypes.OR,
                'not': TokenTypes.NOT,
                'is': TokenTypes.EQUAL,
                'is not': TokenTypes.NOT_EQUAL,
                'return': TokenTypes.RETURN,
                '+': TokenTypes.ADD,
                '-': TokenTypes.SUB,
                '*': TokenTypes.MULT,
                '/': TokenTypes.DIV,
                '%': TokenTypes.MOD,
                '=': TokenTypes.ASSIGN,
                '<': TokenTypes.LESS,
                '>': TokenTypes.GREATER,
                '<=': TokenTypes.LESS_EQUAL,
                '>=': TokenTypes.GREATER_EQUAL,
                '{': TokenTypes.LBRACE,
                '}': TokenTypes.RBRACE,
                '(': TokenTypes.LPAREN,
                ')': TokenTypes.RPAREN,
                '[': TokenTypes.LBRACKET,
                ']': TokenTypes.RBRACKET,
                ';': TokenTypes.SEMI_COLON,
                ',': TokenTypes.COMMA,
                '\n': TokenTypes.NEW_LINE,
                None: TokenTypes.EOF}.get(s, None)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return "Token<type:{}, value:{}>".format(self.type, str(self.value))

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
            return Token(TokenTypes.INT, int(s))
        if isinstance(s, str) and len(s) and alfa_(s[0]) and alnum_(s[1:]):
            return Token(TokenTypes.VAR, s)
        raise ValueError("Invalid input")


class Tokens(object):
    @staticmethod
    def get_all(features):
        keys = Tokens.get_keywords(features)
        keys.update(Tokens.get_non_alpha(features))
        keys.update(Tokens.get_multi_word_keywords(features))
        return OrderedDict(sorted(list(keys.items()), key=lambda t: len(t[0]), reverse=True))

    @staticmethod
    def get_multi_word_keywords(features):
        """This returns an OrderedDict containing the multi word keywords in order of length.
        This is so the tokenizer will match the longer matches before the shorter matches
        """
        keys = {
            'is not': Token(TokenTypes.NOT_EQUAL, 'is not'),
        }
        return OrderedDict(sorted(list(keys.items()), key=lambda t: len(t[0]), reverse=True))

    @staticmethod
    def get_keywords(features):
        keys = {
            'not': Token(TokenTypes.NOT, 'not'),
            'is': Token(TokenTypes.EQUAL, 'is'),
            'and': Token(TokenTypes.AND, 'and'),
            'or': Token(TokenTypes.OR, 'or'),
        }
        if Features.IF in features:
            # TODO: write test cases that test this.
            keys.update({
                'if': Token(TokenTypes.IF, 'if'),
                'else': Token(TokenTypes.ELSE, 'else'),
            })
        if Features.ELIF in features:
            # TODO: write test cases that test this.
            keys.update({
                'elif': Token(TokenTypes.ELIF, 'elif'),
            })
        if Features.FOR_LOOP in features:
            # TODO: write test cases that test this.
            keys.update({
                'for': Token(TokenTypes.FOR_LOOP, 'for'),
            })
        if Features.FUNC in features:
            # TODO: write test cases that test this.
            keys.update({
                'func': Token(TokenTypes.FUNC, 'func'),
                'return': Token(TokenTypes.RETURN, 'return'),
            })
        return keys

    @staticmethod
    def get_non_alpha(features):
        keys = {  # non-alphanumeric single char tokens
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
            ';': Token(TokenTypes.SEMI_COLON, ';'),
            ',': Token(TokenTypes.COMMA, ','),
            '<=': Token(TokenTypes.LESS_EQUAL, '<='),
            '>=': Token(TokenTypes.GREATER_EQUAL, '>='),
        }
        if Features.TYPE_ARRAY in features:
            keys.update({'[': Token(TokenTypes.LBRACKET, '['),
                         ']': Token(TokenTypes.RBRACKET, ']'), })
        return OrderedDict(sorted(list(keys.items()), key=lambda t: len(t[0]), reverse=True))


class Tokenizer(object):
    def __init__(self, text, features=Features.ALL):
        self.text = text
        self.cur_pos = -1
        self.cur_char = ""
        self.last_was_new_line = False
        self.last_was_eof = False
        self.advance()
        self.features = features
        self.history = []
        self.saving = False

        self.keywords = Tokens.get_keywords(features)
        self.mult_keywords = Tokens.get_multi_word_keywords(self.features)
        self.non_alpha = Tokens.get_non_alpha(features)

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_next_token()
        if self.last_was_eof:
            raise StopIteration()
        if token.type == TokenTypes.EOF:
            self.last_was_eof = True
        if self.saving:
            self.history += [token]
        return token

    def start_saving(self, cur_token):
        self.saving = True
        self.history = [cur_token]

    def replay(self):
        self.saving = False
        if self.history:
            self.last_was_eof = False

    # For Python 2 support
    next = __next__

    def advance(self, dist=1):
        self.cur_pos += dist
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
        # TODO: some time in the future add floats here too.
        result = ""
        while self.cur_char is not None and self.cur_char.isdigit():
            result += self.cur_char
            self.advance()

        return Token(TokenTypes.INT, int(result))

    def id(self):
        result = ""
        while self.cur_char is not None and alnum_(self.cur_char):
            result += self.cur_char
            self.advance()

        return self.keywords.get(result, Token(TokenTypes.VAR, result))

    def test_for_multi_word_keyword(self):
        for keyword in self.mult_keywords:
            # match = keyword  # We add a space because a keyword must be followed by a space.
            if self.cur_pos + len(keyword) > len(self.text):
                continue
            if self.text[self.cur_pos:self.cur_pos+len(keyword)] == keyword:  # the keyword is the same as the next chars.
                if self.cur_pos + len(keyword) + 1 > len(self.text):  # Are you at the end
                    return self.mult_keywords[keyword]

                char_after_keyword = self.text[self.cur_pos + len(keyword)]
                if alnum_(char_after_keyword):  # The next char is an alphanum or underscore.
                    continue
                else:
                    return self.mult_keywords[keyword]

    def test_for_non_alpha(self):
        for token in self.non_alpha:
            # match = keyword  # We add a space because a keyword must be followed by a space.
            if self.cur_pos + len(token) > len(self.text):
                continue
            if self.text[self.cur_pos:self.cur_pos+len(token)] == token:  # the token is the same as the next chars.
                return self.non_alpha[token]

    def get_next_token(self):  # TODO: make this private.
        if not self.saving and self.history:
            return self.history.pop(0)
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

            multi_word = self.test_for_multi_word_keyword()
            if multi_word:
                self.advance(dist=len(multi_word.value))
                return multi_word

            if alfa_(self.cur_char):
                return self.id()

            if self.cur_char.isdigit():
                return self.number()

            non_alpha_token = self.test_for_non_alpha()
            if non_alpha_token:
                self.advance(dist=len(non_alpha_token.value))
                return non_alpha_token

            raise Exception("Ran into invalid char '{}' at pos {}".format(self.cur_char, self.cur_pos))

        return Token(TokenTypes.EOF, None)
