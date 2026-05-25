#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class MetaTuple(type):
    def __init__(cls, clsname, bases, clsdict, **kwds):
        fields = clsdict.get("_fields", [])
        for n, fld in enumerate(fields):
            setattr(cls, fld, property(itemgetter(n)))


class Tuple(tuple):
    def __new__(cls, *args):
        na = len(cls._fields)
        if na != len(args):
            raise ValueError(f"{cls.__name__} has {na} arguments, got {len(args)}")
        return super().__new__(cls, args)


class Exercise(Tuple):
    _fields = ["name", "weight", "reps"]


if __name__ == "__main__":
    ex = Exercise("squat", 87.5, 2)
    print(ex)
