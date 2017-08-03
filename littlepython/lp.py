# Copyright (C) Jonathan Beaulieu (beau0307@d.umn.edu)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from littlepython.interpreter import LPProg
from littlepython.parser import Parser, Tokenizer


class Compiler(object):
    def compile(self, prog):
        """Currently this compiler simply returns an interpreter instead of compiling
        TODO: Write this compiler to increase LPProg run speed and to prevent exceeding maximum recursion depth

        Args:
            prog (str): A string containing the program.

        Returns:
            LPProg
        """
        return LPProg(Parser(Tokenizer(prog)).program())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("How to run:")
        print("python lp.py file_to_be_run.lp")
    else:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print("Could not find that file sorry :(")
        lines = open(filename, 'r').read()
        c = Compiler()
        prog = c.compile(lines)
        state = prog.run()
        print("Ending variable Values:")
        print("Name".center(14, "-") + "|" + "Value".center(11, "-"))
        for var in sorted(state):
            print(var.center(14) + "|" + str(state[var]).center(11))
