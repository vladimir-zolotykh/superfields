#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import types
from typing import Callable, Any
import inspect


class MultiDict(dict):
    def __setitem__(self, key, val):
        if key.startswith("__") and key.endswith("__"):
            super().__setitem__(key, val)
            return
        if key in self:
            mm = self[key]
            if isinstance(mm, MultiMethod):
                mm.register(val)
            else:
                mm = MultiMethod(key)
                mm.register(val)
            val = mm
        super().__setitem__(key, val)


class MultiMethod:
    def __init__(self, name=None):
        self._name = name
        self.methods: dict[tuple[Any, ...], Callable] = {}

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return types.MethodType(instance, self)

    def __call__(self, *args, **kwds):
        bound = tuple((type(a) for a in args))
        func = self.methods[bound]
        return func(*args, **kwds)

    def register(self, func: Callable):
        sig = inspect.signature(func)
        _types = [parm.annotation for _, parm in sig.parameters.items()]
        self.methods[tuple(_types)] = func


class MultiMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        return super().__new__(mcls, clsname, bases, clsdict)

    def __prepare__(clsname, bases, clsdict):
        return MultiDict()


class Calc(metaclass=MultiMeta):
    def compute(self, x: int, y: int):
        pass

    def compute(self, x: float, y: float = 6.7):  # noqa: F811
        pass

    def compute(self, x: str, y: str):  # noqa: F811
        pass


if __name__ == "__main__":
    c = Calc()
    c.compute(10, 20)
    c.compute(3.5, 6.7)
    c.compute(3.6)
    c.compute("Hello, ", "World!")
