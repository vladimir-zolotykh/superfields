# tests/test_calc.py

import pytest

from multidict import Calc, MultiMethod


@pytest.fixture
def calc():
    return Calc()


def test_int_dispatch(calc):
    assert calc.compute(10, 20) == 30


def test_float_dispatch_two_args(calc):
    assert calc.compute(3.5, 6.7) == 10.2


def test_float_dispatch_default_argument(calc):
    assert calc.compute(3.6) == 10.3


def test_string_dispatch(calc):
    assert calc.compute("Hello,", "World!") == "Hello,-World!"


def test_compute_is_multimethod_descriptor():
    assert isinstance(Calc.compute, MultiMethod)


def test_registered_signatures():
    methods = Calc.compute.methods

    assert (int, int) in methods
    assert (float, float) in methods
    assert (float,) in methods
    assert (str, str) in methods


def test_unsupported_signature_raises(calc):
    with pytest.raises(KeyError):
        calc.compute(1, "abc")


def test_too_many_arguments(calc):
    with pytest.raises(KeyError):
        calc.compute(1, 2, 3)


def test_no_arguments(calc):
    with pytest.raises(KeyError):
        calc.compute()


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ((5, 7), 12),
        ((2.5, 1.5), 4.0),
        ((2.5,), 9.2),
        (("a", "b"), "a-b"),
    ],
)
def test_dispatch_table(calc, args, expected):
    assert calc.compute(*args) == expected
