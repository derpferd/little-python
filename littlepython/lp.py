# Copyright (C) Jonathan Beaulieu (beau0307@d.umn.edu)
from littlepython.feature import Features
from littlepython.interpreter import LPProg
from littlepython.parser import Parser
from littlepython.tokenizer import Tokenizer


class Compiler(object):
    def compile(self, prog, features=Features.ALL):
        """Currently this compiler simply returns an interpreter instead of compiling
        TODO: Write this compiler to increase LPProg run speed and to prevent exceeding maximum recursion depth

        Args:
            prog (str): A string containing the program.
            features (FeatureSet): The set of features to enable during compilation.

        Returns:
            LPProg
        """
        return LPProg(Parser(Tokenizer(prog, features), features).program(), features)
