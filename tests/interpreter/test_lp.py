# Copyright (C) Jonathan Beaulieu (beau0307@d.umn.edu)
# Copyright (C) Aleksandar Straumann (alstraumann@gmail.com)

from unittest import TestCase

from littlepython.error import ExecutionCountExceededException
from littlepython.lp import Compiler


class TestLPComplierMethods(TestCase):
    def setUp(self):
        self.compiler = Compiler()
        self.binary_combos = [(i, j) for i in [0, 1] for j in [0, 1]]
        self.int_combos = [(i, j) for i in [-10, -2, -1, 0, 1, 2, 5, 10, 100] for j in [-10, -2, -1, 0, 1, 2, 5, 10, 100]]

    def tearDown(self):
        self.compiler = None

    # Here is a sample test. You should copy this to create a new test
    def test_sample(self):
        beginning_state = {}
        code = """"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_blank(self):
        beginning_state = {}
        code = """"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_plus(self):
        beginning_state = {}
        code = """a = 1
        b = 3
        c = a + b"""
        expected_state = {"c": 4, "a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_negative_const(self):
        beginning_state = {}
        code = """a = -1
        b = -3
        c = a + b"""
        expected_state = {"c": -4, "a": -1, "b": -3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_minus_positive(self):
        beginning_state = {}
        code = """a = 3
        b = 1
        c = a - b"""
        expected_state = {"c": 2, "a": 3, "b": 1}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_minus_negative(self):
        beginning_state = {}
        code = """a = 1
        b = 3
        c = a - b"""
        expected_state = {"c": -2, "a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mult_zero(self):
        beginning_state = {}
        code = """a = 0
        b = 3
        c = a * b"""
        expected_state = {"c": 0, "a": 0, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mult_one(self):
        beginning_state = {}
        code = """a = 1
        b = 3
        c = a * b"""
        expected_state = {"c": 3, "a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mult_other(self):
        beginning_state = {}
        code = """a = 50
        b = 43
        c = a * b"""
        expected_state = {"c": 2150, "a": 50, "b": 43}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_normal(self):
        beginning_state = {}
        code = """a = 6
        b = 3
        c = a / b"""
        expected_state = {"c": 2, "a": 6, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_fraction_positive(self):
        beginning_state = {}
        code = """a = 6
        b = 4
        c = a / b"""
        expected_state = {"c": 1, "a": 6, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_fraction_zero(self):
        beginning_state = {}
        code = """a = 1
        b = 2
        c = a / b"""
        expected_state = {"c": 0, "a": 1, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_zero(self):
        beginning_state = {}
        code = """a = 6
        b = 0
        c = a / b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        self.assertRaises(ZeroDivisionError, prog.run, beginning_state)

    def test_op_mod(self):
        beginning_state = {}
        code = """a = 6
        b = 4
        c = a % b"""
        expected_state = {"c": 2, "a": 6, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mod_zero(self):
        beginning_state = {}
        code = """a = 6
        b = 0
        c = a % b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        self.assertRaises(ZeroDivisionError, prog.run, beginning_state)

    def test_op_lt(self):
        code = """c = a < b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.int_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a < b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_gt(self):
        code = """c = a > b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.int_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a > b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_lte(self):
        code = """c = a <= b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.int_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a <= b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_gte(self):
        code = """c = a >= b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.int_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a >= b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_or(self):
        code = """c = a or b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a or b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_and(self):
        code = """c = a and b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a and b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_is(self):
        code = """c = a is b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a is b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_is_not(self):
        code = """c = a is not b"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a is not b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_not(self):
        code = """b = not a"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for a in [0, 1]:
            beginning_state = {"a": a}
            expected_state = {"b": not a, "a": a}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_not_or(self):
        code = """c = not (a or b)"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": not (a or b), "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_only_newlines(self):
        beginning_state = {}
        code = """\n\n\n\n\n"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_trailing_newlines(self):
        beginning_state = {}
        code = """a = 2\n\n\n\n\n"""
        expected_state = {"a": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_int(self):
        beginning_state = {}
        code = """a = 2"""
        expected_state = {"a": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_with_underscore(self):
        beginning_state = {}
        code = """a_b = 2"""
        expected_state = {"a_b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_with_underscore_at_beginning(self):
        beginning_state = {}
        code = """_b = 2"""
        expected_state = {"_b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_simple_expression(self):
        beginning_state = {}
        code = """b = 40 % 1"""
        expected_state = {"b": 40 % 1}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_other_variables(self):
        beginning_state = {}
        code = """a = 2\nb = 0\nc = b + a"""
        expected_state = {"a": 2, "b": 0, "c": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_is_no_trailing_newline(self):
        beginning_state = {}
        code = """if 0 is 0 {
 c = 3
}"""
        expected_state = {"c": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_not(self):
        beginning_state = {}
        code = """if 0 is not 1 {
            c = 3
        }"""
        expected_state = {"c": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var(self):
        beginning_state = {}
        code = """
        c = 3
        if c is 3 {
            d = 4
        }"""
        expected_state = {"c": 3, "d": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var_reassignment(self):
        beginning_state = {}
        code = """
        c = 3
        if c is 3 {
            c = 5
        }"""
        expected_state = {"c": 5}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var_undefined(self):
        beginning_state = {}
        code = """
        if a is 0 {
            c = 5
        }"""
        expected_state = {"c": 5}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var_undefined_2(self):
        beginning_state = {}
        code = """
        if a {
            c = 2
        } else {
            c = 5
        }"""
        expected_state = {"c": 5}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var_undefined_3(self):
        beginning_state = {}
        code = """
        if not a {
            c = 5
        }"""
        expected_state = {"c": 5}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_nested_if(self):
            beginning_state = {}
            code = """if 0 is 0 {
                if 1 is 1 {
                    c = 3
                }
            }"""
            expected_state = {"c": 3}

            # compile code into LPProg
            prog = self.compiler.compile(code)

            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)
    
    def test_nested_if_with_var_reassignment(self):
        beginning_state = {}
        code = """
        c = 3
        if c is 3 {
            c = 4
            if c is 4 {
                c = 5
            }
        }"""
        expected_state = {"c": 5}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_long_alphanumeric_variable_name(self):
        beginning_state = {}
        code = """asdfasdfasdfasdifgasdfhga232hjkbljh123b1jh2b31j2hb = 23"""
        expected_state = {"asdfasdfasdfasdifgasdfhga232hjkbljh123b1jh2b31j2hb": 23}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_line_comment(self):
        beginning_state = {}
        code = """a=3\n# This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_with_spaces(self):
        beginning_state = {}
        code = """a=3 # This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_without_space(self):
        beginning_state = {}
        code = """a=3#This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_in_statement(self):
        beginning_state = {"a": 1, "b": 0}
        code = """if a is 1 { # This is a comment\nb=1\n}"""
        expected_state = {"a": 1, "b": 1}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_in_nested_statement(self):
        beginning_state = {"a": 1, "b": 1, "c": 0}
        code = """if a is 1 { # This is a comment\nif b is 1 {\nc=1\n}\n}"""
        expected_state = {"a": 1, "b": 1, "c": 1}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_beginning_state(self):
        beginning_state = {"b": 2}
        code = """a=b"""
        expected_state = {"a": 2, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_multiple_ifs(self):
        beginning_state = {"a": 2}
        code = """if a is 1 {
        b = 2
        }
        if a is 2 {
        b = 3
        }
        if a is 3 {
        b = 4
        }"""
        expected_state = {"a": 2, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_else(self):
        beginning_state = {"a": 2}
        code = """if a is 1 {
        b = 2
        } else {
        b = 3
        }"""
        expected_state = {"a": 2, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_empty_if(self):
        beginning_state = {"a": 2}
        code = """if a is 1 {
        }
        b = 3"""
        expected_state = {"a": 2, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_empty_if_2(self):
        beginning_state = {"a": 2}
        code = """if a is 2 {
        }
        b = 3"""
        expected_state = {"a": 2, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_empty_if_else(self):
        beginning_state = {"a": 2}
        code = """if a is 1 {
        } else {
            b = 2
        }"""
        expected_state = {"a": 2, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_empty_if_else_2(self):
        beginning_state = {"a": 1, "b": 3}
        code = """if a is 1 {
        } else {
            b = 2
        }"""
        expected_state = {"a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_empty_if_else_3(self):
        beginning_state = {"a": 1, "b": 3}
        code = """if a is 2 {
            b = 2
        } else {
        }"""
        expected_state = {"a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_empty_if_else_4(self):
        beginning_state = {"a": 1, "b": 3}
        code = """if a is 1 {
            b = 2
        } else {
        }"""
        expected_state = {"a": 1, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_nested_empty_if_else(self):
        beginning_state = {"a": 1, "b": 3}
        code = """if a is 1 {
            b = 2
            if a is 2 {
            }
        } else {
        }"""
        expected_state = {"a": 1, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_nested_empty_if_else_2(self):
        beginning_state = {"a": 1, "b": 3}
        code = """if a is 1 {
            b = 2
            if a is 2 {
            }
        } else {
        b = 4
        }"""
        expected_state = {"a": 1, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_array_access(self):
        beginning_state = {"a": [1, 2, 3]}
        code = """if a[0] is 1 {
         b= 2
        }"""
        expected_state = {"a": [1, 2, 3], "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_array_modify(self):
        beginning_state = {"a": [1, 2, 3]}
        code = """a[0] = 3 + 4"""
        expected_state = {"a": [7, 2, 3]}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_array_access_undefined(self):
        beginning_state = {"a": [1, 2, 3]}
        code = """if a[50] {
         b= 2
        }"""
        expected_state = {"a": [1, 2, 3]}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_array_access_undefined_2(self):
        beginning_state = {"a": [1, 2, 3]}
        code = """if a[50] is 0 {
         b= 2
        }"""
        expected_state = {"a": [1, 2, 3], "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_array_access_expr(self):
        beginning_state = {"a": [1, 2, 3]}
        code = """c = 2 +1 -1
        if a[c+2-1-1] is 3 {
         b= 2
        }"""
        expected_state = {"a": [1, 2, 3], "b": 2, "c": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_array_modify_expr(self):
        beginning_state = {"a": [1, 2, 3]}
        code = """c = 2 +1 -1
        a[c+2-1-1] = 3 + 4"""
        expected_state = {"a": [1, 2, 7], "c": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_2d_array_access(self):
        beginning_state = {"a": [[1, 4], [2, 7], [3, 5]]}
        code = """if a[0][0] is 1 {
         b = 2
        }"""
        expected_state = {"a": [[1, 4], [2, 7], [3, 5]], "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_2d_array_modify(self):
        beginning_state = {"a": [[1, 4], [2, 7], [3, 5]]}
        code = """a[1][0] = 4 + 4"""
        expected_state = {"a": [[1, 4], [8, 7], [3, 5]]}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_for_loop(self):
        beginning_state = {}
        code = """for i=0; i < 10; i = i + 1 {a = a + 1}"""
        expected_state = {"a": 10, "i": 10}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_for_loop_array_set(self):
        beginning_state = {"a": []}
        code = """for i=0; i < 10; i = i + 1 {a[i] = i}"""
        expected_state = {"a": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "i": 10}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_for_loop_array_get_and_set(self):
        beginning_state = {"a": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
        code = """for i=0; i < 10; i = i + 1 {a[i] = a[i] + 2}"""
        expected_state = {"a": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "i": 10}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_simple_func(self):
        beginning_state = {}
        code = """func add(a, b){c = a + b
        return c}
        d = add(1, 2)"""
        expected_state = {"d": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_func_no_return(self):
        beginning_state = {}
        code = """func add(a, b){c = a + b}
        d = add(1, 2)"""
        expected_state = {"d": 0}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_func_return(self):
        beginning_state = {}
        code = """func add(a, b){
        c = a + b
        return c
        return 0
        }
        d = add(1, 2)"""
        expected_state = {"d": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_func_scope_1(self):
        beginning_state = {"a": 4, "b": 5, "c": 6}
        code = """func add(a, b){c = a + b
        return c}
        d = add(1, 2)"""
        expected_state = {"a": 1, "b": 2, "c": 3, "d": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_func_recur(self):
        beginning_state = {}
        code = """func fib(n){
        if n is 0 { return 0 }
        if n is 1 { return 1 }
        return fib(n-1)+fib(n-2)}
        d = fib(6)"""
        expected_state = {"d": 8}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_func_recur_large(self):
        beginning_state = {}
        code = """func fib(n){
        if n is 0 { return 0 }
        if n is 1 { return 1 }
        return fib(n-1)+fib(n-2)}
        d = fib(13)"""
        expected_state = {"d": 233}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_func_recur_count_exceeded(self):
        beginning_state = {}
        code = """func fib(n){
        if n is 0 { return 0 }
        if n is 1 { return 1 }
        return fib(n-1)+fib(n-2)}
        d = fib(13)"""
        expected_state = {"d": 233}

        # compile code into LPProg
        prog = self.compiler.compile(code)

        try:
            ending_state = prog.run(beginning_state, max_op_count=1000)
        except ExecutionCountExceededException:
            return
        self.fail("Should have thrown an exception.")

    def test_execution_count_exceeded(self):
        code = """a = 1\na = 1\na = 1\na = 1\na = 1\na = 1\na = 1\na = 1\n"""

        # compile code into LPProg
        prog = self.compiler.compile(code)

        try:
            ending_state = prog.run(max_op_count=3)
        except ExecutionCountExceededException:
            return
        self.fail("Should have thrown an exception.")
