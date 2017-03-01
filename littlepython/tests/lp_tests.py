# Copyright (C) Jonathan Beaulieu (beau0307@d.umn.edu)
# Copyright (C) Aleksandar Straumann (alstraumann@gmail.com)

from unittest import TestCase

from littlepython.lp import Compiler


class TestLPComplierMethods(TestCase):
    def setUp(self):
        self.compiler = Compiler()
        self.binary_combos =  [(i, j) for i in [0,1] for j in [0,1]]

    def tearDown(self):
        self.compiler = None

    # Here is a sample test. You should copy this to create a new test
    def test_sample(self):
        beginning_state = {}
        code = """"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_blank(self):
        beginning_state = {}
        code = """"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_plus(self):
        beginning_state = {}
        code = """a = 1
        b = 3
        c = a + b"""
        expected_state = {"c": 4, "a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_minus_positive(self):
        beginning_state = {}
        code = """a = 3
        b = 1
        c = a - b"""
        expected_state = {"c": 2, "a": 3, "b": 1}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_minus_negative(self):
        beginning_state = {}
        code = """a = 1
        b = 3
        c = a - b"""
        expected_state = {"c": -2, "a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mult_zero(self):
        beginning_state = {}
        code = """a = 0
        b = 3
        c = a * b"""
        expected_state = {"c": 0, "a": 0, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mult_one(self):
        beginning_state = {}
        code = """a = 1
        b = 3
        c = a * b"""
        expected_state = {"c": 3, "a": 1, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mult_other(self):
        beginning_state = {}
        code = """a = 50
        b = 43
        c = a * b"""
        expected_state = {"c": 2150, "a": 50, "b": 43}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_normal(self):
        beginning_state = {}
        code = """a = 6
        b = 3
        c = a / b"""
        expected_state = {"c": 2, "a": 6, "b": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_fraction_positive(self):
        beginning_state = {}
        code = """a = 6
        b = 4
        c = a / b"""
        expected_state = {"c": 1, "a": 6, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_fraction_zero(self):
        beginning_state = {}
        code = """a = 1
        b = 2
        c = a / b"""
        expected_state = {"c": 0, "a": 1, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_div_zero(self):
        beginning_state = {}
        code = """a = 6
        b = 0
        c = a / b"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        self.assertRaises(ZeroDivisionError, prog.run, beginning_state)

    def test_op_mod(self):
        beginning_state = {}
        code = """a = 6
        b = 4
        c = a % b"""
        expected_state = {"c": 2, "a": 6, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_op_mod_zero(self):
        beginning_state = {}
        code = """a = 6
        b = 0
        c = a % b"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        self.assertRaises(ZeroDivisionError, prog.run, beginning_state)

    def test_op_or(self):
        code = """c = a or b"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a or b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_and(self):
        code = """c = a and b"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a and b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_is(self):
        code = """c = a is b"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a is b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_is_not(self):
        code = """c = a is not b"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        for combo in self.binary_combos:
            a, b = combo
            beginning_state = {"a": a, "b": b}
            expected_state = {"c": a is not b, "a": a, "b": b}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_not(self):
        code = """b = not a"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        for a in [0, 1]:
            beginning_state = {"a": a}
            expected_state = {"b": not a, "a": a}
            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)

    def test_op_not_or(self):
        code = """c = not (a or b)"""

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

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
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_trailing_newlines(self):
        beginning_state = {}
        code = """a = 2\n\n\n\n\n"""
        expected_state = {"a": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_int(self):
        beginning_state = {}
        code = """a = 2"""
        expected_state = {"a": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_with_underscore(self):
        beginning_state = {}
        code = """a_b = 2"""
        expected_state = {"a_b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_with_underscore_at_beginning(self):
        beginning_state = {}
        code = """_b = 2"""
        expected_state = {"_b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_simple_expression(self):
        beginning_state = {}
        code = """b = 40 % 1"""
        expected_state = {"b": 40 % 1}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_other_variables(self):
        beginning_state = {}
        code = """a = 2\nb = 0\nc = b + a"""
        expected_state = {"a": 2, "b": 0, "c": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_is_no_trailing_newline(self):
        beginning_state = {}
        code = """if 0 is 0 {
 c = 3
}"""
        expected_state = {"c": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_not(self):
        beginning_state = {}
        code = """if 0 is not 1 {
            c = 3
        }"""
        expected_state = {"c": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var(self):
        beginning_state = {}
        code = """
        c = 3
        if c is 3 {
            d = 4
        }"""
        expected_state = {"c": 3, "d":4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

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
        prog = self.compiler.compile(code.split("\n"))

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
            prog = self.compiler.compile(code.split("\n"))

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
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_long_alphanumeric_variable_name(self):
        beginning_state = {}
        code = """asdfasdfasdfasdifgasdfhga232hjkbljh123b1jh2b31j2hb = 23"""
        expected_state = {"asdfasdfasdfasdifgasdfhga232hjkbljh123b1jh2b31j2hb": 23}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_line_comment(self):
        beginning_state = {}
        code = """a=3\n# This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_with_spaces(self):
        beginning_state = {}
        code = """a=3 # This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_without_space(self):
        beginning_state = {}
        code = """a=3#This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_in_statement(self):
        beginning_state = {"a": 1, "b": 0}
        code = """if a is 1 { # This is a comment\nb=1\n}"""
        expected_state = {"a": 1, "b": 1}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_in_nested_statement(self):
        beginning_state = {"a": 1, "b": 1, "c": 0}
        code = """if a is 1 { # This is a comment\nif b is 1 {\nc=1\n}\n}"""
        expected_state = {"a": 1, "b": 1, "c": 1}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_beginning_state(self):
        beginning_state = {"b": 2}
        code = """a=b"""
        expected_state = {"a": 2, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

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
        prog = self.compiler.compile(code.split("\n"))

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
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)


if __name__ == '__main__':
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLPComplierMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)