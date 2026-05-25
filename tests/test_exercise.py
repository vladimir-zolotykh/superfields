# tests/test_exercise.py

import pytest

from metatuple import Exercise


def test_exercise_creation():
    ex = Exercise("squat", 87.5, 2)

    assert ex == ("squat", 87.5, 2)


def test_exercise_fields_access():
    ex = Exercise("bench press", 100.0, 5)

    assert ex.name == "bench press"
    assert ex.weight == 100.0
    assert ex.reps == 5


def test_exercise_is_tuple():
    ex = Exercise("deadlift", 140, 1)

    assert isinstance(ex, tuple)


def test_exercise_wrong_number_of_arguments_too_few():
    with pytest.raises(ValueError) as excinfo:
        Exercise("squat", 100)

    assert "Exercise has 3 arguments, got 2" in str(excinfo.value)


def test_exercise_wrong_number_of_arguments_too_many():
    with pytest.raises(ValueError) as excinfo:
        Exercise("squat", 100, 5, "extra")

    assert "Exercise has 3 arguments, got 4" in str(excinfo.value)


@pytest.mark.parametrize(
    "name, weight, reps",
    [
        ("squat", 120, 3),
        ("bench press", 90.5, 5),
        ("deadlift", 180, 1),
    ],
)
def test_multiple_exercises(name, weight, reps):
    ex = Exercise(name, weight, reps)

    assert ex.name == name
    assert ex.weight == weight
    assert ex.reps == reps
