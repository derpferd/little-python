from littlepython import Compiler, Features


def compile(code, features=Features.ALL):
    compiler = Compiler()
    return compiler.compile(code, features=features)


def run(code, **kargs):
    if len(kargs) == 1 and "in_state" in kargs:
        return compile(code).run(kargs["in_state"])
    else:
        return compile(code).run(kargs)
