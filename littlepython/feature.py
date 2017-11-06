from __future__ import print_function
from __future__ import unicode_literals

from collections import Iterable


class Feature(object):
    def __init__(self, name):
        self.name = name

    def __contains__(self, item):
        return item in FeatureSet(self)

    def __add__(self, other):
        return FeatureSet(self) + other

    __or__ = __add__

    def __sub__(self, other):
        return FeatureSet(self) - other

    def __str__(self):
        return self.name

    __repr__ = __str__


class FeatureSet(object):
    def __init__(self, val):
        if isinstance(val, Feature):
            val = {val}
        if isinstance(val, FeatureSet):
            val = val.val
        assert isinstance(val, Iterable)
        self.val = set(val)

    def __contains__(self, item):
        return FeatureSet(item).val - self.val == set()

    def __add__(self, other):
        return FeatureSet(self.val | FeatureSet(other).val)

    __or__ = __add__

    def __sub__(self, other):
        return FeatureSet(self.val - FeatureSet(other).val)

    def __str__(self):
        return "<FeatureSet " + ",".join(map(str, self.val)) + ">"

    __repr__ = __str__

    def __iter__(self):
        return self.val.__iter__()


def feature(name):
    return FeatureSet(Feature(name))


class Features(object):
    IF = feature("IF")
    ELIF = feature("ELIF")
    TYPE_ARRAY = feature("TYPE_ARRAY")
    RANDOM_VAR = feature("RANDOM_VAR")
    FOR_LOOP = feature("FOR_LOOP")
    FUNC = feature("FUNC")

    ALL = IF | ELIF | TYPE_ARRAY | RANDOM_VAR | FOR_LOOP | FUNC
    NONE = FeatureSet([])
