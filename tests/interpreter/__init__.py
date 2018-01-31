from littlepython import Compiler, Features


def compile(code, features=Features.ALL):
    compiler = Compiler()
    return compiler.compile(code, features=features)


def run(code, max_op_count=-1, **kargs):
    if len(kargs) == 1 and "in_state" in kargs:
        return compile(code).run(kargs["in_state"], max_op_count=max_op_count)
    else:
        return compile(code).run(kargs, max_op_count=max_op_count)
