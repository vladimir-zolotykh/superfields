#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import types
from typing import Callable, Any
import inspect


class MultiDict(dict):
    def __setitem__(self, key, val):
        if key not in self:
            super().__setitem__(key, val)
            return
        mm = self[key]
        if isinstance(mm, MultiMethod):
            mm.register(val)
        else:
            mm = MultiMethod(key)
            oval = self[key]
            mm.register(oval)
            mm.register(val)
            super().__setitem__(key, mm)


class MultiMethod:
    def __init__(self, name=None):
        self._name = name
        self.methods: dict[tuple[Any, ...], Callable] = {}

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwds):
        bound = tuple((type(a) for a in args[1:]))
        func = self.methods[bound]
        return func(*args, **kwds)

    def register(self, func: Callable):
        sig = inspect.signature(func)
        _types: list[type] = []
        num_defaults: int = 0
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            _types.append(parm.annotation)
            num_defaults += parm.default is not inspect._empty
        key = tuple(_types)
        self.methods[key] = func
        if 0 < num_defaults:
            self.methods[key[:-num_defaults]] = func


class MultiMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        return super().__new__(mcls, clsname, bases, clsdict)

    @classmethod
    def __prepare__(clsname, bases, clsdict):
        return MultiDict()


class Calc(metaclass=MultiMeta):
    def compute(self, x: int, y: int):
        return x + y

    def compute(self, x: float, y: float = 6.7):  # noqa: F811
        return x + y

    def compute(self, x: str, y: str):  # noqa: F811
        return f"{x}-{y}"


if __name__ == "__main__":
    c = Calc()
    print(c.compute(10, 20))
    print(c.compute(3.5, 6.7))
    print(c.compute(3.6))
    print(c.compute("Hello, ", "World!"))
