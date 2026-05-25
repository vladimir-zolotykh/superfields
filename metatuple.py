#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Tuple(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)


if __name__ == "__main__":
    tup = Tuple(1, 2, 3)
    print(tup)
