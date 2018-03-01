

class LittlePythonBaseExcetion(Exception):
    pass


class AlreadyRunningException(LittlePythonBaseExcetion):
    pass


class ExecutionCountExceededException(LittlePythonBaseExcetion):
    pass


class InvalidSyntaxException(LittlePythonBaseExcetion):
    pass


class DivisionByZeroException(LittlePythonBaseExcetion):
    pass
